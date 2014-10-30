This is an example of how you can configure Deadline Slave information
programatically from DeadlineCommand. The example here configures the
override IP address for machines having multiple IP addresses. See the
scriting refrence guide for other possible options:
http://docs.thinkboxsoftware.com/

To run this script, just copy this guy somewhere and call it using
DeadlineCommand's ExecuteScript command like so:

C:\Program Files\Thinkbox\Deadline6\bin\DeadlineCommand ExecuteScript OverrideIPs.py

The function to pull SlaveSettings objects will return a perfectly valid
default instance instead of 'None', so be careful to only use names for
Slaves that actually exist.

As usual, if you have questions, problems, or comments, send them over to
support@thinkboxsoftware.com. Feel free to blame Edwin in the subject