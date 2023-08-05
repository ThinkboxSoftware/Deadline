#!/usr/bin/env python3

from __future__ import absolute_import
import tempfile
import os
import sys
import subprocess
from distutils.util import strtobool

from Deadline.Events import DeadlineEventListener
from Deadline.Scripting import ClientUtils, RepositoryUtils

def GetDeadlineEventListener():
    """This is the function that Deadline calls to get an instance of the
    main DeadlineEventListener class.
    """
    return Hammerspace()

def CleanupDeadlineEventListener(deadlinePlugin):
    """This is the function that Deadline calls when the event plugin is
    no longer in use so that it can get cleaned up.
    """
    deadlinePlugin.Cleanup()

class Hammerspace(DeadlineEventListener):
    """This is the main DeadlineEventListener class for Hammerspace"""

    def __init__(self):
        if sys.version_info.major == 3:
            super().__init__()
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):

        # Try to exit event plugin as early as possible
        hammerspace_job = strtobool(job.GetJobExtraInfoKeyValueWithDefault("HS_PLUGIN_GENERATED", "False"))
        if hammerspace_job:
            return

        # If no job output directories declared, then exit event plugin
        output_dirs = [x for x in job.JobOutputDirectories]
        output_dirs = list(dict.fromkeys(output_dirs)) # remove duplicates
        if not output_dirs:
            return

        # Grab the submission-related plugin override settings
        hsGroup = self.GetConfigEntryWithDefault("Group", "").strip()
        hsPool = self.GetConfigEntryWithDefault("Pool", "").strip()
        hsLimit = self.GetConfigEntryWithDefault("Limit", "").strip()
        hsPriorityOffset = self.GetIntegerConfigEntryWithDefault("PriorityOffset", 0)

        if not hsGroup:
            hsGroup = job.JobGroup

        if not hsPool:
            hsPool = job.JobPool

        if not hsLimit:
            hsLimit = job.JobLimitGroups

        if hsPriorityOffset == 0:
            hsPriority = job.JobPriority
        else:
            hsPriority = max(0, min(100, job.Priority + hsPriorityOffset))

        iteration_delay = self.GetIntegerConfigEntryWithDefault("IterationDelay", 1)
        iteration_count = self.GetIntegerConfigEntryWithDefault("IterationCount", 20)

        if job.JobBatchName == "":
            batch_name = job.JobName
        else:
            batch_name = job.JobBatchName

        dir_job_id = self.submit_dir_create_job(
            job,
            batch_name=batch_name,
            group=hsGroup,
            pool=hsPool,
            priority=hsPriority,
            limits=hsLimit,
            dirs=output_dirs,
            iteration_delay=iteration_delay,
            iteration_count=iteration_count
        )

        # Update the original job
        if job.JobBatchName == "":
            job.JobBatchName = job.JobName
        job.SetJobDependencyIDs([dir_job_id])
        RepositoryUtils.PendJob(job)
        RepositoryUtils.SaveJob(job)

        return dir_job_id

    def submit_dir_create_job(self, job, batch_name, group, pool, priority, limits, dirs, iteration_delay, iteration_count):

        pluginPath = RepositoryUtils.GetEventPluginDirectory("Hammerspace")
        folder_script = os.path.join(pluginPath, "createFolders.py")
        utils_script = os.path.join(pluginPath, "HammerspaceUtils.py")

        deadline_temp = ClientUtils.GetDeadlineTempPath()
        with tempfile.NamedTemporaryFile(mode="w", dir=deadline_temp, delete=False) as fh:
            job_info_file = fh.name
            fh.write("Plugin=DeadlineCommand\n")
            fh.write("Name={0} [{1}]\n".format(job.JobName, "Make Directories"))
            fh.write("BatchName={0}\n".format(batch_name))
            fh.write("Department={0}\n".format(job.JobDepartment))
            fh.write("UserName={0}\n".format(job.JobUserName))
            fh.write("Pool={0}\n".format(pool))
            fh.write("Group={0}\n".format(group))
            fh.write("Priority={0}\n".format(priority))
            fh.write("OnJobComplete={0}\n".format(job.JobOnJobComplete))
            fh.write("LimitGroups={0}\n".format(limits))
            fh.write("Comment=Hammerspace job to create output directories before render\n")
            fh.write("ExtraInfoKeyValue0=HS_PLUGIN_GENERATED=True")

        with tempfile.NamedTemporaryFile(mode="w", dir=deadline_temp, delete=False) as fh:
            plugin_info_file = fh.name
            fh.write("Arguments=--directories \"{0}\" --iteration_delay {1} --iteration_count {2}\n".format(";".join(dirs), iteration_delay, iteration_count))

        output = self.CallDeadlineCommand([job_info_file, plugin_info_file, folder_script, utils_script])

        job_id = ""
        result_array = output.split()
        for line in result_array:
            if line.startswith("JobID="):
                job_id = line.replace("JobID=","")
                break

        return job_id

    def CallDeadlineCommand(self, arguments):
        deadline_bin = ClientUtils.GetBinDirectory()

        deadline_command = ""
        if os.name == 'nt':
            deadline_command = os.path.join(deadline_bin, "deadlinecommandbg.exe")
        else:
            deadline_command = os.path.join(deadline_bin, "deadlinecommandbg")

        arguments.insert(0, deadline_command)
        proc = subprocess.Popen(arguments, cwd=deadline_bin)
        proc.wait()

        output_path = os.path.join(ClientUtils.GetDeadlineTempPath(), "dsubmitoutput.txt")
        with open(output_path, 'r') as fh:
            output = fh.read()
        return output
