
###############################################################
## Imports
###############################################################
import os
import random
import sys
import traceback

from collections import OrderedDict
from time import time

from System.IO import *

from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## This is the function called by Deadline to get an instance of the Zabbix event listener.
###############################################################
def GetDeadlineEventListener():
    return ZabbixEventListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The Zabbix event listener class.
###############################################################
class ZabbixEventListener (DeadlineEventListener):
    def __init__( self ):
        '''
        Hooks up the housecleaning callback.
        '''
        self.OnHouseCleaningCallback += self.OnHouseCleaning

    def Cleanup( self ):
        '''
        Cleans up the housecleaning callback.
        '''
        del self.OnHouseCleaningCallback

    def OnHouseCleaning( self ):
        '''
        This is called at the end of housecleaning, and will push statistics to Zabbix.
        '''
        self.zapi = None
        self.palette = Palette()
        self.slaveInfoSettingsList = []
        self.pluginCountDict = {}
        self.verbose = self.GetBooleanConfigEntry( "Verbose" )
        
        # Only proceed if we can successfully initialize the Zabbix API.
        if self.InitializeZabbixApi():
            
            # Load and cache the current slave info settings.
            self.slaveInfoSettingsList = RepositoryUtils.GetSlaveInfoSettings( True )
            self.LogInfo( "Found %s slave infos" % len(self.slaveInfoSettingsList) )
            
            # Need to calculate the plugin counts before creating the Zabbix items and graphs. This is so that
            # we know which Zabbix items we need to create for the plugins.
            self.CalculatePluginCounts()
            
            # Create the Zabbix items and graphs. Note that this does nothing if the items and graphs already
            # exist. It will also never delete existing items or graphs.
            self.CreateZabbixItemsAndGraphs()
            
            # Generate the statistics and push them to Zabbix.
            self.GenerateStatistics()

    def InitializeZabbixApi( self ):
        '''
        Adds the Zabbix API path to sys.path so that we can import the necessary
        modules to communicate with Zabbix. Returns True if successful, otherwise False.
        '''
        
        # The Zabbix API modules are in the API folder in the Zabbix event directory.
        zabbixPath = Path.Combine( self.GetEventDirectory(), "API" )
        if not os.path.exists( zabbixPath ):
            self.LogInfo( "ERROR: Could not find Zabbix API at expected location '%s'" % zabbixPath )
            return False
        
        # Only add Zabbix to the path if it isn't there already.
        self.LogInfo( "Importing Zabbix API from '%s'..." % zabbixPath )
        if not zabbixPath in sys.path:
            sys.path.append( zabbixPath )
        
        try:
            # These are the modules we need, so import all of them to make sure there are no issues.
            from zabbix.sender import ZabbixMetric, ZabbixSender
            from pyzabbix import ZabbixAPI
            
            serverUrl = self.GetConfigEntry( "ZabbixURL" )
            hostNames = self.GetConfigEntry( "ZabbixHosts" )
            hostNameOrIp = self.GetConfigEntry( "ZabbixHostName" )
            userName = self.GetConfigEntry( "ZabbixUser" )
            password = self.GetConfigEntry( "ZabbixPassword" )
            
            # Do some sanity checks.
            if serverUrl == "":
                self.LogInfo( "No server URL specified in the Zabbix Connection Settings in the event plugin configuration." )
                return False
            
            if hostNames == "":
                self.LogInfo( "No hosts specified in the Zabbix Connection Settings in the event plugin configuration." )
                return False
                
            if hostNameOrIp == "":
                self.LogInfo( "No host name or IP address specified in the Zabbix Connection Settings in the event plugin configuration." )
                return False
                
            if userName == "":
                self.LogInfo( "No user name specified in the Zabbix Connection Settings in the event plugin configuration." )
                return False
            
            # Connect to the Zabbix server so that we can create graphs and items.
            self.LogInfo( "Connecting to Zabbix server '%s' as user '%s'" % (serverUrl, userName) )
            self.zapi = ZabbixAPI( serverUrl )
            self.zapi.login( userName , password )
            
            self.LogInfo( "Connection successful" )
        except:
            self.LogInfo( "An error occurred while trying to initialize Zabbix:" )
            self.LogInfo( traceback.format_exc() )
            return False
        
        return True
        
    def CreateZabbixItemsAndGraphs( self ):
        '''
        Creates the items and graphs in Zabbix. This has no effect if the items or graphs already exist,
        and will never delete existing items or graphs. If new items are added, existing graphs will
        simply be updated.
        '''        
        jobProjects = self.GetConfigEntry( "JobProjects" ).split( ";" )
        slaveRegions = self.GetConfigEntry( "SlaveRegions" ).split( ";" )
        
        # We need to create items and graphs for each Zabbix host.
        hostNames = self.GetConfigEntry( "ZabbixHosts" ).split( ";" )
        for hostName in hostNames:
            self.LogInfo( "Quering host ID and interface for host '%s'..." % hostName )
            
            hostId = None
            hostInterface = None
            
            # For each host, we need to get its host ID and host interface.
            hostsResult = self.zapi.host.get(filter={"host": hostName}, selectInterfaces=["interfaceid"])
            if hostsResult and len(hostsResult) > 0:
                hostId = hostsResult[0]["hostid"]
                hostInterfaceResult = self.zapi.hostinterface.get(filter={"hostid": hostId})
                if hostInterfaceResult and len(hostInterfaceResult) > 0:
                    hostInterface = hostInterfaceResult[0]["interfaceid"]
                    
            # If we don't have a host ID or host interface, then the host doesn't exist on the Zabbix server.
            if hostId and hostInterface:
                self.LogInfo( "  Found host ID '%s' and interface '%s'" % (hostId, hostInterface) )
                
                # Create the slave items and graphs.
                self.LogInfo( "  Creating slave Zabbix items and graphs..." )
                self.CreateSlaveZabbixItemsAndGraph( hostId, hostInterface, "" )
                for slaveRegion in slaveRegions:
                    self.CreateSlaveZabbixItemsAndGraph( hostId, hostInterface, slaveRegion )
                
                # Create the plugin items and graphs. We use the plugin counts that were pre-calculated so that we
                # know which items to create. If there are no active plugins, then we do nothing here.
                self.LogInfo( "  Creating plugin Zabbix items and graphs..." )
                if len(self.pluginCountDict) > 0:
                    self.CreatePluginZabbixItemsAndGraph( hostId, hostInterface, self.pluginCountDict.keys() )
                else:
                    self.LogInfo( "  No slaves are currently rendering" )
                
                # Create the job project items and graphs (if there are any projects specified).
                self.LogInfo( "  Creating project Zabbix items and graphs..." )
                if len(jobProjects) > 0:
                    self.CreateJobProjectZabbixItemsAndGraph( hostName, hostId, hostInterface, jobProjects )
                else:
                    self.LogInfo( "  No projects are currently specified" )
            else:
                self.LogInfo( "  No host ID or interface could be found, which means the host likely does not exist" )
    
    def CreateSlaveZabbixItemsAndGraph( self, hostId, hostInterface, slaveRegion ):
        '''
        Creates the five slave items and two graphs needed to show the slave availability and activity.
        '''
        
        # Create the three items needed for the slave availability graph, and then create the graph.
        slaveAvailabilityItemList = []
        
        totalItemId = self.CreateItem( hostId, hostInterface, slaveRegion, self.GetConfigEntry( "SlaveTotalItemKey" ), self.GetConfigEntry( "SlaveTotalItemName" ) )
        slaveAvailabilityItemList.append({"itemid": totalItemId, "color": "0033CC"})
        
        availableItemId = self.CreateItem( hostId, hostInterface, slaveRegion, self.GetConfigEntry( "SlaveTotalAvailableItemKey" ), self.GetConfigEntry( "SlaveTotalAvailableItemName" ) )
        slaveAvailabilityItemList.append({"itemid": availableItemId, "color": "FFCC00"})
        
        missingItemId = self.CreateItem( hostId, hostInterface, slaveRegion, self.GetConfigEntry( "SlaveTotalMissingItemKey" ), self.GetConfigEntry( "SlaveTotalMissingItemName" ) )
        slaveAvailabilityItemList.append({"itemid": missingItemId, "color": "FF0000"})
        
        self.CreateGraph( slaveRegion + " " + self.GetConfigEntry( "SlaveAvailableGraphName" ), slaveAvailabilityItemList )
        
        # Create the two items needed for the slave activity graph, and then create the graph. Note that we're reusing the Available Item
        # created for the slave availability graph.
        slaveActivityItemList = [{"itemid": availableItemId, "color": "FFCC00"}]
        
        activeItemId = self.CreateItem( hostId, hostInterface, slaveRegion, self.GetConfigEntry( "SlaveTotalActiveItemKey" ), self.GetConfigEntry( "SlaveTotalActiveItemName" ) )
        slaveActivityItemList.append({"itemid": activeItemId, "color": "009900"})
        
        idleItemId = self.CreateItem( hostId, hostInterface, slaveRegion, self.GetConfigEntry( "SlaveTotalIdleItemKey" ), self.GetConfigEntry( "SlaveTotalIdleItemName" ) )
        slaveActivityItemList.append({"itemid": idleItemId, "color": "FF0000"})
        
        self.CreateGraph( slaveRegion + " " + self.GetConfigEntry( "SlaveActiveGraphName" ), slaveActivityItemList )
    
    def CreatePluginZabbixItemsAndGraph( self, hostId, hostInterface, pluginNames ):
        '''
        Creates an item for each plugin, and then creates the graph that shows all the plugin counts.
        '''
        pluginNameItemList = []
        
        for pluginName in pluginNames:
            pluginItemId = self.CreateItem( hostId, hostInterface, pluginName, self.GetConfigEntry( "PluginUsageItemKey" ), self.GetConfigEntry( "PluginUsageItemName" ) )
            pluginNameItemList.append({"itemid": pluginItemId, "color": self.palette.next()})
            
        self.CreateGraph( self.GetConfigEntry( "PluginGraphName" ), pluginNameItemList )
    
    def CreateJobProjectZabbixItemsAndGraph( self, hostName, hostId, hostInterface, jobProjects ):
        '''
        Creates the job project items and the graph that shows their average usage. Each job project has an
        item that keeps track of the counts, and an item that does a calculation based on those counts to
        get the average usage.
        '''
        jobProjectUsageItemList = []
        
        for jobProject in jobProjects:
            projectKey = self.GetKey( jobProject, self.GetConfigEntry( "JobProjectItemKey" ) )
            slaveTotalKey = self.GetConfigEntry( "SlaveTotalItemKey" )
            
            # The formula is the last of the project counts divided by the last of the total slave counts, multiplied by 100 to get the percentage.
            formula = 'last("%s:%s")/last("%s:%s")*100' % (hostName, projectKey, hostName, slaveTotalKey)
            
            # Create the count item.
            self.CreateItem( hostId, hostInterface, jobProject, self.GetConfigEntry( "JobProjectItemKey" ), self.GetConfigEntry( "JobProjectItemName" ) )
            
            # Create the calculation item. This is the item that is used in the graph.
            jobProjectUsageItemId = self.CreateCalculatedItem( hostId, hostInterface, jobProject, self.GetConfigEntry( "JobProjectUsageItemKey" ), self.GetConfigEntry( "JobProjectUsageItemName" ), formula )
            jobProjectUsageItemList.append({"itemid": jobProjectUsageItemId, "color": self.palette.next()})
        
        self.CreateGraph( self.GetConfigEntry( "JobProjectGraphName" ), jobProjectUsageItemList )
    
    def CreateItem( self, hostId, hostInterface, itemPrefix, itemKey, itemName ):
        '''
        A helper function to create a Zabbix trapper item. If the itemPrefix is not empty, it will be prefixed to
        the item key and name. This returns the item id.
        '''
        
        # Get the updated item key and name if a prefix is specified.
        itemKey = self.GetKey( itemPrefix, itemKey )
        itemName = self.GetName( itemPrefix, itemName )
        
        if self.verbose:
            self.LogInfo( "    Creating Zabbix item %s (%s)..." % (itemName, itemKey) )

        # Check if the item already exists, and create it if it doesn't.
        items = self.zapi.item.get( filter={"key_": itemKey} )
        if len(items) > 0:
            itemId = items[0]["itemid"]
            if self.verbose:
                self.LogInfo( "    Item already exists (id = %s)" % itemId )
        else:
            item = self.zapi.item.create( hostid=hostId, name=itemName, key_=itemKey, type=2, value_type=0, interfaceid=hostInterface, delay=30 )
            itemId = item["itemids"][0]
            if self.verbose:
                self.LogInfo( "    Item created successfully (id = %s)" % itemId )
        
        return itemId
        
    def CreateCalculatedItem( self, hostId, hostInterface, itemPrefix, itemKey, itemName, formula ):
        '''
        A helper function to create a Zabbix calculated item. If the itemPrefix is not empty, it will be prefixed to
        the item key and name. This returns the item id.
        '''
        
        # Get the updated item key and name if a prefix is specified.
        itemKey = self.GetKey( itemPrefix, itemKey )
        itemName = self.GetName( itemPrefix, itemName )
        
        if self.verbose:
            self.LogInfo( "    Creating Zabbix item %s (%s)..." % (itemName, itemKey) )
            self.LogInfo( "    Formula: %s" % formula )

        # Check if the item already exists, and create it if it doesn't.
        items = self.zapi.item.get( filter={"key_": itemKey} )
        if len(items) > 0:
            itemId = items[0]["itemid"]
            if self.verbose:
                self.LogInfo( "    Calculated item already exists (id = %s)" % itemId )
        else:
            item = self.zapi.item.create( hostid=hostId, name=itemName, key_=itemKey, type=15, params=formula, value_type=0, interfaceid=hostInterface, delay=30 )
            itemId = item["itemids"][0]
            if self.verbose:
                self.LogInfo( "    Calculated item created successfully (id = %s)" % itemId )
        
        return itemId
        
    def CreateGraph( self, graphName, itemList ):
        '''
        A helper function to create a Zabbix graph. If the graph already exists, any new items will
        be appended to the existing list of graph items.
        '''
        if self.verbose:
            self.LogInfo( "    Creating Zabbix graph %s..." % (graphName) )
        
        # Check if the graph already exists, and create it if it doesn't.
        graphs = self.zapi.graph.get( filter={"name": graphName} )
        if len(graphs) > 0:
            graphId = graphs[0]["graphid"]
            existingItemList = self.zapi.graphitem.get( output="extend", expandData="1", graphids=graphId )
            
            # Only add items if they don't already exist.
            newItemCount = 0
            for item in itemList:
                itemExists = False
                for existingItem in existingItemList:
                    if item["itemid"] == existingItem["itemid"]:
                        itemExists = True
                        break
                
                if not itemExists:
                    existingItemList.append( item )
                    newItemCount = newItemCount + 1
            
            # Update the existing graph with the updated item list (if necessary).
            if newItemCount > 0:
                self.zapi.graph.update( graphid=graphId, gitems=existingItemList )
                if self.verbose:
                    self.LogInfo( "    Graph updated successfully with %s new items (id = %s)" % (newItemCount, graphId) )            
            else:
                if self.verbose:
                    self.LogInfo( "    Graph update not required because there are no new items (id = %s)" % graphId )
        else:
            graph = self.zapi.graph.create( name=graphName, width=900, height=200, gitems=itemList )
            graphId = graph["graphids"][0]
            if self.verbose:
                self.LogInfo( "    Graph created successfully (id = %s)" % graphId )
            
        return graphId
    
    def SendZabbixStatistics( self, zabbixPacket ):
        '''
        A helper function that sends the specified packet contents to Zabbix.
        '''
        from zabbix.sender import ZabbixMetric, ZabbixSender
        
        # Only send the packet contents if the packet isn't empty.
        if len(zabbixPacket) > 0:
            hostName = self.GetConfigEntry( "ZabbixHostName" )
            port = self.GetIntegerConfigEntry( "ZabbixPort" )
            
            self.LogInfo( "  Sending statistics to Zabbix server %s:%s..." % (hostName, port) )
            
            results = ZabbixSender( hostName, port ).send( zabbixPacket )
            self.LogInfo( "  Results: %s" % results )
        else:
            self.LogInfo( "  Zabbix packet is empty, nothing to send" )
        
    def GetKey( self, prefix, key ):
        '''
        If the prefix isn't empty, it is prefixed to the key. All spaces are replaced with underscores.
        '''
        newKey = key
        if prefix != "":
            newKey = prefix + "_" + newKey
        return newKey.replace( " ", "_" )
        
    def GetName( self, prefix, name ):
        '''
        If the prefix isn't empty, it is prefixed to the name.
        '''
        newName = name
        if prefix != "":
            newName = prefix + " " + newName
        return newName
        
    def CalculatePluginCounts( self ):
        '''
        Calculates the current plugin counts from the cached slave info settings.
        '''
        self.LogInfo( "Calculating plugin counts..." )
        
        # Loop through each slave info settings object.
        for slaveInfoSettings in self.slaveInfoSettingsList:
            
            # Only check enabled slaves.
            if slaveInfoSettings.Settings.SlaveEnabled:
            
                # Only check slaves that are rendering or starting jobs.
                if slaveInfoSettings.Info.SlaveState == "Rendering" or slaveInfoSettings.Info.SlaveState == "StartingJob":
                    
                    # Get the slave's plugin, and update the plugin's count.
                    pluginName = slaveInfoSettings.Info.SlaveCurrentPlugin 
                    if pluginName != "":
                        if pluginName not in self.pluginCountDict:
                            self.pluginCountDict[pluginName] = 0
                        self.pluginCountDict[pluginName] = self.pluginCountDict[pluginName] + 1
            
    def GenerateStatistics( self ):
        '''
        Generates the statistics to send to Zabbix.
        '''
        from zabbix.sender import ZabbixMetric, ZabbixSender
        
        # Cache the current time so that all entries have the same entry date.
        clock = int(time())
        
        # Generate stats for all slaves first.
        self.GenerateSlaveStatistics( "", clock )
        
        # Generate stats for each individual region.
        slaveRegions = self.GetConfigEntry( "SlaveRegions" ).split( ";" )
        for slaveRegion in slaveRegions:
            self.GenerateSlaveStatistics( slaveRegion, clock )
            
        # Generate the plugin and job plugin stats.
        self.GeneratePluginStatistics( clock )
        self.GenerateProjectStatistics( clock )
    
    def GenerateSlaveStatistics( self, slaveRegion, clock ):
        '''
        Generates the slave statistics to send to Zabbix.
        '''
        from zabbix.sender import ZabbixMetric
        
        totalCount = 0
        activeCount = 0
        idleCount = 0
        
        if slaveRegion == "":
            self.LogInfo( "Generating slave statistics for all regions" )
        else:
            self.LogInfo( "Generating slave statistics for region %s" % slaveRegion )
        
        # Loop through each slave info settings object.
        for slaveInfoSettings in self.slaveInfoSettingsList:
            
            # Check if the slave's extra info property matches the current region. If the region is empty, then we're checking all slaves.
            if slaveRegion == "" or slaveRegion == self.GetSlaveExtraInfoValue( slaveInfoSettings.Settings ):
                totalCount = totalCount + 1
            
                # Only check enabled slaves.
                if slaveInfoSettings.Settings.SlaveEnabled:
                    
                    # Active slaves are those that are rendering or starting a job.
                    if slaveInfoSettings.Info.SlaveState == "Rendering" or slaveInfoSettings.Info.SlaveState == "StartingJob":
                        activeCount = activeCount + 1
                    elif slaveInfoSettings.Info.SlaveState == "Idle":
                        idleCount = idleCount + 1
        
        # Calculate the available and missing counts.
        availableCount = activeCount + idleCount
        missingCount = totalCount - availableCount
        
        self.LogInfo( "  Total count: %s" % totalCount )
        self.LogInfo( "  Available count: %s" % availableCount )
        self.LogInfo( "  Missing count: %s" % missingCount )
        self.LogInfo( "  Active count: %s" % activeCount )
        self.LogInfo( "  Idle count: %s" % idleCount )
        
        # Create the slave packets for each host.
        zabbixPacket = []
        hostNames = self.GetConfigEntry( "ZabbixHosts" ).split( ";" )
        for hostName in hostNames:
            zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( slaveRegion, self.GetConfigEntry( "SlaveTotalItemKey" ) ), totalCount, clock ) )
            zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( slaveRegion, self.GetConfigEntry( "SlaveTotalAvailableItemKey" ) ), availableCount, clock ) )
            zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( slaveRegion, self.GetConfigEntry( "SlaveTotalMissingItemKey" ) ), missingCount, clock ) )
            zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( slaveRegion, self.GetConfigEntry( "SlaveTotalActiveItemKey" ) ), activeCount, clock ) )
            zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( slaveRegion, self.GetConfigEntry( "SlaveTotalIdleItemKey" ) ), idleCount, clock ) )
            
        # Send the statistics.
        self.SendZabbixStatistics( zabbixPacket )
        
    def GeneratePluginStatistics( self, clock ):
        '''
        Generates the plugin statistics to send to Zabbix.
        '''
        from zabbix.sender import ZabbixMetric
        
        self.LogInfo( "Generating plugin statistics" )
        
        # Only generate stats if there are any active plugins.
        if len(self.pluginCountDict) > 0:
            zabbixPacket = []
            hostNames = self.GetConfigEntry( "ZabbixHosts" ).split( ";" )
            
            # Create a packet for each plugin count that needs to be sent to Zabbix.
            for pluginName in self.pluginCountDict:
                self.LogInfo( "  %s: %s" % (pluginName, self.pluginCountDict[pluginName]) )
                
                # Need to create a packet for each host.
                for hostName in hostNames:
                    zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( pluginName, self.GetConfigEntry( "PluginUsageItemKey" ) ), self.pluginCountDict[pluginName], clock ) )
                
            # Send the statistics.
            self.SendZabbixStatistics( zabbixPacket )
        else:
            self.LogInfo( "  No slaves are currently rendering" )
        
    def GenerateProjectStatistics( self, clock ):
        '''
        Generates the job project statistics to send to Zabbix.
        '''
        from zabbix.sender import ZabbixMetric
        
        self.LogInfo( "Generating job project statistics" )
        
        # Get the list of job projects.
        jobProjects = self.GetConfigEntry( "JobProjects" ).split( ";" )
        if len(jobProjects) > 0:
            cachedJobs = {}
            
            # Initialze the project counts to 0 for each project.
            projectCounts = OrderedDict()
            for jobProject in jobProjects:
                projectCounts[jobProject] = 0
            
            # Loop through each slave info settings object.
            for slaveInfoSettings in self.slaveInfoSettingsList:
                
                # Only check enabled slaves.
                if slaveInfoSettings.Settings.SlaveEnabled:
                
                    # Only check slaves that are rendering or starting jobs.
                    if slaveInfoSettings.Info.SlaveState == "Rendering" or slaveInfoSettings.Info.SlaveState == "StartingJob":
                        
                        # Get the current job ID, and make sure it's a valid ID.
                        jobId = slaveInfoSettings.Info.SlaveCurrentJobId
                        if jobId != "":
                            
                            # If the job is already cached, then use it, otherwise add it to the cache.
                            if jobId not in cachedJobs:
                                job = RepositoryUtils.GetJob( jobId, True )
                                if job:
                                    cachedJobs[jobId] = job
                            
                            job = cachedJobs.get( jobId, None )
                            if job:
                                # Get the project from the job, and increment its count.
                                project = self.GetJobExtraInfoValue( job )
                                if project in projectCounts:
                                    projectCounts[project] = projectCounts[project] + 1
            
            # Create the job project packets for each host.
            hostNames = self.GetConfigEntry( "ZabbixHosts" ).split( ";" )
            zabbixPacket = []
            for jobProject in projectCounts:
                self.LogInfo( "  %s: %s" % (jobProject, projectCounts[jobProject]) )
                for hostName in hostNames:
                    zabbixPacket.append( ZabbixMetric( hostName, self.GetKey( jobProject, self.GetConfigEntry( "JobProjectItemKey" ) ), projectCounts[jobProject], clock ) )
                    
            # Send the statistics.
            self.SendZabbixStatistics( zabbixPacket )
        else:
            self.LogInfo( "  No projects are currently specified" )
        
    def GetJobExtraInfoValue( self, job ):
        '''
        Gets the job extra info value for the extra info index specified in the event plugin configuration.
        '''
        extraInfoNumber = self.GetIntegerConfigEntry( "JobExtraInfoWithProject" )
        if extraInfoNumber == 0:
            return job.JobExtraInfo0
        elif extraInfoNumber == 1:
            return job.JobExtraInfo1
        elif extraInfoNumber == 2:
            return job.JobExtraInfo2
        elif extraInfoNumber == 3:
            return job.JobExtraInfo3
        elif extraInfoNumber == 4:
            return job.JobExtraInfo4
        elif extraInfoNumber == 5:
            return job.JobExtraInfo5
        elif extraInfoNumber == 6:
            return job.JobExtraInfo6
        elif extraInfoNumber == 7:
            return job.JobExtraInfo7
        elif extraInfoNumber == 8:
            return job.JobExtraInfo8
        elif extraInfoNumber == 9:
            return job.JobExtraInfo9
            
    def GetSlaveExtraInfoValue( self, slaveSettings ):
        '''
        Gets the slave extra info value for the extra info index specified in the event plugin configuration.
        '''
        
        # Check if we need to pull the region from the extra info, or the slave's region setting.
        if self.GetBooleanConfigEntry( "SlaveRegionInExtraInfo" ):
            extraInfoNumber = self.GetIntegerConfigEntry( "SlaveExtraInfoWithRegion" )
            if extraInfoNumber == 0:
                return slaveSettings.SlaveExtraInfo0
            elif extraInfoNumber == 1:
                return slaveSettings.SlaveExtraInfo1
            elif extraInfoNumber == 2:
                return slaveSettings.SlaveExtraInfo2
            elif extraInfoNumber == 3:
                return slaveSettings.SlaveExtraInfo3
            elif extraInfoNumber == 4:
                return slaveSettings.SlaveExtraInfo4
            elif extraInfoNumber == 5:
                return slaveSettings.SlaveExtraInfo5
            elif extraInfoNumber == 6:
                return slaveSettings.SlaveExtraInfo6
            elif extraInfoNumber == 7:
                return slaveSettings.SlaveExtraInfo7
            elif extraInfoNumber == 8:
                return slaveSettings.SlaveExtraInfo8
            elif extraInfoNumber == 9:
                return slaveSettings.SlaveExtraInfo9
            
            self.LogInfo( "Extra info index %s is not valid" % extraInfoNumber )
            return ""
        else:
            return RepositoryUtils.GetRegionNameFromId( slaveSettings.SlaveRegion )
        
###############################################################
## The Palette class for randomly generating colors.
###############################################################
class Palette:
    '''
    A helper class to randomly generate colors.
    '''
    colors = ["C04000", "800000", "191970", "3EB489", "FFDB58", "000080",
              "CC7722", "808000", "FF7F00", "002147", "AEC6CF", "836953",
              "CFCFC4", "77DD77", "F49AC2", "FFB347", "FFD1DC", "B39EB5",
              "FF6961", "CB99C9", "FDFD96", "FFE5B4", "D1E231", "8E4585",
              "FF5A36", "701C1C", "FF7518", "69359C", "E30B5D", "826644",
              "FF0000", "414833", "65000B", "002366", "E0115F", "B7410E",
              "FF6700", "F4C430", "FF8C69", "C2B280", "967117", "ECD540",
              "082567"]
 
    def next( self ):
        '''
        Gets the next random color.
        '''
        return random.choice(self.colors)
