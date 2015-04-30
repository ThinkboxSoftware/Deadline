#!/bin/sh

# Edwin (me!) wrote this quick script for offsetting a given address for IPMI
# purposes. Hopefully you can find this useful for your power management goods.
# It's also IPv4 only. Because hex math is a pain.

# Configuration stuff:
address=$1
offset1=0
offset2=0
offset3=0
offset4=-10

# Data masseuse
octet1=`echo $1 | cut -d '.' -f 1`
octet2=`echo $1 | cut -d '.' -f 2`
octet3=`echo $1 | cut -d '.' -f 3`
octet4=`echo $1 | cut -d '.' -f 4`

octet1=$(($octet1 + $offset1))
octet2=$(($octet2 + $offset2))
octet3=$(($octet3 + $offset3))
octet4=$(($octet4 + $offset4))

# Create new address
addr="$octet1.$octet2.$octet3.$octet4"

echo "Modified $1 to $addr for IPMI"
echo
echo "Waking machine $addr"
echo "...Your IPMI command goes here"