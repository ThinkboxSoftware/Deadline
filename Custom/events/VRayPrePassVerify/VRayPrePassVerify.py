from System.Diagnostics import *
from System.IO import *

from Deadline.Events import *
from Deadline.Scripting import *

###############################################################
## This is the function called by Deadline to get an instance
## of the VRay Pre Pass Verify event listener.
###############################################################
def GetDeadlineEventListener():
    return VRayPrePassEventListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()

###############################################################
## The VRay event listener class.
###############################################################
class VRayPrePassEventListener( DeadlineEventListener ):
    '''
    Verify V-Ray animation pre-pass *.vrmap files have been successfully saved back to the network file server.
    If the *.vrmap file is missing, then requeue the task(s) automatically.
    '''
    def __init__( self ):
        self.OnJobFinishedCallback += self.OnJobFinished

    def Cleanup( self ):
        del self.OnJobFinishedCallback

    ## This is called when the job finishes rendering.
    def OnJobFinished( self, job ):

        # Check job is a 3dsMax job
        if job.JobPlugin != "3dsmax":
            return

        # Check job is a V-Ray job
        vrayFilterExists = self.GetPluginInfoEntryWithDefault( "vray_filter_on", "" )
        if vrayFilterExists == "":
            return

        # Check GI is enabled
        vray_gi_on = self.GetPluginInfoEntryWithDefault( "vray_GI_on", "" )
        if vray_gi_on != "true":
            return

        # Check job is an animation pre-pass job
        vray_adv_irradmap_mode = self.GetPluginInfoEntryWithDefault( "vray_adv_irradmap_mode", "" )
        if vray_adv_irradmap_mode != "6":
            return

        self.LogInfo( "Event Plugin: V-Ray PrePass Verify Started" )

        vray_adv_irradmap_autoSaveFileName = self.GetPluginInfoEntryWithDefault( "vray_adv_irradmap_autoSaveFileName", "" )
        filePath = Path.GetDirectoryName( vray_adv_irradmap_autoSaveFileName )
        fileName = Path.GetFileNameWithoutExtension( vray_adv_irradmap_autoSaveFileName )
        vrmapFile = str( fileName ) + "####.vrmap"
        vrmapFile = Path.Combine( filePath, vrmapFile )
        padding = "####"
        taskIdsToRequeue = []

        tasks = RepositoryUtils.GetJobTasks( job, True )

        for task in tasks:
            for frame in task.TaskFrameList:
                frameNumber = StringUtils.ToZeroPaddedString( frame, 4 )
                currFile = vrmapFile.replace( padding, frameNumber )

                if not File.Exists( currFile ):
                    
                    self.LogWarning( "Missing: %s" % currFile )
                    
                    if not task in taskIdsToRequeue:
                        taskIdsToRequeue.append( task.TaskId )

        if len(taskIdsToRequeue) > 0:
            
            taskIdsToRequeue = list(set(taskIdsToRequeue))
            
            for task in tasks.Tasks:
                for i in taskIdsToRequeue:
                    if i == task.TaskId:
                        self.LogInfo( "Requeuing Task: %s" % task.TaskId )
                        RepositoryUtils.RequeueTasks( job, [task,] )

        self.LogInfo( "Event Plugin: V-Ray PrePass Verify Finished" )
