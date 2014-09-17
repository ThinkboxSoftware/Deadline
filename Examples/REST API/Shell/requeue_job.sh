SERVER=http://192.168.2.186:8080
JOB_ID=53ed30b6f4b70d991c6a3be0

curl -i -H "Accept: application/json" -X PUT -d "{'Command': 'requeue', 'JobID': '$JOB_ID'}" $SERVER/api/jobs