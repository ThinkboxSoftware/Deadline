"""
SlaveIPMI.py
Remotely execute IPMI command to machine(s) in Deadline via Pulse Server
(Pulse may be the only machine residing on the Mgmt VLAN with access to IPMI)

Example Syntax:
"C:/Program Files/Thinkbox/Deadline7/bin/DeadlineCommand.exe" -ExecuteScript "<repo>/custom/scripts\Pulse\PulseIPMI.py" 10.2.1.3 reset
"""
from System.IO import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

########################################################################
## Globals
########################################################################
scriptDialog = None
settings = None
deadlineExec = "C:/Program Files/Thinkbox/Deadline7/bin/DeadlineCommand.exe"

########################################################################
## Main Function
########################################################################
def __main__ ():
	global scriptDialog
	global settings

	scriptDialog = DeadlineScriptDialog()
	scriptDialog.AllowResizingDialog( False )
	scriptDialog.SetTitle( "IPMI - Remote Command" )

	# Check at least 1 Pulse machine has been defined in Deadline
	pulseNames = RepositoryUtils.GetPulseNames( True )
	
	if len( pulseNames ) == 0:
		scriptDialog.ShowMessageBox( "At least 1 Pulse server must exist in Deadline for this script to function correctly!", "Error" )
		return

	pulseNames = list( pulseNames )

	scriptDialog.AddGrid()
	scriptDialog.AddControlToGrid( "IPMILabel0", "LabelControl", "Select valid Pulse to execute IPMI command via:", 0, 0, "Select which Pulse to execute IPMI command.", False )
	PulseSelected = scriptDialog.AddComboControlToGrid( "PulseName", "ComboControl", "", pulseNames, 0, 1, "List of Pulse Servers registered in Deadline.", False )
	PulseSelected.ValueModified.connect( PulseSelectionChanged )

	scriptDialog.AddControlToGrid( "IPMILabel1", "LabelControl", "IPMI Command to execute:", 1, 0, "Select which IPMI command to execute.", False )
	CommandSelected = scriptDialog.AddComboControlToGrid( "Command", "ComboControl", "power on", ("power on","soft power off","power off","power reset"), 1, 1, "List of IPMI Commands.", False )
	CommandSelected.ValueModified.connect( CommandSelectionChanged )
	scriptDialog.EndGrid()

	scriptDialog.AddGrid()
	scriptDialog.AddHorizontalSpacerToGrid( "DummyLabel0", 0, 0 )
	executeButton = scriptDialog.AddControlToGrid( "ExecuteButton", "ButtonControl", "Execute", 0, 1, expand=False )
	executeButton.ValueModified.connect( ExecuteButtonPressed )
	closeButton = scriptDialog.AddControlToGrid( "CloseButton", "ButtonControl", "Close", 0, 2, expand=False )
	closeButton.ValueModified.connect( CloseButtonPressed )
	scriptDialog.EndGrid()

	settings = ( "PulseName", "Command" )

	scriptDialog.LoadSettings( GetSettingsFilename(), settings )
	scriptDialog.EnabledStickySaving( settings, GetSettingsFilename() )

	scriptDialog.Shown.connect( InitializeDialog )

	scriptDialog.ShowDialog( True )

########################################################################
## Helper Functions
########################################################################
def GetSettingsFilename():
	return Path.Combine( ClientUtils.GetUsersSettingsDirectory(), "IPMIRemoteCommandSettings.ini" )

def InitializeDialog( *args ):
	global scriptDialog

	PulseSelectionChanged( None )
	CommandSelectionChanged( None )

def PulseSelectionChanged( *args ):
	global scriptDialog
	global pulse

	pulse = scriptDialog.GetValue( "PulseName" )

def CommandSelectionChanged( *args ):
	global scriptDialog
	global IpmiCommand

	command = scriptDialog.GetValue( "Command" )

	if command == "power on":
		IpmiCommand = "on"
	elif command == "soft power off":
		IpmiCommand = "soft"
	elif IpmiCommand == "power off":
		IpmiCommand = "off"
	else:
		IpmiCommand = "reset"

def CloseDialog():
	global scriptDialog
	global settings

	scriptDialog.SaveSettings( GetSettingsFilename(), settings )
	scriptDialog.CloseDialog()

def CloseButtonPressed( *args ):
	CloseDialog()

def GetSupportedMachines():
	ipmiFilename = Path.Combine( RepositoryUtils.GetRootDirectory(), "custom/scripts/Slaves/SupportedMachines.ini" )
	ipmiFilename = PathUtils.ToPlatformIndependentPath(ipmiFilename)
	return File.ReadAllLines( ipmiFilename )

def isIPMIsupported( slave ):
	supportedMachines = GetSupportedMachines()
	for machineName in supportedMachines:
		if slave.lower() == machineName.lower():
			return True
	return False

def ExecuteButtonPressed( *args ):
	global scriptDialog

	# Check Pulse has been selected!
	if( scriptDialog.GetValue( "PulseName" ) == "" ):
		scriptDialog.ShowMessageBox( "Make sure you select a Pulse Machine!", "Error" )
		return

	# Double-check the number of machines to execute the remote IPMI command ON!
	slaves = MonitorUtils.GetSelectedSlaveNames()
	if len( slaves ) > 1:
		MessageString = "Execute remote IPMI command on %s machines, Are you sure?" % str( len( slaves ) )
		result = scriptDialog.ShowMessageBox( MessageString, "Warning", ( "Yes", "No" ) )
		if( result == "No" ):
			return

	# loop slaves calling IPMI command
	FailedSlaves = []
	for slave in slaves:
		if isIPMIsupported( slave ):
			machineIP = SlaveUtils.GetMachineIPAddresses([RepositoryUtils.GetSlaveInfo(slave, False)])
			machineIP = machineIP[0]
			IPMIreset( machineIP )
		else:
			FailedSlaves.append( slave )

	if len( FailedSlaves ) > 0:
		failedSlavesStr = ", ".join(FailedSlaves)
		scriptDialog.ShowMessageBox( "The following slaves\n\n" + failedSlavesStr + "\n\nare not declared as having IPMI support.\n\nYou can add support to " + Path.Combine( RepositoryUtils.GetRootDirectory(), "custom/scripts/Slaves/SupportedMachines.ini" ) + " to prevent this message from appearing.", "Error" )

	# exit gracefully
	CloseDialog()

def IPMIreset( ipaddress ):
	global scriptDialog
	global pulse
	global IpmiCommand

	ipmiScript = ( Path.Combine( RepositoryUtils.GetRootDirectory(), "custom/scripts/Pulse/PulseIPMI.py" ) )
	ipmiScript = PathUtils.ToPlatformIndependentPath(ipmiScript)
	CliCommand = "-ExecuteScript"
	args = "\"" + deadlineExec + "\" " + CliCommand + " \"" + ipmiScript + "\" " + ipaddress + " " + IpmiCommand
	#scriptDialog.ShowMessageBox( "Pulse: %s\nScript: %s" % ( pulse, args ), "info" ) #debug
	SlaveUtils.SendRemoteCommand( pulse, args )
