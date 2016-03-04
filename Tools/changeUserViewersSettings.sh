#!/bin/sh
# This bash script will change the current deadline 7 linux viewer settings
# You'll have to change the PATH_TO_RV_LAUNCHER
settingsFile=~/.config/Thinkbox/Deadline\ Monitor\ 7.ini
settingsFileBackup="$settingsFile-$(date +"%F-%Hh%Mm")"
echo "Backup settings file is $settingsFileBackup"
cp "$settingsFile" "$settingsFileBackup"

echo "Before modifications :"
cat "$settingsFile" | grep Viewer

sed -i.bak 's/^CustomViewerArguments1=.*/CustomViewerArguments1=\\\"{SEQ#}\\\"/' "$settingsFile"
sed -i.bak 's/^CustomViewerArguments2=.*/CustomViewerArguments2=\\\"{FRAME}\\\"/' "$settingsFile"
sed -i.bak 's/^CustomViewerArguments3=.*/CustomViewerArguments3=/' "$settingsFile"
sed -i.bak 's/^CustomViewerExecutable1=.*/CustomViewerExecutable1=PATH_TO_RV_LAUNCHER' "$settingsFile"
sed -i.bak 's/^CustomViewerExecutable2=.*/CustomViewerExecutable2=PATH_TO_RV_LAUNCHER' "$settingsFile"
sed -i.bak 's/^CustomViewerExecutable3=.*/CustomViewerExecutable3=/' "$settingsFile"
sed -i.bak 's/^CustomViewerHandlesChunkedTasks1=.*/CustomViewerHandlesChunkedTasks1=false/' "$settingsFile"
sed -i.bak 's/^CustomViewerHandlesChunkedTasks2=.*/CustomViewerHandlesChunkedTasks2=false/' "$settingsFile"
sed -i.bak 's/^CustomViewerHandlesChunkedTasks3=.*/CustomViewerHandlesChunkedTasks3=false/' "$settingsFile"
sed -i.bak 's/^CustomViewerName1=.*/CustomViewerName1=rv sequence/' "$settingsFile"
sed -i.bak 's/^CustomViewerName2=.*/CustomViewerName2=rv frame/' "$settingsFile"
sed -i.bak 's/^CustomViewerName3=.*/CustomViewerName3=/' "$settingsFile"
sed -i.bak 's/^PreferredViewer=.*/PreferredViewer=1/' "$settingsFile"
rm "$settingsFile".bak

echo "After modifications :"
cat "$settingsFile" | grep Viewer
