'''
DeadlineV5Migration.py - Easily Migrate Deadline v5 -> v6 (only)
Batch migrate en mass all Deadline v5 users/slaves/pools/groups/limits to a Deadline v6 DB
For Sys Admins / IT only. Be careful as existing v6 settings can be overwritten!
Deadline v7 ships with an [IMPORT SETTINGS] WIZARD, so please use this feature for v6 -> v7 migrations in the future.
'''
from System.IO import *
from System.Collections.Specialized import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

import os

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

########################################################################
#  Globals
########################################################################
scriptDialog = None


########################################################################
#  Main Function Called By Deadline
########################################################################
def __main__():
    global scriptDialog

    dialogWidth = 500
    dialogHeight = -1
    buttonWidth = 100
    labelWidth = 300
    controlWidth = 400

    scriptDialog = DeadlineScriptDialog()

    scriptDialog.SetSize(dialogWidth, dialogHeight)
    scriptDialog.SetTitle("Deadline v5 --> v6 Migration Tool")

    scriptDialog.AddRow()
    scriptDialog.AddControl("RepoPathLabel", "LabelControl", "v5 Repository Root Directory", labelWidth - 100, -1, "Select the (rooted - mapped drive letter) v5 Root Directory in your Deadline Repository.")
    scriptDialog.AddSelectionControl("RepoPathBox", "FolderBrowserControl", "", "", controlWidth, -1)
    scriptDialog.EndRow()

    scriptDialog.AddControl("Separator1", "SeparatorControl", "Pools / Groups", labelWidth + controlWidth - 100, -1)

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("PoolsBox", "CheckBoxControl", False, "Migrate Pools", labelWidth, -1)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("GroupsBox", "CheckBoxControl", False, "Migrate Groups", labelWidth, -1)
    scriptDialog.EndRow()

    scriptDialog.AddControl("Separator2", "SeparatorControl", "Slaves", labelWidth + controlWidth - 100, -1)

    scriptDialog.AddRow()
    SlavesBoxButton = scriptDialog.AddSelectionControl("SlavesBox", "CheckBoxControl", False, "Migrate Slaves", labelWidth, -1)
    SlavesBoxButton.ValueModified.connect(SlavesBoxButtonPressed)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("OverwriteExistingSlavesBox", "CheckBoxControl", False, "Force Overwrite of Existing Identical Slaves", labelWidth + 200, -1, "If enabled, any existing v6 slaves with the same name as an imported XML file, will be overwritten!")
    scriptDialog.SetEnabled("OverwriteExistingSlavesBox", False)
    scriptDialog.EndRow()

    scriptDialog.AddControl("Separator3", "SeparatorControl", "Limits", labelWidth + controlWidth - 100, -1)

    scriptDialog.AddRow()
    LimitsBoxButton = scriptDialog.AddSelectionControl("LimitsBox", "CheckBoxControl", False, "Migrate Limits", labelWidth, -1)
    LimitsBoxButton.ValueModified.connect(LimitsBoxButtonPressed)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("OverwriteExistingLimitsBox", "CheckBoxControl", False, "Force Overwrite of Existing Identical Limits", labelWidth + 200, -1, "If enabled, any existing v6 limits with the same name, will be overwritten!")
    scriptDialog.SetEnabled("OverwriteExistingLimitsBox", False)
    scriptDialog.EndRow()

    scriptDialog.AddControl("Separator4", "SeparatorControl", "Users", labelWidth + controlWidth - 100, -1)

    scriptDialog.AddRow()
    UsersBoxButton = scriptDialog.AddSelectionControl("UsersBox", "CheckBoxControl", False, "Migrate Users", labelWidth, -1)
    UsersBoxButton.ValueModified.connect(UsersBoxButtonPressed)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("OverwriteExistingUsersBox", "CheckBoxControl", False, "Force Overwrite of Existing Identical User Names", labelWidth + 200, -1, "If enabled, any existing v6 users with the same name as an imported XML file, will be overwritten!")
    scriptDialog.SetEnabled("OverwriteExistingUsersBox", False)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddSelectionControl("MigrateGroupsBox", "CheckBoxControl", False, "Migrate v5 User Groups (Ensure 'Normal' / 'Power' groups created prior)", labelWidth + 200, -1, "If enabled, Deadline v5 User Groups: Normal & Power will be migrated and applicable users added automatically.")
    scriptDialog.SetEnabled("MigrateGroupsBox", False)
    scriptDialog.EndRow()

    scriptDialog.AddRow()
    scriptDialog.AddControl("DummyLabel1", "LabelControl", "", dialogWidth - (buttonWidth * 2) + 95, -1)
    sendButton = scriptDialog.AddControl("SelectButton", "ButtonControl", "Execute", buttonWidth, -1)
    sendButton.ValueModified.connect(ExecuteMigration)
    closeButton = scriptDialog.AddControl("CloseButton", "ButtonControl", "Close", buttonWidth, -1)
    closeButton.ValueModified.connect(CloseButtonPressed)
    scriptDialog.EndRow()

    scriptDialog.ShowDialog(True)


