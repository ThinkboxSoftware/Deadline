###############################################################
# Imports
###############################################################
from System import *

from Deadline.Events import *
from Deadline.Scripting import *


##################################################################################################
# This is the function called by Deadline to get an instance of the Draft event listener.
##################################################################################################
def GetDeadlineEventListener():
    return OverrideJobNameListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


###############################################################
# The event listener class.
###############################################################
class OverrideJobNameListener (DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):

        # Exit this event plugin as soon as possible if not a 3dsMax job
        if job.JobPlugin != "3dsmax":
            return
        
        self.LogInfo("On Job Submitted Event Plugin: Override Job Name Started")

        prefix = self.GetConfigEntryWithDefault("Prefix", "")
        suffix = self.GetConfigEntryWithDefault("Suffix", "")

        tempName = ""

        if prefix != "":
            tempName += prefix + "_"

        if job.JobName != "":
            tempName += str(job.JobName)
            tempName += "_"

        tempName += str(job.JobId)

        if suffix != "":
            tempName += "_" + suffix

        job.JobName = tempName

        self.LogInfo("Job Name changed to: %s" % tempName)

        RepositoryUtils.SaveJob(job)

        self.LogInfo("On Job Submitted Event Plugin: Override Job Name Finished")
