Behold! A sample event plugin!

This is for those like me who are too lazy to read documentation :D
(that's here by the way: http://www.thinkboxsoftware.com/deadline-6-scripteventssdk/)

If you have problems, send an e-mail to support@thinkboxsoftware.com
or go over to the forums. Lots of helpful folks over there.

The notes are helpful. Read them. Especially if you want to use CPython.

- Edwin


Notes:
=====================================
You'll notice everything has the same name. The main folder, and the files
inside it, etc. That's required. One day we might change that, but for now,
that's how she be.

Copy the 'Sample' folder with contents to 'custom/events' folder in the
root of the repository and start coding, then replace every instance of the
word "Sample" with something else. That goes for file names, as well as
anything you find in the files themselves. I have no idea what Slave will do
if it loads two plugins with the same Python class name, so make sure that
doesn't happen. It could rip a hole in space time or something.
