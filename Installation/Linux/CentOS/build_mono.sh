#!/bin/sh

# This is a simple build script I use to get Mono 2.10.2 onto CentOS.
# It'll install to /opt/mono so that it's modular and off to the side
# making it easy to delete or uninstall


# Pre-flight stuff
yum install automake libtool autoconf gcc-c++ bison gettext make # Mono deps
yum install glib2-devel libpng-devel libX11-devel fontconfig-devel freetype-devel #libgdiplus deps

# Download and extract mono
curl -L http://ftp.novell.com/pub/mono/sources/mono/mono-2.10.2.tar.bz2 | tar jx
cd mono*

# Build it
./autogen.sh --prefix=/opt/mono
make all
make install

cd ..

# Download and extract libgdi plus
curl -L http://ftp.novell.com/pub/mono/sources/libgdiplus/libgdiplus-2.10.tar.bz2 | tar jx
cd libgdi*

# Build that too
./configure --prefix=/opt/mono
make all
make install

cd ..

# Post-flight goodies
echo 'export PATH=/opt/mono/bin:$PATH' > /etc/profile.d/deadline-path.sh
echo "/opt/mono/lib" > /etc/ld.so.conf.d/deadline-mono.conf
ldconfig

echo "Now you'll need to log out and back in for the PATH changes to take effect"
