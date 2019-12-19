from Deadline.Events import *
from Deadline.Scripting import *

##################################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
##################################################################################
def GetDeadlineEventListener():
    return AutomaticPreviewJobSubmissionListener()

##################################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
##################################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

##################################################################################
## This is the main DeadlineEventListener class for AutomaticPreviewJobSubmission.
## This Event Plugin is intended to resume the first, middle, and last
## tasks of any submitted Job.
## Originally intended for a usecase of submitting a Job as suspended, and
## then queueing up those previously mentioned tasks.
##################################################################################
class AutomaticPreviewJobSubmissionListener (DeadlineEventListener):

    def __init__( self ):
        # Set up the event callbacks here
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup( self ):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted( self, job ):
        self.LogInfo("On Job Submitted Event Plugin: AutomaticPreviewJobSubmission started")

        # Resume first, middle, and last tasks
        tasks = list(RepositoryUtils.GetJobTasks( job, True ).TaskCollectionAllTasks)
        middleIndex = (len(tasks) - 1)/2
        RepositoryUtils.ResumeTasks(job, [tasks[0], tasks[middleIndex], tasks[-1]])

        self.LogInfo("On Job Submitted Event Plugin: AutomaticPreviewJobSubmission finished")
