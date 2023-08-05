#!/usr/bin/env python3

import os
import json
import uuid

from datetime import datetime

class NotHammerspaceManagedException(Exception):
    pass

def get_oldest_send_time(directory):
    replication_status_json = read_shadow_data(directory)

    replication_details = replication_status_json['REPLICATION_DETAILS_TABLE']
    send_times = []
    for obj in replication_details:
        time_string = obj['SEND_TIME']['date']
        time_string = time_string.replace('Z', '+0000')
        timestamp = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S%z")
        send_times.append(timestamp)
    send_times.sort()
    return int(send_times[-1].timestamp())

def get_mtime(directory):
	return int(os.stat(directory).st_mtime)

# this gets us out of requiring hstk in the environment for this one job
def read_shadow_data(directory):

    replication_query_cmd = './?.eval_json replication_details'

    # Add padding for windows, writes don't get pushed through the stack for if there is not enough data
    if os.name == 'nt':
        replication_query_cmd += '\0'*50

    # Unique work id to identify the shadow request
    work_id = hex(uuid.uuid4().int)
    shadow_path = '{}.fs_command_gateway {}'.format(directory, work_id)

    # Open read/write file handle for shadow command
    with open(shadow_path, 'w') as fd:
        # Write shadow command to get replication details in JSON
        fd.write(replication_query_cmd)

    # Read back the results
    with open(shadow_path) as results_handle:
        results = results_handle.read()

    try:
        response = json.loads(results)
    except json.decoder.JSONDecodeError: 
        if results == replication_query_cmd:
            os.remove(shadow_path)
            raise NotHammerspaceManagedException
        else:
            raise

    # Return the JSON formatted response
    return response

def sync_completed(dir_path):
    mtime = get_mtime(dir_path)
    sendtime = get_oldest_send_time(dir_path)
    return mtime < sendtime
