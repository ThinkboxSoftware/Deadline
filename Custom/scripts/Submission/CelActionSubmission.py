import traceback
import os

from System import *
from System.Collections.Specialized import *
from System.IO import *
from System.Text import *

from Deadline.Scripting import *

from System.IO import File
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

########################################################################
## Globals
########################################################################
scriptDialog = None
outputBox = None
sceneBox = None
defaultLocation = None
settings = None

########################################################################
## Main Function Called By Deadline
########################################################################
def __main__( *args ):
    global scriptDialog
    global settings
    global defaultLocation
    global outputBox
    global sceneBox

    defaultLocation = ""

    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle( "Submit CelAction Job To Deadline" )
    scriptDialog.SetIcon(os.path.join(RepositoryUtils.GetRootDirectory(), 'custom', 'plugins', 'CelAction', 'CelAction.ico'))

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator1", "SeparatorControl", "Job Description", 0, 0, colSpan=2 )

    scriptDialog.AddControlToGrid( "NameLabel", "LabelControl", "Job Name", 1, 0, "The name of your job. This is optional, and if left blank, it will default to 'Untitled'.", False )
    scriptDialog.AddControlToGrid( "NameBox", "TextControl", "Untitled", 1, 1 )

    scriptDialog.AddControlToGrid( "CommentLabel", "LabelControl", "Comment", 2, 0, "A simple description of your job. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "CommentBox", "TextControl", "", 2, 1 )

    scriptDialog.AddControlToGrid( "DepartmentLabel", "LabelControl", "Department", 3, 0, "The department you belong to. This is optional and can be left blank.", False )
    scriptDialog.AddControlToGrid( "DepartmentBox", "TextControl", "", 3, 1 )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid( "Separator2", "SeparatorControl", "Job Options", 0, 0, colSpan=3 )

    scriptDialog.AddControlToGrid( "PoolLabel", "LabelControl", "Pool", 1, 0, "The pool that your job will be submitted to.", False )
    scriptDialog.AddControlToGrid( "PoolBox", "PoolComboControl", "none", 1, 1 )

    scriptDialog.AddControlToGrid( "SecondaryPoolLabel", "LabelControl", "Secondary Pool", 2, 0, "The secondary pool lets you specify a Pool to use if the primary Pool does not have any available Slaves.", False )
    scriptDialog.AddControlToGrid( "SecondaryPoolBox", "SecondaryPoolComboControl", "", 2, 1 )

    scriptDialog.AddControlToGrid( "GroupLabel", "LabelControl", "Group", 3, 0, "The group that your job will be submitted to.", False )
    scriptDialog.AddControlToGrid( "GroupBox", "GroupComboControl", "none", 3, 1 )

    scriptDialog.AddControlToGrid( "PriorityLabel", "LabelControl", "Priority", 4, 0, "A job can have a numeric priority ranging from 0 to 100, where 0 is the lowest priority and 100 is the highest priority.", False )
    scriptDialog.AddRangeControlToGrid( "PriorityBox", "RangeControl", RepositoryUtils.GetMaximumPriority() / 2, 0, RepositoryUtils.GetMaximumPriority(), 0, 1, 4, 1 )

    scriptDialog.AddControlToGrid( "TaskTimeoutLabel", "LabelControl", "Task Timeout", 5, 0, "The number of minutes a slave has to render a task for this job before it requeues it. Specify 0 for no limit.", False )
    scriptDialog.AddRangeControlToGrid( "TaskTimeoutBox", "RangeControl", 0, 0, 1000000, 0, 1, 5, 1 )
    scriptDialog.AddSelectionControlToGrid( "AutoTimeoutBox", "CheckBoxControl", False, "Enable Auto Task Timeout", 5, 2, "If the Auto Task Timeout is properly configured in the Repository Options, then enabling this will allow a task timeout to be automatically calculated based on the render times of previous frames for the job." )

    scriptDialog.AddControlToGrid( "ConcurrentTasksLabel", "LabelControl", "Concurrent Tasks", 6, 0, "The number of tasks that can render concurrently on a single slave. This is useful if the rendering application only uses one thread to render and your slaves have multiple CPUs.", False )
    scriptDialog.AddRangeControlToGrid( "ConcurrentTasksBox", "RangeControl", 1, 1, 16, 0, 1, 6, 1 )
    scriptDialog.AddSelectionControlToGrid( "LimitConcurrentTasksBox", "CheckBoxControl", True, "Limit Tasks To Slave's Task Limit", 6, 2, "If you limit the tasks to a slave's task limit, then by default, the slave won't dequeue more tasks then it has CPUs. This task limit can be overridden for individual slaves by an administrator." )

    scriptDialog.AddControlToGrid( "MachineLimitLabel", "LabelControl", "Machine Limit", 7, 0, "Use the Machine Limit to specify the maximum number of machines that can render your job at one time. Specify 0 for no limit.", False )
    scriptDialog.AddRangeControlToGrid( "MachineLimitBox", "RangeControl", 0, 0, 1000000, 0, 1, 7, 1 )
    scriptDialog.AddSelectionControlToGrid( "IsBlacklistBox", "CheckBoxControl", False, "Machine List Is A Blacklist", 7, 2, "You can force the job to render on specific machines by using a whitelist, or you can avoid specific machines by using a blacklist." )

    scriptDialog.AddControlToGrid( "MachineListLabel", "LabelControl", "Machine List", 8, 0, "The whitelisted or blacklisted list of machines.", False )
    scriptDialog.AddControlToGrid( "MachineListBox", "MachineListControl", "", 8, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "LimitGroupLabel", "LabelControl", "Limits", 9, 0, "The Limits that your job requires.", False )
    scriptDialog.AddControlToGrid( "LimitGroupBox", "LimitGroupControl", "", 9, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "DependencyLabel", "LabelControl", "Dependencies", 10, 0, "Specify existing jobs that this job will be dependent on. This job will not start until the specified dependencies finish rendering.", False )
    scriptDialog.AddControlToGrid( "DependencyBox", "DependencyControl", "", 10, 1, colSpan=2 )

    scriptDialog.AddControlToGrid( "OnJobCompleteLabel", "LabelControl", "On Job Complete", 11, 0, "If desired, you can automatically archive or delete the job when it completes.", False )
    scriptDialog.AddControlToGrid( "OnJobCompleteBox", "OnJobCompleteControl", "Nothing", 11, 1 )
    scriptDialog.AddSelectionControlToGrid( "SubmitSuspendedBox", "CheckBoxControl", False, "Submit Job As Suspended", 11, 2, "If enabled, the job will submit in the suspended state. This is useful if you don't want the job to start rendering right away. Just resume it from the Monitor when you want it to render." )
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()

    scriptDialog.AddControlToGrid( "Separator3", "SeparatorControl", "CelAction Options", 0, 0, colSpan=4 )

    scriptDialog.AddControlToGrid( "SceneLabel", "LabelControl", "CelAction File", 1, 0, "The TVPaint script to be rendered.", False )
    scriptDialog.AddSelectionControlToGrid( "SceneBox", "FileBrowserControl", "", "CelAction Files (*.scn);;All Files (*)", 1, 1, colSpan=5 )

    scriptDialog.AddControlToGrid( "OutputLabel", "LabelControl", "Output Folder", 2, 0,  "The output path to render to.", False )
    scriptDialog.AddSelectionControlToGrid( "OutputBox", "FileSaverControl", "", "PNG Files (*.png);;All Files (*)", 2, 1, colSpan=5 )

    scriptDialog.AddControlToGrid( "FramesLabel", "LabelControl", "Frame List", 3, 0, "The list of frames for the normal job.", False )
    scriptDialog.AddControlToGrid( "FramesBox", "TextControl", "", 3, 1 )

    scriptDialog.AddControlToGrid( "ChunkSizeLabel", "LabelControl", "Frames Per Task", 3, 2, "This is the number of frames that will be rendered at a time for each job task.", False )
    scriptDialog.AddRangeControlToGrid( "ChunkSizeBox", "RangeControl", 1, 1, 1000000, 0, 1, 3, 3 )

    scriptDialog.AddControlToGrid( "WidthLabel", "LabelControl", "Width", 4, 0, "Resolution Width", False )
    scriptDialog.AddRangeControlToGrid( "WidthBox", "RangeControl", 1920, 1, 1000000, 0, 1, 4, 1 )
    scriptDialog.AddControlToGrid( "HeightLabel", "LabelControl", "Height", 4, 2, "Resolution Height", False )
    scriptDialog.AddRangeControlToGrid( "HeightBox", "RangeControl", 1080, 1, 1000000, 0, 1, 4, 3)

    scriptDialog.AddControlToGrid( "AlphaLabel", "LabelControl", "Alpha", 5, 0, "If this option is enabled, the images with have alpha embedded.", False )
    scriptDialog.AddSelectionControlToGrid( "AlphaBox", "CheckBoxControl", True, "", 5, 1, "", "" )
    scriptDialog.AddControlToGrid( "LevelSplitLabel", "LabelControl", "Level Split", 5, 2, "If this option is enabled, the output images with be split into the levels.", False )
    scriptDialog.AddSelectionControlToGrid( "LevelSplitBox", "CheckBoxControl", False, "", 5, 3, "", "" )

    scriptDialog.AddControlToGrid( "FramePaddingLabel", "LabelControl", "Frame Padding", 6, 0, "This is the number of padding on frames.", False )
    scriptDialog.AddRangeControlToGrid( "FramePaddingBox", "RangeControl", 4, 1, 10, 0, 1, 6, 1)

    scriptDialog.AddControlToGrid( "RenderSeparatorLabel", "LabelControl", "Render Separator", 6, 2, "This is the character(s) to separate filename from frame padding.", False )
    scriptDialog.AddControlToGrid( "RenderSeparatorBox", "TextControl", ".", 6, 3 )

    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid( "HSpacer1", 0, 0)
    submitButton = scriptDialog.AddControlToGrid( "SubmitButton", "ButtonControl", "Submit", 0, 1, expand=False )
    submitButton.ValueModified.connect(SubmitButtonPressed)

    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 2, expand=False )
    closeButton.ValueModified.connect(scriptDialog.closeEvent)
    scriptDialog.EndGrid()

    settings = ("DepartmentBox","CategoryBox","PoolBox","SecondaryPoolBox","GroupBox","PriorityBox","MachineLimitBox","IsBlacklistBox","MachineListBox","LimitGroupBox","FramesBox","ChunkSizeBox", "SceneBox", "OutputBox", "HeightBox", "WidthBox", "AlphaBox", "LevelSplitBox")
    scriptDialog.LoadSettings( GetSettingsFilename(), settings )
    scriptDialog.EnabledStickySaving( settings, GetSettingsFilename() )

    scriptDialog.ShowDialog( False )

