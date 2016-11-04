# Init System #

The [basic Dockerfile examples](../BasicDockerfiles) do not use an init system to manage processes within the 
container.  If you are deploying containers into a production environment, there are 
[reasons why](https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/) you may wish to add 
an init system to your containers.  Here are some links you may find useful:

* The [CentOS page on DockerHub](https://hub.docker.com/_/centos/) discusses systemd integration.
* If you're using Ubuntu, you might consider the 
[Phusion baseimage for Ubuntu](http://phusion.github.io/baseimage-docker/).
* And there are other alternatives, such as [dumb-init](https://github.com/Yelp/dumb-init).

![End](../../../thinkbox_tiny.png)
