import constants
from Variable import Variable
from LockTable import  LockTable


class DataManager:
    """
    Every Site has its own data manager.
    The DM manages variables stored on the site and its locktable
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 20th November, 2019
    """
    def __init__(self, id):
        self.siteId = id
        self.lockTable = LockTable()
        self.variables = dict()

        for i in range(0, 21):
            if i % 2 == 0 or (1 + i % 10) == id:
                variable = Variable('x' + str(i), i, 10 * i, self.siteId)
                self.variables['x' + str(i)] = variable

    def getVariable(self,name):
        """
        Return variable from its dictionary of stored variables
        :param name: name of variable
        :return: Variable if present else None
        """
        if name in self.variables:
            return self.variables[name]
        else:
            return None

    def getLockTable(self):
        """
        Getter for Site's lock table
        :return: lockTable
        """
        return self.lockTable

    def getAllVariables(self):
        """
        Get all variables on this site
        :return: variables dict
        """
        return self.variables

    def addVariable(self, name, variable):
        """
        Add variable to dictionary
        :param name: name of variable
        :param variable: Variable object
        """
        self.variables[name] = variable

    def siteHasVariable(self, name):
        """
        Check if site has variable
        :param name: name of variable being searched
        :return: True if present else False
        """
        if name not in self.variables:
            return False
        return True

    def acquireLock(self, transaction, type, variable):
        """
        Transaction tries to acquire a lock on a variable.
        If the transaction already had a lock and it was only of one type then a lock is granted.
        Otherwise:
            if locktype is read and the variable isn't already write-locked, a lock is granted.
            if locktype is write and the variable isn't already locked, a lock is granted.
        :param transaction: transaction that wants a lock
        :param type: type of lock requested
        :param variable: variable on which lock is requested
        :return: True if lock was acquired else False
        """
        hasLock = self.lockTable.checkTransactionHasLock(transaction, variable)
        if hasLock:
            # self.lockTable.setLock(transaction, type, variable)
            # return True
            if self.lockTable.getNumOfLock(variable) == 1:
                self.lockTable.setLock(transaction, type, variable)
                return True
            else:
                return False
        if type == constants.LockType.read and not self.lockTable.checkWriteLocked(variable):
            self.lockTable.setLock(transaction, type, variable)
            return True
        elif type == constants.LockType.write and not self.lockTable.checkLocked(variable):
            self.lockTable.setLock(transaction, type, variable)
            return True
        else:
            if type == constants.LockType.read:
                  pass
#                 print("Can't read, there is no read lock")
            else:
                  pass
#                 print("Can't write, there is no write lock")
            return False

    def writeVariableForTransaction(self,transaction,variable,value):
        """
        Writes out variables that transaction wrote at commit time.
        :param transaction: transaction that is being committed
        :param variable: variable to be written
        :param value: new value to be written
        :return: True if transaction had the appropriate lock else False
        """
        if self.lockTable.checkTransactionHasLock(transaction, variable, constants.LockType.write):
            self.variables[variable].setValue(value)
            return True
        return False

    def releaseLock(self, lock, variable):
        """
        Release lock on variable
        :param lock: lock to remove
        :param variable: variable that is locked
        """
        self.lockTable.releaseLock(lock, variable)
