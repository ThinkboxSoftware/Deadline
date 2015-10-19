OverrideJobName.py
==================================

This example event plugin script hooks into the "OnJobSubmitted" callback and allows a studio to globally manipulate the job name of "3dsmax" jobs after they have been submitted by a user. In our example, we are going to inject the really long Deadline JobId 'string' into the JobName as well as an optional PREFIX & SUFFIX, if configured.

Typically, you could submit a job and edit the job properties post submission via the Monitor GUI or provide the correct KEY=VALUE pairs (KVP's) at submission time (see our docs on 'Manual Job Submission'). However, you may wish to hook into the OnJobSubmitted event and handle the job naming as per say, your studio/pipeline conventions. In our exmaple, we just play with "3dsMax" jobs, but this can be extended/updated as you see fit.

A good habit to get into when scripting event plugins is to try and exit the event plugin as soon as it's no longer relevant. ie: Test against the job plugin type and if it's not a "3dsmax" job then exit ASAP. This is smarts for when you have lots of event plugins and performance is important.

Printing some logging messages is always a good idea as well:

    self.LogInfo( "On Job Submitted Event Plugin: Override Job Name Started" )

it also means an event plugin log report is created for your job in the Deadline queue. Could be handy to keep track of what event plugins have fired on a submitted job.

So, let's test if it's a 3dsMax job:

    if job.JobPlugin == "3dsmax":
        #do stuff

Cool. The callback returns the 3dsmax only job object for us so we can modify it:

def OnJobSubmitted(self, job):

Then we proceed to pull the event plugin config settings for what we have set via the "Configure Events..." dialog via Monitor:

    prefix = self.GetConfigEntryWithDefault("prefix", "")
    suffix = self.GetConfigEntryWithDefault("suffix", "")

and then apply them to the "job" object via:

    job.JobName = (prefix + "_" + job.JobName + "_" + job.JobId + "_" + suffix)

and then finally we need to save this new JobName setting we have set in the job object back to the actual Mongo DB:

    RepositoryUtils.SaveJob(job)

A final end of message is good to know the event plugin has completed and not crashed on us.

    self.LogInfo("On Job Submitted Event Plugin: Override Job Name Finished")
