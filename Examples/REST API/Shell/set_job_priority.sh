#!/usr/bin/env bash

# Example of setting the priority of a Job using REST via curl.
#
# See:  http://docs.thinkboxsoftware.com/products/deadline/8.0/1_User%20Manual/manual/rest-jobs.html
#

# NOTE: The general approach for modifiying job properties via REST is to first retrieve the job data, then modify it,
# and then send it back enclosed inside the save command as demonstrated below.
#
# NOTE: Bash is generally not the easiest way to work with the REST API.  Instead, the Standalone Pythone API, which
# wraps the REST API, is one alternative.  However, the examples below using curl may help convey the structure of the
# data sent to the web service.

SERVER=http://localhost:8082
JOB_ID=5774169f86e590000fa27122
PRIORITY=70


# First, retreive the Job data from the web service into a variable.
JOBINFORAW=$(curl --silent $SERVER/api/jobs?JobID=$JOB_ID)

# Take the Job dicitionary out of the square brackets (the Job info is returned inside a JSON array).
JOBINFO=${JOBINFORAW:1:-1}


echo -------- Job Data Before --------
echo $JOBINFO
echo ---------------------------------
echo

# Replace the Priority portion of the Job dictionary.
pri_re='"Pri":'[[:digit:]]+

if [[ $JOBINFO =~ $pri_re ]] ; then
  echo The regex matches!
  REPLACER=$(echo ${BASH_REMATCH[*]})
  echo $REPLACER
  echo
  UPDATED=$(echo ${JOBINFO//$REPLACER/\"Pri\":$PRIORITY})
fi

echo -------- Job Data After ---------
echo $UPDATED
echo ---------------------------------
echo

# Form the final command data.
JSONDATA=$(echo '{"Command":"save", "Job":'$UPDATED'}')

# Send command and get the response.
RESPONSE=$(curl -H "Content-Type: application/json" -X PUT -d "$JSONDATA" $SERVER/api/jobs)

echo $RESPONSE
