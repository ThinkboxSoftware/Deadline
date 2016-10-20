#!/usr/bin/env python

import argparse
import codecs
import collections

from datetime import datetime, timedelta


def inspect_file(delay, filename):
    '''
        Run through a file and print out areas of the log where
        delays of 'delay' seconds were found between lines.
    '''

    file = codecs.open(filename, "r", "utf-8")
    log = collections.deque(maxlen=2)
    last_time = datetime.min

    for line in file.readlines():
        line = line.strip().encode('ascii', 'ignore')

        date_text = line[:19]

        date = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")

        if last_time < date - timedelta(seconds=delay):
            print("...")

            for history_line in log:
                print("\t" + history_line)

            print("\t" + line)

        else:
            log.append(line.strip())

        # Keep track of the times
        last_time = date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Deadline logs and show delays')
    parser.add_argument('--delay', type=int, default=3,
                        help='Number of seconds between lines. Defaults to 3')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='Log file(s) to read through')

    args = parser.parse_args()
    for file_name in args.files:
        inspect_file(args.delay, file_name)
