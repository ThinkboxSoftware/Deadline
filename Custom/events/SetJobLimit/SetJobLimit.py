
###############################################################
## Imports
###############################################################
from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## This is the function called by Deadline to get an instance of the Draft event listener.
###############################################################
def GetDeadlineEventListener():
    return SetJobLimitListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The event listener class.
###############################################################
class SetJobLimitListener (DeadlineEventListener):
    def __init__( self ):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup( self ):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted( self, job ):
        limitNames = self.GetConfigEntry( "JobLimits" ).split(',')
        
        for limitName in job.JobLimitGroups:
            if limitName.lower() not in limitNames:
                limitNames.append(limitName)
        
        job.SetJobLimitGroups(limitNames)
        RepositoryUtils.SaveJob(job)

