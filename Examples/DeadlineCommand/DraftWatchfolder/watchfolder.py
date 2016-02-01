import sys
import os
import time

from System import Array
from System.Collections.Specialized import *
from System.IO import *
from System.Text import *
from System.Diagnostics import *

from Deadline.Scripting import *

from DraftIntegration import *

# For Draft Integration
import imp
import os
imp.load_source(
    'DraftIntegration',
    os.path.join(
        RepositoryUtils.GetRootDirectory(),
        "submission",
        "Draft",
        "Main",
        "DraftIntegration.py"))


# Change these to match your own environment
# Do not make watchfolder = outputfolder
path_to_watch = "\watchfolder"
path_to_send = "\outputfolder"
script_to_run = "\codecconvert.py"


def __main__(*args):

    # Create a dictionary of all the files in the watchfolder (a.k.a. path_to_watch)
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:
        # How many seconds to wait between folder checks - be careful about making this less than 2
        time.sleep(5)

        # Create a dictionary of all the files in the watchfolder
        after = dict([(f, None) for f in os.listdir(path_to_watch)])

        # Compare the two lists to find new files
        added = [f for f in after if f not in before]

        # Compare the two lists to find files that were removed
        # removed = [f for f in before if not f in after]

        if added:
            # print "Added: ", ", ".join (added)

            for f in added:
                # Create a new deadline job for each new file
                CreateAndSubmitJobs(f)
                # Here you can add any code to move/delete/etc. the file you just made a job out of

            # print "Job(s) Created"

        # Here you can add code to act when a file gets removed. By default this is not used
        # if removed:
            # print "Removed: ", ", ".join (removed)

        before = after


def CreateAndSubmitJobs(newFile):
    """
    Creates a Draft job, with file named newFile.
    """

    # These values are all rough defaults, you may need to change them to match your farm
    # Creating the job file programmatically
    # http://docs.thinkboxsoftware.com/products/deadline/7.0/1_User%20Manual/manual/manual-submission.html#job-info-file
    jobInfoFilename = Path.Combine(GetDeadlineTempPath(),
                                   "draft_job_info.job")  # This can be named whatever you wish
    writer = StreamWriter(jobInfoFilename, False, Encoding.Unicode)

    try:
        writer.WriteLine("Plugin=Draft")
        writer.WriteLine("Name=WatchfolderJob-" + newFile)
        writer.WriteLine("Comment=Created automatically by watchfolder.py")

        # If you've got a specific machine you want to test all this locally on,
        # set this to that machine
        # writer.WriteLine("Whitelist=my-machine")

        # Limits the number of machines working on the job to 1, just for testing
        # writer.WriteLine("MachineLimit=1")
        writer.WriteLine("OutputDirectory0=%s\n" % path_to_send)

    finally:
        writer.Close()

    # Create plugin info file programmatically
    # http://docs.thinkboxsoftware.com/products/deadline/7.0/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    pluginInfoFilename = Path.Combine(GetDeadlineTempPath(),
                                      "draft_plugin_info.job")  # This can be named whatever you wish

    writer = StreamWriter(pluginInfoFilename, False, Encoding.Unicode)
    try:
        # Lots of these are required values, and I've left them blank. They can be
        # populated if you choose
        writer.WriteLine("scriptFile=%s\n" % script_to_run)
        writer.WriteLine("ScriptArg0=username=\"\"")
        writer.WriteLine("ScriptArg1=entity=\"\"")
        writer.WriteLine("ScriptArg2=version=\"\"")
        writer.WriteLine("ScriptArg3=frameList=")
        writer.WriteLine("ScriptArg4=outFolder=%s\n" % path_to_send)
        writer.WriteLine("ScriptArg5=outFile=%s\n" % Path.Combine(path_to_send, newFile))
        writer.WriteLine("ScriptArg6=inFile=%s\n" % Path.Combine(path_to_watch, newFile))
    finally:
        writer.Close()

    # Setup the command line arguments.
    arguments = StringCollection()

    arguments.Add(jobInfoFilename)
    arguments.Add(pluginInfoFilename)

    ScriptUtils.ExecuteCommand(arguments)
