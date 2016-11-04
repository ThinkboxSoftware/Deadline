# Reducing the Container Image Size #

It is often desireable to keep container images as small as possible.  This can be somewhat challenging given that the 
union filesystem used by Docker containers is purely additive in nature.  Once one or more files are added to the 
filesystem with the ```COPY``` or ```ADD``` build commands, subsequent commands to remove the file(s) will not reduce 
the container size, even though the file is deleted from the perspective of the container's filesystem.

Using the ubuntu1404_client8 example, we add the installer to the container using

    COPY DeadlineClient-8.*-linux-x64-installer.run /thinkboxsetup/

a subsequent command to remove the installer after it has been run, such as

    RUN rm -rf /thinkboxsetup

will not reduce the size of the built image.  And given that the installer weighs in at nearly 200MB, that is rather 
substantial.

There are a couple of approaches to preventing the installer from adding unnecessary weight to the resulting image.
One approach is to use post-build tools such as [docker-slim](https://github.com/cloudimmunity/docker-slim), 
[docker-squash](https://github.com/jwilder/docker-squash), and others.  These are useful tools worth learning if you 
make heavy use of containers, but they can introduce challenges of their own.

Here is an alternative approach that prevents the installer from remaining with the resulting image.  The approach is
to add the installer, run it, and remove it all in one build step.  The question is, how do we get the installer into
the image without using build commands like ```COPY``` or ```ADD```?  

One way is to place the installer on an internal server such that it can be retrieved with ```wget```.  You may need
to add the ```wget``` program to your image first.

    RUN apt-get update && apt-get -y install wget

    RUN mkdir /thinkboxsetup/ \ 
        && cd /thinkboxsetup \
        && wget http://my.internal.server/deadline7_installer/DeadlineClient-7.2.3.0-linux-x64-installer.run \
        && chmod +x *.run \
        && /thinkboxsetup/DeadlineClient-7.*-linux-x64-installer.run \
            --mode unattended \
            --unattendedmodeui minimal \ 
            --repositorydir /mnt/DeadlineRepository7 \ 
            --licenseserver @lic_thinkbox \ 
            --noguimode true \ 
            --restartstalled true \
       && cd .. \
       && rm -rf /thinkboxsetup

Since the ```/thinkboxsetup``` folder is created, the installer is pulled down, the installer is executed, and the 
folder is removed *all in one build step*, the installer folder and .run file do not become part of the resulting build 
layer, thus preventing the hefty installer file from contributing to the final size of the image.

Note that since HTTP retrieval does not support globbing, it is necessary to specify the exact name of the installer 
file to be pulled down from the server.  ```wget``` provides advanced options to work around the lack of globbing, but 
those options are beyond the scope of this document.  (But 
[here is a handy set of examples](http://www.editcorp.com/personal/lars_appel/wget/v1/wget_7.html#SEC33)).

![End](../../../thinkbox_tiny.png)