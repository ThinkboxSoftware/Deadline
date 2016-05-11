'''
    GetSlaveState.py - List if Slaves are running or not
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com
'''

# This package is available only to scripts running within Deadline.
# It's magically handled by Python.net.
from Deadline.Scripting import *

stateMapping = {
    # This maps different states to what power management sees
    "Idle": "On",
    "Rendering": "On",
    "Starting Job": "On",
    "Offline": "Off",
    "Stalled": "Off",
    # This state is due to a missing slaveInfo document and
    # shouldn't be acted upon
    "Unknown": "Unknown"
}


def __main__():
    slaveInfos = RepositoryUtils.GetSlaveInfos(True)

    for slaveInfo in slaveInfos:
        state = stateMapping[slaveInfo.SlaveState]
    
        print(("{0: <30}{1}".format(slaveInfo.SlaveName, state)))
