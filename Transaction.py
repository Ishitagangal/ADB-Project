from constants import TransactionState


class Transaction:
    """
    Transaction objects holds information of the transaction.
    Stores:
        id - Transaction ID
        name - Transaction Name
        readyOnly - Boolean indicating whether transaction is ready only or not
        state - State of trasaction : running, waiting, blocked, committed, aborted
        variablestoBeCommitted - list of variables written by Transaction to be changed on sites.
        startTime - time wen transaction started, used as indicator of age when choosing youngest
                    transaction to abort
                    
    Authors: Ishita Gangal and Divya Juneja
    Date: 20th November, 2019
    """
    def __init__(self, transaction_id, name, tick, readOnly = False):
        self.id = transaction_id
        self.name = name
        self.readOnly = readOnly
        self.state = TransactionState.running
        self.variablesToBeCommitted = dict()
        self.readVar = dict()
        self.writeVar = dict()
        self.startTime = tick

    def getTransactionId(self):
        """
        Get transaction id
        :return: transaction id
        """
        return self.id

    def getTransactionState(self):
        """
        Get transaction state: running, waiting, blocked, committed, aborted
        :return: state
        """
        return self.state

    def getTransactionStartTime(self):
        """
        Return start time of transaction, used to indicate age
        :return: startTime
        """
        return self.startTime

    def checkIfTransactionReadOnly(self):
        """
        Return true if transaction is read only
        :return: True if read only else False
        """
        return self.readOnly

    def getTransactionName(self):
        """
        Return transaction name
        :return: name
        """
        return self.name

    def getReadVariables(self):
        """
        Get all variables read by this transaction
        :return: dict of read variables
        """
        return self.readVar

    def getVariablesToBeCommitted(self):
        """
        Return dictionary of variables written by this transaction
        :return: dictionary of written variables yet to be committed
        """
        return self.variablesToBeCommitted

    def setTransactionState(self, state):
        """
        Set state of transaction
        :param state: state to be set to
        :return: Value error if invalid state
        """
        if state in TransactionState:
            self.state = state
        else:
            raise ValueError("Invalid status of Transaction" + self.id)

    def clearAllUncommittedVariables(self):
        """
        Clears dict of variables to be committed when transaction is aborted/committed
        """
        self.variablesToBeCommitted = dict()
