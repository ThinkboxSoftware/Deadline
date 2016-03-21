
# 1. Find the name of the TAP service with a PowerShell prompt using:
# get-wmiobject win32_networkadapter -filter "netconnectionstatus = 2"
# 2. Set the $TAP_SERVICE_NAME variable to the exact service name.
# 3. Set the $DLCMD_PATH variable to point to the deadlinecommand executable.
#
# Note:  You may have to enable PowerShell script exectution.  See:
# https://technet.microsoft.com/en-us/library/ee176961.aspx


$TAP_SERVICE_NAME="tap0901"
$DLCMD_PATH="'C:\\Program Files\\Thinkbox\\Deadline8\\bin\\deadlinecommand.exe'"

$TAP_IP=(get-WmiObject Win32_NetworkAdapterConfiguration|Where {$_.ServiceName -eq $TAP_SERVICE_NAME} | 
  select ipaddress).ipaddress[0]
Write-Host Found TAP IP:  $TAP_IP

$COMMANDSTR="$DLCMD_PATH SetSlaveSetting $env:computername HostMachineIPAddressOverride $TAP_IP"
Write-Host Running: $COMMANDSTR
Invoke-Expression "& $COMMANDSTR"
