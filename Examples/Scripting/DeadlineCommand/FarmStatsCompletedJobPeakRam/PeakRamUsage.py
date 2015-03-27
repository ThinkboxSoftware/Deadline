from Deadline.Scripting import *
from Deadline.Jobs import *

def __main__():

    print "Script Started..."

    for job in RepositoryUtils.GetJobs( True ):
        # Filter completed jobs
        if job.JobStatus != "Completed":
            continue

        jobId = job.JobId

        job = RepositoryUtils.GetJob( jobId, True )
        tasks = RepositoryUtils.GetJobTasks( job, True )
        stats = JobUtils.CalculateJobStatistics( job, tasks )

        jobPeakRamUsage = stats.PeakRamUsage/1024/1024
        print "JobPeakRamUsage: %sMb" % jobPeakRamUsage

    print "...Script Completed"