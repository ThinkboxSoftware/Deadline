#!/usr/bin/env bash

# ©2016 Thinkbox Software Inc.

SCRIPT_NAME="ubuntu1604-repo-vm-provisioner.sh"
printf "Starting ${SCRIPT_NAME} script.\n\n"

# ======== Variables ========
EXPORTPATH=/export
REPOPATH=$EXPORTPATH/repository
REPO_IP_FILENAME=/vagrant/repo_ip.txt


# ======== Update ========
printf "\n127.0.0.1 ${HOSTNAME}\n" >> /etc/hosts

export DEBIAN_FRONTEND=noninteractive
apt-get update 
# apt-get upgrade -y


# ======== NFS installation ========
# See:  https://help.ubuntu.com/community/SettingUpNFSHowTo

HAS_NFS=$(dpkg -l | grep nfs-kernel-server)
echo "HAS_NFS is: ${HAS_NFS}"

if [ "$HAS_NFS" ]; then
	printf "NFS Kernel Server already installed.\n"
else
	printf "Installing NFS Kernel Server...\n"
	apt-get install -y nfs-kernel-server
fi

# Create the reposiotry directory.
if [ -d "$REPOPATH" ]; then
	printf "${REPOPATH} already exists.\n"
else
	mkdir -m 0777 -p $EXPORTPATH
	mkdir -m 0777 $REPOPATH
	chown nobody:nogroup $EXPORTPATH
	chown nobody:nogroup $REPOPATH
fi

# Add line to /etc/exports if needed.
NFS_EXPORTS_STR="${REPOPATH} 192.168.1.0/24(rw,nohide,insecure,no_subtree_check,async)"
echo NFS_EXPORTS_STR: $NFS_EXPORTS_STR
grep -q -F "${NFS_EXPORTS_STR}" /etc/exports || echo $NFS_EXPORTS_STR >> /etc/exports

# Refresh and restart NFS-related services.
printf "Restarting NFS-related services.\n"
exportfs -ra
service portmap restart
service nfs-kernel-server restart

# ======== SMB Installation ========
# See: https://help.ubuntu.com/16.04/serverguide/samba-fileserver.html
apt-get install -y samba

# Add the repository share.
printf "
[repository]
    comment = Ubuntu File Server Share for Deadline Repository
    path = ${REPOPATH}
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755
" >> /etc/samba/smb.conf

# Refresh SMB services (systemd)
printf "Restarting SMB-related services.\n"
sudo systemctl restart smbd.service nmbd.service


# ======== Repository Installation ========
printf "\nInstalling Deadline Database and Repository.\n"
cd /tmp

DL_VER=`ls /vagrant/*.tar | grep -o '\([0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}\)'`
DL_VER_MAJOR=`expr match "$DL_VER" '^\([0-9]\{1,3\}\)'`
DL_TARFILENAME=Deadline-$DL_VER-linux-installers.tar
printf "Extracting found tar file: ${DL_TARFILENAME}\n"

tar -xvf /vagrant/$DL_TARFILENAME -C .

./DeadlineRepository-$DL_VER-linux-x64-installer.run \
  --mode unattended \
  --prefix $REPOPATH \
  --backuprepo false \
  --installmongodb true


# ======== Record Repo IP ========
function int-extractip { /sbin/ifconfig $1 | grep "inet" | awk 'FNR==1 {print $2}' | grep -o '\([0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}\)'; }
REPO_IP=`int-extractip enp0s8`

echo Repo IP: $REPO_IP

if [ -e $REPO_IP_FILENAME ]; then
   rm $REPO_IP_FILENAME
fi

echo $REPO_IP >> $REPO_IP_FILENAME


# ======== Provisioning Completed ========
printf "\nProvisioning script ${SCRIPT_NAME} completed.\n\n"
