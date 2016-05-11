"""
QueryFarmLimits.py - query and print to console ALL Deadline farm limits and their current stubs
Copyright Thinkbox Software 2016
"""

from Deadline.Scripting import *

def __main__():

	limitGroups = RepositoryUtils.GetLimitGroups(True)
	
	for limitGroup in limitGroups:		
		print("----------------------------------------------")
		print("LimitGroupName: %s" % limitGroup.LimitGroupName)
		print("LimitCurrentHolders: %s" % limitGroup.LimitCurrentHolders)
		print("LimitGroupExcludedSlaves: %s" % limitGroup.LimitGroupExcludedSlaves)
		print("LimitGroupLimit: %s" % limitGroup.LimitGroupLimit)
		print("LimitGroupListedSlaves: %s" % limitGroup.LimitGroupListedSlaves)
		print("LimitGroupReleasePercentage: %s" % limitGroup.LimitGroupReleasePercentage)
		print("LimitGroupWhitelistFlag: %s" % limitGroup.LimitGroupWhitelistFlag)
		print("LimitInUse: %s" % limitGroup.LimitInUse)
		print("LimitStubLevel: %s" % limitGroup.LimitStubLevel)

		currentHolders = limitGroup.LimitCurrentHolders
		for currentHolder in currentHolders:
			print("CurrentHolders: %s" % currentHolder)

		excludedSlaves = limitGroup.LimitGroupExcludedSlaves
		for excludedSlave in excludedSlaves:
			print("ExcludedSlaves: %s" % excludedSlave)

		listedSlaves = limitGroup.LimitGroupListedSlaves
		for listedSlave in listedSlaves:
			print("ListedSlaves: %s" % listedSlave)

	#RepositoryUtils.SetLimitGroupMaximum(string name, int limit)
	#RepositoryUtils.SetLimitGroupMaximum( "nuke", 666 )
