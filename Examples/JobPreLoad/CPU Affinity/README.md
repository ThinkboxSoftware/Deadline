CPU Affinity:
======================

This script will ind what the affinity settings are for the Slave and set them up into convenient envrionment variables for the render scripts. The DEADLINE_CPUS_LINUX is for use with the `taskset -c 1,2,3` command while the DEADLINE_CPUS_WINDOWS is meant for hex `start /AFFINITY DEADBEEF` command.

For any application where you might need to use this, just drop the py file into the matching '[repo]/plugins/[app name]' folder.

You will however need to create a matching shell or batch file to handle actually setting affinity for yourself. Two examples:

```
REM Windows example
start /AFFINITY %DEADLINE_CPUS_WINDOWS% "c:\program files\blender\blender.exe" %*
```

```
#!/bin/sh
# Linux example
taskset -c $DEADLINE_CPUS_LINUX /opt/blender/blender
```

If you need help making your own scripts, feel free to e-mail support@thinkboxsoftware.com. Also, hopefully by Deadline 9 the need to manually set affinity won't be needed, and this will be a fun little footnote.

