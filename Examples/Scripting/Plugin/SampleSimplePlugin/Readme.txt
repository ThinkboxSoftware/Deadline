Behold! A sample regular plugin! Or, sample simple plugin. Now Deadline 6.x
only!

You might say that this script is similar to the events plugins. You'd
be right. Why mess with a good thing right? So, the big question is what's
the difference? 

Mainly, plugins are the heart of the render process in Deadline. They handle
setting up the environment, getting the arguments just right based on submitted
info, and figure out which render executable to use. Look in other plugins
for great examples. I stole most of this from the Deadline 5.1 TileAssembler!

To start hacking on this, copy the whole thing into the "[repo]\custom\plugins"
folder, then rename files/folders. Basically, rename any files or folders that
are named "SampleSimplePlugin" to what you want it to be referenced by in
Deadline. Be sure to rename everyting to match. Like socks.

The really tricky part for this is submitting a job so that this plugin is
called! I don't have an example of that yet, but you'll need to look into how
the submission process works for now. One day I'll get an example submitter
here too. For now, hyperlink!:  (who calls them that anymore? I'm clearly an OG)
http://www.thinkboxsoftware.com/deadline-5-scriptpluginsdk/

If you have problems, send an e-mail to support@thinkboxsoftware.com
or go over to the forums. Lots of helpful folks over there.

- Edwin
