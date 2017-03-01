What everyone's been waiting for, a way to limit users from hogging the farm.

The idea is that you can prevent everyone but blessed users from specific
user groups from submitting jobs higher than a certain priority.

Copy this whole folder into '[repo]/custom/events', reload the scripts in your
Monitor under the 'tools' menu, and go into 'Configure Plugins' to set up what
user group you'd like to bless with allowing submissions higher than the
maximum (also settable).

You'll want to map them like so:
group<priority

For example, for regular users, you can prevent them from submitting jobs higher
than 50 with the following line:
everyone<50

For those unfamiliar with user groups, check out the 7.0 documentation on the
subject:
http://docs.thinkboxsoftware.com/products/deadline/7.0/1_User%20Manual/manual/user-management.html#managing-user-groups

If there are problems or if you'd like us to change something e-mail
the support team at support@thinkboxsoftware.com
