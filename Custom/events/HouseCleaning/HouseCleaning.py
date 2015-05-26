from Deadline.Events import *
from Deadline.Scripting import *


def GetDeadlineEventListener():
    return HouseCleaningEvent()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()


class HouseCleaningEvent (DeadlineEventListener):
    def __init__(self):
        self.OnHouseCleaningCallback += self.OnHouseCleaning
    
    def Cleanup(self):
        del self.OnHouseCleaningCallback

    # Utility function that creates a Deadline Job based on given parameters
    def OnHouseCleaning(self):
        print("Howdy!")
