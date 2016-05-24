"""
ListRequiredAssets.py - Print out to Deadline Monitor Console the Selected Job's Required Assets
Copyright Thinkbox Software 2016
"""

from Deadline.Scripting import *


def __main__():
    jobs = MonitorUtils.GetSelectedJobs()

    for job in jobs:
        RequiredAssets = job.JobRequiredAssets
        
        print("JobName: %s" % job.JobName)
        print("JobID: %s" % job.JobId)
        print("Number of Required Assets: %s" % len(RequiredAssets))

        if len(RequiredAssets) > 0:
            for RequiredAsset in RequiredAssets:
                print(RequiredAsset)
        else:
            print("Job does not contain any Required Assets")
