'''
This script shows an example of working with the output of the GetJobTasks subcommand.  

The script takes a single argument, which is the JobID of the job.  When calculating the elapsed time for
rendering tasks, the script does not account for daylight savings time differences or time zone differences.
Elapsed time for rendering tasks is rounded to the nearest second.

IMPORTANT:
Adjust the DEADLINECOMMAND_FULLPATH below to point your deadlinecommand executable.

USAGE EXAMPLE:
"C:\Program Files\Thinkbox\Deadline7\bin\deadlinecommand.exe" ExecuteScript GetJobTaskTimes.py 563c31ef2f359219f8745420

OUTPUT EXAMPLE:
0: 00:00:05.0140000 (Completed)
1: 00:00:02.4510000 (Completed)
2: 00:00:03.3090000 (Completed)
3: 00:00:02.7700000 (Completed)
4: 00:00:04.6160000 (Completed)
5: 00:00:02.8120000 (Completed)
6: 00:00:02.0000000 (Rendering)
7: 00:00:00.0000000 (Queued)
8: 00:00:00.0000000 (Queued)
9: 00:00:00.0000000 (Queued)
10: 00:00:00.0000000 (Queued)
11: 00:00:00.0000000 (Queued)

'''

# ======== Constants ========
DEADLINECOMMAND_FULLPATH="C:\\Program Files\\Thinkbox\\Deadline7\\bin\\deadlinecommand.exe"

# ======== Imports ========
import datetime
from time import time
import copy
import pprint
import subprocess

from Deadline.Scripting import *
from Deadline.Jobs import *

#======== Function Definitions ========
def secToHHMMSS(seconds):
    """
    Converts input seconds into the desired output display format.
    Rounds to the nearest second.
    """
    rndSec = int (seconds + 0.5) #  rounded seconds
    
    hrs = int( rndSec/3600 )
    min = int(   (rndSec - hrs*3600) / 60   )
    sec = rndSec - hrs*3600 - min*60
    
    return str(hrs).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2) + ".0000000"


def FixRenderTime( TaskDict ):
    """
    Estimates the render time for tasks that are rendering, and handles some special cases.
    """
    
    # Can't help you if the required keys are missing.
    if (not "TaskStatus" in TaskDict ) or (not "RenderStartTime" in TaskDict ):
        return
    
    # Estimate the Render time when rendering
    if ("Rendering" == TaskDict["TaskStatus"]):
        
        # Handle a special case:
        if ("Jan 01/01  00:00:00" == TaskDict["RenderStartTime"]):
            TaskDict["RenderTime"] = "00:00:00.0000000"
            TaskDict["TaskRenderTime"] = TaskDict["RenderTime"]
            return

        # Parse the string into a Python  datetime
        # Expected format is 'Nov 09/15  11:16:30'
        # See: http://strftime.org/
        
        dtStart = datetime.datetime.strptime(TaskDict["RenderStartTime"], "%b %d/%y  %H:%M:%S")
        dtNow = datetime.datetime.now()
        
        # print ("%s --> %s" % (TaskDict["RenderStartTime"], dtStart.isoformat() ) )
        
        timeDelta = dtNow - dtStart
        
        TaskDict["RenderTime"] = secToHHMMSS( timeDelta.seconds )
        TaskDict["TaskRenderTime"] = TaskDict["RenderTime"]
    else:
        # ASSUMPTION: Assume zero for all other TaskStatus values.
        TaskDict["RenderTime"] = "00:00:00.0000000"
        TaskDict["TaskRenderTime"] = TaskDict["RenderTime"]
        
    return


def ParseGetJobTasksOutput( output ):
    """
    Parses the output of the call to GetJobTasks.  The result is a "TaskList", mean a list of "TaskDict"s,
    where a "TaskDict" is a dictionary of key,value pairs of information about the Task.
    """
    
    TaskList = []
    
    # All entries in this dictionary must be lower case.
    IntegerKeysDict={'averageram', 'averagerampercentage', 'averageswap', 'cpuutilisation', 'errorcount', 
        'imagefilesize', 'peakcpuusage', 'peakrampercentage', 'peakramusage', 'peakswap', 'taskaverageram',
        'taskaveragerampercentage', 'taskaverageswap', 'taskcpuitilisation', 'taskerrorcount', 'taskid',
        'taskimagefilesize', 'taskpeakcpuusage', 'taskpeakrampercentage', 'taskpeakramusage', 'taskpeakswap',
        'tasktotalcpuclocks', 'taskusedcpuclocks', 'totalcpuclocks', 'usedcpuclocks'}
    
    # All entries in this dictionary must be lower case.
    BooleanKeysDict={'isstarting', 'taskisstarted', 'taskwaitingtostart', 'waitingtostart'}
    
    # Parse the lines
    TaskDict = {}
    lines = output.splitlines()
    for line in lines:
        if ( not line.strip() ):
            if (len(TaskDict) > 0):
                if ( "10675199.02:48:05.4775807" == TaskDict["TaskRenderTime"]):
                    FixRenderTime( TaskDict )
                TaskList.append( copy.copy(TaskDict) )
                TaskDict = {}
                
            continue
        
        # Split the non-empty line into key and value.
        kv = line.split('=', 1)
            
        # Check for and handle keys with no value.
        if (len(kv) < 2):
            TaskDict[kv[0]] = None
            continue
        
        # Check for and handle keys that should have integer values.
        if (kv[0].lower() in IntegerKeysDict):
            TaskDict[kv[0]] = int(kv[1])
            continue
            
        # Check for and handle keys that should have boolean values.
        if (kv[0].lower() in BooleanKeysDict):
            TaskDict[kv[0]] = ( kv[1].lower() in ("true", "t", "yes", "y", "1") )
            continue
        
        # Assume all other keys have string values.
        TaskDict[kv[0]] = kv[1]
            
    return TaskList


def PrintJobTaskTimes( TaskList ):
    """
    Prints out the task times for tasks contained in the TaskList.
    """
    
    for TaskDict in TaskList:
        TaskID = "?"
        if ( "TaskId" in TaskDict):
            TaskID = ("%d" % TaskDict["TaskId"])
        
        print ( "%s: %s (%s)" % (TaskID, TaskDict["TaskRenderTime"], TaskDict["TaskStatus"] ) )
    
#======== Main Entry Point ========
def __main__(jobId):
    
    job =RepositoryUtils.GetJob(jobId, True)
    if (not job):
        print("The specified Job ID was not found: %s" % jobId)
        exit
    
    call_deadline = subprocess.Popen([DEADLINECOMMAND_FULLPATH, 'GetJobTasks', jobId], stdout=subprocess.PIPE)
    output = call_deadline.communicate()[0]
    
    TaskList=ParseGetJobTasksOutput(output)
    
    # Uncomment the following lines to see a full readout of each Task's information.
    #for TaskDict in TaskList:
    #    print("--")
    #    pprint.pprint(TaskDict)

    PrintJobTaskTimes( TaskList )
    
