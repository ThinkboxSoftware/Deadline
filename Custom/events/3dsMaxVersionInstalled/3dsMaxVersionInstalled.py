'''
    Show what versions of 3dsMax is installed on your
    Windows nodes in the 'Extra Info 0' column.
'''

from System.Diagnostics import *
from System.IO import *
from System import *

import os

from Deadline.Events import *
from Deadline.Scripting import *

def GetDeadlineEventListener():
    return ConfigSlaveEventListener()

def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()

class ConfigSlaveEventListener (DeadlineEventListener):
    def __init__(self):
        self.OnSlaveStartedCallback += self.OnSlaveStarted

    def Cleanup(self):
        del self.OnSlaveStartedCallback

    # This is called every time the Slave starts
    def OnSlaveStarted(self, slavename):
        
        # exit if not Windows slave
        if os.name != 'nt':
            return

        configVersions = self.GetConfigEntry("MaxVersions").strip()
        maxVersions = StringUtils.FromSemicolonSeparatedString( configVersions )

        versionList = []

        for maxVersion in maxVersions:
            if File.Exists( maxVersion ):
                # Figure out .NET FileVersion of 3dsmax.exe
                exeVersion = FileUtils.GetExecutableVersion( maxVersion )
                # append to our list
                versionList.append(exeVersion)

        if len(versionList) > 0:
            versions = ','.join(versionList)
            self.LogInfo( "3dsMax.exe versions: %s" % versions )

            slave = RepositoryUtils.GetSlaveSettings(slavename, True)
            slave.SlaveExtraInfo0 = versions
            
            RepositoryUtils.SaveSlaveSettings(slave)
