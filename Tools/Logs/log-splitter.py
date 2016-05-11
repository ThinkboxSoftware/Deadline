#!/usr/bin/env python

'''
    Take a Deadline Slave log and put the individual task output into
    distinct files. Currently does not support concurrent tasks in the
    log.
'''

import re
import argparse
import os.path

parser = argparse.ArgumentParser(description='Extract task logs from Slave log')
parser.add_argument('file', help='Slave log to extract from')
args = parser.parse_args()

original = open(args.file, "r")

new = open("slave.txt", "w")
num = 0
jobs = None

files = {"0": None,
         "1": None,
         "2": None,
         "3": None,
         "4": None,
         "5": None,
         "6": None,
         "7": None,
         "8": None,
         "9": None,
         "10": None,
         "11": None,
         "12": None,
         "13": None,
         "14": None,
         "15": None, }


# Checks if this line is the start of a new task
def task_start(line, position):
    global num
    begin = re.search('job starting', line)
    if begin:
        filename = "./" + str("task%s-%s.txt" % (position, num))
        if os.path.isfile(filename):
            num += 1
            files[position].close()
            return True
        else:
            return False


# Creates new file and puts in files dictionary
def new_file(position, num):
    files[position] = open("task%s-%s.txt" % (position, num), "w")


# Begins Here...
for line in original:
    m = re.search('^.{20}\s+(\d{1,2}):', line)
    if m:
        position = line[21:24].strip()
        position = position.replace(":", "")
        if files[position] is None:
            new_file(position, num)
        # Checks if file exists
        elif task_start(line, position):
            new_file(position, num)

        jobs = files[position]
        jobs.write(line)
    # If not a task line
    else:
        new.write(line)

# Closes all rest of files
for key, value in list(files.items()):
    if value is not None:
        value.close()

new.close()
original.close()
