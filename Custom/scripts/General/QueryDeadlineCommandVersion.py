"""
QueryDeadlineCommandVersion.py - Example of how to query via .NET the DeadlineCommand.exe assembly file version (works on Windows OS only)
Copyright Thinkbox Software 2016
"""

from System.IO import *
from System.Diagnostics import *

from Deadline.Scripting import *

def __main__():
	if( SystemUtils.IsRunningOnWindows ):
		DeadlineCommandExe = Path.Combine( ClientUtils.GetBinDirectory(), "deadlinecommand.exe" )
		DeadlineCommandExeInfo = FileVersionInfo.GetVersionInfo( DeadlineCommandExe )
		version = DeadlineCommandExeInfo.FileVersion
		print version