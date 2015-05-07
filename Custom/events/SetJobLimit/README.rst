SetJobLimit.py
==================================

A user asked how can I always make sure ALL my jobs have a certain Deadline "limit" applied to them, so I don't go over budget on my floating license server and get in a situation where my render nodes are pulling more licenses than I own?

Let's use the on job submitted event callback which returns the 'job' object for us as well: ::

	def OnJobSubmitted( self, job ):

In the "SetJobLimit.param" file, let's expose a string field, which as "Super-User" we can type in the "limit(s)" which we want to apply in the "Configure Events..." dialog via Monitor: ::

	[JobLimits]
	Type=string
	Category=Options
	CategoryOrder=0
	CategoryIndex=1
	Label=Limits
	Default=
	Description=A comma separated list of limits to set automatically when the job is submitted.
    
There are many possibilites here in what types of UI you can build yourself and expose. Please see our "Scripting Overview" sections of our User Manual for more details.

So, on the event plugin executing flipside, let's pick up the 1 or more "limit(s)" that have been typed into the text field via the UI above and add them to a list: ::

	limitNames = self.GetConfigEntry( "JobLimits" ).split(',')

	for limitName in job.JobLimitGroups:
		if limitName.lower() not in limitNames:
			limitNames.append(limitName)

and finally let's apply these limits to the job object and save it back to the MongoDB: ::

	job.SetJobLimitGroups(limitNames)
	RepositoryUtils.SaveJob(job)

As always, log messages would be a good idea to report what's going on to the users if they look at the job's log reports and wonder why their job now has certain "limits" applied to it.

