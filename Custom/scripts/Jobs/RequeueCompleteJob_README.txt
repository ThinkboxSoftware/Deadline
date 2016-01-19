Here's a job script which will requeue a job and then instantly complete the job again. This helps to force the triggering of event plugins such as Draft again.

However, in Deadline 6, there was a Scripting API bug, which meant "RepositoryUtils.CompleteJob()" was broken. Luckily, we have "DeadlineCommand.exe" which for the most part, has a duplicate command that we can use by spawning a process in the py script instead.

[INSERT reference here about more than one way to skin a cat]