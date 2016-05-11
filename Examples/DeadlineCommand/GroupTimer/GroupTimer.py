'''
    GroupTimer.py - Assign groups based on the time of day.
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com
    
    RepositoryUtils.GetSlaveSettings will return an empty, valid,
    SlaveSettings object. Change 'slaveNameX' entries below to avoid
    creating fake Slaves within the Database.
'''

from Deadline.Scripting import *

import datetime

time_start = datetime.time(9, 00)
time_end = datetime.time(17, 00)
time_current = datetime.datetime.now().time()

group_map = [
    {
        "on": "g1",
        "off": "g2",
        "hosts": [
            "slavename1",
            "slavename2",
            "slavename3"
        ]
    },
]


def __main__():
    for group in group_map:
        if time_start < time_current and time_current < time_end:
            group_name = group["on"]
        else:
            group_name = group["off"]

        print(("Using {0}. Tested if the time was between {1} and {2}.".format(group_name, time_start, time_end)))

        for hostname in group["hosts"]:
            slave = RepositoryUtils.GetSlaveSettings(hostname, True)
            
            groups = list(slave.SlaveGroups)

            # Remove any reference to the groups we want to add
            remove_item(groups, group["off"])
            remove_item(groups, group["on"])
            groups.append(group_name)

            slave.SetSlaveGroups(groups)
            
            try:
                RepositoryUtils.SaveSlaveSettings(slave)
                print(("Slave '{0}' group updated.".format(hostname)))
            except Exception as e:
                print(("Slave '{0}' failed to update. {1}.".format(hostname, e.message.capitalize())))


def remove_item(list, item):
    while item in list:
        list.remove(item)
