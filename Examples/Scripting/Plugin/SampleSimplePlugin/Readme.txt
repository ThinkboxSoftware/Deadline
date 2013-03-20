Behold! A sample regular plugin! Or, sample simple plugin. For Deadline 5.x only

You might say that this script is similar to the events plugins. You'd
be right. Why mess with a good thing right? So, the big question is what's
the difference? 

Mainly, plugins are the heart of the render process in Deadline. They handle
setting up the environment, getting the arguments just right based on submitted
info, and figure out which render executable to use. Look in other plugins
for great examples. I stole most of this from the TileAssembler!

To start hacking on this, copy the whole thing into the Repository's "plugins"
folder, then rename files/folders. Basically, do a find/replace for the files
and folders and contents named "SampleSimplePlugin" to what you want it to be
called. Be sure to rename everyting to match.

The really tricky part for this is submitting a job so that this plugin is
called! I don't have an example of that yet, but you'll need to look into how
the submission process works for now. One day I'll get an example submitter
here too. For now, hyperlink!:  (who calls them that anymore? I'm clearly an OG)
http://www.thinkboxsoftware.com/deadline-5-scriptpluginsdk/


If you have problems, send an e-mail to support@thinkboxsoftware.com
or go over to the forums. Lots of helpful folks over there.

- Edwin
