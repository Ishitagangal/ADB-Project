import os
import sys
import time


class Variable():
    """
    Variable represents each variable(data) stored on the sites.
    Args:
        name: Variable name
        index: Variable index
        value: Initial value
        siteId: Index of site which holds this variable
        
    Authors: Ishita Gangal and Divya Juneja
    Date: 8th November, 2019

    """
    def __init__(self, name, index, value, siteId):
        self.name = name
        self.value = value
        self.index = index
        self.lock_type = None
        self.locked = False
        self.latestUpdate = 0 # not used anymore
        self.siteId = siteId

    def getValue(self):
        """
        Get variable's value
        :return: value
        """
        return self.value

    def setValue(self, value):
        """
        Sets value of the variable
        :param value: new value to be set to
        """
        self.value = value

    def isLocked(self):
        """
        Checks if this variable has a lock
        :return: type of lock if present else None
        """
        return self.lock_type

    def setLockType(self, lock_type):
        """
        Sets type of lock to variable
        :param lock_type: Read or Write
        """
        self.lock_type = lock_type

    @staticmethod
    def getListOfSites(var):
        """
        Returns list of sites that have this variable
        :param var: index of variable
        :return: list of sites that have the var
        """
        if type(var) == str:
            var = int(var[1:])
        if var % 2 == 0:
            return "all"
        else:
            return (var % 10) + 1

    def getCurrentSite(self):
        """
        Returns current siteID
        :return: siteID
        """
        return self.siteId
