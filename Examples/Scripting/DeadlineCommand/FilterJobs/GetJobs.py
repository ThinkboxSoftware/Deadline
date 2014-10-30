'''
    GetJobs.py - List specific jobs by criteria
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com
'''

from Deadline.Scripting import *
from datetime import date, timedelta

# C# goods. This is because the jobs dates will be .net objects
from System import DateTime
last24 = DateTime.Now.AddDays(-1)

def __main__(*args):
    jobs = RepositoryUtils.GetJobs(True)
    for job in jobs:
        # Skip out if not within the last 24 hours
        if DateTime.Compare(job.JobSubmitDateTime, last24) < 0:
            print("Skipped by date")
            continue
            
        # Skip if the status isn't right
        if not (job.JobStatus == 'Active' or job.JobStatus == 'Failed'):
            print("Skipped by status")
            continue
    
        print('Job: {0} ({1})'.format(job.JobName, job.JobId))

   