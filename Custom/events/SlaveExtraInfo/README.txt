SlaveExtraInfo.py

A user asked how can they query on a semi-regular basis each of their slaves for 1 or more system environment variables entered on the individual machine and somehow send that information back so it can be visible via Deadline Monitor?

~I'm glad you asked that question! :-)

So, let's use one of those shiny new "slave" centric event callbacks and hook into whenever a slave first gets booted up. That's a slave gets started NOT the machine get's booted up: ::

	self.OnSlaveStartedCallback += self.OnSlaveStarted

	def OnSlaveStarted( self, slaveName ):

This event callback also returns the "slaveName" in question which is might handy as we need that.

Let's populate an "Extra Info X" column in Deadline Monitor for each environment variable we want to query, store and display via Monitor. Let's expose this as a setting we can modify via the "Configure Events..." dialog in Monitor: ::

	[Enabled]
	Type=boolean
	Category=Options
	CategoryOrder=0
	CategoryIndex=0
	Label=Enabled
	Default=false
	Description=If this event plugin is enabled.

	[ExtraInfo0]
	Type=string
	Category=Extra Info Options
	CategoryOrder=1
	CategoryIndex=0
	Label=Extra Info 0
	Default=
	Description=Environment Variable if present under the current process when slave starts to be inserted into Extra Info 0 column in monitor

Don't forget to also set a "default" value of all these settings via the "SlaveExtraInfo.dlinit" file. Let's set them all to BLANK: ::

	Enabled=False
	ExtraInfo0=
	ExtraInfo1=
	ExtraInfo2=
	ExtraInfo3=
	ExtraInfo4=
	ExtraInfo5=
	ExtraInfo6=
	ExtraInfo7=
	ExtraInfo8=
	ExtraInfo9=

So, we can loop through the 10 x Extra Info fields in the "SlaveExtraInfo" event plugin in your repository, check to see if an ENV VARIABLE has been declared. If it has, let's query the slave's machine on slave startup and if anything is returned, let's inject that SYS ENV VARIABLE into it's slave "Extra Info" column, so you can see it in the "Slave Panel" in Monitor: ::

	for i in range(0, 9):
	tempExtraInfo = "ExtraInfo" + str(i)
	extraInfoQuery = self.GetConfigEntryWithDefault( tempExtraInfo, "" )

	if extraInfoQuery != "":
	    envValue = Environment.GetEnvironmentVariable( extraInfoQuery )

	    if envValue != "":
	        slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )

	        if i == 0:
	            slaveSettings.SlaveExtraInfo0 = envValue

and finally, we need to save these new slave settings back to the MongoDB. ::

	RepositoryUtils.SaveSlaveSettings( slaveSettings)

Obvious enhancements are to wrap the query with a try(except) in case the environment variable returns NULL or you want to return a special value. You could also hook into other slave centric callbacks to update the Slave Info more frequently such as whenever a slave starts a new job or starts to render or becomes IDLE.

Finally, you could use this event plugin framework to build a tool which queries what version(s) of Maya or 3dsMax are installed on a machine and then populate one of the "Extra Info X" columns with this information for tracking purposes. Handy to know what slaves have recieved the software patch install or not...
