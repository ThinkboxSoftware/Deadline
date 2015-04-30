Example of how to calculate on the fly, the jobs stats object for each job and
then inject certain job stats information into a couple of the "ExtraInfoX"
columns, thereby allowing you to display certain information visually in the
monitor to your artists. Please see the script comments on how it works.

The script itself will list all failed and currently rendering jobs from the
past 24 hours. There is also some debugging left to show when jobs are skipped.

To run this script, just copy this guy somewhere and call it using
DeadlineCommand's ExecuteScript command like so:

C:\Program Files\Thinkbox\Deadline6\bin\DeadlineCommand ExecuteScript GetJobs.py

As usual, if you have questions, problems, or comments, send them over to
support@thinkboxsoftware.com. Feel free to blame Edwin in the subject