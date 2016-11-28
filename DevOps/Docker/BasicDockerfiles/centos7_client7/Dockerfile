FROM centos:7

# 1. Use your own e-mail for the maintainer.
MAINTAINER yourname@yourcompany.com

# Perform a general update of the OS.
RUN yum -y upgrade

# Add requirements for Deadline 7 headless Slave.
RUN yum -y install redhat-lsb \ 
 && yum -y install libX11 \
 && yum -y install libXext \
 && yum -y install mesa-libGL  

# Copy over the installer.
# 2. Be sure the installer .run file has been placed in the same folder as the Dockerfile.
RUN mkdir /tmp/thinkboxsetup/
COPY DeadlineClient-7.*-linux-x64-installer.run /tmp/thinkboxsetup/

# Run the installer.
# 3. Replace the name of the license server after --licenseserver below with that of your actual license server.
RUN /tmp/thinkboxsetup/DeadlineClient-7.*-linux-x64-installer.run \
    --mode unattended \
    --unattendedmodeui minimal \ 
    --repositorydir /mnt/DeadlineRepository7 \ 
    --licenseserver @lic-thinkbox \ 
    --noguimode true \ 
    --restartstalled true 

WORKDIR /opt/Thinkbox/Deadline7/bin/

