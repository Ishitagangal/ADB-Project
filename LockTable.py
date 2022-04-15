import constants
from Lock import Lock


class LockTable:
    """
    Lock Table maintained by Data Manager on each site.
    Holds the lock dictionary.
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 24th November, 2019
    """
    def __init__(self):
        self.lockDict = dict()

    def get_lockDict(self):
        """
        Get lock dictionary
        :return: lockDict
        """
        return self.lockDict

    def getNumOfLock(self, variable):
        """
        Returns number of locks on a variable in the lock dictionary
        :param variable: variable we want to look up
        :return: length of lock dict for this variable
        """
        if variable in self.lockDict:
            # print(str(len(self.lockDict[variable])))
            return len(self.lockDict[variable])
        else:
            return 0

    def setLock(self, transaction, type, variable):
        """
        Sets the lock for transaction on variable
        :param transaction: transaction requesting lock
        :param type: lock type that is being requested
        :param variable: variable on which lock is requested
        :return: True if lock is set, else False
        """
        newLock = Lock(type, transaction)
        if variable not in self.lockDict:
            self.lockDict[variable] = []

        for l in self.lockDict[variable]:
            if l == newLock:
                return
        self.lockDict[variable].append(newLock)

    def checkReadLocked(self,variable):
        """
        Checks if variable has a read lock on it
        :param variable: variable to look up
        :return: True if it read locked, else False
        """
        if variable in self.lockDict:
            for lock in self.lockDict[variable]:
                if lock.getType() == constants.LockType.read:
                    return True
                else:
                    return False
        else:
            return False

    def checkWriteLocked(self,variable):
        """
        Checks if variable has a write lock on it
        :param variable: variable to look up
        :return: True if it write locked, else False
        """
        if variable in self.lockDict:
            for lock in self.lockDict[variable]:
                if lock.getType() == constants.LockType.write:
                    return True
                else:
                    return False
        else:
            return False

    def checkLocked(self, variable):
        """
        Checks if variable has a lock on it
        :param variable: variable to look up
        :return: True if has lock(read or write), else False
        """
        if variable in self.lockDict:
            if len(self.lockDict[variable]) == 0:
                return False
            else:
                return True
        else:
            return False

    def checkTransactionHasLock(self, curTransaction, variable, type = None):
        """
        Checks if transaction already has a lock on the variable
        :param curTransaction: transaction to check if it has a lock on variable
        :param variable: variable to look up
        :param type: type of lock if specified else None
        :return: True if curTransaction has lock else False
        """
        if variable not in self.lockDict:
            return False
        else:
            for lock in self.lockDict[variable]:
                transaction = lock.getTransaction()
                if curTransaction.getTransactionId() == transaction.getTransactionId():
                    if type is None or type == lock.getType():
                        return True

    def releaseLock(self, lock, variable):
        """
        Releases lock on variable if exists
        :param lock: lock type
        :param variable: variable to be released from lock
        :return: True if released, False if no lock on variable
        """
        if variable in self.lockDict.keys():
            try:
                # print(str(variable))
                # print("Lock dictioonary:"+str(self.lockDict))
                # print("index = :"+str(self.lockDict[variable].i))
                index = self.lockDict[variable].index(lock)
                self.lockDict[variable] = self.lockDict[variable][:index] + self.lockDict[variable][index + 1:]
                if len(self.lockDict[variable]) == 0:
                    self.lockDict.pop(variable)
                return True
            except ValueError:
                pass
        else:
            return False

    def releaseAllLocks(self, variable):
        """
        Releases all locks on variable
        :param variable: variable to be released
        """
        self.lockDict.pop(variable)

