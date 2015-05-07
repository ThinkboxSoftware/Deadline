JobStats.py

An example event plugin script which executes on job completion for any job in your queue, calculating and returning the job statistics object, allowing you to retireve information.

In this trival example, we log the job's average frame time and peak ram usage. As we are printing a LogInfo message within an event plugin for job completion, the completed job will now contain an additional log report for this event plugin with these 2 x log messages.

The example shows how this completed job stats information can also be retirved via our API. This data is also injected into the built-in Deadline "Farm Reports" system.

A possible workflow could be sending select job stats information to another DB or to email.

Finally, we show how some of the 'time' based values in Deadline are returned as a 'TimeSpan' object and how these can be handled for display purposes.
