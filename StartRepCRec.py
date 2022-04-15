import argparse
import sys
from Site import Site
from Variable import Variable
from ParseCommands import ParseCommands
from TransactionManager import TransactionManager
from LockTable import LockTable
from SiteManager import SiteManager


def main():
    """
    Main Function that initializes siteManager, Locktable, Transaction Manager.
    Calls parser in ParseCommands(...) to start reading the test file.
    Output is written out to file if specified with --outFile else prints to stdout
    
    Authors: Ishita Gangal and Divya Juneja
    Date: 18th October, 2019
    """
    parser = argparse.ArgumentParser(description='ADB project')
    parser.add_argument('--filePath', type=str,
                        help="path to file which has the instructions")
    parser.add_argument('--num_sites', type=int, default=10,
                        help='Number of sites')
    parser.add_argument('--num_Var', type=int, default=20,
                        help='number of variables')
    parser.add_argument('--outFile', type=str,
                        help='Output file, if not passed default to stdout')

    args = parser.parse_args()
    if args.outFile:
        sys.stdout = open(args.outFile, "w")
    lockTable = LockTable()
    siteManager = SiteManager(args.num_sites, args.num_Var)
    transactionManager = TransactionManager(lockTable, siteManager)
    parser = ParseCommands(args.filePath, siteManager, transactionManager, lockTable)
    parser.parseFileCommands()


if __name__ == '__main__':
    main()

