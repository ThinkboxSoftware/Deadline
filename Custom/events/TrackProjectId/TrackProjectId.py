###############################################################
# Imports
###############################################################
from __future__ import print_function
from System import *

from Deadline.Events import *
from Deadline.Scripting import *

##################################################################################################
# This is the function called by Deadline to get an instance of the TrackProjectId event listener.
##################################################################################################
def GetDeadlineEventListener():
    return TrackProjectIdListener()

def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()

###############################################################
# The event listener class.
###############################################################
class TrackProjectIdListener (DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):

        # Exit this event plugin as soon as possible if job name length is less than valid 5 characters
        if len(job.JobName) < 5:
            return
        
        projectId = job.JobName[0:5]
        print( "Submitted DL job for Project Id: {}".format(projectId) )
        
        job.JobExtraInfo0 = projectId
        RepositoryUtils.SaveJob(job)
