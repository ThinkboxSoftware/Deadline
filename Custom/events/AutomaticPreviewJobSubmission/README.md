# AutomaticPreviewJobSubmission.py

## Overview

This script came from a customer request on how they could go about submitting Jobs to their repository as suspended and then having the first, middle, and last tasks of those jobs enabled automatically immediately after submission.

## Usecase

The need for this stems from allowing a customer to be able to use Deadline to get a preview of how a larger job will go.

The customer can use this Event Plugin to get a **preview** of what their render result might look like, and maybe more importantly get an idea of how long the job will take to complete based on how long this short subset of tasks takes to complete.

## What does it do?

In this case all we have to do is create an OnJobSubmitted event plugin that will grab the collection of tasks for any submitted job, and then forcefully resume each of the first, middle, and last tasks.

Note that this example plugin script is for a very basic usecase, as this will apply to all submitted job regardless of their status.

For our requesting customer, we just assume all the jobs are submitted as suspended.

So if you want to adapt this for your own usecase, you should supply some more stringent parameters for when to perform the resume operation.

## Usage Instructions

This [page of our documentation](https://docs.thinkboxsoftware.com/products/deadline/10.0/1_User%20Manual/manual/event-plugins.html#creating-an-event-plug-in) provides a more in-depth look at how to create a custom Event Plugin.

But to "plug-and-play" with this example plugin, all you need to do is:
* Copy the `AutomaticPreviewJobSubmission` folder from this repository to the `custom/events` folder under your DeadlineRepository path.
* Then in the Deadline Monitor you can:
    * Click `Tools -> Synchronize Monitor Scripts and Plugins` to sync your new Event Plugin
    * Then in `Tools -> Configure Events...`:
        * Select `AutomaticPreviewJobSubmission` and change the state to `Global Enabled`
* Then you're done! Any submitted job should then have its first, middle, and last tasks forcefully resumed on job submission.
