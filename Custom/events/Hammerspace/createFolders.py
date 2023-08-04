#!/usr/bin/env python3
import argparse
import os
import sys
import time

from Deadline.Scripting import RepositoryUtils

hsUtilsPath = os.path.dirname(os.path.abspath(__file__))

if not hsUtilsPath in sys.path:
    sys.path.append(hsUtilsPath)

from HammerspaceUtils import sync_completed, NotHammerspaceManagedException

def __main__(*args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--directories', type=str, help="Comma separated list of directories to create")
    parser.add_argument('--iteration_delay', type=int, help="Seconds to wait after each iteration when polling Hammerspace")
    parser.add_argument('--iteration_count', type=int, help="Maximum number of iterations")

    args = parser.parse_args(args)
    directories = args.directories.split(";")

    directories = RepositoryUtils.CheckPathMappingForMultiplePaths(directories)
    directories = [dir.replace("\\", os.path.sep).replace("/", os.path.sep) for dir in directories]
    print("Directories to create: \n{0}".format("\n".join(directories)))
    print("-"*50)

    create_directories(directories)
    
    sync_status = {}

    for d in directories:
        sync_status[d] = False 

    for i in range(args.iteration_count):
        progress =  int((float(i+1) / float(args.iteration_count)) * 100)
        print("Iteration {0}/{1}. Progress: {2}%".format(i+1, args.iteration_count, progress))
        sys.stdout.flush()

        time.sleep(args.iteration_delay)
        for d in directories: 
            # Skip the directories that are already synced
            if sync_status[d] in [None, True]:
                continue

            try:
                sync_status[d] = sync_completed(d)
            except NotHammerspaceManagedException:
                sync_status[d] = None 

        # If there are no outstanding directories, exit the loop
        if not False in sync_status.values():
            break

    synced_dirs = []
    skipped_dirs = []
    remaining_dirs = []

    for (d,status) in sync_status.items():
        if status == True:
            synced_dirs.append(d)
        elif status == False:
            remaining_dirs.append(d)
        else:
            skipped_dirs.append(d)
            
    print("-"*50)
    for d in synced_dirs:
        print("Sync Complete: "+d)
    for d in remaining_dirs:
        print("Sync Timed Out: "+d)
    for d in skipped_dirs:
        print("Sync Skipped: "+d)


def create_directories(dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)
