'''
    QueryDeadlineInjectData.py - Capture and record custom job statistics

    Puesdo-code:
    Check every active job in the queue:
    IF job is currently active (rendering/queued) THEN
        Return job object & tasks and calculate job stats object
        Query & inject average frame render time into column "ExtraInfo2" for each job
        Query & inject peak ram usage into column "ExtraInfo3" for each job

    Notes:
    1. It is assumed a studio will rename the "ExtraInfo2" column used to something more meaningful such as "Average Frame Render Time" via repo options
    2. It is assumed a studio will rename the "ExtraInfo3" column used to something more meaningful such as "Peak RAM Usage" via repo options
    2. It is assumed we are only checking currently "Active" & "Queued" jobs only
    3. It is assumed we are running this python script on a machine that has the Deadline client software already installed
'''

from System import TimeSpan

from Deadline.Scripting import *
from Deadline.Jobs import *

def __main__():

    print "Script Started..."

    MIN_COMPLETED_TASKS = 0 #Min - Number of Completed Tasks BEFORE the job is queried. Change as applicable

    # Grab all jobs
    alljobs = RepositoryUtils.GetJobs( True )

    # Filter down to only "Active" jobs
    jobs=[]
    for job in alljobs:
        if job.JobStatus == "Active":
            jobs.append( job )

    for job in jobs:

        print "JobStatus: %s" % job.JobStatus

        jobId = job.JobId
        print "JobId: %s" % jobId
        
        jobName = job.JobName
        print "JobName: %s" % jobName

        JobTaskCount = job.JobTaskCount
        print "JobTaskCount: %s" % JobTaskCount
        
        jobCompletedChunks = job.CompletedChunks
        print "JobCompletedChunks: %s" % jobCompletedChunks

        job = RepositoryUtils.GetJob( jobId, True )
        tasks = RepositoryUtils.GetJobTasks( job, True )
        stats = JobUtils.CalculateJobStatistics( job, tasks )
        
        jobAverageFrameRenderTime = stats.AverageFrameRenderTime
        jobPeakRamUsage = stats.PeakRamUsage/1024/1024

        print "JobAverageFrameRenderTime: %s" %  jobAverageFrameRenderTime
        print "JobPeakRamUsage: %s" % jobPeakRamUsage

        if jobCompletedChunks >= MIN_COMPLETED_TASKS:
            if not jobAverageFrameRenderTime.Equals(TimeSpan.Zero):
                if jobPeakRamUsage != 0:
                    
                    timeSpan = jobAverageFrameRenderTime
                    timeSpan = "%02dd:%02dh:%02dm:%02ds" % (timeSpan.Days, timeSpan.Hours, timeSpan.Minutes, timeSpan.Seconds)

                    job.ExtraInfo2 = str(timeSpan)
                    job.ExtraInfo3 = str(jobPeakRamUsage) + "Mb"

                    RepositoryUtils.SaveJob( job )
                else:
                    print  "Job Peak Ram Usage is 0Mb at this time, skipping check until next scan..."
            else:
                print "Job Average Frame Render Time is 00:00:00 at this time, skipping check until next scan..."
        else:
            print "Min Number of Completed Tasks: %s not yet reached, skipping check until next scan..." % MIN_COMPLETED_TASKS

    print "...Script Completed"
