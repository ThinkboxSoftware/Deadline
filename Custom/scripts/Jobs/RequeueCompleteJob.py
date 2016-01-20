"""
    RequeueCompleteJob.py - Requeue and then Complete a job to force the Draft event plugin to execute
"""
from System.IO import *
from System.Diagnostics import *

from Deadline.Scripting import *


########################################################################
# Main Function Called By Deadline
########################################################################
def __main__():
    selectedJobs = MonitorUtils.GetSelectedJobs()
    for job in selectedJobs:

        RepositoryUtils.RequeueJob(job)
        
        # Broken in Deadline 6.2, fixed in Deadline 7/8 onwards
        # RepositoryUtils.CompleteJob(job)

        # Use different technique to workaround broken Scripting API function above
        deadlineCommand = Path.Combine(ClientUtils.GetBinDirectory(), "DeadlineCommand.exe")
        arguments = "-CompleteJob " + job.JobId
        process = ProcessUtils.SpawnProcess(deadlineCommand, arguments, ClientUtils.GetBinDirectory(), ProcessWindowStyle.Hidden, True)
        ProcessUtils.WaitForExit(process, -1)
