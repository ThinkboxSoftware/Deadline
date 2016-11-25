"""
JobCleanup.py event script

Slave Started event callback script which deletes jobs older than a confirgurable number of days.

1. Configure how many days a job can stay in the farm via delete_days variable (INTEGER only).
2. verbose variable is purely for testing/dev. usage and should be left False as it effects the script performance.
3. dry_run variable allows execution of the script without affecting jobs
"""

#########################################################################################################
# Imports
#########################################################################################################
from Deadline.Events import *
from Deadline.Scripting import *
from System import DateTime, TimeSpan

import os
import time


#########################################################################################################
# This is the function called by Deadline to get an instance of the event listener.
#########################################################################################################
def GetDeadlineEventListener():
    return JobCleanupListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.cleanup()

#########################################################################################################
# The event listener class.
#########################################################################################################
class JobCleanupListener(DeadlineEventListener):
    def __init__(self):
        self.OnHouseCleaningCallback += self.house_cleaning

        self.delete_days = 30
        self.verbose = True
        self.dry_run = True

    def cleanup(self):
        del self.OnHouseCleaning

    def log_verbose(self, message):
        if self.verbose:
            self.LogInfo(message)

    def delete_jobs(self):
        current_time = DateTime.Now
        hours = self.delete_days * 24


        jobs = list(RepositoryUtils.GetJobs(True))
        self.log_verbose("Found {0} jobs. Scanning...".format(len(jobs)))

        older_than = current_time.Subtract(TimeSpan(hours, 0, 0))
        for job in jobs:
            submitted = job.JobSubmitDateTime
            if submitted == DateTime.MinValue:
                continue
            if DateTime.Compare(submitted, older_than) < 0:
                if not self.dry_run:
                    self.log_verbose("Removing job {1} - {0}. Submitted on {2}.".format(job.JobName, job.JobId, submitted))
                    RepositoryUtils.ArchiveJob(job, True, None)
                else:
                    self.log_verbose("Would have removed job {1} - {0}. Submitted on {2}.".format(job.JobName, job.JobId, submitted))

        print("Older than {0}".format(older_than))

    def house_cleaning(self):
        self.LogInfo("Job Cleanup Started")

        self.delete_days = self.GetIntegerConfigEntryWithDefault("DeleteDays", 30)
        self.verbose = self.GetBooleanConfigEntryWithDefault("Verbose", False)
        self.dry_run = self.GetBooleanConfigEntryWithDefault("DryRun", False)

        self.log_verbose("delete_days: %s" % self.delete_days)
        self.log_verbose("dry_run: %s" % self.dry_run)

        self.delete_jobs()

        self.LogInfo("Job Cleanup Completed")
