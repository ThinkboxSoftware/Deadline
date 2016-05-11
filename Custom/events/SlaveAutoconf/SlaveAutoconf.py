'''
    Stolen from Gavin's great example on this forum thread:
    https://forums.thinkboxsoftware.com/viewtopic.php?f=11&t=13396#p59978
'''

from System.Diagnostics import *
from System.IO import *
from System import TimeSpan

from Deadline.Events import *
from Deadline.Scripting import *

import re
import sys
import os
import subprocess
import traceback
import shlex

SLAVE_NAME_PREFIX = "mobile-"
POOLS = ["one", "two", "three"]


def GetDeadlineEventListener():
    return ConfigSlaveEventListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


class ConfigSlaveEventListener (DeadlineEventListener):
    def __init__(self):
        self.OnSlaveStartedCallback += self.OnSlaveStarted

    def Cleanup(self):
        del self.OnSlaveStartedCallback

    # This is called every time the Slave starts
    def OnSlaveStarted(self, slavename):
        if not slavename.lower().startswith(SLAVE_NAME_PREFIX):
            return

        print(("Slave automatic configuration for {0}".format(slavename)))
        for pool in POOLS:
            try:
                print(("\tAdding pool {0}".format(pool)))
                RepositoryUtils.AddPoolToSlave(slavename, pool)

                # Power management example:
                # pmanage = RepositoryUtils.GetPowerManagementOptions()
                # pmanage.Groups[0].SlaveNames.append(slavename)

            except:
                ClientUtils.LogText(traceback.format_exc())
