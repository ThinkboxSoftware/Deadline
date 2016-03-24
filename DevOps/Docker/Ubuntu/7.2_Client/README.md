
**IMPORTANT**:  Before continuing, please be sure to [read the overview here](../../README.md).  


## Example Build Command ##

Note that the Linux installer .run file (e.g. ```DeadlineClient-7.2.3.0-linux-x64-installer.run```) should be placed in
the same folder as the Dockerfile before issuing the build command.  Don't forget to edit the Dockerfile to reflect the 
name of the installer file (and other things like the name of your license server).  

    docker build -t deadline7/ubuntu1404_client:7.2 .

### Explanation ###

 ```-t deadline7/ubuntu1404_client:7.2``` causes the resulting image to be tagged.  Choose a tag that suits 
your environment and naming conventions.  Be aware that the tag used here is used in the following examples, so if you
change the tag, you will need to also change it in the examples.


## Example Run Command for Slave ##

This command will run the Slave executable.  Be sure to alter the command to point to the path to the repository folder,
which should be visible to the Docker host.

    docker run --rm --name dockerslave01 -h dockerslave01 \
    -v /c/Users/James/DeadlineRepository7:/mnt/DeadlineRepository7 \
    deadline7/ubuntu1404_client:7.2 ./deadlineslave -nogui 

### Explanation ###

 ```--rm``` causes the container to be removed when it exits.

 ```--name dockerslave01``` names the running container dockerslave01 for easy identification.

 ```-h dockerslave01``` causes the hostname of the running container to be dockerslave01.  This affects how the 
containerized Slave will appear in Deadline Monitor. 

 ```-v /c/Users/James/DeadlineRepository7:/mnt/DeadlineRepository7``` causes the folder  ```/mnt/DeadlineRepository7``` 
in the container to mount ```/c/Users/James/DeadlineRepository7``` on the Docker host.  In the case of Docker Toolbox, 
the host is a VirtualBox VM which is auto-configured to mount ```/c/Users``` on the host VM to ```C:\Users``` 
(on Windows) on the physical machine.  By installing the repository folder structure somewhere under ```C:\Users``` on 
the physical host, it can easily be made visible to containers without installing network client libraries (samba or 
NFS) on the container.  In a production scenario, such network client libraries would likely be needed to mount the 
repository on the network file server.

 ```deadline7/ubuntu1404_client:7.2``` is simply the tag of the image that we wish to instantiate as a running container.

 ```./deadlineslave -nogui``` is the name of the executable and options to be run when the container starts.

    
## Example Interactive Session ##

    docker run -ti --rm --name dockerslave01 -h dockerslave01 \
    -v /c/Users/James/DeadlineRepository7:/mnt/DeadlineRepository7 \
    --entrypoint /bin/bash deadline7/ubuntu1404_client:7.2

Once running, you could, for example, run Deadline Slave by switching to the ```/opt/Thinkbox/Deadline7/bin``` folder
and running ```./deadlineslave --nogui```


### Explanation ###

Most of the options are the same as those of the prior example, so only the diffrences will be discussed here.

```-ti``` is shorthand for ```-t -i``` meaning "terminal mode" and "interactive" respectively.

```--entrypoint /bin/bash``` causes bash to be run as the terminal program when the container starts.


## More Info ##

Questions or comments about these examples?  Visit our support forum at http://forums.thinkboxsoftware.com and post your 
comment or question.

As with all of our examples, we encourage corrections and suggestions for improvments. Feel free to issue a 
[Pull Request](https://help.github.com/articles/using-pull-requests/)!

 