###############################################################
# Imports
###############################################################
from System import *

from Deadline.Events import *
from Deadline.Scripting import *

#########################################################################################
# This is the function called by Deadline to get an instance of the Draft event listener.
#########################################################################################
def GetDeadlineEventListener():
    return OverrideJobNameListener()

def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()

###############################################################
# The event listener class.
###############################################################
class OverrideJobNameListener (DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted
    
    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):
       
        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Started")

        

        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Finished")