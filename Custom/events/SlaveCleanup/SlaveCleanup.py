"""
SlaveCleanup.py event script

Slave Started event callback script which recursively crawls file-system and purges ALL files & directories with a MODIFIED TIME older than [DELETE_DAYS] variable.

1. Define top-level directory paths (network/[local to slave] shares) to be scanned in CLEANUP_PATHS list (absolute file path only, relative not supported).
2. Configure number of delete days via DELETE_DAYS variable (INTEGER only).
3. VERBOSE variable is purely for testing/dev. usage and should be left False as it effects the script performance.
4. DRYRUN variable allows execution of the script, but with ALL actual file-system operations being replaced with a print statement, describing intent.
"""

#########################################################################################################
# Imports
#########################################################################################################
from System import *

from Deadline.Events import *
from Deadline.Scripting import *

import os
import time


#########################################################################################################
# This is the function called by Deadline to get an instance of the Slave Cleanup event listener.
#########################################################################################################
def GetDeadlineEventListener():
    return SlaveCleanupListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


#########################################################################################################
# The event listener class.
#########################################################################################################
class SlaveCleanupListener (DeadlineEventListener):
    def __init__(self):
        self.OnSlaveStartedCallback += self.OnSlaveStarted

        self.CLEANUP_PATHS = []
        self.DELETE_DAYS = 30
        self.VERBOSE = True
        self.DRYRUN = True
    
    def Cleanup(self):
        del self.OnSlaveStartedCallback

    def GetImmediateSubDirs(self, dirs_list):
        subDirs = []
        for dir in dirs_list:
            if dir != "":
                if not os.path.isdir(dir):
                    self.LogInfo("Error - Path does not exist or is unavailable: %s" % dir)
                    pass
                else:
                    subDirs.append(dir)
                    for name in os.listdir(dir):
                        if os.path.isdir(os.path.join(dir, name)):
                            subDirs.append(os.path.join(dir, name))
        return subDirs

    def DeleteFilesByAge(self, path):

        currTime = time.time()

        for root, dirs, files in os.walk(path, topdown=False):

            for name in files:
                fname = os.path.join(root, name)
                
                if self.VERBOSE:
                    self.LogInfo("FILE: %s" % fname)

                if os.stat(fname).st_mtime < (currTime - (self.DELETE_DAYS * 86400)):
                    try:
                        if (not self.DRYRUN):
                            os.remove(fname)
                        else:
                            self.LogInfo("DRYRUN: DELETED FILE: %s" % fname)
                        if self.VERBOSE:
                            self.LogInfo("DELETED FILE: %s" % fname)
                    except OSError as e:
                        self.LogInfo("Error: %s" % e)
                        pass

            for name in dirs:
                dirname = (os.path.join(root, name))
                
                if self.VERBOSE:
                    self.LogInfo("DIR: %s" % dirname)
                
                if (os.stat(dirname).st_mtime < (currTime - (self.DELETE_DAYS * 86400))) or (len(os.listdir(dirname)) == 0):
                    try:
                        if (not self.DRYRUN):
                            os.rmdir(dirname)
                        else:
                            self.LogInfo("DRYRUN: DELETED DIR: %s" % dirname)
                        if self.VERBOSE:
                            self.LogInfo("DELETED DIR: %s" % dirname)
                    except OSError as e:
                        self.LogInfo("Error: %s" % e)
                        pass

    def SlaveCleanup(self):
        
        tempPaths = self.GetConfigEntryWithDefault("CleanupPaths", "")
        self.CLEANUP_PATHS = StringUtils.FromSemicolonSeparatedString(tempPaths, False)

        self.DELETE_DAYS = self.GetIntegerConfigEntryWithDefault("DeleteDays", 30)
        self.VERBOSE = self.GetBooleanConfigEntryWithDefault("Verbose", False)
        self.DRYRUN = self.GetBooleanConfigEntryWithDefault("DryRun", False)

        self.LogInfo("CLEANUP_PATHS: %s" % self.CLEANUP_PATHS)
        self.LogInfo("DELETE_DAYS: %s" % self.DELETE_DAYS)
        self.LogInfo("VERBOSE: %s" % self.VERBOSE)
        self.LogInfo("DRYRUN: %s" % self.DRYRUN)

        if self.CLEANUP_PATHS is not None and self.CLEANUP_PATHS != "":
            if len(self.CLEANUP_PATHS) > 0:
                paths = self.GetImmediateSubDirs(self.CLEANUP_PATHS)
                if self.VERBOSE:
                    self.LogInfo("paths: %s" % paths)
                    self.LogInfo("paths count: %s" % len(paths))

                if len(paths) > 0:
                    for path in paths:
                        self.DeleteFilesByAge(path)

    def OnSlaveStarted(self, slaveName):
        self.LogInfo("Slave Cleanup Started")
        self.SlaveCleanup()
        self.LogInfo("Slave Cleanup Completed")
