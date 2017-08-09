from Deadline.Plugins import *
from Deadline.Scripting import *

from pprint import pprint

import csv
import os

def build_dict(obj):
    '''
        Because Python.net objects have no __dict__, this will build
        it from `dir`. Also take the opportunity to call ToString() on stuff
    '''
    items = {}
    filter_prexes = [
        "get",
        "set",
        "_",
        "Overloads",
        "ReferenceEquals",
        "MemberwiseClone",
        "GetType",
        "GetHashCode",
        "Finalize",
        "Equals",
        "Couch",
        "ToString"]
    for a in dir(obj):
        # Skip over junk we don't care about
        filter = False
        for filter_string in filter_prexes:
            if a.startswith(filter_string):
                filter = True;

        if filter is True:
            continue

        item = getattr(obj, a)

        print(a)
        try:
            # If we've got seconds, we're a timespan
            items[a] = item.TotalSeconds
            print(" As seconds")
        except AttributeError:
            try:
                # Get the .net string repr
                items[a] = item.ToString()
                print(" As .net string")
            except AttributeError:
                # Or get Python's
                items[a] = unicode(item)
                print(" As python string")

    return items

def write_csv(dict_list, filename):
    with open(filename, 'wb') as f:
        w = csv.DictWriter(f, dict_list[0].keys())
        w.writeheader()
        for item in dict_list:
            w.writerow(item)

def __main__():
    job_stats = []

    for job in RepositoryUtils.GetJobs(True):
        tasks = RepositoryUtils.GetJobTasks(job, True)
        stats = JobUtils.CalculateJobStatistics(job, tasks)

        job_stats.append(build_dict(stats))
        
        print('.')

    pprint(job_stats)
        
    path = os.path.join(os.path.dirname(__file__), "jobs.csv")
    write_csv(job_stats, path)
    print("Saved stats to {}".format(path))
