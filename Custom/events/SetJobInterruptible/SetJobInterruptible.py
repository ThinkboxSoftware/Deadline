###############################################################
#  Imports
###############################################################
from Deadline.Events import *
from Deadline.Scripting import *


###############################################################
#  This is the function called by Deadline to get an instance of the Draft event listener.
###############################################################
def GetDeadlineEventListener():
    return SetJobInterruptibleListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


###############################################################
#  The event listener class.
###############################################################
class SetJobInterruptibleListener (DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):
        
        self.LogInfo( ">Checking if submitted job should be made interruptible" )

        poolNames = self.GetConfigEntry( "JobPools" ).split( ',' )
        interruptible = self.GetBooleanConfigEntryWithDefault( "Interruptible", True )
        interruptiblePercentage = self.GetIntegerConfigEntryWithDefault( "InterruptiblePercentage", 100 )
        
        for poolName in poolNames:
            if poolName.lower() == job.JobPool.lower():
                job.JobInterruptible = True
                self.LogInfo ( "+Job Is Interruptible is Enabled" )
                job.JobInterruptiblePercentage = interruptiblePercentage
                self.LogInfo ( "+Job Interruptible Percentage set to: %s" % interruptiblePercentage )
                break

        RepositoryUtils.SaveJob(job)
