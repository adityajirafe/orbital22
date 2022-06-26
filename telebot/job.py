from enum import Enum

class Jobs(Enum):
    START = 1
    USERNAME = 2
    PASSWORD = 3
    LONGTRADE = 4
    SHORTTRADE = 5
    LOGOUT = 6
    SLEEP = 7
    LISTEN = 8
    CLOSELONG = 9
    CLOSESHORT = 10
    NOTRADE = 11