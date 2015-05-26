'''
    Right now, this dumps everything into the current working directory.
'''

import zipfile
import bz2
import sys
import argparse
import json
import os


JOB_FILENAME = 'job.json'
LOG_FOLDER = 'logs'
LOG_SUFFIX = 'bz2'

parser = argparse.ArgumentParser(description='Extract and format job files')
parser.add_argument('file', help='Job file to extract')

args = parser.parse_args()
filename = args.file

file = zipfile.ZipFile(filename, "r")

print("Opening {0}...".format(filename))

for name in file.namelist():
    if "json" not in name:
        continue

    sys.stdout.write(" Extracting {0}... ".format(name))
    data = json.load(file.open(name))

    out_file = open(name, 'w')
    json.dump(data, out_file, sort_keys=True, indent=1)
    out_file.close()
    print("Done")

if os.path.exists(LOG_FOLDER):
    raise Exception('Log folder exists. Considering working directory unsafe')

os.makedirs(LOG_FOLDER)

for name in file.namelist():
    if LOG_SUFFIX not in name:
        continue

    sys.stdout.write(' Extracting log {0}... '.format(name))

    # remove extension from log
    bare_name = os.path.splitext(name)[0]

    with open(LOG_FOLDER + '/' + bare_name, 'w') as log:
        # Requires that the log fit in memory!!!
        log.write(bz2.decompress(file.read(name)))

    print('Done')


print("Closing")
file.close()

job_file = open(JOB_FILENAME, 'r')
job = json.load(job_file)
job_file.close()

print("")
print("Information:")
print(" Job Name: {0}".format(job['Props']['Name']))
print(" Plugin:   {0}".format(job['Plug']))
print(" Job ID:   {0}".format(job['_id']))

print("Done")
