
###############################################################
## Imports
###############################################################
from System.Diagnostics import *
from System.IO import *
from System import TimeSpan

from Deadline.Events import *
from Deadline.Scripting import *

import re, sys, os

###############################################################
## This is the function called by Deadline to get an instance of the Salt event listener.
###############################################################
def GetDeadlineEventListener():
    return JobEventListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## priority event listener class.
###############################################################
class JobEventListener (DeadlineEventListener):
    def __init__( self ):
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup( self ):
        del self.OnJobSubmittedCallback


    ## This is called when a job is submitted
    def OnJobSubmitted(self, job):
        user = job.JobUserName
        priviledged = False
        
        priority = self.GetIntegerConfigEntry("Priority")
        usergroup = self.GetConfigEntry("UserGroups")

        groups = RepositoryUtils.GetUserGroupsForUser( user )

        for group in groups:
            if group == usergroup:
                priviledged = True

        if not priviledged and job.JobPriority > priority:
            job.JobPriority = priority
            print("Job priority downgraded to {0}. See someone in the {1} group for assistance".format(priority, group))

        RepositoryUtils.SaveJob(job)