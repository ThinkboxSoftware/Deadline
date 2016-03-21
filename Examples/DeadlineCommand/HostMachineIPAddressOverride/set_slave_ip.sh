#!/usr/bin/env bash

# This script sets the HostMachineIPAddressOverride value in Deadline to the IP address of the tap0 interface.
# This allows remote commands to work over a VPN.
# Run this script on virtual machine startup, after the VPN connection has been established.

function int-ip { /sbin/ifconfig $1 | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}'; }

TAP0IP=`int-ip tap0`
echo Found tap0 IP:  $TAP0IP

echo Running: ./deadlinecommand SetSlaveSetting $HOSTNAME HostMachineIPAddressOverride $TAP0IP 
RESULT=`./deadlinecommand SetSlaveSetting $HOSTNAME HostMachineIPAddressOverride $TAP0IP`

echo $RESULT
