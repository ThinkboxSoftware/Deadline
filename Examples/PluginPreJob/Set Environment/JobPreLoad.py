'''
    JobPreLoad.py - Set environment variables for current plugin
    
    This should work on Deadline 6 and 7's APIs. If there are problems,
    please report them to support@thinkboxsoftware.com
    
    Written by Edwin Amsler <support@thinkboxsoftware.com>
'''
from Deadline.Scripting import *


environment = {
    "a": "b",
    "x": "y",
    "1": "2"
}


def __main__(deadlinePlugin):
    ''' Entry point and good times '''

    ClientUtils.LogText("Adding enviornment variables to Maya job")

    for k, v in environment.items():
        ClientUtils.LogText(" {0}={1}".format(k, v))
        deadlinePlugin.SetProcessEnvironmentVariable(k, v)
