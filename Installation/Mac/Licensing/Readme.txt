This is a handy plist for the Darwin/OS X Launch Daemon. It should start lmgrd
for you on reboot and keep it alive if it dies.



Install:
=====================
Installation is straightforward, but there are a few steps.

First, make a user and group named 'deadline'. If you have one for rendering
already, feel free to use it, but you'll need to edit the plist to reflect
those differences.

Next, create a folder for the licensing binaries. We expect it to be
"/usr/local/Thinkbox/lmgrd". Create folders as necessary with 
`mkdir -p /usr/local/Thinkbox/lmgrd` in a Terminal window.

Now that that's done, copy all of the licensing binaries from either the
download section of the website, or from the Repository. You'll need to put
them into a local folder or the Repository into "/usr/local/Thinkbox/lmgrd",
and set the ownership of the contents to belong to the 'thinkbox' user and
group.

Now, copy the "com.thinkbox.license.plist" file into "/Library/LaunchDaemons"
and install it with the following command, again in a Terminal window:
`launchctl load -w /Library/LaunchDaemons/com.thinkbox.license.plist`

And that should be it for installing! If something went awry running it, lmgrd
should have helpful output in "/usr/local/Thinkbox/lmgrd/Thinkbox.log". Keep
reading for important infos.

Summary as a script: (one day we'll include it with the license download)
mkdir -p /usr/local/Thinkbox/lmgrd
cd /usr/local/Thinkbox/lmgrd/
cp $license_bin_dir .
chown -R deadline:deadline .
cp com.thinkbox.license.plist /Library/LaunchDaemons/com.thinkbox.license.plist
launchctl load -w /Library/LaunchDaemons/com.thinkbox.license.plist



Assumptions:
=====================
We're making the following assumptions with this setup:
	1) There is a user named 'deadline' on the system
	2) There's also a group named 'deadline'
	3) The license tools were copied to /usr/local/Thinkbox/lmgrd/
	4) Everything in there is readable/writable by the thinkbox:thinkbox peeps
	5) Your license file is in the folder and is named 'Thinkbox_license.lic'
	
Now, if anything there isn't true, feel free to edit the plist to reflect
reality. Support is going to assume the above are true though.



Usage:
=====================
Unloading the license service (stop it from running):
launchctl unload Library/LaunchAgents/com.thinkbox.license.plist

Re-load it:
launchctl load Library/LaunchAgents/com.thinkbox.license.plist



Help:
=====================
If you hit any snags using this, as usual, e-mail support@thinkboxsoftware.com