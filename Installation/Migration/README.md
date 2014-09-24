DeadlineV5Migration.py - Easily Migrate Deadline v5 -> v6 (only)

![Screenshot of the script](/ThinkboxSoftware/Deadline/tree/master/Installation/Migration/Screenshot.png?raw=true)

DISCLAIMER: This script has the ability to wipe all your Deadline v6 settings for slaves, limits, pools, groups, users. It doesn't migrate any of the main repo options, as these can easily be modified once in the "Configure Repository Options". So much has changed between versions 5 and 6 that it would be inappropriate to try and automatically migrate these settings. It is recommended that this script has its security permissions limited to only experienced Deadline / IT staff.


Batch migrate en mass all Deadline v5 users/slaves/pools/groups/limits to a Deadline v6 DB

For Sys Admins / IT only. Be careful as existing v6 settings can be overwritten!

INSTALL Instructions
Copy the python script into Deadline v6 repository path "../scripts/General", execute the script by clicking in Monitor > scripts > "DeadlineV5Migration".

Note: Deadline v7.0 will have an "import settings" wizard, so future migrations will be supported natively within Deadline itself.
