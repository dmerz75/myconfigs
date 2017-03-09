#!/usr/bin/env python
import sys
import os
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-j","--job_id",help="Job Id list, individual or as array")
    parser.add_argument("-g","--group_type",help="select asarray or individual(default)")
    args = vars(parser.parse_args())
    # return parser.parse_args()
    return args

import subprocess

def run_command(command):
    pipe=subprocess.Popen(command,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr

def construct_jobs_array(args):
    job_start_stop = args['job_id'].split(':')
    job_array_list = [i for i in range(int(job_start_stop[0]),\
                                       int(job_start_stop[-1])+1)]
    return job_array_list


# --- Start Here ---

# - Get arguments -
args = parse_arguments()
if args['group_type'] == None: args['group_type'] = 'individual'
''' Options:
args['job_id'] = None (default)
args['group_type'] = 'individual' (default)
'''

# - build job array -
jobs = construct_jobs_array(args)
print jobs

# - process qdel job_id command -
for j in jobs:
    # run_command(['echo',str(j)])
    run_command(['qdel',str(j)])
