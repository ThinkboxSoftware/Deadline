#############################################################################################
#  Imports
#############################################################################################
from System.Diagnostics import *
from System.IO import *

from Deadline.Events import *
from Deadline.Scripting import *

#############################################################################################
#  This is the function called by Deadline to get an instance of AutoChunker.
#############################################################################################
def GetDeadlineEventListener():
	return AutoChunker()

def CleanupDeadlineEventListener( eventListener ):
	eventListener.Cleanup()

#############################################################################################
#  AutoChunker generic event listener class.
#############################################################################################
class AutoChunker( DeadlineEventListener ):
	'''
	AutoChunker attempts to calculate an optimal ChunkSize for all Maya jobs submitted to Deadline,
	based on slave count in pool, slave count in group, limit(s) applied to the job, a user controlled
	multiplying factor, and finally the actual frame range. Various control knobs are exposed in the
	event plugin to let users tinkle with what best works for the majority of jobs in their studio.
	
	Currently limited to Maya jobs, but could easily be tweaked to work against all/some job plugins.
	'''
	
	def __init__( self ):
		self.OnJobSubmittedCallback += self.OnJobSubmitted

	def Cleanup( self ):
		del self.OnJobSubmittedCallback

	# This is called when a job is submitted.
	def OnJobSubmitted( self, job ):
		
		# Only execute for Maya jobs.
		jobPlugin = job.JobPlugin
		if jobPlugin != "MayaBatch" or jobPlugin != "MayaCmd":
			return

		# Only execute if it's a job submitted by user "dave", for say, testing purposes.
		# if job.JobUserName != "dave":
		# 	return

		print "AutoChunker running as this is a Maya job"

		self.Verbose = self.GetBooleanConfigEntryWithDefault( "Verbose", False )
		print "Verbose Logging: %s" % self.Verbose

		minFrameCount = self.GetIntegerConfigEntryWithDefault( "MinFrameCount", 10 )
		print "MinFrameCount: %s" % minFrameCount

		jobFramesList = job.JobFramesList
		frameCount = len(jobFramesList)

		if self.Verbose:
			print "Frame Count: %s" % frameCount
		
		if minFrameCount > frameCount:
			print "AutoChunker exiting as job frame count is less than min frame count"
			return

		print "BEFORE [ChunkSize]: %s" % job.JobFramesPerTask
		
		limitGroups = list(job.JobLimitGroups)
		
		if self.Verbose:
			print "jobPool: %s" % job.JobPool
			print "jobGroup: %s" % job.JobGroup
			print "jobLimits: %s" % limitGroups

		usePool = self.GetBooleanConfigEntryWithDefault( "UsePool", True )
		useGroup = self.GetBooleanConfigEntryWithDefault( "UseGroup", True )
		useLimits = self.GetBooleanConfigEntryWithDefault( "UseLimits", True )

		slavePool=None
		slaveGroup=None
		slaveLimits=None

		if usePool:
			slavePool = len(self.GetSlaveNamesInPool( job.JobPool ))
		
		if useGroup:
			slaveGroup = len(self.GetSlaveNamesInGroup( job.JobGroup ))

		if useLimits:
			slaveLimits = len(self.GetLimitBasedSlaves( limitGroups ))

		if self.Verbose:
			print "slavePool: %s" % slavePool
			print "slaveGroup: %s" % slaveGroup
			print "slaveLimits: %s" % slaveLimits

		multiplyFactor = self.GetIntegerConfigEntryWithDefault( "MultiplyFactor", 2 )
		print "MultiplyFactor: %s" % multiplyFactor

		# Calculate number of potential slots
		if slaveLimits > 0:
			l = [(multiplyFactor*slavePool),slaveGroup,slaveLimits]
		else:
			l = [(multiplyFactor*slavePool),slaveGroup]

		slots = min(i for i in l if i is not None)

		if slots == 0:
			print "There are no Slaves which satisfy the job requirements. Submitting anyways with default slots of 1"
			slots = 1

		if self.Verbose:
			print "slots: %s" % slots

		maxChunkSize = self.GetIntegerConfigEntryWithDefault( "MaxChunkSize", 50 )
		print "MaxChunkSize: %s" % maxChunkSize

		chunkSize = min(slots, maxChunkSize)

		RepositoryUtils.SetJobFrameRange( job, job.JobFrames, chunkSize )
		# RepositoryUtils.SaveJob( job )

		print "AFTER [ChunkSize]: %s" % job.JobFramesPerTask

	def GetLimitBasedSlaves( self, limitGroups ):
		'''
		Given any limits for the job, return list of slaves which will actually be
		applicable for the job at this exact moment during job submission.
		'''
		slaves=[]
		whitelistedSlaves=[]
		blacklistedSlaves=[]

		for limit in limitGroups:
			
			limitGroup = RepositoryUtils.GetLimitGroup( limit, True )
			listedSlaves = limitGroup.LimitGroupListedSlaves
			
			for slave in listedSlaves:
				if limitGroup.LimitGroupWhitelistFlag:
					whitelistedSlaves.append(slave)
				else:
					blacklistedSlaves.append(slave)

		slaves = list(set(whitelistedSlaves)-set(blacklistedSlaves))

		if self.Verbose:
			print "GetLimitBasedSlaves: %s" % slaves
		
		return slaves

	def GetSlaveNamesInPool( self, poolName ):
		'''
		Given the pool for the job, return list of slaves which are enabled and
		members of this pool, correct at moment of job submission.
		'''
		slaves=[]
		slaveSettings = RepositoryUtils.GetSlaveSettingsList( True )
		for slave in slaveSettings:
			if slave.SlaveEnabled and poolName in slave.SlavePools:
				slaves.append(slave.SlaveName)

		if self.Verbose:
			print "GetSlaveNamesInPool: %s" % slaves

		return slaves

	def GetSlaveNamesInGroup( self, groupName ):
		'''
		Given the group for the job, return list of slaves which are enabled and
		members of this group, correct at moment of job submission.
		'''
		slaves=[]
		slaveSettings = RepositoryUtils.GetSlaveSettingsList( True )
		for slave in slaveSettings:
			if slave.SlaveEnabled and groupName in slave.SlaveGroups:
				slaves.append(slave.SlaveName)

		if self.Verbose:
			print "GetSlaveNamesInGroup: %s" % slaves

		return slaves
