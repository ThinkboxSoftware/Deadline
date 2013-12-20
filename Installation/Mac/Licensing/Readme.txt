About:
=====================
This is a handy plist for the Darwin/OS X Launch Daemon. It should start lmgrd
for you on reboot and keep it alive if it dies. You should make sure lmgrd can
run on its own with the right license file first before setting this up.


Install:
=====================
Installation is straightforward, but there are a few steps.

Create a folder for the licensing binaries. We expect it to be
"/usr/local/Thinkbox/flexnet". Create folders as necessary with 
`mkdir -p /usr/local/Thinkbox/flexnet` in a Terminal window or manually from the
finder.

Now that that's done, copy all of the licensing binaries from either the
download section of the website, or from the Deadline Repository if you have
one. You'll need to put them into the local folder
"/usr/local/Thinkbox/flexnet", and set the permissions so that the 'daemon'
user can access it. It's likely good by default.

You'll also need to copy your license file into the 'flexnet' folder and rename
it to 'Thinkbox_license.lic'. You can always edit the plist for this if you
want to change the name or location of the license file.

Now, copy the "com.thinkbox.license.plist" file into "/Library/LaunchDaemons"
and install it with the following command, again in a Terminal window:
`launchctl load -w /Library/LaunchDaemons/com.thinkbox.license.plist`

And that should be it for installing! If something goes wrong running it,
launchd should have written helpful output in 
"/usr/local/Thinkbox/flexnet/Thinkbox.log". Keep reading for important infos.

Summary of steps as a script:
mkdir -p /usr/local/Thinkbox/flexnet
cd /usr/local/Thinkbox/flexnet/
cp $license_bin_dir/* .
chown -R nobody:nogroup . # Make sure you're in the right directory!
chmod -R 755 *            # Ditto for this one
cp com.thinkbox.license.plist /Library/LaunchDaemons/com.thinkbox.license.plist
launchctl load -w /Library/LaunchDaemons/com.thinkbox.license.plist



Assumptions:
=====================
We're making the following assumptions with this setup:
	1) The license tools were copied to /usr/local/Thinkbox/lmgrd/
	2) Everything in there is readable by the 'daemon' and 'nogroup' user&group.
	3) Your license file is in the folder and is named 'Thinkbox_license.lic'
	
Now, if anything there isn't true, feel free to edit the plist to reflect
reality. Our support staff are going to assume that you have things configured
as above.



Usage of launchctl:
=====================
Unloading the license service (stop it from running):
`launchctl unload -w /Library/LaunchDaemons/com.thinkbox.license.plist`

Re-load it:
`launchctl load -w /Library/LaunchDaemons/com.thinkbox.license.plist`



Help:
=====================
The Launch daemon writes errors to /var/log/system.log with a prefix of
"com.apple.launchd[1]". Usually, if you it's not working, make sure that
the license file exists and reflects your machine. Usually it's helpful to try
and run lmgrd first to see that the license file works, and then move on to
this.

If you hit any snags using this, as usual, e-mail support@thinkboxsoftware.com