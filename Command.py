import re


class Command:
    """
    Command read from the test operations
    Stores:
        type of transaction: begin, end, read, beingRO, write,
                             dump, fail, recover
        transaction parameters: everything within (...)
        
    Authors: Ishita Gangal
    Date: 20th October, 2019
    """

    pattern = "\((.*?)\)"

    def __init__(self, transaction):
        self.transactionType = (transaction.split('(')[0]).strip(" ")
        self.transactionParameters = re.search(self.pattern, transaction).group()
        self.transactionParameters = self.transactionParameters.strip('()')
        self.transactionParameters = map(lambda x: x.strip(), self.transactionParameters.split(','))
        self.transactionParameters = list(self.transactionParameters)

    def get_transactionType(self):
        """
        Getter for transaction type
        :return: the type of transaction : begin, beingRO, read, write, end, dump, fail, recover
        """
        return self.transactionType

    def get_transactionParameters(self):
        """
        Getter for transaction parameters
        :return: parameters
        """
        return self.transactionParameters
