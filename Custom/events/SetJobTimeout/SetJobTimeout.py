###############################################################
# Imports
###############################################################
from Deadline.Events import *
from Deadline.Scripting import *


def GetDeadlineEventListener():
    return SetJobTimeout()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


###############################################################
# The event listener class.
###############################################################
class SetJobTimeout(DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):
        min_time = self.GetIntegerConfigEntryWithDefault("MinMinute", 0)
        max_time = self.GetIntegerConfigEntryWithDefault("MaxMinute", 0)

        self.LogInfo("Setting minimum and maximum job timeouts to {0} and {1} minutes".format(min_time, max_time))

        job.JobTaskTimeoutSeconds = max_time * 60
        job.JobMinRenderTimeSeconds = min_time * 60

        RepositoryUtils.SaveJob(job)
