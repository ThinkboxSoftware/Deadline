from System import *
from System.Diagnostics import *
from System.IO import *

from Deadline.Plugins import *
from Deadline.Scripting import *

######################################################################
## This is the function that Deadline calls to get an instance of the
## plugin. It allows us to abstract away the name
######################################################################
def GetDeadlinePlugin():
    return SampleSimplePlugin()
    
class SampleSimplePlugin(DeadlinePlugin):
    MyClassScopedVariable = 0
    
    def __init__(self):
        """
            Used to set up really basic stuff like event callbacks. In general,
            we use the same function names across the board for these, so using
            this whole function verbatim is likely a good idea.
        """
        
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        self.PreRenderTasksCallback += self.PreRenderTasks
        self.PostRenderTasksCallback += self.PostRenderTasks
    
    def Cleanup(self):
        """
            We need to clean up after ourselves or risk leaking memory in the
            interpreter. Any callbacks assigned *MUST* be removed
        """
        
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback
        
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
        del self.PreRenderTasksCallback
        del self.PostRenderTasksCallback
    
    def InitializeProcess( self ):
        """
            Here we initialize the plugin more deeply. Setting listening hooks
            needs to be here instead of the init function since the plugin
            needs to be fully loaded.
        """
        
        self.SingleFramesOnly = True # Does this plugin support ranges?
        self.PluginType = PluginType.Simple # We aren't to managing a process
        
        self.UseProcessTree = True # End the spawned process if the slave exits
        self.StdoutHandling = True # Actually watch the output. See below
        
        self.AddStdoutHandlerCallback("ERROR:.*").HandleCallback += self.HandleError
        self.AddStdoutHandlerCallback("Fake progress ([0-9]*) of ([0-9]*)").HandleCallback += self.HandleProgress
    
    def PreRenderTasks( self ):
        """
            Stuff to do before we start the render process
        """
        
        Environment.SetEnvironmentVariable("Cake", "Flake")
        self.LogInfo("Preparing for awesome sauce.")
    
    def PostRenderTasks( self ):
        """
            Stuff to do after the render process has exited.
            Note that this and the PreRender work can also be
            done via an external script so you can plug in
            different functionality based on the submitted job
        """
        
        self.LogInfo("Sauce may or may not have been acquired.")    
    
    def RenderExecutable( self ):
        """
            Return the executable path to run here. In all of our plugins
            we allow specifying the path to the executable in the "configure
            plugins" section of the Monitor, and usually we verify what
            version we'll be running. That version number is saved during
            submission, but it's not actually a feature built into the core
            of Deadline. Fun facts :)
        """
        
        self.LogInfo("Supplying program executable for sauce collection.")
        return "cmd.exe"
    
    def RenderArgument( self ):
        """
            Return the argument list we'll pass to the program to run.
            This is usually where the magic happens of converting submission
            option boxes into command line flags. The exceptions of course
            being the complex plugins like MayaBatch and 3DSMax plugins.
        """
    
        self.LogInfo("Argumentating (supplying command line arguments)")

        # Some example calls to configuration params in the dlinit/params files
        config1 = self.GetConfigEntry("SampleProperty")
        config2 = int(self.GetConfigEntryWithDefault("FakeProp1", "-1"))
        
        # These values are submitted with the plugin specific job file.
        option  = self.GetPluginInfoEntryWithDefault("option", "")
        
        # Lots more handy functions here:
        # http://www.thinkboxsoftware.com/deadline-6-scriptpluginsdk/
        
        return "/c echo Sauce please!"
    
    def HandleError( self ):
        """
            This is actually user-specified. You'll notice it from the
            AddStdoutHandler calls above. We just like calling it this.
        """
        
        self.LogInfo("Sauce related problems occured!")
        
        # All of the calls from AddStdoutHandler() will populate regex matches
        # in a local variable for the call it invokes. So, if you want to grab
        # a specific tile, frame, error condition from the output line that
        # matched, use brackets for capture groups.
        #
        # This stuff'll always be returned as text, so cast/convert accordingly!
        #
        # Also, FailRender() does exactly what you expect. It throws a special
        # exception that blows up the RenderTask function and classifies this
        # run as an error for logging purposes.
        FailRender( self.GetRegexMatch(0) )
    
    def HandleProgress( self ):
        """
            This is one is user-specified too. It can be named anything, though
            it's our practice to name progressy things this.
        """
        
        # Specifying a float out of 100 will let the Slave update the per-task
        # progress. This value doesn't count directly to the job progress yet,
        # but it's handy to see where tasks are at. Job progress is the number
        # of tasks that have been completed.
        SetProgress(59.6)

        # See the "HandleError" function for how to pull progress-like things
        # from the match that is done.