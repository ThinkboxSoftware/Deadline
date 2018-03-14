#
# Imports
#
import json
import re

from Deadline.Events import *
from Deadline.Scripting import *

#
# This is the function that Deadline calls to get an instance of the
# main DeadlineEventListener class.
#
def GetDeadlineEventListener():
    return HostnameConfigurationListener()

#
# This is the function that Deadline calls when the event plugin is
# no longer in use so that it can get cleaned up.
#
def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

#
# This is the main HostnameConfigurationListener class.
#
class HostnameConfigurationListener( DeadlineEventListener ):

    def __init__( self ):
        self.OnSlaveStartedCallback += self.OnSlaveStarted
        self.OnHouseCleaningCallback += self.OnHouseCleaning

    def Cleanup( self ):
        del self.OnSlaveStartedCallback
        del self.OnHouseCleaningCallback

    def OnSlaveStarted( self, slaveName ):
        self.LogInfo( "Hostname Configuration Listener Plugin - On Slave Started - {}".format( slaveName ) )
        self.AssignSlave( slaveName )

    def OnHouseCleaning( self ):
        try:
            self.LogInfo( "Hostname Configuration Listener Plugin - On House Cleaning " )
            # Reassign all slaves per mapping
            if self.GetBooleanConfigEntryWithDefault( "PerformAssignmentOnHouseCleaning", False ):
                # Get slaves
                slaveNames = RepositoryUtils.GetSlaveNames( True )
                # Iterate through all slaves
                for slave in slaveNames:
                    self.AssignSlave( slave )
        except Exception as e:
            self.LogWarning( str(e) )

    def AssignSlave( self, slaveName ):
        # Load assignment mapping
        mapping = json.loads( ''.join( self.GetConfigEntryWithDefault( "Mapping", "{}" ).split(';') ) )
        # Parse and assign
        for rule in mapping.keys():
            # Prepare regex pattern
            pattern = re.compile(rule)
            # Try to match
            if pattern.match(slaveName):
                # Get the Slave settings
                slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )
                # Parse groups and pools
                groups = mapping[rule]["Groups"]
                pools = mapping[rule]["Pools"]
                # Assign the Slave into the group and pools only when not assigned or needs to be overrided
                if (len( slaveSettings.SlaveGroups ) == 0 and len( slaveSettings.SlavePools ) == 0) or mapping[rule]["Override"] == 'True':
                    # Set groups and pools
                    if ''.join(slaveSettings.SlaveGroups) != ''.join(groups):
                        self.LogInfo( "Hostname Configuration Listener Plugin - Adding the Slave '" + slaveName + "' to groups '" + ', '.join(groups) + "'." )
                        slaveSettings.SetSlaveGroups( groups )
                    if ''.join(slaveSettings.SlavePools) != ''.join(pools):
                        self.LogInfo( "Hostname Configuration Listener Plugin - Adding the Slave '" + slaveName + "' to pools '" + ', '.join(pools) + "'." )
                        slaveSettings.SetSlavePools( pools )
                    # Save the Slave settings
                    RepositoryUtils.SaveSlaveSettings( slaveSettings )