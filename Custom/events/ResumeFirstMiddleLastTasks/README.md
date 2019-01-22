# ResumeFirstMiddleLastTasks.py

This script came from a customer request on how they could go about submitting Jobs to their repository as suspended and then having the first, middle, and last tasks of those jobs enabled automatically immediately after submission.

In this case all we have to do is create an OnJobSubmitted event plugin that will grab the collection of tasks for any submitted job, and then forcefully resume each of the first, middle, and last tasks.

Note that this example plugin script is for a very basic usecase, as this will apply to all submitted job regardless of their status.
For our requesting customer, we just assume all the jobs are submitted as suspended.
So if you want to adapt this for your own usecase, you should supply some more stringent parameters for when to perform the resume operation.
