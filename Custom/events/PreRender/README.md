# PreRender.py

## What does it do?
This plugin will run whatever command you place in the config (seperated by OS) right before the application to render is started. The command provided is run just as if you had run it from a command prompt on the Worker machine.

In the original case, this was used to call a script to mount drives, but it could be used for anything you want to be ready just before rendering starts.

## Usage Instructions

This [page of our documentation](https://docs.thinkboxsoftware.com/products/deadline/10.1/1_User%20Manual/manual/event-plugins.html#creating-an-event-plug-in) provides a more in-depth look at how to create a custom Event Plugin.

But to "plug-and-play" with this example plugin, all you need to do is:

* Copy the `PreRender` folder from this repository to the `custom/events` folder under your DeadlineRepository path.
* Then in the Monitor go to `Tools -> Configure Events...`
* Select `PreRender` and change the state to `Global Enabled`
* Restart the Workers or wait for them to detect the change.
* Then you're done! Any Worker that begins rendering will first run the command specified in the config!
