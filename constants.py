import enum
"""
List of constants used in the Transaction Manager and Site Manager
"""
BEGIN = "begin"
READ_ONLY = "beginRO"
READ = "R"
WRITE= "W"
DUMP = "dump"
END = "end"
FAIL = "fail"
RECOVER = "recover"

"""
Enums used : Locktype, TransactionnState, SiteStatus

Authors: Ishita Gangal and Divya Juneja
Date: 28th October, 2019
"""


class LockType(enum.Enum):
    read = 0
    write = 1


class TransactionState(enum.Enum):
    committed = 0
    running = 1
    waiting = 2
    blocked = 3
    aborted = 4


class SiteStatus(enum.Enum):
    UP = 0
    DOWN = 1
    RECOVERING = 2





