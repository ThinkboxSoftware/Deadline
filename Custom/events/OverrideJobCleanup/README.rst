OverrideJobCleanup.py

This example event plugin script hooks into the "OnJobSubmitted" callback and allows a studio to globally configure different job cleanup settings per appplication plugin type.

Typically, you could submit a job and edit the job properties post submission via the Monitor GUI or provide the correct KEY=VALUE pairs (KVP's) at submission time (see our docs on 'Manual Job Submission'). However, a far cleaner apporoach, which automates the task is to hook into the OnJobSubmitted event and handle applying the different job cleanup settings at submission time by filtering the job plugin type.

A good habit to get into when scripting event plugins is to try and exit the event plugin as soon as it's no longer relevant. ie: Test against the job plugin type and if it's not a "3dsmax", "MayaBatch", "MayaCmd" or "Nuke" job then exit ASAP. This is smarts for when you have lots of event plugins and performance is important.

Printing some logging messages is always a good idea as well: ::

	self.LogInfo( "On Job Submitted Event Plugin: Override Job Cleanup Started" )

it also means an event plugin log report is created for your job in the Deadline queue. Could be handy to keep track of what event plugins have fired on a submitted job.

So, let's test if it's a Nuke job: ::

	if job.JobPlugin == "Nuke":
		#do stuff

Cool. The callback returns the job object for us so we can modify it: ::

	def OnJobSubmitted( self, job ):

Then we proceed to pull the event plugin config settings for what we have set via the "Configure Events..." dialog via Monitor: ::

	nukeJobCleanupDays = self.GetConfigEntryWithDefault( "nukeJobCleanupDays", "-1" )
	nukeOverrideJobCleanupType = self.GetConfigEntryWithDefault( "nukeOverrideJobCleanupType", "Disabled" )
 
and then apply them to the "job" object: ::

	job.JobOverrideAutoJobCleanup = True
	job.JobOverrideJobCleanup = True
	job.JobCleanupDays = int(nukeJobCleanupDays)

	# JobOverrideJobCleanupType is either 0, 1 or 2 meaning "DISABLED", "Archive" or "Delete"
	job.JobOverrideJobCleanupType

and then finally we need to save these new settings we have set in the job object back to the actual Mongo DB: ::

	RepositoryUtils.SaveJob(job)

A final end of message is good to know the event plugin has completed and not crashed on us. ::

	self.LogInfo( "On Job Submitted Event Plugin: Override Job Cleanup Finished" )
