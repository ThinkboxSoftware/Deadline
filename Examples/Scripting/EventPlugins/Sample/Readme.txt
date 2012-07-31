Behold! A sample event plugin!

This is for those like me who are too lazy to read documentation :D
(that's here by the way: http://www.thinkboxsoftware.com/deadline-5-scripteventssdk/)

If you have problems, send an e-mail to support@thinkboxsoftware.com
or go over to the forums. Lots of helpful folks over there.

- Edwin


Notes:
=====================================
You'll notice everything has the same name. The main folder, and the files
inside it, etc. That's required. One day we might change that, but for now,
that's how she be. It'd certainly be easier to create these things...

Copy the 'Sample' folder with contents to the 'events' folder in the root of
the repository and start coding, then replace every instance of the word
"Sample" with something else. That goes for file names, as well as anything
you find in the files themselves. I have no idea what Slave will do if it
loads two plugins with the same name, so make sure that doens't happen. It
could rip a hole in space time or something.

This event plugin is run through the IronPython engine. For boring old CPython,
you'll need to make some changes. Once I know what those changes are, and
remember to look at this file again, I'll let you know. If you know, feel free
to edit this.