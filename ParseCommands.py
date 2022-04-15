import os

import Variable
from Command import Command


class ParseCommands:
    """
    Responsible for reading each line in the file of operations.
    Processes each line and decides whether to call Site Manager or Transaction Manager.
    Site Manager is called for fail, recover, dump transaction types
    Transaction Manager is called for begin, beginRO, read, write, end
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 19th October, 2019
    """

    def __init__(self, file, site_manager, transaction_manager,lock_table):
        self.file = file
        self.siteManager = site_manager
        self.transactionManager = transaction_manager
        self.lockTable = lock_table
        self.lines = self.getLine()
        self.current_time = 0

    def getLine(self):
        """
        Gets next line in file
        """
        with open(self.file, 'r') as test_file:
            for line in test_file:
                if len(line) > 1:
                    yield line

    def getNextCommand(self):
        """
        Returns next command in the line
        :return:
        """
        line = next(self.lines, None)
        if line is None:
            return line
        else:
            return self.processCommand(line)

    def processCommand(self, line):
        """
        Removes comments
        :param line: line read from file
        :return: commands list
        """
        line = line.strip().split("\n")
        commands = []
        for t in line:
            if t.find("//") == 0: #for the comments in test file
                continue
            commands.append(Command(t))
        return commands

    def parseFileCommands(self):
        """
        Calls Site Manager functions or Transaction Manager functions
        based on type of transaction in command
        """
        commands = self.getNextCommand()
        while commands is not None:
            for c in commands:
                self.current_time += 1
                if c.transactionType in ["recover","fail","dump"]:
                    # print("Call Site Manager")
                    self.siteManager.mainSiteManager(c)
                elif c.transactionType in ["R","W","begin","end","beginRO"]:
                    # print("Call Transaction Manager")
                    self.transactionManager.mainTransactionManager(c, self.current_time)
                else:
                    print("Invalid command")
            commands = self.getNextCommand()
        print("Done reading file.")



