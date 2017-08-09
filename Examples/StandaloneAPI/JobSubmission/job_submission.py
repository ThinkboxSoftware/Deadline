from pprint import pprint

import Deadline.DeadlineConnect as Connect
conn = Connect.DeadlineCon('localhost', 8082)

JOB_NAME = 'Ping Localhost'
CMD_APP = r'c:\windows\system32\cmd.exe'
CMD_ARG = r'/c ping localhost'

JobInfo = {
    "Name": JOB_NAME,
    "Frames": "1",
    "Plugin": "CommandLine"
    }

PluginInfo = {
    'Shell': 'default',
    'ShellExecute': False,
    'StartupDirectory': '',
    'Executable': CMD_APP,
    'Arguments': CMD_ARG
    }

try:
    new_job = conn.Jobs.SubmitJob(JobInfo, PluginInfo)
    print("Job created with id {}".format(new_job['_id']))
except:
    print("Submission failed")
