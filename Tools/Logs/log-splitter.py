#!/usr/bin/env python

'''
    Take a Deadline Slave log and put the individual task output into
    distinct files. Currently does not support concurrent tasks in the
    log.
'''

import re
import argparse

parser = argparse.ArgumentParser(description='Extract task logs from Slave log')
parser.add_argument('file', help='Slave log to extract from')
args = parser.parse_args()

original = open(args.file, "r")

new = open("slave.txt", "w")
job = 0
jobs = open("task%s.txt" % job, "w")

for line in original:
    m = re.search('^.{20}\s*(\d{1,2}):', line)
    end = re.search('Exited ThreadMain', line)

    if end:
        jobs.write(line)
        job += 1
        jobs.close()
        jobs = open("task%s.txt" % job, "w")
    if m:
        jobs.write(line)
    else:
        new.write(line)

jobs.close()
new.close()
original.close()
