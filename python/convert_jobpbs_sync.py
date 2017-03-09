#!/usr/bin/env python
import sys
import os
import time
import re

# DESCRIPTION:
# take 0 line
# find line with word, 'environment'
# keep last 3 lines


my_dir = os.path.abspath(os.path.dirname(__file__))

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
# from plot.wlc import WormLikeChain


from mylib.findall_files import *
dct_find = {'cwd':my_dir,'pattern':'job.pbs'}
x = findall_files(dct_find)
lst_jobs = x.get_files()

print lst_jobs

for job in lst_jobs:
    lines_keep = []
    mid_lines = []
    with open(job) as fh:
        lines = fh.readlines()
        # print type(lines)

    for i,line in enumerate(lines):
        ans = re.search('environment',line)
        if ans != None:
            # print ans.group()
            # print i,line
            mid_lines.append(i)
        prep = re.search('Prepare',line)
        if prep != None:
            # print prep.group()
            # print i,line
            mid_lines.append(i)

    lines_keep.append(lines[0])
    for i in range(mid_lines[0],mid_lines[-1]):
        lines_keep.append(lines[i])
    # lines_keep.append(lines[mid_lines[0]:mid_lines[-1]:])
    # lines_keep.append(lines[-3::])
    lines_keep.append(lines[-3])
    lines_keep.append(lines[-2])
    lines_keep.append(lines[-1])

    # print job
    # print os.path.dirname(job)
    fp_sync = os.path.join(os.path.dirname(job),'sync.sh')
    with open(fp_sync,'w') as f_sync:
        for l in lines_keep:
            f_sync.write(l)
    os.system('chmod +x %s' % fp_sync)
    # sys.exit()
