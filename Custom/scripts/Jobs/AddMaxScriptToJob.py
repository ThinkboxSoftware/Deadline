from System.IO import *
from Deadline.Scripting import *

from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

########################################################################
# Globals
########################################################################
scriptDialog = None
settings = None

########################################################################
# Main Function Called By Deadline
########################################################################


def __main__():
    global scriptDialog
    global settings

    scriptDialog = DeadlineScriptDialog()

    selectedJobs = MonitorUtils.GetSelectedJobs()

    totalJobCount = len(selectedJobs)

    jobCount = 0
    for job in selectedJobs:
        if job.JobPlugin == "3dsmax":
            jobCount += 1

    if totalJobCount != jobCount:
        scriptDialog.ShowMessageBox("One or more selected jobs is NOT a 3dsMax job. Only 3dsMax jobs are supported.", "Error")
        return

    scriptDialog.AllowResizingDialog(True)
    scriptDialog.SetSize(600, 100)
    scriptDialog.SetTitle("Add MAXScript(s) to 3dsMax Job")

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("PreLoadScriptLabel", "LabelControl", "Run Pre-Load Script", 0, 0, "Run a MAXScript specified in the file browser field BEFORE the 3ds Max scene is loaded for rendering by the Slave.", False)
    scriptDialog.AddSelectionControlToGrid("PreLoadScriptBox", "FileBrowserControl", "", "MAXScript File (*.ms)", 0, 1, colSpan=2)

    scriptDialog.AddControlToGrid("PostLoadScriptLabel", "LabelControl", "Run Post-Load Script", 1, 0, "Run a MAXScript specified in the file browser field AFTER the 3ds Max scene is loaded for rendering by the Slave.", False)
    scriptDialog.AddSelectionControlToGrid("PostLoadScriptBox", "FileBrowserControl", "", "MAXScript File (*.ms)", 1, 1, colSpan=2)

    scriptDialog.AddControlToGrid("PreFrameScriptLabel", "LabelControl", "Run Pre-Frame Script", 2, 0, "Run a MAXScript specified in the file browser field BEFORE the Slave renders a frame.", False)
    scriptDialog.AddSelectionControlToGrid("PreFrameScriptBox", "FileBrowserControl", "", "MAXScript File (*.ms)", 2, 1, colSpan=2)

    scriptDialog.AddControlToGrid("PostFrameScriptLabel", "LabelControl", "Run Post-Frame Script", 3, 0, "Run a MAXScript specified in the file browser field AFTER the Slave renders a frame.", False)
    scriptDialog.AddSelectionControlToGrid("PostFrameScriptBox", "FileBrowserControl", "", "MAXScript File (*.ms)", 3, 1, colSpan=2)
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid("HSpacer1", 0, 0)
    applyButton = scriptDialog.AddControlToGrid("ApplyButton", "ButtonControl", "Apply", 0, 1, expand=False)
    applyButton.ValueModified.connect(ApplyButtonPressed)
    closeButton = scriptDialog.AddControlToGrid("CloseButton", "ButtonControl", "Close", 0, 2, expand=False)
    closeButton.ValueModified.connect(CloseButtonPressed)
    scriptDialog.EndGrid()

    settings = ("PreLoadScriptBox", "PostLoadScriptBox", "PreFrameScriptBox", "PostFrameScriptBox")
    scriptDialog.LoadSettings(GetSettingsFilename(), settings)
    scriptDialog.EnabledStickySaving(settings, GetSettingsFilename())

    scriptDialog.ShowDialog(True)


def GetSettingsFilename():
    return Path.Combine(GetDeadlineSettingsPath(), "AddMaxScriptFileSettings.ini")


def ApplyButtonPressed(*args):
    global scriptDialog

    jobs = MonitorUtils.GetSelectedJobs()

    preLoadScript = scriptDialog.GetValue("PreLoadScriptBox")
    postLoadScript = scriptDialog.GetValue("PostLoadScriptBox")
    preFrameScript = scriptDialog.GetValue("PreFrameScriptBox")
    postFrameScript = scriptDialog.GetValue("PostFrameScriptBox")

    for job in jobs:

        auxDirectory = RepositoryUtils.GetJobAuxiliaryPath(job)

        if preLoadScript != "":
            if File.Exists(preLoadScript):
                fileName = Path.GetFileName(preLoadScript)
                job.SetJobPluginInfoKeyValue("PreLoadScript", fileName)
                try:
                    tempFile = Path.Combine(auxDirectory, fileName)
                    File.Copy(preLoadScript, tempFile, True)
                    ClientUtils.LogText("Successfully added a MAXScript Pre-Load Script: %s" % tempFile)
                except:
                    ClientUtils.LogText("Failed to copy MAXScript Pre-Load Script to auxiliary job directory: %s" % job.JobId)

        if postLoadScript != "":
            if File.Exists(postLoadScript):
                fileName = Path.GetFileName(postLoadScript)
                job.SetJobPluginInfoKeyValue("PostLoadScript", fileName)
                try:
                    tempFile = Path.Combine(auxDirectory, fileName)
                    File.Copy(postLoadScript, tempFile, True)
                    ClientUtils.LogText("Successfully added a MAXScript Post-Load Script: %s" % tempFile)
                except:
                    ClientUtils.LogText("Failed to copy MAXScript Post-Load Script to auxiliary job directory: %s" % job.JobId)

        if preFrameScript != "":
            if File.Exists(preFrameScript):
                fileName = Path.GetFileName(preFrameScript)
                job.SetJobPluginInfoKeyValue("PreFrameScript", fileName)
                try:
                    tempFile = Path.Combine(auxDirectory, fileName)
                    File.Copy(preFrameScript, tempFile, True)
                    ClientUtils.LogText("Successfully added a MAXScript Pre-Frame Script: %s" % tempFile)
                except:
                    ClientUtils.LogText("Failed to copy MAXScript Pre-Frame Script to auxiliary job directory: %s" % job.JobId)

        if postFrameScript != "":
            if File.Exists(postFrameScript):
                fileName = Path.GetFileName(postFrameScript)
                job.SetJobPluginInfoKeyValue("PostFrameScript", fileName)
                try:
                    tempFile = Path.Combine(auxDirectory, fileName)
                    File.Copy(postFrameScript, tempFile, True)
                    ClientUtils.LogText("Successfully added a MAXScript Post-Frame Script: %s" % tempFile)
                except:
                    ClientUtils.LogText("Failed to copy MAXScript Post-Frame Script to auxiliary job directory: %s" % job.JobId)

        RepositoryUtils.SaveJob(job)


def CloseButtonPressed(*args):
    global scriptDialog
    scriptDialog.CloseDialog()
