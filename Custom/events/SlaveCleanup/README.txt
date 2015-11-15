SlaveCleanup.py

DISCLAIMER:
This slave event plugin could do dangerous things like delete lots of important files/directories. You have been warned!

Question:
A user asked how can they cleanup all the files & directories in one or more locations on a local or indeed, network location on a semi-regular basis.

Answer:
So, let's use one of those shiny new "slave" centric event callbacks and hook into whenever a slave gets started up. That's a slave gets started NOT the machine get's booted up: ::

	self.OnSlaveStartedCallback += self.OnSlaveStarted

	def OnSlaveStarted( self, slaveName ):

A number of variables have been exposed to the "Configure Evenets..." dialog to allow users to configure what paths are recurvisely searched, how old (modified date) the files and directories must be, before being considered for deletion (DELETE_DAYS). Finally, "VERBOSE" and "DRYRUN" options are given, so that verbose logging will be logged to the slave reports and dry run, allows you to execute the event plugin on a slave and it doesn't actually do anything, execept log to the slave report what it would have deleted if it had been allowed.

Further Enhancements:
If your not running this event plugin on Windows slaves, then you could take advantage of the commented out code in the SlaveCleanup.py file to use Python's multiprocessing module and the "Pool()" function to speed up the file/dir deletion. Sadly, this isn't supported on Windows OS due to mapped drive paths.

You could also expose an option to control what file formats are considered for deletion. Currently, we consider all files & dirs.
