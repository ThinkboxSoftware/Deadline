"""
QuerySlaveInfo.py - Example of querying ALL slave state/info for ALL slaves in the farm and print to console the results
Copyright Thinkbox Software 2016
"""

from Deadline.Scripting import *

def __main__():
	slaveNames = RepositoryUtils.GetSlaveNames(True)
	for slaveName in slaveNames:
		slaveInfo = RepositoryUtils.GetSlaveInfo( slaveName, True )
		print "Slave Name: %s, Slave State: %s" % (slaveInfo.SlaveName, slaveInfo.SlaveState)

	slaveInfos = RepositoryUtils.GetSlaveInfos(True)
	for slaveInfo in slaveInfos:
		print "Slave Name: %s, Slave State: %s" % (slaveInfo.SlaveName, slaveInfo.SlaveState)

	slaveSettings = RepositoryUtils.GetSlaveSettingsList(True)
	for slaveSetting in slaveSettings:
		print "Slave Name: %s, Slave Description: %s" % (slaveSetting.SlaveName, slaveSetting.SlaveDescription)
