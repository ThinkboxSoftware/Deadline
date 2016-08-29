#!/usr/bin/env bash

# ©2016 Thinkbox Software Inc.

SCRIPT_NAME="ubuntu1604-client-vm-provisioner.sh"
printf "Starting ${SCRIPT_NAME} script.\n\n"


# ======== Variables ========
REPO_MOUNTPOINT=/mnt/repository
REPO_SHARE=/export/repository
REPO_IP_FILENAME=/vagrant/repo_ip.txt
SLAVE_LIC_SERVER=@192.168.2.14


# ======== Update ========
export DEBIAN_FRONTEND=noninteractive
apt-get update

# ======== NFS and Samba Installation ========
apt-get install -y nfs-common cifs-utils

# ======== Mount the Share on the Repo Server ========
REPO_IP=$(<$REPO_IP_FILENAME)
echo Using Repo IP: $REPO_IP

mkdir $REPO_MOUNTPOINT

printf "
${REPO_IP}:${REPO_SHARE} ${REPO_MOUNTPOINT} nfs rsize=8192,wsize=8192,timeo=14,intr
" >> /etc/fstab

mount -a



# ======== Deadline Client ========

cd /tmp

DL_VER=`ls /vagrant/*.tar | grep -o '\([0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}\)'`
DL_VER_MAJOR=`expr match "$DL_VER" '^\([0-9]\{1,3\}\)'`
DL_TARFILENAME=Deadline-$DL_VER-linux-installers.tar
printf "Extracting found tar file: ${DL_TARFILENAME}\n"

tar -xvf /vagrant/$DL_TARFILENAME -C .


# ---- Deadline Client dependencies for Ubunutu Desktop 16.04 ----


# ---- Deadline Client installer ----
mkdir /tmp/thinkboxsetup

tar -zxvf /vagrant/Deadline-$DL_VER-linux-installers.tar -C /tmp/thinkboxsetup 

/tmp/thinkboxsetup/DeadlineClient-*-linux-x64-installer.run \
    --mode unattended \
    --unattendedmodeui minimal \
    --repositorydir $REPO_MOUNTPOINT \
    --licenseserver $SLAVE_LIC_SERVER \
    --slavestartup false

   --noguimode true \
   --restartstalled true    

rm -rf /tmp/thinkboxsetup


# ======== Provisioning Completed ========
printf "\nProvisioning script ${SCRIPT_NAME} completed.\n\n"