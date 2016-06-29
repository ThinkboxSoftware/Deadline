#!/usr/bin/env bash

# Example of submitting a CommandScript Job using REST via curl.
#
# See:  http://docs.thinkboxsoftware.com/products/deadline/8.0/1_User%20Manual/manual/rest-jobs.html
#
# IMPORTANT NOTE:
#
# For testing purposes, the AuxFiles array is left empty in this script.  To actually function, a CommandScript job
# requires the text file to hold the command(s) to be run. Therefor, in practice, within the JSON data the AuxFiles 
# name would contain the path to the text file that contains the actual command:   "AuxFiles":["/path/to/command.txt"]
#
# The REST API does not handle file transfer, so the filename(s) supplied in the AuxFiles array must be given from the 
# perspective of the web service, rather than from the perspective of the client that is making the REST call.  This 
# implies that the files should be transferred to a location visible to the web service prior to the submission 
# of the Job.
#

SERVER=http://localhost:8082

JSONDATA='{"JobInfo":{"Plugin":"CommandScript","Frames":"0","Name":"Test REST Job"},"PluginInfo":{"StartupDirectory":"/"},"AuxFiles":[],"IdOnly":true}'

RESPONSE=$(curl -H "Content-Type: application/json" -X POST -d "$JSONDATA" $SERVER/api/jobs)

echo $RESPONSE
