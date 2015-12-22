###############################################################
# Imports
###############################################################
from Deadline.Events import *
from Deadline.Scripting import *


def GetDeadlineEventListener():
    ''' Return an instance of the event listener '''
    return PluginListener()


def CleanupDeadlineEventListener(eventListener):
    ''' Free items set by Python as they can leak with Python.net '''
    eventListener.Cleanup()


###############################################################
#  The event listener class.
###############################################################
class PluginListener(DeadlineEventListener):
    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted(self, job):
        user = job.JobUserName
        user_groups = list(RepositoryUtils.GetUserGroupsForUser(user))
        verbose = self.GetBooleanConfigEntry('Verbose')
        secondary_pool = self.GetConfigEntry('SecondaryPool')
        default_group = ''

        if verbose:
            print("Found these user groups for {0}: {1}.".format(user, ','.join(user_groups)))

        if job.JobPool not in user_groups:
            if verbose:
                print("Job's pool name does not match any of {0}'s group names.".format(user))
                print("Setting pool to '{0}'.".format(default_group))
            job.JobPool = default_group
        
        if secondary_pool is not '':
            job.JobSecondaryPool = secondary_pool

        RepositoryUtils.SaveJob(job)