########################################################################
#  Helper Functions
########################################################################
def InitializeDialog(*args):
    global scriptDialog

    SlavesBoxButtonPressed()
    LimitsBoxButtonPressed()
    UsersBoxButtonPressed()

    
def CloseButtonPressed(*args):
    global scriptDialog
    scriptDialog.CloseDialog()

    
def SlavesBoxButtonPressed(*args):
    global scriptDialog

    checked = scriptDialog.GetValue("SlavesBox")
    if bool(checked):
        scriptDialog.SetEnabled("OverwriteExistingSlavesBox", True)
    else:
        scriptDialog.SetEnabled("OverwriteExistingSlavesBox", False)

        
def LimitsBoxButtonPressed(*args):
    global scriptDialog

    checked = scriptDialog.GetValue("LimitsBox")
    if bool(checked):
        scriptDialog.SetEnabled("OverwriteExistingLimitsBox", True)
    else:
        scriptDialog.SetEnabled("OverwriteExistingLimitsBox", False)

        
def UsersBoxButtonPressed(*args):
    global scriptDialog

    checked = scriptDialog.GetValue("UsersBox")
    if bool(checked):
        scriptDialog.SetEnabled("OverwriteExistingUsersBox", True)
        scriptDialog.SetEnabled("MigrateGroupsBox", True)
    else:
        scriptDialog.SetEnabled("OverwriteExistingUsersBox", False)
        scriptDialog.SetEnabled("MigrateGroupsBox", False)

        
