from Deadline.Events import DeadlineEventListener
from Deadline.Scripting import SystemUtils
from subprocess import check_output

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return PreRender()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for PreRender.
######################################################################
class PreRender (DeadlineEventListener):

    def __init__( self ):
        self.OnSlaveRenderingCallback += self.PopulatePath

    def Cleanup ( self ):
        del self.OnSlaveRenderingCallback

    def PopulatePath( self, *args ):
        commandPath = ""

        self.LogMessage("Starting PreRender script")

        if SystemUtils.IsRunningOnMac():
            commandPath = self.GetConfigEntryWithDefault("MacOSPath","")
        elif SystemUtils.IsRunningOnWindows():
            commandPath = self.GetConfigEntryWithDefault("WindowsPath","")
        elif SystemUtils.IsRunningOnLinux():
            commandPath = self.GetConfigEntryWithDefault("LinuxPath","")

        if commandPath == "":
            self.LogWarning("No command set")
        else:
            self.ExecuteScript(commandPath)

        self.LogMessage("PreRender script finished")

    def ExecuteScript( self, commandPath ):
        self.LogMessage("Executing command " + commandPath)

        try:
            self.LogMessage(check_output(commandPath.split(' '), shell=True))
        except Exception as exc:
            print(str(exc))
