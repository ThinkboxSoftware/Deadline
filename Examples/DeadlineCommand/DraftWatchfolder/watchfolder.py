import sys
import os
import time
import subprocess
import codecs

# Change these to match your own environment
# Do not make watchfolder = outputfolder
path_to_watch = "\path\of\watchfolder"
path_to_send = "\path\of\outputfolder"
script_to_run = "\path\of\script"


def __main__():

    # Create a dictionary of all the files in the watchfolder (a.k.a. path_to_watch)
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:
        # How many seconds to wait between folder checks - be careful about making this less than 2
        time.sleep(5)

        # Create a dictionary of all the files in the watchfolder
        after = dict([(f, None) for f in os.listdir(path_to_watch)])

        # Compare the two lists to find new files
        added = [f for f in after if f not in before]

        if added:
            # print "Added: ", ", ".join(added)

            for f in added:
                # Create a new deadline job for each new file
                CreateAndSubmitJobs(f)
                # Here you can add any code to move/delete/etc. the file you just made a job out of

        before = after


def CreateAndSubmitJobs(newFile):
    """
    Creates a Draft job, using a file named newFile.
    """

    # These values are all rough defaults, you may need to change them to match your farm
    # Creating the job file programmatically
    # http://docs.thinkboxsoftware.com/products/deadline/7.0/1_User%20Manual/manual/manual-submission.html#job-info-file

    # This is where your temp files will be placed. You may want to change
    # this, as this is assuming a default Windows 10 install of deadline
    temp_path = os.path.join(GetCurrentUserHomeDirectory(), "temp")
    jobInfoFilename = os.path.join(temp_path,
                                   "draft_job_info.job")  # This can be named whatever you wish
    writer = open(jobInfoFilename, 'w')

    try:
        writer.write("Plugin=Draft\n")
        writer.write("Name=WatchfolderJob-" + newFile + "\n")
        writer.write("Comment=Created automatically by watchfolder.py\n")

        # If you've got a specific machine you want to test this locally on,
        # set this to that machine
        # writer.write("Whitelist=mobile-010\n")

        writer.write("OutputDirectory0=%s\n" % path_to_send)

    finally:
        writer.close()

    # Create plugin info file programmatically
    # http://docs.thinkboxsoftware.com/products/deadline/7.0/1_User%20Manual/manual/manual-submission.html#plug-in-info-file
    # This can be named whatever you wish
    pluginInfoFilename = os.path.join(temp_path, "draft_plugin_info.job")

    writer = open(pluginInfoFilename, 'w')
    try:
        # Lots of these are required values, and I've left them blank. They can be
        # populated if you choose
        writer.write("scriptFile=%s\n" % script_to_run)
        writer.write("ScriptArg0=username=\"\"\n")
        writer.write("ScriptArg1=entity=\"\"\n")
        writer.write("ScriptArg2=version=\"\"\n")
        writer.write("ScriptArg3=frameList=\n")
        writer.write("ScriptArg4=outFolder=%s\n" % path_to_send)
        writer.write("ScriptArg5=outFile=%s\n" % os.path.join(path_to_send, newFile))
        writer.write("ScriptArg6=inFile=%s\n" % os.path.join(path_to_watch, newFile))
    finally:
        writer.close()

    # Setup the command line arguments.
    SubmitJobs(jobInfoFilename, pluginInfoFilename)


def SubmitJobs(file1, file2):
    """
    Wrapper for CallDeadlineCommand to make creating jobs simpler
    """
    print(CallDeadlineCommand([file1, file2]))


def GetCurrentUserHomeDirectory():
    output = CallDeadlineCommand(["-GetCurrentUserHomeDirectory"])
    return output.replace("\r", "").replace("\n", "").replace("\\", os.sep)


def GetRepositoryRoot():
    output = CallDeadlineCommand(['-root'])
    return output.replace("\r", "").replace("\n", "").replace("\\", os.sep)


def CallDeadlineCommand(args):
    """
    Calls deadlinecommand with arguments as passed args with 'deadlinecommand' as the first argument
    """
    # On OSX, we look for the DEADLINE_PATH file. On other platforms, we use
    # the environment variable.
    if os.path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as f:
            deadlineBin = f.read().strip()
        deadlineCommand = "%s/deadlinecommand" % deadlineBin
    else:
        try:
            deadlineBin = os.environ['DEADLINE_PATH']
        except KeyError:
            return ""

        if os.name == 'nt':
            deadlineCommand = "%s\\deadlinecommand.exe" % deadlineBin
        else:
            deadlineCommand = "%s/deadlinecommand" % deadlineBin

    # insert deadlineCommand as the first argument
    args.insert(0, deadlineCommand)

    # Specifying PIPE for all handles to workaround a Python bug on Windows.
    # The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen(
        args,
        cwd=deadlineBin,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=None)
    proc.stdin.close()
    proc.stderr.close()

    output = proc.stdout.read()
    output = output.decode("utf_8")

    return output

if __name__ == "__main__":
    __main__()
