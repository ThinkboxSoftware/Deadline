CountSlaves.py - Example of how to count the number of Slaves which worked on a job
===

There are really two ways you can count the Slaves. The first is by using the job reports, which would include every machine that ever tried to render the job including failures or re-queues. The other is by using the task list, which gets re-written whenever a Slave re-tries a particular task.

This also should be a good reference for accessing the task list and reports list for a job. You will need to change the job id in the script to use it properly, but call it like so:

```
deadlinecommand ExecuteScript CountSlaves.py 
```

