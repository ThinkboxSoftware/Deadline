###############################################################
# Imports
###############################################################
import sys

from Deadline.Events import DeadlineEventListener
from Deadline.Scripting import RepositoryUtils

import os
import string
#########################################################################################
# This is the function called by Deadline to get an instance of the Draft event listener.
#########################################################################################


def GetDeadlineEventListener():
    return CustomEnvironmentCopyListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()

###############################################################
# The event listener class.
###############################################################


class CustomEnvironmentCopyListener (DeadlineEventListener):

    def __init__(self):
        if sys.version_info.major == 3:
            super().__init__()        
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):
        # List of environment keys you don't want passed.
        unwantedkeys = self.GetConfigEntryWithDefault("UnwantedEnvKeys", "")

        # Split out on commas, gettting rid of excess whitespace and make uppercase
        unwantedkeys = [x.strip().upper() for x in unwantedkeys.split(',')]

        wantedkeys = []

        self.LogInfo("Unwanted Environment keys defined as:")
        self.LogInfo(str(unwantedkeys))

        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Started")

        # Go through the current system environment variables not copying the unwanted keys
        for key in os.environ:
            if key.upper() not in unwantedkeys:
                wantedkeys.append(key)

        # Set chosen variables to job
        for key in wantedkeys:
            self.LogInfo("Setting %s to %s" % (key, os.environ[key]))
            job.SetJobEnvironmentKeyValue(key, os.environ[key])

        RepositoryUtils.SaveJob(job)

        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Finished")
