'''
    OverrideIPs.py - Assign IP overrides to a list of Slaves
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com
    
    RepositoryUtils.GetSlaveSettings will return an empty, valid,
    SlaveSettings object. Change 'slaveNameX' entries below to avoid
    creating fake Slaves within the Database.
'''

from Deadline.Scripting import *

machines = {
    "slaveName1": "192.168.0.1",
    "slaveName2": "192.168.0.2",
    "slaveName3": "192.168.0.3",
}


def __main__():
    for hostname, ip in machines.items():
        # This is extremely inefficent as it needs to do
        # multiple queries to the database for each Slave.
        
        # Running within a context where Slave information
        # would already be loaded (the Monitor, Pulse), use
        # 'False' to use the internal cache
        
        slave = RepositoryUtils.GetSlaveSettings(hostname, True)
        
        oldIp = slave.HostMachineIPAddressOverride
        slave.HostMachineIPAddressOverride = ip
        
        try:
            RepositoryUtils.SaveSlaveSettings(slave)
            print("Slave '{0}' updated to address override from '{1}' to '{2}' successfully.".format(hostname, oldIp, ip))
        except Exception as e:
            print("Slave '{0}' failed to update. {1}.".format(hostname, e.message.capitalize()))