def ExecuteMigration():
    global scriptDialog

    try:

        # Check Repo Path has been specified
        repoPath = scriptDialog.GetValue("RepoPathBox")
        if repoPath == "":
            scriptDialog.ShowMessageBox("No Repository Root Directory specified!", "Error")
            return

        # Check it looks like a v5 Repo Path and if not, return
        poolsFile = (os.path.join(repoPath, "settings", "pools.ini"))
        groupsFile = (os.path.join(repoPath, "settings", "groups.ini"))
        slavesPath = (os.path.join(repoPath, "slaves"))
        usersPath = (os.path.join(repoPath, "users"))
        limitsPath = (os.path.join(repoPath, "limitGroups"))

        if(not File.Exists(poolsFile)):
            scriptDialog.ShowMessageBox("pools.ini File [%s] does not exist!\n\nAre you sure this is a valid Deadline v5 Repository Path?" % poolsFile, "Error")
            return
        
        if(not File.Exists(groupsFile)):
            scriptDialog.ShowMessageBox("groups.ini File [%s] does not exist!\n\nAre you sure this is a valid Deadline v5 Repository Path?" % groupsFile, "Error")
            return

        if(not Directory.Exists(slavesPath)):
            scriptDialog.ShowMessageBox("Slaves Directory [%s] does NOT exist!\n\nAre you sure this is a valid Deadline v5 Repository Path?" % slavesPath, "Error")
            return

        if(not Directory.Exists(usersPath)):
            scriptDialog.ShowMessageBox("Users Directory [%s] does NOT exist!\n\nAre you sure this is a valid Deadline v5 Repository Path?" % usersPath, "Error")
            return

        if(not Directory.Exists(limitsPath)):
            scriptDialog.ShowMessageBox("Limits Directory [%s] does NOT exist!\n\nAre you sure this is a valid Deadline v5 Repository Path?" % limitsPath, "Error")
            return

        # Read INI File
        def ReadINIFile(iniFile):
            if iniFile != "":
                Lines = open(iniFile, "r").read().splitlines()
                return Lines
            else:
                LogWarning("No [*_*.ini] File Found?")
                return ""

        # POOLS
        migratePools = scriptDialog.GetValue("PoolsBox")
        if bool(migratePools):

            pools = []
            paths = ReadINIFile(poolsFile)
            for path in paths:
                key, val = path.split("=")
                pools.append(key)
            
            print("pools: %s" % pools)

            poolAdded = 0
            poolDuplicate = 0

            for pool in pools:
                try:
                    RepositoryUtils.AddPool(pool)
                    poolAdded += 1
                except:
                    poolDuplicate += 1

            scriptDialog.ShowMessageBox("Pools injected into DB: %d\nPools failed to be injected into DB: %d" % (poolAdded, poolDuplicate), "Pool Results")

        # GROUPS
        migrateGroups = scriptDialog.GetValue("GroupsBox")
        if bool(migrateGroups):
            
            groups = []
            paths = ReadINIFile(groupsFile)
            for path in paths:
                key, val = path.split("=")
                groups.append(key)
            
            print("groups: %s" % groups)

            groupAdded = 0
            groupDuplicate = 0

            for group in groups:
                try:
                    RepositoryUtils.AddGroup(group)
                    groupAdded += 1
                except:
                    groupDuplicate += 1
            
            scriptDialog.ShowMessageBox("Groups injected into DB: %d\nGroups failed to be injected into DB: %d" % (groupAdded, groupDuplicate), "Group Results")

        # SLAVES
        migrateSlaves = scriptDialog.GetValue("SlavesBox")
        if bool(migrateSlaves):

            ssFiles = Directory.GetFiles(slavesPath, "*.slaveSettings", SearchOption.AllDirectories)

            args = StringCollection()
            args.Add("-GetSlaveNames")
            ExistingSlaves = (ClientUtils.ExecuteCommandAndGetOutput(args)).split()
            
            slavesAdded = 0
            slavesSkipped = 0

            # Create v6 Slave Object if not already existing for each old v5 slave name
            for ssFile in ssFiles:

                slaveName = (Path.GetFileNameWithoutExtension(ssFile)).lower()

                # Initalise for each Slave XML File
                Description = ""

                if slaveName in ExistingSlaves and (not scriptDialog.GetValue("OverwriteExistingSlavesBox")):
                    slavesSkipped += 1
                else:
                    # Parse Slave Settings XML File
                    tree = xml.ElementTree()
                    tree.parse(ssFile)
                    root = tree.getroot()

                    for child in root.getchildren():
                        if child.tag == 'Description':
                            if child.text is not None:
                                if child.text != "":
                                    Description = str(child.text)
                                else:
                                    Description = "BLANK"

                    args = StringCollection()
                    args.Add("-SetSlaveSetting")
                    args.Add("%s" % slaveName)
                    args.Add("Description %s" % Description)

                    ClientUtils.ExecuteCommand(args)

                    slaveSettings = RepositoryUtils.GetSlaveSettings(slaveName, True)

                    # Initalise for each Slave Settings XML File
                    Comment = ""
                    ConcurrentTasksLimit = 0
                    Enabled = True
                    SlaveIncludeInNoneGroup = True
                    SlaveIncludeInNonePool = True
                    NormalizedRenderTimeMultiplier = 0.0
                    NormalizedTimeoutMultiplier = 0.0
                    OverrideCpuAffinity = False
                    CpuAffinity = []
                    Pools = []
                    Groups = []

                    # Parse Slave Settings XML File
                    tree = xml.ElementTree()
                    tree.parse(ssFile)
                    root = tree.getroot()

                    for child in root.getchildren():
                        if child.tag == 'Comment':
                            if child.text is not None:
                                if child.text != "":
                                    slaveSettings.SlaveComment = str(child.text)
                        if child.tag == 'ConcurrentTasksLimit':
                            if child.text is not None:
                                slaveSettings.SlaveConcurrentTasksLimit = int(child.text)
                        if child.tag == 'Description':
                            if child.text is not None:
                                if child.text != "":
                                    slaveSettings.SlaveDescription = str(child.text)
                        if child.tag == 'Enabled':
                            if child.text is not None:
                                if child.text == "true":
                                    slaveSettings.SlaveEnabled = True
                                else:
                                    slaveSettings.SlaveEnabled = False
                        if child.tag == 'SlaveIncludeInNoneGroup':
                            if child.text is not None:
                                if child.text == "true":
                                    slaveSettings.SlaveIncludeInNoneGroup = True
                                else:
                                    slaveSettings.SlaveIncludeInNoneGroup = False
                        if child.tag == 'SlaveIncludeInNonePool':
                            if child.text is not None:
                                if child.text == "true":
                                    slaveSettings.SlaveIncludeInNonePool = True
                                else:
                                    slaveSettings.SlaveIncludeInNonePool = False
                        if child.tag == 'NormalizedRenderTimeMultiplier':
                            if child.text is not None:
                                slaveSettings.SlaveNormalizedRenderTimeMultiplier = float(child.text)
                        if child.tag == 'NormalizedTimeoutMultiplier':
                            if child.text is not None:
                                slaveSettings.SlaveNormalizedTimeoutMultiplier = float(child.text)
                        
                        if child.tag == 'OverrideCpuAffinity':
                            if child.text is not None:
                                if child.text == "true":
                                    slaveSettings.SlaveOverrideCpuAffinity = True
                                    OverrideCpuAffinity = True
                                else:
                                    slaveSettings.SlaveOverrideCpuAffinity = False
                        if child.tag == 'CpuAffinity':
                            if child.text is not None:
                                if OverrideCpuAffinity:
                                    slaveSettings.SlaveCpuAffinity = child.text

                        if child.tag == 'Pools':
                            for step_child in child:
                                if step_child is not None:
                                    Pools.append(str(step_child.text))
                        if child.tag == 'Groups':
                            for step_child in child:
                                if step_child is not None:
                                    Groups.append(str(step_child.text))

                    # Set Pools for Slave
                    slaveSettings.SetSlavePools(Pools)

                    # Set Groups for Slave
                    slaveSettings.SetSlaveGroups(Groups)

                    # Save all the settings for this slave object
                    RepositoryUtils.SaveSlaveSettings(slaveSettings)

                    slavesAdded += 1

            scriptDialog.ShowMessageBox("Slaves injected into DB: %d\nSlaves skipped: %d\n" % (slavesAdded, slavesSkipped), "Slaves Results")

        # USERS
        migrateUsers = scriptDialog.GetValue("UsersBox")
        if bool(migrateUsers):

            userFiles = Directory.GetFiles(usersPath, "*.xml", SearchOption.TopDirectoryOnly)

            if(len(userFiles) == 0):
                scriptDialog.ShowMessageBox("No User XML file(s) found!", "Error")
                return

            if(scriptDialog.GetValue("MigrateGroupsBox")):
                result = scriptDialog.ShowMessageBox("Have you already created User Groups: 'Normal' and 'Power' in your repository?", "Warning", ("Yes", "No"))
                if(result == "No"):
                    return

            args = StringCollection()
            args.Add("-GetUserNames")
            ExistingUsers = (ClientUtils.ExecuteCommandAndGetOutput(args)).split()

            successes = 0
            failures = 0

            for userFile in userFiles:
                # Initalise for each User XML File
                UserName = ""
                Email = ""
                MachineName = ""
                NotifyByEmail = ""
                NotifyByPopupMessage = ""
                UserLevel = "Normal"

                UserName = (Path.GetFileNameWithoutExtension(userFile)).lower()

                if UserName in ExistingUsers and (not scriptDialog.GetValue("OverwriteExistingUsersBox")):
                    failures += 1
                else:
                    # Parse User XML File
                    tree = xml.ElementTree()
                    tree.parse(userFile)
                    root = tree.getroot()

                    for child in root.getchildren():
                        if child.tag == 'EmailAddress':
                            if child.text is not None:
                                Email = child.text
                        if child.tag == 'MachineName':
                            if child.text is not None:
                                MachineName = child.text
                        if child.tag == 'EmailNotification':
                            if child.text is not None:
                                NotifyByEmail = child.text
                        if child.tag == 'NetsendNotification':
                            if child.text is not None:
                                NotifyByPopupMessage = child.text
                        if child.tag == 'UserLevel':
                            if child.text is not None:
                                UserLevel = child.text

                    args = StringCollection()
                    args.Add("-SetUser")
                    args.Add("%s" % UserName)
                    args.Add("%s" % Email)
                    args.Add("%s" % MachineName)
                    args.Add("%s" % NotifyByEmail)
                    args.Add("%s" % NotifyByPopupMessage)

                    if bool(scriptDialog.GetValue("MigrateGroupsBox")) is True:
                        args.Add("%s" % UserLevel)

                    exitCode = ClientUtils.ExecuteCommand(args)

                    if(exitCode == 0):
                        successes = successes + 1
                    else:
                        failures = failures + 1

            scriptDialog.ShowMessageBox("Users successfully injected into DB: %d\nUsers failed to be injected into DB: %d" % (successes, failures), "User Account Migration Results")

        # LIMITS
        migrateLimits = scriptDialog.GetValue("LimitsBox")
        if bool(migrateLimits):
            
            limitsFiles = Directory.GetFiles(limitsPath, "*.limitGroup", SearchOption.TopDirectoryOnly)

            args = StringCollection()
            args.Add("-GetLimitGroupNames")
            ExistingLimits = (ClientUtils.ExecuteCommandAndGetOutput(args)).split()

            limitsAdded = 0
            limitsSkipped = 0
            limitsFailed = 0

            for limitsFile in limitsFiles:

                # Initalise for each limitGroup XML File
                Name = ""
                Limit = 0
                ReleasePercentage = -1
                IsJobSpecific = True
                ListedSlaves = []
                WhitelistFlag = False
                ExcludedSlaves = []

                # Parse User XML File
                tree = xml.ElementTree()
                tree.parse(limitsFile)
                root = tree.getroot()

                for child in root.getchildren():
                    if child.tag == 'Name':
                        if child.text is not None:
                            Name = child.text
                    if child.tag == 'Limit':
                        if child.text is not None:
                            Limit = child.text
                    if child.tag == 'ReleasePercentage':
                        if child.text is not None:
                            ReleasePercentage = child.text
                    if child.tag == 'IsJobSpecific':
                        if child.text is not None:
                            if child.text == "true":
                                IsJobSpecific = True
                            else:
                                IsJobSpecific = False
                    if child.tag == 'ListedSlaves':
                        if child.text is not None:
                            ListedSlaves = child.text
                    if child.tag == 'WhitelistFlag':
                        if child.text is not None:
                            WhitelistFlag = child.text
                    if child.tag == 'ExcludedSlaves':
                        if child.text is not None:
                            ExcludedSlaves = child.text

                if Name in ExistingLimits and (not scriptDialog.GetValue("OverwriteExistingLimitsBox")):
                    limitsSkipped += 1
                else:
                    if not IsJobSpecific:
                        try:
                            RepositoryUtils.SetLimitGroup(str(Name), int(Limit), ListedSlaves, bool(WhitelistFlag), ExcludedSlaves, float(ReleasePercentage))
                            limitsAdded += 1
                        except:
                            limitsFailed += 1
                    else:
                        limitsSkipped += 1

            scriptDialog.ShowMessageBox("Limits injected into DB: %d\nLimits skipped: %d\nLimits failed to be injected into DB: %d" % (limitsAdded, limitsSkipped, limitsFailed), "Limits Results")

        scriptDialog.ShowMessageBox("v5 -> v6 Migration Completed", "Completed")

    except:
        import traceback
        scriptDialog.ShowMessageBox(str(traceback.format_exc()), "Error")
