###############################################################
# This is an IronPython script. You'll need to convert it to  #
# a CPython script to make use of the 'os' package and others #
#                                                             #
# To use CPython, add "#Python.NET" as the first line of this #
# file. Make sure you don't use the quotes.                   #
#                                                             #
# I should also mention that this is a "simple plugin"        #
# which isn't as powerful as the complex plugin route         #
###############################################################
from System import *
from System.Diagnostics import *
from System.IO import *

from Deadline.Plugins import *
from Deadline.Scripting import *

######################################################################
## This is the function that Deadline calls to get an instance of the
## overloaded plugin class.
######################################################################
def GetDeadlinePlugin():
	return SampleSimplePlugin()
	
######################################################################
## This is the object we pass back to Deadline. Not all functions
## are represented yet. I'm still learning this stuff myself. :D
##                                                - Edwin
######################################################################
class SampleSimplePlugin(DeadlinePlugin):
	MyClassScopedVariable = 0
	
	## Called by Deadline to initialize the process.
	def InitializeProcess( self ):
		self.SingleFramesOnly = True
		self.PluginType = PluginType.Simple
		
		self.UseProcessTree = True
		self.StdoutHandling = True
		
		self.AddStdoutHandler( "ERROR:.*", self.HandleError )
		self.AddStdoutHandler( "Fake progress ([0-9]*) of ([0-9]*)", self.HandleProgress )
	
	def PreRenderTasks( self ):
		Environment.SetEnvironmentVariable("Cake", "Flake")
		LogInfo("Preparing for awesome sauce.")
	
	def RenderExecutable( self ):
		LogInfo("Supplying program executable for sauce collection.")
		return "cmd.exe"
	
	def RenderArgument( self ):
		LogInfo("Argumentating (supplying command line arguments)")

		# Some example calls to configuration params in the dlinit/params files
		config1 = GetConfigEntry("SampleProperty")
		config2 = int(GetConfigEntryWithDefault("FakeProp1", -1))
		
		# These values are submitted with the plugin specific job file.
		option  = GetPluginInfoEntry("option")
		
		# Lots more handy functions here:
		# http://www.thinkboxsoftware.com/deadline-5-scriptpluginsdk/
		
		return "/c echo Sauce please!"
	
	def PostRenderTasks( self ):
		LogInfo("Sauce may or may not have been acquired.")	
	
	def HandleError( self ):
		"""
			This is actually user-specified. You'll notice it from the
			AddStdoutHandler calls above. We just like calling it this.
		"""
		LogInfo("Sauce related problems occured!")
		
		# All of the calls from AddStdoutHandler() will populate the
		# regex matches for the call it invokes. So, if you want to grab a
		# specific tile, frame, error condition from the output line that
		# matched, use brackets for capture groups. It'll always be returned
		# as text, so cast/convert accordingly!
		# Also, FailRender() does exactly what you expect. It throws a special
		# exception that blows up the RenderTask function.
		FailRender( self.GetRegexMatch(0) )
	
	def HandleProgress( self ):
		"""
			This is one is user-specified too. It can be named anything, though
			it's our practice to name it this.
		"""
		
		# Specifying a float out of 100 will let the Slave update the per-task
		# progress. That value doesn't count directly to the job progress yet,
		# but it's handy to see where people's tasks are at.
		SetProgress(59.6)

		# See the "HandleError" function for how to pull progress-like things
		# from the match that is done.