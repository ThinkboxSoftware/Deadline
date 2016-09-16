#! /usr/bin/python
# -*- coding: utf-8
# Copyright 2014 Klimenko Artyem <aklim007(at)gmail(dot)com>
# Based on work by Rob Cherry <zsend(at)lxrb(dot)com>
# > Based on work by Enrico Tr�ger <enrico(dot)troeger(at)uvena(dot)de>
# License: GNU GPLv2


import socket
import struct
import json
import time
import sys
import re

ZABBIX_SERVER = "127.0.0.1"
ZABBIX_PORT = 10051


class ZSend:
    def __init__(self, server=ZABBIX_SERVER, port=ZABBIX_PORT, verbose=False):
        self.zserver = server
        self.zport = port
        self.verbose = verbose
        self.list = []
        self.inittime = int(round(time.time()))
        self.clock_flag = False

    def add_data(self, host, key, value, clock=None):
        obj = {
            'host': host,
            'key': key,
            'value': value,
        }
        if clock:
            obj['clock'] = clock
            self.clock_flag = True
        self.list.append(obj)

    def print_vals(self):
        for elem in self.list:
            print( u'{0}'.format(elem) )
        print( u'Count: {0}'.format(len(self.list)) )

    def build_all(self):
        send_data = {
            "request": "sender data",
            "data": [],
        }
        if self.clock_flag:
            send_data['clock'] = self.inittime
        send_data['data'] = self.list
        return json.dumps(send_data)

    def build_single(self, data):
        send_data = {
            "request": "sender data",
            "data": [],
        }
        if 'clock' in data:
            send_data['clock'] = self.inittime
        send_data['data'].append(data)
        return json.dumps(send_data)

    def send(self, mydata):
        socket.setdefaulttimeout(5)
        data_length = len(mydata)
        data_header = '{0}{1}'.format(struct.pack('i', data_length), '\0\0\0\0')
        data_to_send = 'ZBXD\1{0}{1}'.format(data_header, mydata)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.zserver, self.zport))
            sock.send(data_to_send)
        except Exception as err:
            err_message = u'Error talking to server: {0}\n'.format(err)
            sys.stderr.write(err_message)
            return 255, err_message

        response_header = sock.recv(5)
        if not response_header == 'ZBXD\1':
            err_message = u'Invalid response from server. Malformed data?\n---\n{0}\n---\n'.format(mydata)
            sys.stderr.write(err_message)
            return 254, err_message
        response_data_header = sock.recv(8)
        response_data_header = response_data_header[:4]
        response_len = struct.unpack('i', response_data_header)[0]
        response_raw = sock.recv(response_len)
        sock.close()
        response = json.loads(response_raw)
        match = re.match('^.*failed.+?(\d+).*$', response['info'].lower() if 'info' in response else '')
        if match is None:
            err_message = u'Unable to parse server response - \n{0}\n'.format(response)
            sys.stderr.write(err_message)
            return 2, response
        else:
            fails = int(match.group(1))
            if fails > 0:
                if self.verbose is True:
                    err_message = u'Failures reported by zabbix when sending:\n{0}\n'.format(mydata)
                    sys.stderr.write(err_message)
                return 1, response
        return 0, response

    def bulk_send(self):
        data = self.build_all()
        result = self.send(data)
        return result

    def iter_send(self):
        retarray = []
        for i in self.list:
            (retcode, retstring) = self.send(self.build_single(i))
            retarray.append((retcode, i))
        return retarray


# ####################################
# --- Examples of usage ---
#####################################
#
# Initiating a Zsend object -
# z = ZSend() # Defaults to using ZABBIX_SERVER,ZABBIX_PORT
# z = ZSend(verbose=True) # Prints all sending failures to stderr
# z = ZSend(server="172.0.0.100",verbose=True)
# z = ZSend(server="zabbix-server",port=10051)
# z = ZSend("zabbix-server", 10051)
#

# --- Adding data to send later ---
# Host, Key, Value are all necessary
# z.add_data("host","cpu.ready","12")
#
# Optionally you can provide a specific timestamp for the sample
# z.add_data("host","cpu.ready","13",1365787627)
#
# If you provide no timestamp, the initialization time of the class
# is used.

# --- Printing values ---
# Not that useful, but if you would like to see your data in tuple form
# with assumed timestamps
# z.print_vals()

# --- Building well formatted data to send ---
# You can send all of the data in one batch -
# z.build_all() will return a string of packaged data ready to send
# z.build_single((host,key,value,timestamp)) will return a packaged single

# --- Sending data manually ---
# Typical example 1 - build all the data and send it in one batch -
#
# z.send(z.build_all())
#
# Alternate example - build the data individually and send it one by one
# so that we can see errors for anything that doesnt send properly -
#
# for i in z.list:
#    (code,ret) = z.send(z.build_single(i))
#    if code == 1:
#       print "Problem during send!\n%s" % ret
#    elif code == 0:
#       print ret
#
# --- Sending data with built in functions ---
#
# Sending everything at once, with no concern about
# individual item failure -
#
# (retcode,retstring) = z.bulk_send()
# print "Result: %s -> %s" % (str(retcode),retstring)
#
# Sending every item individually so that we can capture
# success or failure
#
# results = z.iter_send()
# for (code,data) in results:
#   (h,k,v,t) = data
#   if code == 1:
#      print "Failed to update key: %s for host: %s" % (k,h)
#
#
#####################################
# Mini example of a working program #
#####################################
#
# import sys
# sys.path.append("/path/to/Zsend.py")
# from ZSend import ZSend
#
# z = ZabbixSender() # Defaults to using ZABBIX_SERVER,ZABBIX_PORT
