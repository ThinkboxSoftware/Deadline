'''
    JobPreLoad.py - Set Deadline job properties as variables
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com

    Similar to the other script here, but our mappings are what job
    properties to make available to scripts being run. You can get
    a full list possible of properties here:
    http://docs.thinkboxsoftware.com/products/deadline/7.0/2_Scripting%20Reference/class_deadline_1_1_jobs_1_1_job.html
    
    Written by Edwin Amsler <support@thinkboxsoftware.com>
'''
from System import *
from System.IO import *


MAP = [
    ('JobPriority', 'DEADLINE_PRIORITY'),
    ('JobId', 'DEADLINE_JOBID'),
    ('JobInterruptible', 'DEADLINE_INTERRUPTABLE')
]


def __main__(deadlinePlugin):
    deadlinePlugin.LogInfo("Setting environment")

    job = deadlinePlugin.GetJob()

    for item in MAP:
        data = getattr(job, item[0])
        deadlinePlugin.SetProcessEnvironmentVariable(item[1], str(data))
