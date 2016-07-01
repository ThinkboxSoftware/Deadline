#!/usr/bin/env bash

# Example of requeing a Job using REST via curl.
#
# See:  http://docs.thinkboxsoftware.com/products/deadline/8.0/1_User%20Manual/manual/rest-jobs.html
#

SERVER=http://localhost:8082
JOB_ID=5773e4ea86e590000fa27110

JSONDATA='{"Command":"requeue","JobID":"'$JOB_ID'"}'

RESPONSE=$(curl -H "Accept: application/json" -X PUT -d "$JSONDATA" $SERVER/api/jobs)

echo $RESPONSE

