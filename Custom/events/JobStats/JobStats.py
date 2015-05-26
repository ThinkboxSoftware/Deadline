###############################################################
# Imports
###############################################################
from System import TimeSpan

from Deadline.Events import *
from Deadline.Scripting import *


###############################################################
# Give Deadline an instance of this class so it can use it.
###############################################################
def GetDeadlineEventListener():
    return StatsListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


###############################################################
# The Stats event listener class.
###############################################################
class StatsListener (DeadlineEventListener):

    def __init__(self):
        self.OnJobFinishedCallback += self.OnJobFinished
    
    def Cleanup(self):
        del self.OnJobFinishedCallback
            
    # This is called when the job finishes rendering.
    def OnJobFinished(self, job):

        # Make sure we have the latest job info
        job = RepositoryUtils.GetJob(job.ID, True)

        tasks = RepositoryUtils.GetJobTasks(job, True)
        stats = JobUtils.CalculateJobStatistics(job, tasks)
        
        jobAverageFrameRenderTime = stats.AverageFrameRenderTime
        jobPeakRamUsage = stats.PeakRamUsage / 1024 / 1024

        timeSpan = jobAverageFrameRenderTime
        timeSpan = "%02dd:%02dh:%02dm:%02ds" % (timeSpan.Days, timeSpan.Hours, timeSpan.Minutes, timeSpan.Seconds)
        
        # Just print it for now. Trival, but left to the user to send this information to a more relevant location or via email.
        self.LogInfo("JobAverageFrameRenderTime: %s" % timeSpan)
        self.LogInfo("JobPeakRamUsage: %sMb" % jobPeakRamUsage)
