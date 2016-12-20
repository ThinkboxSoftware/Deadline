'''
    CountSlaves.py - An example of how to find the number of Slaves which have worked on a job
'''

from Deadline.Plugins import *
from Deadline.Scripting import *

from sets import Set


def __main__():
    '''
        Try both methods for counting Slaves on a particular job
    '''
    job_id = "5851875be9faf18185fa9334"
    slave_count = reports_way(job_id)
    print("Number of slaves: {}".format(slave_count))
    slave_count = tasks_way(job_id)
    print("Number of slaves: {}".format(slave_count))


def tasks_way(string_job_id):
    '''
    	Return the number of Slaves which worked on this job by using the task objects.
        This will not count Slaves which tried to render a task if it was completed by
        a different machine at a later date.
    '''
    job = RepositoryUtils.GetJob(string_job_id, True)
    tasks = RepositoryUtils.GetJobTasks(job, True)
    tasks = list(tasks.TaskCollectionAllTasks)

    print("Found {} tasks.".format(len(tasks)))

    slaves = Set()
    for task in tasks:
        slaves.add(task.TaskSlaveName)

    return len(slaves)


def reports_way(string_job_id):
    '''
    	Return the number of Slaves which worked on this job. Note that this
    	will include *all* Slaves, including those which may have thrown errors
        or for tasks that have been re-tried since.
    '''
    report_collection = RepositoryUtils.GetJobReports(string_job_id)
    reports = list(report_collection.GetAllReports())

    print("Found {} reports.".format(len(reports)))

    slaves = Set()
    # This could be done with a Python one-liner. I'm just a noob :D
    for report in reports:
        slaves.add(report.ReportSlaveName)

    return len(slaves)
