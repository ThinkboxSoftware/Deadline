# Set environment variables for current plugin
# Should work with 6.0 and up, maybe 5.x as well.
# Written by Edwin Amsler <support@thinkboxsoftware.com>

###############################################################
## Imports
###############################################################

from Deadline.Scripting import *

environment = {
    "a": "b",
    "x": "y",
    "1": "2"
}

###############################################################
## Entry point and good times
###############################################################
def __main__( deadlinePlugin ):
    ClientUtils.LogText("Adding enviornment variables to Maya job")

    for k, v in environment.items():
        ClientUtils.LogText(" {0}={1}".format(k, v))
        deadlinePlugin.SetProcessEnvironmentVariable(k, v)