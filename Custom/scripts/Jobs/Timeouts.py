"""
Copyright Thinkbox Software 2016
"""

from System.IO import *
from Deadline.Scripting import *

from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

scriptDialog = None

def __main__():
    global scriptDialog
    
    scriptDialog = DeadlineScriptDialog()
    scriptDialog.AllowResizingDialog( False )
    scriptDialog.SetTitle( "Timeouts" )
    
    scriptDialog.AddGrid()
    scriptDialog.AddSelectionControlToGrid( "EnableTimeoutsJobScriptsBox", "CheckBoxControl", False, "Enable Timeouts For Pre/Post Job Scripts", 0, 0 , "If checked, then the timeouts for this job will also affect its pre/post job scripts, if any are defined.")
    scriptDialog.AddSelectionControlToGrid( "UseFrameTimeoutsBox", "CheckBoxControl", False, "Use Frame Timeouts", 1, 0 , "If enabled, timeouts will be calculated based on frames instead of by tasks. The timeouts entered for tasks will be used for each frame in that task.")

    applyButton = scriptDialog.AddControlToGrid( "ApplyButton", "ButtonControl", "Apply", 1, 2, expand=False )
    applyButton.ValueModified.connect(ApplyButtonPressed)

    closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 2, 2, expand=False )
    closeButton.ValueModified.connect(CloseButtonPressed)
    
    scriptDialog.EndGrid()
    
    scriptDialog.ShowDialog( False )
    
def ApplyButtonPressed( *args ):
    global scriptDialog
    
    jobs = MonitorUtils.GetSelectedJobs()
    
    for job in jobs:
        job.JobEnableTimeoutsForScriptTasks = scriptDialog.GetValue( "EnableTimeoutsJobScriptsBox" )
        job.JobEnableFrameTimeouts = scriptDialog.GetValue( "UseFrameTimeoutsBox" )
        RepositoryUtils.SaveJob(job)
    
def CloseButtonPressed( *args ):
    global scriptDialog
    scriptDialog.CloseDialog()
