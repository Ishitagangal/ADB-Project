import os
import sys
import time
import Variable
from Site import Site
import constants
from Variable import Variable
from LockTable import LockTable


class SiteManager():
    """
    Responsible for processing site management requests. Takes care of sites if they are in 
    recovery, UP and DOWN state. Makes calls to sites and maintains variable values on each one of them.
    numSites : number of total sites are given as 10
    numVars: number of total variables are given as 20
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 28th November, 2019
    """

    def __init__(self, numSites, numVars):
        self.sites = [None] + [Site(i) for i in range(1, numSites + 1)]
        # self.getSites(10)
        self.countOfSites = numSites
        self.countOfVariables = numVars

    def mainSiteManager(self, command):
        """
        Main method of site manager, calls fail(), recover() for particular siteId.
        :param command: site command that is being executed/has been read
        """
        transactionParams = list(command.get_transactionParameters())

        if command.get_transactionType() == constants.DUMP:
            if len(transactionParams[0]) == 0:
                for site in self.sites[1:]:
                    site.dump()
            else:
                print("Invalid dump() function")
        elif command.get_transactionType() == constants.FAIL:
            self.fail(int(transactionParams[0]))
        elif command.get_transactionType() == constants.RECOVER:
            self.recover(int(transactionParams[0]))

        return

    def getSite(self, index):
        """
        Getter for site instance at a particular index
        :param index: site instance to be returned at a particular index
        """
        if index > 10 or index <=0:
            raise ValueError("Index must be in between 1 and 10")
        return self.sites[index]

    def getLock(self, transaction, type, variable):
        """
        Getter for a read or write lock on variable by a transaction. Returns if lock is acquired, no site is available,
        no lock is available or site is in recovery state but lock acquired.
        :param transaction: transaction that needs a lock on a variable
        :param type: type of read or write lock needed
        :param variable: variable on which lock is needed
        """
        # print("reached sitemanager getlock")
        sites = Variable.getListOfSites(variable)
        if sites == 'all':
            sites = range(1, 11)
        else:
            sites = [sites]
        flag = 1
        noSiteAvailable = 1
        recovering = 0
        evenIndex = int(variable[1:]) % 2 == 0
        for site in sites:
            status = self.sites[site].getStatus()
            # print("check status: "+str(status)+)
            if self.sites[site].getStatus() == constants.SiteStatus.DOWN:
                continue
            if self.sites[site].getStatus() == constants.SiteStatus.RECOVERING and type == constants.LockType.read:
                if variable not in self.sites[site].foundVariables:
                    continue
                elif not evenIndex:
                    recovering = 1
            noSiteAvailable = 0

            acquireLockFlag = self.sites[site].acquireLockOnSite(transaction, type, variable)
            if acquireLockFlag == 1 and type == constants.LockType.read:
                if recovering:
                    return "GotLockRecoveringSite"
                else:
                    return "GotLock"
            flag &= acquireLockFlag
            # print(str(acquireLockFlag))
        # print(str(acquireLockFlag))
        if noSiteAvailable == 1:
            # print("o site")
            return "NoSiteAvailable"
        elif flag == 0:
            # print("no lock")
            return "NoLockAvailable"
        else:
            # print("got lock")
            return "GotLock"

    def getVariablesValues(self, inputVar=None):
        """
        Get value of a variable if index given, else return values of all variables
        :param index: index of variable of which value needs to be read
        """
        values = dict()
        #print(str(inputVar))
        for site in self.sites[1:]:
            if site.site_status == constants.SiteStatus.UP:
                variables = site.getVariablesOnThisSite()
                for var in variables:
                    # print("variables on site"+str(site.site_id)+" "+ str(var.name))
                    if inputVar is not None and var.name == inputVar:
                        # print("came to if")
                        return var.value
                    values[var.name] = var.value
                if len(values) == self.countOfVariables:
                    return values
            elif site.site_status == constants.SiteStatus.RECOVERING:
                variables = site.getVariablesOnThisSite()
                for var in variables:
                    if var.name in site.foundVariables:
                        if inputVar is not None and var.name == inputVar:
                            return var.value
                        values[var.name] = var.value
            if len(values) == self.countOfVariables:
                return values
        if inputVar is None:
            return values
        else:
            return None

    def getAllLocksSet(self):
        """
        Get all the locks that are stored in locktable. Returns locktable containing information
        of which variable has been acquired by which transaction and type of its lock.
        """
        locks = dict()
        for site in self.sites[1:]:
            lockDict = site.SiteDataManager.lockTable.lockDict
            for variable, l in lockDict.items():
                if variable not in locks:
                    locks[variable] = []
                for lock in l :
                    if lock not in locks[variable]:
                        locks[variable].append(lock)
        lockTable = LockTable()
        lockTable.lockDict = locks
        return lockTable

    def releaseLocks(self, lock, variable):
        """
		Releases lock for variable
		:param lock: lock object to be released
		:param variable: variable on which this lock is present
        """
        sites = Variable.getListOfSites(variable)
        if sites == 'all':
            sites = range(1, 11)
        else:
            sites = [sites]
        for i in sites:
            site = self.sites[i]
            site.releaseLockOnSite(lock, variable)

    def fail(self, indexOfSite):
        """
	    Calls the site fail method to mark site as failed
		:param indexOfSite: index of site that failed
        """       
        if 0 < indexOfSite <= 10:
            print("Site " +str(indexOfSite)+" failed")
            self.sites[indexOfSite].fail()

    def recover(self, indexOfSite):
        """
	    Calls the site recover method to mark site as recovering
		:param indexOfSite: index of site that needs to be recovered
        """   
        if 0 < indexOfSite <= 10:
            print("Site " +str(indexOfSite)+" recovered")
            self.sites[indexOfSite].recover()

    def getUPsites(self):
        """
	    Get the list of all the sites that are UP
        """   
        UPsites = list()
        for site in self.sites[1:]:
            if site.site_status == constants.SiteStatus.UP:
                UPsites.append(site)
        return UPsites

    def writeCommitToSites(self, transaction, var, value):
        """
	    Write the values to be committed to the sites that are UP
        :param transaction: transaction that needs the value to be written
        :param var: variable on which value needs to be written
        :param value: value that needs to be written on a variable
        """   
        sitesUP = self.getUPsites()
        for site in sitesUP:
            print(str(site))
            if var in site.getVariablesOnThisSite():
                print(str(var))
                site.writeVariable(transaction, var, value)
                # site.SiteDataManager.variables[var].setValue(value)
                # site.foundVariables.add(var)

