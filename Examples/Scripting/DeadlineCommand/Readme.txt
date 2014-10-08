This is an example of how you can pull Deadline specific information from
the command line using DeadlineCommand. It's possible to get information
using the Standalone Python API, but this example doesn't require Pulse to
be running.

The script itself will list all failed and currently rendering jobs from the
past 24 hours. There is also some debugging left to show when jobs are skipped.

To run this script, just copy this guy somewhere and call it using
DeadlineCommand's ExecuteScript command like so:

C:\Program Files\Thinkbox\Deadline6\bin\DeadlineCommand ExecuteScript GetJobs.py

When you read the script, you'll notice that because Python.net doesn't change
the .net DateTime object to a Python datetime, we're using what's provided by
Mono or Microsoft's CLR. It'll look pretty strange if you're not used to it.

As usual, if you have questions, problems, or comments, send them over to
support@thinkboxsoftware.com. Feel free to blame Edwin in the subject