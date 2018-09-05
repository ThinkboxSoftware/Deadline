SlaveAutoconf.py
==================================

This script was written to do a quick audit of V-Ray versions installed for
3DS Max 2014. This is drop-in safe, so you can just copy it over to your
"custom" folder, edit it for the software title you like and restart a
Slave or two. They'll only update the "Extra Info 0" column at startup, so
that restart is necessary.

The text search is very simple. This script will search for a sub-string of
text entered in the whole list of installed applications. When it finds the
first match, it will return that version. That means that putting in "3dsmax"
when you have eight versions installed like I do will return probably version
2008.

This script should be safe on mixed OS farms, but since it uses the Registry
to find the software, it won't work on Linux and OS X.
