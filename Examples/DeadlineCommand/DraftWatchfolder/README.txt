Before running these batch files and scripts, you will need to review and edit them to match your envronment.
This means setting which folder to watch for new files, where to send the converted files, and what script to use to convert them.

watchfolder.bat will run the watchfolder script via deadlinecommand.exe and display output to an open command prompt. So long as it is run from the same folder as the script you want it to automatically run it should work.

watchfolderheadless.bat will run the watchfolder script via deadlinecommandbg.exe (for runnning in background) and show no output. It currently places all its logs in the default location detailed here: http://docs.thinkboxsoftware.com/products/deadline/7.2/1_User%20Manual/manual/command.html

Note that watchfolderheadless will create a process called Deadline Command BG 7.2 (if you're running Deadline 7.2), just in case you've accidently started more than one instance of the watchfolder. If you find the watchfolder submitting duplicates its probably running more than one instance.