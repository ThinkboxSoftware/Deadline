# My usual warning holds true:
#	This script is for learning purposes. It might work, it might delete everything in your farm.
#   Please be cautious since I likely haven't had time to test this.

from System.IO import *
from Deadline.Scripting import *
import os

def __main__():
	""" Replace specified text in all file names within the job output directory """
	toReplace = "_tmp"
	replaceWith = ""

	LogInfo("Renamer script started")

	# Sadly, there are instances where Deadline can't track the output directory so this script
	# isn't guaranteed to work for every plugin. Even different jobs for the same plugin 
        #may not work reliably
	outputDirectories = SlaveUtils.GetCurrentJobValue( "OutputDirectories" )
	for dir in outputDirectories:
		LogInfo("Searching for files to rename in " + dir)
		for file in os.listdir(dir):
			LogInfo("Checking filename " + file)
			oldname = file
			newname = oldname.replace(oldname, toReplace, replaceWith )
			if (oldname != newname):
				LogInfo("Renaming " + oldname)
				os.rename(oldname, newname)
