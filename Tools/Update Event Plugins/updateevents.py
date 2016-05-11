import sys
import os
import re

# Created by Justin Blagden - May 2016
# No warrenty - make good descisions. Email support@thinkboxsoftware if it
# breaks. Blame Justin in that case.

# This goes through a folder (or all subfolders) and:
# Deletes the unneeded .dlinit file
# Replaces the [Enabled] property with the [State] property


def main(argv):
    # check that we pointed at a folder
    if len(argv) <= 1:
        print("Choose one or more folders to convert. Choose all with *")
        return

    if argv[1] == '*':
        folderList = next(os.walk('.'))[1]
    else:
        folderList = argv[1:]

    for pluginFolder in folderList:
        pluginName = pluginFolder

        # Delete the .dlinit file - we don't need it anymore
        try:
            dlinit = os.path.join(pluginName, pluginName + '.dlinit')
            os.remove(dlinit)
        except WindowsError:
            print("%s doesn't have a dlinit file inside" % pluginName)

        # Update the .params file
        try:
            param = os.path.join(pluginName, pluginName + '.param')
            paramFile = open(param, 'rb+')

            content = paramFile.read()

            find = r"\[Enabled\].*?(\n\s|$)"
            replace = (
                r"[State]\n"
                r"Type=Enum\n"
                r"Items=Global Enabled;Opt-In;Disabled\n"
                r"Label=State\n"
                r"Default=Disabled\n"
                r"Description=How this event plug-in should respond to events."
                r" If Global, all jobs and slaves will trigger the events for this plugin. "
                r"If Opt-In, jobs and slaves can choose to trigger the events for this plugin. "
                r"If Disabled, no events are triggered for this plugin.\n"
            )

            # Do a find-replace to swap out the old with the new
            contentTuple = re.subn(find, replace, content, flags=re.S)

            # Break out the tuple we got back
            content = contentTuple[0]
            foundCount = contentTuple[1]

            # After reading, reset file pointer to top of file and clear the file
            paramFile.seek(0)
            paramFile.truncate()
            paramFile.write(content)
            paramFile.close()

        except IOError:
            print("%s.param not found" % pluginName)
        except:
            print("Error encountered converting %s" % pluginName)
            e = sys.exc_info()[0]
            print("Error: %s" % e)
        else:
            if foundCount >= 1:
                print("%s converted successfully" % pluginName)
            else:
                if foundCount == 0:
                    print(
                        "%s failed to convert - .param file doesn't match Deadline 7 style" %
                        pluginName)
                else:
                    print("%s failed to convert" % pluginName)

        print("")

if __name__ == "__main__":
    main(sys.argv[0:])
