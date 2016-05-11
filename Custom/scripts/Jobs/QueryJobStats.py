"""
QueryJobStats.py - Example of how to calculate job statistics for a selected job and print to console the result for average frame render time & peak ram usage
Copyright Thinkbox Software 2016
"""

from System import TimeSpan

from Deadline.Scripting import *


def __main__():

    jobIds = MonitorUtils.GetSelectedJobIds()

    for jobId in jobIds:
        job = RepositoryUtils.GetJob( jobId, True )
        tasks = RepositoryUtils.GetJobTasks( job, True )
        stats = JobUtils.CalculateJobStatistics( job, tasks )
        
        jobAverageFrameRenderTime = stats.AverageFrameRenderTime
        jobPeakRamUsage = stats.PeakRamUsage/1024/1024

        timeSpan = jobAverageFrameRenderTime
        timeSpan = "%02dd:%02dh:%02dm:%02ds" % (
            timeSpan.Days, timeSpan.Hours, timeSpan.Minutes, timeSpan.Seconds)

        print("JobAverageFrameRenderTime: %s" %  timeSpan)
        print("JobPeakRamUsage: %sMb" % jobPeakRamUsage)
