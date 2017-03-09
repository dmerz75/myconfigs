#!/usr/bin/env python
import sys
import os
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

try:
    fn_argument = sys.argv[1]
except IndexError:
    fn_argument = 'job.pbs'

with open(fn_argument) as f:
    lst_lines = f.readlines()


lst_indices = [0,4,5,6,7,8,9,42,43]

with open('sync_out.sh','w+') as sf:
    for i in lst_indices:
        sf.writelines(lst_lines[i])
        print lst_lines[i]
    

os.system('chmod +x sync_out.sh')
