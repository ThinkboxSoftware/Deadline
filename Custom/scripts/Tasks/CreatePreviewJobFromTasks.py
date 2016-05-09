#---------------------------------------
# Created by Justin Blagden - March 2016
#---------------------------------------
from Deadline.Scripting import *
from Deadline.Jobs import *
from Deadline.Users import *

import os
import socket


def __main__(*args):
    selectedTasks = MonitorUtils.GetSelectedTasks()
    selectedJobs = MonitorUtils.GetSelectedJobs()
    framelist = ""

    if len(selectedTasks) > 0 and len(selectedJobs) == 1:
        for i, task in enumerate(selectedTasks):
            framelist += task.TaskFrameString

            if i < len(selectedTasks) - 1:
                framelist += ","

        # Now set the values we're going to change when we dupe the job files
        # Grab our 1 job
        selectedJob = selectedJobs[0]  # We know we only have one selected job

        # We're going to make this *slightly* more important than the original job
        highpriority = selectedJob.Priority

        # Deadline doesn't allow priorities greater than 100
        highpriority += 1
        if highpriority > 100:
            highpriority = 100

        deadlineTemp = ClientUtils.GetDeadlineTempPath()
        jobInfoFile = os.path.join(deadlineTemp, "duplicate_job_info.job")
        pluginInfoFile = os.path.join(deadlineTemp, "duplicate_plugin_info")

        # Create the replacement dictionary
        # Defined just like the job or plugin files are
        replaceDict = {'Name': 'Preview of %s' % (selectedJob.JobName),
                       'Frames': framelist,
                       'Priority': highpriority,
                       'ChunkSize': 1}

        # Create the job and plugin files, replaceing designated key+value pairs
        DuplicateJobProperties(selectedJob, jobInfoFile, pluginInfoFile, replaceDict)

        # Submit the preview job with our new job files
        submissionArray = [jobInfoFile, pluginInfoFile]
        auxFiles = selectedJob.JobAuxiliarySubmissionFileNames
        submissionArray.extend(auxFiles)
        RepositoryUtils.SubmitJob(submissionArray)

        # Now we need to make sure that the tasks we've selected are set to
        # 'Completed' so we aren't doing work twice
        hostname = socket.gethostname()
        RepositoryUtils.CompleteTasks(selectedJob, selectedTasks, hostname)


def DuplicateJobProperties(originalJob, jobInfoFile, pluginInfoFile, replaceDict):
    # This'll go through the job's properites and copy everything that isn't blank or supposed to be overwritten
    # Make the job file
    try:
        fileHandle = open(jobInfoFile, "w")

        # Loop through the JobInfoKeys
        for key in originalJob.GetJobInfoKeys():
            value = originalJob.GetJobInfoKeyValue(key)

            if key in replaceDict:
                fileHandle.write("%s=%s\n" % (key, replaceDict[key]))
            elif value != "":
                fileHandle.write("%s=%s\n" % (key, value))

        # Loop through the JobExtraInfoKeys
        for key in originalJob.GetJobExtraInfoKeys():
            value = originalJob.GetJobInfoKeyValue(key)

            if key in replaceDict:
                fileHandle.write("%s=%s\n" % (key, replaceDict[key]))
            elif value != "":
                fileHandle.write("%s=%s\n" % (key, value))
    finally:
        fileHandle.close()

    # Make the plugin file
    try:
        fileHandle = open(pluginInfoFile, "w")

        # Loop through the JobPluginInfo
        for key in originalJob.GetJobPluginInfoKeys():
            value = originalJob.GetJobPluginInfoKeyValue(key)

            if key in replaceDict:
                fileHandle.write("%s=%s\n" % (key, replaceDict[key]))
            else:
                fileHandle.write("%s=%s\n" % (key, value))
    finally:
        fileHandle.close()
