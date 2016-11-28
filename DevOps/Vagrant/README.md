# Vagrant #

## About Vagrant ##

[HashiCorp's Vagrant](https://www.vagrantup.com) is software that can automatically provision virtual machines to
various [providers](https://www.vagrantup.com/docs/providers/).  If your workstation or laptop has 
[Oracle's VirtualBox](https://www.virtualbox.org/) (the most common choice for Vagrant) or 
[VMWare](http://www.vmware.com/) installed, Vagrant can provision virtual machines locally.

This makes it very easy to generate reproducible virtual machines for testing and development and then tear them down
again when they are not needed.  In many cases this is preferable to installing the software being tested directly on
the workstation or laptop, which can sometimes be difficult to fully and cleanly remove.  This makes Vagrant a
valuable tool for TDs, developers, and administrators.

If you are not already familiar with Vagrant, it is strongly recommended that you work through the 
[Getting Started tutorial on the Vagrant site](https://www.vagrantup.com/docs/getting-started/).  It only takes a short 
time, and it will introduce you to the key concepts of Vagrant.


## Vagrant Quick Tips ##

1. Vagrant is primarily used for development, testing, and learning.  As such, Vagrant virtual machines often have 
minimal or no security and should not be used in production unless specifically built and tested for production use.

2. Virtual machines created by Vagrant should always be started by navigating to the folder containing the 
```Vagrantfile``` and then using the ```vagrant up``` command.  This ensures things such as network configuration and 
folders shared with the host machine (meaning your workstation or laptop) are properly configured.

3. If the virtual machine that is being provisioned uses a [base box](https://www.vagrantup.com/docs/boxes.html) 
that has not been previously downloaded, Vagrant will automatically download the base box and import it.  This step
generally only needs to be done once.  Be aware that base boxes can be large and take a while to download depending on 
the speed of your internet connection.

4. For virtual machines that show a desktop interface, it's possible that the interface will appear before the 
provisioning script has completed.  Be sure to allow the provisioning script to fully complete before interacting with 
the virtual machine.

5. If you no longer need the virtual machine, or wish to re-provision it from scratch for a clean start, use the 
```vagrant destroy``` command.  This will remove the virtual machine but will not remove the base box on which it is
based.  This is a good thing, since it means the base box will not need to be re-downloaded the next time you provision
the virtual machine.

![End](../../thinkbox_tiny.png)