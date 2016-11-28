# Repository Server Basic Examples #

These examples use Vagrant to automatically provision example virtual machines in VirtualBox. The virtual machines will
include a repository that is shared through either SMB or NFS or both, and will also include a running instance of 
MongoDB.

## Requirements ##

To use these examples, you will need the following:

* [HashiCorp Vagrant](https://www.vagrantup.com/downloads.html)
* [Oracle VirtualBox](https://www.virtualbox.org/)
* [Oracle VirtualBox Extension Pack](https://www.virtualbox.org/)
* Deadline installer tar file.

## Usage ##

Note:  These are general instructions for the examples in this section. There may be additional notes in README.md files 
in the subfolders for specific Deadline or OS versions.

1. Place the Deadline installer tar file (e.g., ```Deadline-8.0.11.2-linux-installers.tar``` ) in the folder that 
contains the file named ```Vagrantfile```.  This folder will be shared through to the VM, and this is how the 
provisioning script will locate the installer.

2. Open a command prompt and navigate to the folder containing the ```Vagrantfile```.

3. Provision the virtual machine using the command ```vagrant up```

The first time the virtual machine is provisioned, Vagrant will need to download the 
[base box](https://www.vagrantup.com/docs/boxes.html) from Vagrant Atlas.  This may take some time depending on the 
speed of your internet connection.

Virtual machines created by Vagrant should always be started by navigating to the folder containing the 
```Vagrantfile``` and then using the ```vagrant up``` command.

Virtual machines created by Vagrant, and properly started using the vagrant up command, can be accessed via SSH by
navigating to the folder containing the ```Vagrantfile``` and using the ```vagrant ssh``` command.

![End](../../../thinkbox_tiny.png)