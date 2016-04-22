"""
PulseIPMI.py
Deadline Power Management IPMI Pulse Script

Example Syntax:
"../DeadlineCommand.exe" -ExecuteScript "../<repo>/custom/scripts/Pulse/PulseIPMI.py" {SLAVE_IP} {IPMI_COMMAND}

{SLAVE_IP} : variable that Deadline passes through to the PM IPMItool executable
Swap out DataIP: 10.2.1.x with Management VLAN IP: 10.2.16.x

{IPMI_COMMAND} : variable that controls what type of IPMI Command is executed on the machines

Example Syntax:
execute "../install/path/ipmiutil.exe reset -u -N SLAVE_IP -U root -P calvin
"""
import clr
import sys
import time

from System.Diagnostics import *
from System.IO import *

from Deadline.Scripting import *

########################################################################
# Globals
########################################################################
USERNAME = "root"
PASSWORD = "calvin"
IPMIExec = "C:/Program Files (x86)/sourceforge/ipmiutil/ipmiutil.exe"  # replace with "../ipmitool" depending on your hardware being used
DataIP = "10.2.1."
MgmtIP = "10.2.16."

########################################################################
# Main Function
########################################################################


def __main__(*args):

    if len(args) == 2:

        SLAVE_IP = args[0]
        SLAVE_IP = SLAVE_IP.replace(DataIP, MgmtIP)

        IPMI_COMMAND = args[1]  # possible options are: "on", "soft", "off", "reset"

        # Example ipmitool syntax
        # ipmitool -H SLAVE_IP -U USERNAME -P PASSWORD chassis power on
        # ipmitool -H SLAVE_IP -U USERNAME -P PASSWORD chassis power soft
        # ipmitool -H SLAVE_IP -U USERNAME -P PASSWORD chassis power off
        # ipmitool -H SLAVE_IP -U USERNAME -P PASSWORD chassis power reset

        if IPMI_COMMAND == "on":
            args = "-H %s -U %s -P %s chassis power on" % (SLAVE_IP, USERNAME, PASSWORD)
        elif IPMI_COMMAND == "soft":
            args = "-H %s -U %s -P %s chassis power soft" % (SLAVE_IP, USERNAME, PASSWORD)
        elif IPMI_COMMAND == "off":
            args = "-H %s -U %s -P %s chassis power off" % (SLAVE_IP, USERNAME, PASSWORD)
        else:
            args = "-H %s -U %s -P %s chassis power reset" % (SLAVE_IP, USERNAME, PASSWORD)
            # args = "reset -u -N %s -U %s -P %s" % (SLAVE_IP, USERNAME, PASSWORD ) #different syntax if your using "../ipmiutil" instead of "../ipmitool"

        print "arguments: %s" % args

        if File.Exists(IPMIExec):
            process = ProcessUtils.SpawnProcess(IPMIExec, args, None, ProcessWindowStyle.Hidden, True)
            ProcessUtils.WaitForExit(process, -1)  # Wait for IPMI process to exit before continuing

            if process.StandardOutput != None:
                output = process.StandardOutput.ReadToEnd()
                print "%s" % output
            else:
                print "IPMI StdOut could not be obtained"
                return
        else:
            print "Missing IPMI Exec: %s could not be found!" % IPMIExec
            return

        # Slowdown IPMI commands so not too many requests are made through the same chassis backboard at once!
        time.sleep(10)

    else:
        print "Failed to execute PulseIPMI.py script - 2 arguments must be provided!"
