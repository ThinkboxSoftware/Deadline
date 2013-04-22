#!/bin/bash

# This script will attempt to download and install everything you could possibly need to
# run mono 2.10.9 for CentOS, Fedora, and Debian Distributions of Linux.
# A lot will already installed and hence will be skipped over.

SOURCE_URL="http://download.mono-project.com/sources/mono/mono-2.10.9.tar.bz2"
PACKAGES=" gettext bzip2 fontconfig unzip curl automake autoconf gcc bison screen automake autoconf libtool make"
MONO_LOG="mono_output.log"

# This lets us kill the installation process from subshells.
trap "exit 1" TERM
export TOP_PID=$$

# Function to display a loading notification for long running processes.
# $1 - The long running process.
# $2 - Messages to display.
loadingbar()
{

local pid=$1
local msg=$2
local delay=0.25
local spinstr="|/-\\"

echo -ne "${msg}                       \r"

while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
	local temp=${spinstr:0:1}
    echo -ne "${msg} [${temp}]\r"
    local spinstr=${spinstr:1}$temp
	
	sleep $delay
done

echo -ne "${msg} Complete.\r"
echo -ne '\n'
}

set +e # Exit on error.
# Attempt to update all the mono depedencies.
if [ -f /usr/bin/apt-get ]; then
	apt-get update
	apt-get install $PACKAGES
	apt-get install g++	
elif [ -f /usr/bin/yum ]; then
	yum update
	yum install $PACKAGES
	yum install gcc-c++
else
	echo 'Could not located apt-get or yum package managers.'
	echo 'Now exiting installation...'
	exit 1
fi

echo 'Dependencies up-to-date.'

# Download mono.2.10.9, unzip and configure.
# Only download if it doesn't aready exist in the current directory.
if [ ! -f mono-2.10.9.tar ]; then
	echo "Downloading mono.2.10.9 source code..."
	set +e
	
	if ! curl -O $SOURCE_URL; then 
		echo "mono.2.10.9 download failed."
		exit 1
	fi
	
	echo "Unzipping source code..."
	bunzip2 -q mono-2.10.9.tar.bz2 
fi

# Mono Installation.
#------------------------------------------------------
set -e 
( tar xvf mono-2.10.9.tar > /dev/null ) &
loadingbar $! "Extracting source code"
cd mono-2.10.9

echo 'Mono 2.10.9 will now be configured. Output can be found in '$MONO_LOG
set +e

# Configure Mono installation.
( 
if ! ./configure --prefix=/opt/mono-2.10.9 >> ../$MONO_LOG 2>&1; then 
	echo "mono2.10.9 configuration failed." 
	kill -s TERM $TOP_PID; 
fi 
) &
loadingbar $! "Configuring mono.2.10.9"

# Make Mono installation.
( 
if ! make >> ../$MONO_LOG 2>&1; then
	echo "Failed to make mono.2.10.9."
	kill -s TERM $TOP_PID
fi
) &
loadingbar $! "Making mono.2.10.9"

# Install mono installation.
( 
if ! make install >> ..$MONO_LOG 2>&1; then
	echo "Failed to make install mono.2.10.9." 
	kill -s TERM $TOP_PID 
fi
) &
loadingbar $! "Installing mono.2.10.9"
set -e

# Post Installation.
#-------------------------------------------------------
echo 'Performing cleanup and maintenance...'
cd ..

# Remove the mono source code.
rm -rf mono-2.10.9
rm -rf mono-2.10.9.tar

# Add the mono to the user startup scripts and the loader config
echo 'export PATH=/opt/mono-2.10.9/bin:$PATH' > /etc/profile.d/deadline-path.sh
echo "/opt/mono-2.10.9/lib" > /etc/ld.so.conf.d/deadline-mono.conf
echo 'Mono setup complete. Please log out then back in to begin using mono.'