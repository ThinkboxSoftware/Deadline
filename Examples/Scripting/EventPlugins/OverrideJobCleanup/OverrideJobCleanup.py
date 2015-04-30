
###############################################################
## Imports
###############################################################
from System import *

from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## This is the function called by Deadline to get an instance of the Draft event listener.
###############################################################
def GetDeadlineEventListener():
    return OverrideJobCleanupListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The event listener class.
###############################################################
class OverrideJobCleanupListener (DeadlineEventListener):
    def __init__( self ):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup( self ):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted( self, job ):

        # Exit this event plugin as soon as possible if not applicable
        if job.JobPlugin != "Nuke" and job.JobPlugin != "3dsmax" and job.JobPlugin != "MayaBatch" and job.JobPlugin != "MayaCmd":
            return
        
        self.LogInfo( "On Job Submitted Event Plugin: Override Job Cleanup Started" )

        #Nuke Jobs
        if job.JobPlugin == "Nuke":
            nukeJobCleanupDays = self.GetConfigEntryWithDefault( "nukeJobCleanupDays", "-1" )
            nukeOverrideJobCleanupType = self.GetConfigEntryWithDefault( "nukeOverrideJobCleanupType", "Disabled" )

            if nukeJobCleanupDays != "-1":
                job.JobOverrideAutoJobCleanup = True
                job.JobOverrideJobCleanup = True
                job.JobCleanupDays = int(nukeJobCleanupDays)
                self.LogInfo( "Nuke: Job Cleanup Days changed to: %s" % nukeJobCleanupDays )

                if nukeOverrideJobCleanupType != "Disabled":
                    if nukeOverrideJobCleanupType == "Archive":
                        job.JobOverrideJobCleanupType = 1
                    elif nukeOverrideJobCleanupType == "Delete":
                        job.JobOverrideJobCleanupType = 2
                    self.LogInfo( "Nuke: Job Override Job Cleanup Type changed to: %s" % nukeOverrideJobCleanupType )

        #3ds Max Jobs
        if job.JobPlugin == "3dsmax":
            maxJobCleanupDays = self.GetConfigEntryWithDefault( "maxJobCleanupDays", "-1" )
            maxOverrideJobCleanupType = self.GetConfigEntryWithDefault( "maxOverrideJobCleanupType", "Disabled" )

            if maxJobCleanupDays != "-1":
                job.JobOverrideAutoJobCleanup = True
                job.JobOverrideJobCleanup = True
                job.JobCleanupDays = int(maxJobCleanupDays)
                self.LogInfo( "3dsMax: Job Cleanup Days changed to: %s" % maxJobCleanupDays )

                if maxOverrideJobCleanupType != "Disabled":
                    if maxOverrideJobCleanupType == "Archive":
                        job.JobOverrideJobCleanupType = 1
                    elif maxOverrideJobCleanupType == "Delete":
                        job.JobOverrideJobCleanupType = 2
                    self.LogInfo( "3dsMax: Job Override Job Cleanup Type changed to: %s" % maxOverrideJobCleanupType )

        #Maya Jobs
        if job.JobPlugin == "MayaBatch" or job.JobPlugin == "MayaCmd":
            mayaJobCleanupDays = self.GetConfigEntryWithDefault( "mayaJobCleanupDays", "-1" )
            mayaOverrideJobCleanupType = self.GetConfigEntryWithDefault( "mayaOverrideJobCleanupType", "Disabled" )

            if mayaJobCleanupDays != "-1":
                job.JobOverrideAutoJobCleanup = True
                job.JobOverrideJobCleanup = True
                job.JobCleanupDays = int(mayaJobCleanupDays)
                self.LogInfo( "Maya: Job Cleanup Days changed to: %s" % mayaJobCleanupDays )

                if mayaOverrideJobCleanupType != "Disabled":
                    if mayaOverrideJobCleanupType == "Archive":
                        job.JobOverrideJobCleanupType = 1
                    elif mayaOverrideJobCleanupType == "Delete":
                        job.JobOverrideJobCleanupType = 2
                    self.LogInfo( "Maya: Job Override Job Cleanup Type changed to: %s" % mayaOverrideJobCleanupType )
        
        RepositoryUtils.SaveJob(job)

        self.LogInfo( "On Job Submitted Event Plugin: Override Job Cleanup Finished" )
