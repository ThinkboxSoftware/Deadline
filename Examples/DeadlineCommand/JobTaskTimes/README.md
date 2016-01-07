# About This Script #

**GetJobTaskTimes.py** shows an (indirect) example of working with the output of the GetJobTasks subcommand 
to DeadlineCommand.

More specifically, this script prints Task times for the specified JobId.  See additional notes in the script's header.

## Usage Example ##
    "C:\Program Files\Thinkbox\Deadline7\bin\deadlinecommand.exe" ExecuteScript GetJobTaskTimes.py 563c31ef2f359219f8745420

## Output Example ##

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


Feel free to make improvements to the script by submitted a pull request.  If you have questions, post them
to our [Forum](https://forums.thinkboxsoftware.com).
