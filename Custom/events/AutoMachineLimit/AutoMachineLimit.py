###############################################################
#  Imports
###############################################################
from System.Diagnostics import *
from System.IO import *
from System import TimeSpan

from Deadline.Events import *
from Deadline.Scripting import *

import re
import sys
import os


###############################################################
#  This is the function called by Deadline to get an instance of the job event listener.
###############################################################
def GetDeadlineEventListener():
    return JobEventListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


###############################################################
#  Priority clamp event listener class.
###############################################################
class JobEventListener (DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup(self):
        del self.OnJobSubmittedCallback

    # This is called when a job is submitted.
    def OnJobSubmitted(self, job):
        user = job.JobUserName
        priviledged = False
        
        limit = self.GetIntegerConfigEntry("Limit")
        usergroup = self.GetConfigEntry("UserGroups")

        groups = RepositoryUtils.GetUserGroupsForUser(user)

        for group in groups:
            if group == usergroup:
                priviledged = True

        if not priviledged and (job.MachineLimit > limit or job.MachineLimit == 0 ):
            job.MachineLimit = limit
            print("Job machine limit downgraded to {0}. See someone in the {1} group for assistance".format(limit, group))

        RepositoryUtils.SaveJob(job)