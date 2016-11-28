# Basic Dockerfiles #

**IMPORTANT**:  If you have not already done so, please be sure to [read the overview here](../README.md).

This brief guide will describe a general approach to using the basic ```Dockerfile``` examples found in this folder.

## Building the Container Image ##

### Pre-Build Steps ###

1. **Install a test Deadline Repository under your User folder.**  More information about this is provided in the 
Running Containers section below. 

2. **Place the Deadline installer run file next to the Dockerfile.** You should have received a download link for the 
Deadline Linux installers from Thinkbox Sales (e.g. ```Deadline-8.0.11.2-linux-installers.tar```).  Extract from this 
file the Linux installer .run file (e.g. ```DeadlineClient-8.0.11.2-linux-x64-installer.run```) and place it in the 
same folder as the Dockerfile.

3. **Customize the Dockerfile.**  Within each Dockerfile are numbered comments that suggest parts of the Dockerfile 
that should be customized before building the container image.  Make the necessary edits to the Dockerfile for your 
needs.

### Build the Image ###

When building an image, a tag (or name) for the image should be specified.  In this documentation, the following  
convention is used for for image names, but you may use any convention that suits your needs:

[*NameOfOSandVersion*]/deadline_client:[*MajorVersion.MinorVersion*]

Using this convention, to build the example Dockerfile in the ```centos7_client8``` folder (CentOS 7 with Deadline 8), 
here's an example build command:

    docker build -t centos7/deadline_client:8.0 .


## Running Containers ##

Deadline client programs like Slave, Pulse, and so forth require access to the MongoDB database and to the Repository 
file structure.  

For the database, as long as the container has access to the IP address and port of the database, nothing further is 
required.  In most cases, containers have the same access to IPs as the Docker host on which they are running, so 
nothing special is needed beyond specifying the correct IP (or hostname) and port when configuring Deadline.

For the Repository file structure, some additional steps are needed.  While it is possible to install NFS or SMB 
clients into the container, it can be tricky.  The more common approach is to mount the Repository share on the Docker 
host (such as your workstation, laptop, are a dedicated server), and then make that share accessible to a container by 
using the Docker ```-v``` volume option.  In order to keep the basic Dockerfile examples concise, they assume that the 
volume command is being used to make the Repository file structure visible to the container.  However, this approach 
comes with some caveats.      

For Docker running on Linux, if the Repository exists in a local folder on the host, or has been mounted as a 
network share on the host, then the Docker volume command should allow a container to mount that same folder.

However, when Docker is running on Windows or OSX via Docker Toolbox, the Docker host is a VirtualBox VM.  Docker 
configures this host VM to auto-mount ```C:\Users``` (Windows) or ```/Users``` (OSX) as ```/c/Users``` on the Docker 
host VM.  This means that the test Repository will need to be installed beneath ```C:\Users``` or ```/Users``` to be 
made visible to containers via the Docker volume command.  As a result, it is recommend to install the test Repository 
in your home folder, for example, into ```C:\Users\James\DeadlineRepository8```.


### Interactive Session ###

When testing out a new container image, it's often useful to interactively run a container based on the image and make 
sure it behaves as expected by manually executing commands and observing the result.  Assuming the example Dockerfile 
in the ```centos7_client8``` folder was built and tagged as ```centos7/deadline_client:8.0```, here is a sample command 
to run an interactive session:

    docker run -ti --rm --name InteractiveTest -h interactivetest \
    -v /c/Users/James/DeadlineRepository8:/mnt/DeadlineRepository8 \
    --entrypoint /bin/bash centos7/deadline_client:8.0


Here is a brief explanation of the options that are being passed to the ```docker run``` command:

```-ti``` is shorthand for ```-t -i``` meaning "terminal mode" and "interactive" respectively.

```--rm``` causes the container to be removed when it exits.  If you wish to examine the contents of a container after 
 it has exited, then omit this option.

```--name InteractiveTest``` names the running container "InteractiveTest" for easy reference in other Docker commands. 

```-h interactivetest``` causes the hostname of the running container to be "interactivetest".

```-v /c/Users/James/DeadlineRepository8:/mnt/DeadlineRepository8``` causes the folder  ```/mnt/DeadlineRepository8``` 
in the container to mount ```/c/Users/James/DeadlineRepository8``` on the Docker host.  Don't forget to switch to your 
own username after the third slash.

