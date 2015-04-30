#!/usr/bin/env python
'''
    license_usage.py - Caculate Deadline usage stats from license file
    
    Usage:
        python license_usage.py Thinkbox.log
    
    Note that this is untested for accuracy, and should be inaccurate for logs
    which ran over DST changes.
'''

import sys
import time
from datetime import datetime, timedelta, MINYEAR

class checkout_tracker():
    def __init__(self):
        self.duration = timedelta(0)
        self.checkout_time = []
    
    def check_in(self, time):
        start_time = self.checkout_time.pop()
        self.duration += time - start_time
    
    def check_in_remaining(self, time):
        ''' Calculate the duration for what's left '''
        while len(self.checkout_time) > 0:
            self.check_in(time)
    
    def check_out(self, time):
        self.checkout_time.append(time)
        
    def __unicode__(self):
        return str(self.duration)
        
    def __str__(self):
        return self.__unicode__()

        
def main():
    time_total   = datetime.min
    time_current = datetime.min
    time_last    = datetime.min
    time_start   = datetime.min
    
    machines = {}

    try:
        file = open(sys.argv[1])
    except IOError:
        print("Unable to open file.")
        sys.exit(2)
    except IndexError:
        print("No log file given.")
        sys.exit(1)
    
    for line in process_file(file):
        (timestamp, vendor, state, feature, key) = line.split()

        time_current = datetime.strptime(timestamp, "%H:%M:%S")
        
        if time_total == datetime.min:
            time_total = time_current
            time_start = time_current
        else:
            # Dealing with the clock rolling over to a new day...
            time_total += account_time(time_last, time_current)
                
        time_last = time_current
        
        process_element(machines, time_total, vendor, state, feature, key)

    # Tabulate everything, check in whatever was still out, etc
    total_duration = timedelta(0)
    for machine, duration in machines.items():
        duration.check_in_remaining(time_total)
        total_duration += duration.duration
    
        print("{0:<40}{1}".format(machine, duration))

    total_runtime = time_total - time_start
        
    print("-" * 50)
    print("{0:<40}{1}".format("Total used hours", total_duration))
    print("{0:<40}{1}".format("Total server runtime", total_runtime))
    print()
    print("These values may not be accurate (especially across time changes).")
    
    
    file.close()

def account_time(old, new):
    ''' Do the math if the time rolled over '''
    if new < old:
        # Time rolled over
        duration  = timedelta(days=1)
        duration -= old - new
    else:
        duration = new - old
        
    return duration
    
def process_file(file):
    ''' Weed out unwanted lines and pass them on to tracking '''
    for line in file:
        if "OUT:" in line or "IN:" in line:
            yield line.strip()

def process_element(machines, timestamp, vendor, state, feature, key):
    if feature != '"deadline"':
        return
        
    if vendor != '(thinkbox)':
        return
    
    if state == "OUT:":
        if key in machines:
            machines[key].check_out(timestamp)
        else:
            new_tracker = checkout_tracker()
            new_tracker.check_out(timestamp)
            machines[key] = new_tracker
    elif state == "IN:":
        if key in machines:
            machines[key].check_in(timestamp)
        else:
            print("Unexpected checkin!")
    else:
        print("Unexpected state!")
    
main()