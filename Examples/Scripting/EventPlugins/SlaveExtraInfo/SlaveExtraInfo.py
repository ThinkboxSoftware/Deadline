
###############################################################
## Imports
###############################################################
from System import *

from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## This is the function called by Deadline to get an instance of the Draft event listener.
###############################################################
def GetDeadlineEventListener():
    return SlaveExtraInfoListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The event listener class.
###############################################################
class SlaveExtraInfoListener (DeadlineEventListener):
    def __init__( self ):
        self.OnSlaveStartedCallback += self.OnSlaveStarted
    
    def Cleanup( self ):
        del self.OnSlaveStartedCallback

    def OnSlaveStarted( self, slaveName ):
        for i in range(0, 9):
            tempExtraInfo = "ExtraInfo" + str(i)
            extraInfoQuery = self.GetConfigEntryWithDefault( tempExtraInfo, "" )

            if extraInfoQuery != "":
                envValue = Environment.GetEnvironmentVariable( extraInfoQuery )

                if envValue != "":
                    slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )

                    if i == 0:
                        slaveSettings.SlaveExtraInfo0 = envValue
                    elif i == 1:
                        slaveSettings.SlaveExtraInfo1 = envValue
                    elif i == 2:
                        slaveSettings.SlaveExtraInfo2 = envValue
                    elif i == 3:
                        slaveSettings.SlaveExtraInfo3 = envValue
                    elif i == 4:
                        slaveSettings.SlaveExtraInfo4 = envValue
                    elif i == 5:
                        slaveSettings.SlaveExtraInfo5 = envValue
                    elif i == 6:
                        slaveSettings.SlaveExtraInfo6 = envValue
                    elif i == 7:
                        slaveSettings.SlaveExtraInfo7 = envValue
                    elif i == 8:
                        slaveSettings.SlaveExtraInfo8 = envValue
                    elif i == 9:
                        slaveSettings.SlaveExtraInfo9 = envValue                    

                    RepositoryUtils.SaveSlaveSettings( slaveSettings)