```--entrypoint /bin/bash``` causes bash to be run as the terminal program when the container starts.  Depending on the 
OS referenced in the base image of the container, you may need to use ```--entrypoint /bin/sh``` instead.

The last parameter, ```centos7/deadline_client:8.0``` is simply the image on which the container will be based.


The container should start up almost instantly.  And once you are at the prompt, you could, for example, run 
Deadline Slave with the following commands:

    cd /opt/Thinkbox/Deadline8/bin
    ./deadlineslave --nogui


### Launching Client Programs ###

Having tested your container with an interactive session, you are now ready to directly execute a target program when 
the container starts.  The following command will run the Slave executable.  Be sure to alter the command to point to 
the path to the repository folder, which should be visible to the Docker host.

    docker run --rm --name dockerslave01 -h dockerslave01 \
    -v /c/Users/James/DeadlineRepository8:/mnt/DeadlineRepository8 \
    --entrypoint /opt/Thinkbox/Deadline8/bin/deadlinelauncher \
    centos7/deadline_client:8.0

First, note the absence of the ``-ti`` option, since this is not an interactive terminal mode session.

```--rm``` causes the container to be removed when it exits.  If you wish to examine the contents of a container after 
 it has exited, then omit this option.

```--name dockerslave01``` names the running container "dockerslave01" for easy identification.

```-h dockerslave01``` causes the hostname of the running container to be dockerslave01.  This affects how the 
containerized Slave will appear in Deadline Monitor. 

```deadline_client/centos7:8.0``` is the name of the image on which the running container will be based.

```--entrypoint /opt/Thinkbox/Deadline8/bin/deadlinelauncher``` is the name of the executable to be run when the 
container starts.  This will cause Deadline Launcher to start which will then launch other client programs as specified 
in the deadline.ini file. The installer parameters in the Dockerfile examples are such that 
```LaunchSlaveAtStartup=true``` is set in the deadline.ini file, causing the Launcher to automatically start 
Deadline Slave.

```centos7/deadline_client:8.0``` is the name of the image on which the container is based.


In general, ```deadlinelauncher``` should be the entrypoint, and the client application (Slave, Balancer, Web Service, 
etc.) to be started should be specified by the deadline.ini file.  See the 
[Client Configuration](http://docs.thinkboxsoftware.com/products/deadline/8.0/1_User%20Manual/manual/client-config.html) 
page in the Deadline User Manual and also 
[this Deadline Feature Blog article](http://deadline.thinkboxsoftware.com/feature-blog/2016/10/28/redundancy-plans-are-redundant) 
for more information.

#### Detached ####

The example ```docker run``` command above runs the container in 
[foreground](https://docs.docker.com/engine/reference/run/#foreground) mode which attaches the standard input, output, 
and standard error of the root process in the container to the terminal from which it was launched.  This is good for 
testing since the output can be directly inspected.  However, in practice it may be desireable to start the container 
in [detached](https://docs.docker.com/engine/reference/run/#/detached--d) mode so that the terminal can be used for 
other things.  To run the container detached, supply the ```-d``` option and *do not* supply the ```--rm``` option:

    docker run -d --name dockerslave01 -h dockerslave01 \
    -v /c/Users/James/DeadlineRepository8:/mnt/DeadlineRepository8 \
    --entrypoint /opt/Thinkbox/Deadline8/bin/deadlinelauncher \
    centos7/deadline_client:8.0


### Licensing ###

It may be the case that the license server is hosted on a different network than that of the Docker host on which a 
given container is running.  Rather than adding complex routing rules to your network it is easier and better practice 
to simply tell the container where to find the license server.  This is can be done with the 

    --add-host lic-thinkbox:192.168.4.28 \

Where ```lic-thinkbox``` is the name of the license server as supplied to the Deadline installer inside the Dockerfile, 
and ```192.168.4.28``` would be replaced with the actual IP address of the license server.  The full example run 
command would then be:

    docker run --rm --name dockerslave01 -h dockerslave01 \
    -v /c/Users/James/DeadlineRepository8:/mnt/DeadlineRepository8 \
    --add-host lic-thinkbox:192.168.4.28 \
    --entrypoint /opt/Thinkbox/Deadline8/bin/deadlinelauncher \
    centos7/deadline_client:8.0


## Next Steps ##

With an understanding of the basics of how to run Deadline client programs in containers, a good next step is to review 
the [Advanced Examples](../AdvancedExamples/README.md).

![End](../../../thinkbox_tiny.png)