def GetSettingsFilename():
    return Path.Combine( GetDeadlineSettingsPath(), "CommandLineSettings.ini" )

def SubmitButtonPressed(*args):
    global scriptDialog

    if not os.path.exists(scriptDialog.GetValue('SceneBox')):
        scriptDialog.ShowMessageBox( "CelAction file doesn't exist!", "Error" )
        return

    if not os.path.exists(os.path.dirname(scriptDialog.GetValue('OutputBox'))):
        scriptDialog.ShowMessageBox( "Output folder doesn't exist!", "Error" )
        return

    # Create job info file.
    jobInfoFilename = Path.Combine( GetDeadlineTempPath(), "celaction_job_info.job" )
    writer = StreamWriter( jobInfoFilename, False, Encoding.Unicode )
    writer.WriteLine( "Plugin=CelAction" )
    writer.WriteLine( "Name=%s" % scriptDialog.GetValue( "NameBox" ) )
    writer.WriteLine("Frames=%s" % scriptDialog.GetValue("FramesBox"))
    writer.WriteLine("ChunkSize=%s" % scriptDialog.GetValue("ChunkSizeBox"))
    writer.WriteLine( "Comment=%s" % scriptDialog.GetValue( "CommentBox" ) )
    writer.WriteLine( "Department=%s" % scriptDialog.GetValue( "DepartmentBox" ) )
    writer.WriteLine( "Pool=%s" % scriptDialog.GetValue( "PoolBox" ) )
    writer.WriteLine( "SecondaryPool=%s" % scriptDialog.GetValue( "SecondaryPoolBox" ) )
    writer.WriteLine( "Group=%s" % scriptDialog.GetValue( "GroupBox" ) )
    writer.WriteLine( "Priority=%s" % scriptDialog.GetValue( "PriorityBox" ) )
    writer.WriteLine( "TaskTimeoutMinutes=%s" % scriptDialog.GetValue( "TaskTimeoutBox" ) )
    writer.WriteLine( "EnableAutoTimeout=%s" % scriptDialog.GetValue( "AutoTimeoutBox" ) )
    writer.WriteLine( "ConcurrentTasks=%s" % scriptDialog.GetValue( "ConcurrentTasksBox" ) )
    writer.WriteLine( "LimitConcurrentTasksToNumberOfCpus=%s" % scriptDialog.GetValue( "LimitConcurrentTasksBox" ) )

    writer.WriteLine( "MachineLimit=%s" % scriptDialog.GetValue( "MachineLimitBox" ) )
    if( bool(scriptDialog.GetValue( "IsBlacklistBox" )) ):
        writer.WriteLine( "Blacklist=%s" % scriptDialog.GetValue( "MachineListBox" ) )
    else:
        writer.WriteLine( "Whitelist=%s" % scriptDialog.GetValue( "MachineListBox" ) )

    writer.WriteLine( "LimitGroups=%s" % scriptDialog.GetValue( "LimitGroupBox" ) )
    writer.WriteLine( "JobDependencies=%s" % scriptDialog.GetValue( "DependencyBox" ) )
    writer.WriteLine( "OnJobComplete=%s" % scriptDialog.GetValue( "OnJobCompleteBox" ) )

    if( bool(scriptDialog.GetValue( "SubmitSuspendedBox" )) ):
        writer.WriteLine( "InitialStatus=Suspended" )

    split = os.path.splitext(scriptDialog.GetValue("OutputBox"))
    frame_padding = scriptDialog.GetValue("FramePaddingBox")
    output_path = split[0] + scriptDialog.GetValue("RenderSeparatorBox") + frame_padding * '#' + split[-1]
    writer.WriteLine("OutputFilename0=%s" % output_path)

    writer.Close()

    # Create plugin info file.
    pluginInfoFilename = Path.Combine( GetDeadlineTempPath(), "celaction_plugin_info.job" )
    writer = StreamWriter( pluginInfoFilename, False, Encoding.Unicode )

    writer.WriteLine("SceneFile=%s" % scriptDialog.GetValue("SceneBox"))

    args = '<QUOTE>%s<QUOTE>' % scriptDialog.GetValue("SceneBox")
    if scriptDialog.GetValue("AlphaBox"):
        args += ' -a'
    if scriptDialog.GetValue("LevelSplitBox"):
        args += ' -l'
    args += ' -s <STARTFRAME> -e <ENDFRAME>'
    args += ' -d <QUOTE>%s<QUOTE>' % os.path.dirname(scriptDialog.GetValue("OutputBox"))
    args += ' -r <QUOTE>%s<QUOTE>' % os.path.basename(scriptDialog.GetValue("OutputBox"))
    args += ' -x %s' % scriptDialog.GetValue("WidthBox")
    args += ' -y %s' % scriptDialog.GetValue("HeightBox")
    args += ' -= AbsoluteFrameNumber=on -= ClearAttachment=on'
    args += ' -= PadDigits=%s' % scriptDialog.GetValue("FramePaddingBox")
    writer.WriteLine("Arguments=%s" % args)
    writer.WriteLine("RenderNameSeparator=%s" % scriptDialog.GetValue("RenderSeparatorBox"))

    writer.Close()

    # Setup the command line arguments.
    arguments = StringCollection()

    arguments.Add( jobInfoFilename )
    arguments.Add( pluginInfoFilename )

    # Now submit the job.
    results = ClientUtils.ExecuteCommandAndGetOutput( arguments )
    scriptDialog.ShowMessageBox( results, "Submission Results" )
