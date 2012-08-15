###############################################################
# This is an IronPython script. You'll need to convert it to  #
# a CPython script to make use of the 'os' package and others #
#                                                             #
# To use CPython, add "#Python.NET" as the first line of this #
# file. Make sure you don't use the quotes.                   #
###############################################################

###############################################################
## Imports
###############################################################
from System.Diagnostics import *
from System.IO import *

from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## Give Deadline an instance of this class so it can use it.
## If you've dug around the repository, you'll notice I poached
## this from our Draft code.
###############################################################
def GetDeadlineEventListener():
	return SampleListener()

###############################################################
## The Draft event listener class.
###############################################################
class SampleListener (DeadlineEventListener):
	def OnJobFinished(self, job):
		goods = GetConfigEntryWithDefault( "SampleProperty", "123" )
		bads  = GetConfigEntryWithDefault( "FakeProp1", "also a string" )
		uglys = job.Name
		pass
		
	def OnJobArchived(self, job):
		pass
		
	def OnJobFailed(self, job):
		pass
		
	def OnJobFinished(self, job):
		pass
		
	def OnJobPended(self, job):
		pass
		
	def OnJobReleased(self, job):
		pass
		
	def OnJobRequeued(self, job):
		pass
		
	def OnJobResumed(self, job):
		pass
		
	def OnJobStarted(self, job):
		pass
		
	def OnJobSubmitted(self, job):
		pass
		
	def OnJobSuspended(self, job):
		pass
		
	def OnJobUnarchived(self, job):
		pass
