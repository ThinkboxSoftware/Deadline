# NFS and SMB #

This document provides suggestions for accessing NFS and SMB network shares from Docker containers.


## Good Luck With That ##

Installing reliable NFS and/or SMB client services into containers is annoyingly difficult, and appears to *not* be a 
recommended approach.  The more common pattern is to do the following:

1. Install NFS/SMB client services on the Docker host machine,
2. Mount the network share on the Docker host machine, either as part of the startup or just before running a container 
that requires it.
3. Expose the mounted share to a container using the ```-v``` (or ```--volume```) option to the ```docker run``` 
command.

See Also:  The Docker tutorial on how to 
[manage data in containers](https://docs.docker.com/engine/tutorials/dockervolumes/).


## Docker Volume Plugins ##

Docker [volume plugins](https://docs.docker.com/engine/extend/plugins_volume/) allow Docker to be extended so that 
containers can access different external storage systems.  

One such plugin, called [Netshare](http://netshare.containx.io/) allows containers to mount NFS v3/4, AWS EFS or CIFS 
(SMB) shares.  At the time of this article, this plugin has not been tested at Thinkbox Software.


## Contribute Your Knowledge ##

If you would like to share your techniques for accessing NFS, SMB, and other filesystem shares from containers, please 
contribute by issuing a pull request against this document.


