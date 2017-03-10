#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

# Directions:
"""
list, check, deactivate|reactivate
1. ./usermod_deactivate.py -l 1
   ... comment users ..
2. ./usermod_deactivate.py -c 1
   ... see right users .. else insert # into "users"
3. ./usermod_deactivate.py -d 1  (deactivate)
or ./usermod_deactivate.py -r 1  (reactivate)
"""

import subprocess

def run_command(invocation):
    pipe=subprocess.Popen(invocation,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr
    # os.chdir(os.path.dirname(script))
    # run_command('touch',script)
    # os.chdir(my_dir)


def list_users():
    os.system("rm users")
    os.system("cut -d: -f1 /etc/passwd >> users")
    # users = os.system("cut -d: -f1 /etc/passwd")
    # print users

def check_users():
    o = open('users','r+')
    text=o.readlines()
    o.close()
    users = []
    for line in text:
        # print line
        if not line.startswith('#'):
            users.append(line)
            # print line
    return users

def run_on_users(users,command):
    for u in users:
        command_string = "passwd %s %s" % (u,command)
        print command_string
        if args['deactivate'] == '99':
            # os.system(command_string)
            run_command(command_string)
        # os.system("echo %s %s" % (u,command))
        # print u,command


#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--listall",help="list all users")
    parser.add_argument("-c","--check",help="check users")
    parser.add_argument("-d","--deactivate",help="deactivate users")
    parser.add_argument("-r","--reactivate",help="reactivate users")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
if args['listall'] != None:
    list_users()

if args['check'] != None:
    users = check_users()
    print users

if args['deactivate'] != None:
    users = check_users()
    run_on_users(users,"-l")

if args['reactivate'] != None:
    users = check_users()
    run_on_users(users,"-u")
