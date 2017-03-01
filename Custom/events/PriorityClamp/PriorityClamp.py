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
        priority = 0

        priority_map = self.GetConfigEntry('PriorityMap')

        groups = RepositoryUtils.GetUserGroupsForUser(user)
        priorities = priority_map.split(';') # Breaks up into groups

        for i in priorities:
            # Skip over empty lines
            if len(i) < 1:
                continue

            (group, group_priority) = tuple(i.split('<'))

            # Clean up any accidental whitespace
            group = group.strip()
            group_priority = int(group_priority.strip())

            if group in groups:
                priority = max(priority, group_priority)
                print("Allowed job priority upgraded because you're a member of {0}. Currently {1}.".format(group, priority))

        if priority > 0 and job.JobPriority > priority:
            job.JobPriority = priority
            RepositoryUtils.SaveJob(job)
