PROBLEM:
Renderfarms with newer machines that only support IPMI and not WOL. Typically these render machines reside on the same or cross-over VLAN between your workstations. However, IPMI communication is typically reserved to operate over a separate Management VLAN, which more than likely your workstations running Deadline Monitor won't have access to. So, when you want to send a remote shutdown, startup, power reset, etc to one or more IPMI based rendernodes, you are unable to do this from the comfort of the Deadline Monitor, which means your stuffed; just like a turkey at Xmas!

SOLUTION:
If your reading this, then please do check out Deadline 8.1 or later as Thinkbox intend to add this functionality in a future version of Deadline. For the time being, we can work around this issue with a couple of Deadline scripts, which can be customised further by users if required. So, a slave script provides a UI, allowing you to select the Pulse machine to use as the "go-between" or "via point" and the UI also provides a list to choose the particular IPMI command you wish to execute remotely. When the "Execute" button is clicked, the script will send this IPMI remote command to the nominated machine running Pulse and then, this Pulse machine will dispatch the IPMI command for you. You just need to make sure that the machine(s) running Pulse does have access to the mgmt VLAN which IPMI communication travels over.

USAGE:
1. Copy "SlaveIPMI.py" & "SupportedMachines.ini" into ``<repo>/custom/scripts/Slave/``

2. Copy "PulseIPMI.py" into ``<repo>/custom/scripts/Pulse/``

3. Execute Script via: Monitor -> Slave Panel -> "Select one or more Slave(s)" -> Scripts -> SlaveIPMI

4. Choose "Pulse" to recieve the remote command and execute the IPMI command (you may have more than one Pulse running in your Deadline farm)

5. Choose IPMI command to execute on your machines (on, soft off, off, reset). "Execute" or "Close" the script UI.

CONFIGURATION:
1. Configure line: #19 of "SlaveIPMI.py" to the path location of your locally installed: deadlineExec = "C:/Program Files/Thinkbox/Deadline7/bin/DeadlineCommand.exe"

2. Configure "SupportedMachines.ini" contains all your slaveNames which are IPMI capable. One slave name entry per line. Save the file. Useful, if you still have some machines which work fine with WOL.

3. Configure lines: #28-32 of "PulseIPMI.py":

	USERNAME = "root" #type in your IPMI username here
	PASSWORD = "calvin" #type in your IPMI password here
	IPMIExec = "C:/Program Files (x86)/sourceforge/ipmiutil/ipmiutil.exe" #replace with the path to "../ipmitool" depending on your hardware/platform being used
	DataIP = "10.2.1." #enter your 'data vlan' ip range to be 'found' here
	MgmtIP = "10.2.16." #enter your 'mgmt vlan' ip range to be 'swapped' to here

4. The "PulseIPMI.py" script currently supports "ipmitool". However, we leave it to the user to suport other variants of IPMI executables such as "ipmiutil". (Change the syntax on lines: #53, #55, #57, #59 to "ipmiutil" compatiable commands).
