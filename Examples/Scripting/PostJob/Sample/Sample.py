#Python.NET
###############################################################
# This is an Python.net/CPython script.                       #
# To use IronPython, remove  "#Python.NET" from the first     #
# line of this file.                                          #
###############################################################

###############################################################
## Imports
###############################################################
from System.IO import *
from Deadline.Scripting import *
import os

###############################################################
## Entry point and other source
###############################################################
def __main__():
	""" This is run by Deadline before or after a task depending on which context its used in """

	LogInfo("Script ran.")
	LogInfo("...And did absolutely nothing")
