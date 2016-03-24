# Dockerizing Deadline #

In this section we provide basic Dockerfiles to promote the understanding of running Deadline components in
Docker containers. These examples are written for local experimentation using Docker Toolbox rather than for
production deployment.

## Prerequisites ###
These examples assume you have [Docker Toolbox](https://www.docker.com/products/docker-toolbox) installed, which 
includes [Virtual Box](https://www.virtualbox.org/).  These examples assume you also have 
[a basic understanding of using Docker and the Docker Quickstart Terminal](https://docs.docker.com/windows/).

In a Docker Toolbox installation, the default Docker host VM is auto-configured to mount ether ```/Users``` (on OSX) or 
```C:\Users``` (on Windows).  In these examples, we take advantage of this by installing the Deadline7 repository 
somewhere under the ```C:\Users``` folder (e.g. C:\Users\James\DeadlineRepository7).  This way containers can access the 
repository using Docker volume commands.

In a production environment, it would be necessary to install samba or NFS client software onto the container images and 
configure the container to mount an actual repository file server via fstab.

## Other Considerations ##

The examples in this section do not use an init system to manage processes within the container.  If you are deploying 
containers into a production environment, there are 
[reasons why](https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/) you may wish to add 
an init system to your containers.  Here are some links you may find useful:

* The [CentOS page on DockerHub](https://hub.docker.com/_/centos/) discusses systemd integration.
* If you're using Ubuntu, you might consider [the Phusion basimge for Ubunutu](http://phusion.github.io/baseimage-docker/).
* And there are other alternatives, such as [dumb-init](https://github.com/Yelp/dumb-init).

## More Info ##

Questions or comments about these examples?  Visit our support forum at http://forums.thinkboxsoftware.com and post your 
comment or question.

As with all of our examples, we encourage corrections and suggestions for improvements. Feel free to issue a 
[Pull Request](https://help.github.com/articles/using-pull-requests/)!

