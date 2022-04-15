import constants

from Transaction import Transaction


class Lock:
    """
    Represents a lock and holds information of type of lock and Transaction that holds it
    type : type of the lock, R or W
    transaction : Transaction that holds this lock
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 20th November, 2019
    """
    def __init__(self, type = None, transaction = None):
        self.type = type
        self.transaction = transaction

    def getTransaction(self):
        """
        Gets transaction holding this lock
        :return: transaction
        """
        return self.transaction

    def setTransaction(self, transaction):
        """
        Sets transaction for this lock
        :param transaction: transaction to be set
        :return: Error if invalid Transaction
        """
        if transaction is None or isinstance(transaction, Transaction):
            self.transaction = transaction
        else:
            raise ValueError("Invalid transaction")

    def getType(self):
        """
        Returns type of lock
        :return: type of lock, read or write
        """
        return self.type

    def setType(self):
        """
        Sets the type of Lock
        :return: Error if invalid type
        """
        if type in constants.LockType:
            self.type = type
        else:
            raise ValueError("Invalid type of lock. Can only be Read or Write")


