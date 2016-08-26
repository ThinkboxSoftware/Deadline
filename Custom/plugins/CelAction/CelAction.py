import os
import re
import _winreg

from System.Text.RegularExpressions import *

from Deadline.Plugins import *
from Deadline.Jobs import *
from Deadline.Scripting import *


######################################################################
# This is the function that Deadline calls to get an instance of the
# main DeadlinePlugin class.
######################################################################
def GetDeadlinePlugin():
    return CelActionPlugin()


def CleanupDeadlinePlugin(deadlinePlugin):
    deadlinePlugin.Cleanup()


######################################################################
# This is the main DeadlinePlugin class for the CelAction plugin.
######################################################################
class CelActionPlugin(DeadlinePlugin):

    def __init__(self):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        self.PostRenderTasksCallback += self.PostRenderTasks

    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
        del self.PostRenderTasksCallback

    def InitializeProcess(self):
        # Set the plugin specific settings.
        self.SingleFramesOnly = False

        # Set the process specific settings.
        self.StdoutHandling = True
        self.PopupHandling = True

        # Ignore 'celaction' Pop-up dialogs
        self.AddPopupIgnorer(".*Rendering.*")
        self.AddPopupIgnorer(".*Wait.*")

        # Modify registry for frame separation
        path = r'Software\CelAction\CelAction2D\User Settings'
        _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, path)
        hKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, path, 0,
                               _winreg.KEY_ALL_ACCESS)

        _winreg.SetValueEx(hKey, 'RenderNameUseSeparator', 0,
                           _winreg.REG_DWORD, 1)
        _winreg.SetValueEx(hKey, 'RenderNameSeparator', 0, _winreg.REG_SZ,
                           self.GetPluginInfoEntry("RenderNameSeparator"))

    def RenderExecutable(self):
        for path in self.GetConfigEntry("RenderExecutable").split(";"):
            if os.path.exists(path):
                return path.replace("/", "\\")

    def RenderArgument(self):
        arguments = self.GetPluginInfoEntry("Arguments").strip()
        arguments = RepositoryUtils.CheckPathMapping(arguments)
        arguments = arguments.replace("<STARTFRAME>",
                                      str(self.GetStartFrame()))
        arguments = arguments.replace("<ENDFRAME>", str(self.GetEndFrame()))
        arguments = self.ReplacePaddedFrame(arguments,
                                            "<STARTFRAME%([0-9]+)>",
                                            self.GetStartFrame())
        arguments = self.ReplacePaddedFrame(arguments, "<ENDFRAME%([0-9]+)>",
                                            self.GetEndFrame())
        arguments = arguments.replace("<QUOTE>", "\"")
        return arguments

    def PostRenderTasks(self):
        output_dir = self.GetJob().JobOutputDirectories[0]
        output_name = self.GetJob().JobOutputFileNames[0]

        padding = len(output_name.split('#')) - 1
        head = output_name.split('#' * padding)[0]
        tail = output_name.split('#' * padding)[1]
        render_separator = self.GetPluginInfoEntry("RenderNameSeparator")

        files = []
        pattern = r'%s.*%s[0-9]{%s}%s' % (head, render_separator, padding,
                                          tail)
        for f in os.listdir(output_dir):
            if re.findall(pattern, f):
                files.append(f.replace(tail, '')[:-padding])

        output_paths = []
        output_paths.append(os.path.join(output_dir, output_name))

        for item in list(set(files)):
            value = item + '#' * padding + tail
            output_paths.append(os.path.join(output_dir, value))

        job = self.GetJob()
        RepositoryUtils.UpdateJobOutputFileNames(job, output_paths)

    def ReplacePaddedFrame(self, arguments, pattern, frame):
        frameRegex = Regex(pattern)
        while True:
            frameMatch = frameRegex.Match(arguments)
            if frameMatch.Success:
                paddingSize = int(frameMatch.Groups[1].Value)
                if paddingSize > 0:
                    padding = StringUtils.ToZeroPaddedString(frame,
                                                             paddingSize,
                                                             False)
                else:
                    padding = str(frame)
                arguments = arguments.replace(frameMatch.Groups[0].Value,
                                              padding)
            else:
                break

        return arguments
