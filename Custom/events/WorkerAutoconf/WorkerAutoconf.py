'''
    Stolen from Gavin's great example on this forum thread:
    https://forums.thinkboxsoftware.com/viewtopic.php?f=11&t=13396#p59978
'''
from System import TimeSpan

from Deadline.Events import DeadlineEventListener
from Deadline.Scripting import RepositoryUtils, ClientUtils

import re
import sys
import os
import subprocess
import traceback
import shlex

WORKER_NAME_PREFIX = "" # Example: "mobile-"
POOLS = [] # Example: ["one", "two", "three"]
LISTENING_PORT=None # or 27100


def GetDeadlineEventListener():
    return ConfigSlaveEventListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


class ConfigSlaveEventListener (DeadlineEventListener):
    def __init__(self):
        if sys.version_info.major == 3:
            super().__init__()
        self.OnSlaveStartedCallback += self.OnSlaveStarted

    def Cleanup(self):
        del self.OnSlaveStartedCallback

    # This is called every time the Worker starts
    def OnSlaveStarted(self, slavename):
        # Load Worker settings for when we needed
        worker = RepositoryUtils.GetSlaveSettings(slavename, True)

        # Skip over Workers that don't match the prefix
        if not slavename.lower().startswith(WORKER_NAME_PREFIX):
            return

        print("Worker automatic configuration for {0}".format(slavename))

        # Set up the Pools we want to use
        for pool in POOLS:
            try:
                print("   Adding pool {0}".format(pool))
                RepositoryUtils.AddPoolToSlave(slavename, pool)

                # Power management example:
                # pmanage = RepositoryUtils.GetPowerManagementOptions()
                # pmanage.Groups[0].SlaveNames.append(slavename)

            except:
                ClientUtils.LogText(traceback.format_exc())

        # Set up the listening port
        if LISTENING_PORT:
            print("   Configuring Worker to listen on port {0}".format(LISTENING_PORT))
            worker.SlaveListeningPort = LISTENING_PORT
            worker.SlaveOverrideListeningPort = True
        else:
            print("   Configuring Worker to use random listening port".format(LISTENING_PORT))
            worker.SlaveOverrideListeningPort = False

        # Save any changes we've made back to the database
        RepositoryUtils.SaveSlaveSettings(worker)
