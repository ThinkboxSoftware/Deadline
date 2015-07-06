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
jobs = None

files = {"0":None, 
         "1":None, 
         "2":None, 
         "3":None, 
         "4":None, 
         "5":None, 
         "6":None, 
         "7":None, 
         "8":None, 
         "9":None, 
         "10":None, 
         "11":None, 
         "12":None, 
         "13":None, 
         "14":None, 
         "15":None, }

for line in original:
    m = re.search('^.{20}\s+(\d{1,2}):', line)    
    if m:
        position = line[21:24].strip()
        position = position.replace(":", "")

        if files[position] == None:
            files[position] = open("task%s.txt" % position, "w")
            jobs = files[position]
        else:
            jobs = files[position]
            jobs.write(line)
    else:
        new.write(line)

# Cleanup
for key, value in files.iteritems():
    if value is not None:
        value.close()
new.close()
original.close()