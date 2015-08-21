3dsMaxVersionInstalled.py
==================================

An alternative approach than our other example: "SoftwareAudit.py" to regularly injecting the 3dsmax.exe version installed on a slave into the ExtraInfo0 column.

Both examples are valid; this just shows yet another way, Deadline can be flexible here!

This is drop-in safe, so you can just copy it over to your "custom" folder, edit it for the particular versions of 3dsmax you have and
restart a Slave or two. They'll only update the "Extra Info 0" column at startup, so that restart is necessary.

This script should be safe on mixed OS farms, as the local paths won't exist on Linux or OSX.
