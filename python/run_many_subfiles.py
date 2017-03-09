#!/usr/bin/env python
import sys
import os
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

import subprocess

def run_command(invocation,script):
    pipe=subprocess.Popen([invocation,script],stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr

    # os.chdir(os.path.dirname(script))
    # run_command('touch',script)
    # os.chdir(my_dir)


# Call Routine: ____________________________________________
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.findall_files import *
dct_find = {'cwd':my_dir,'pattern':'sync.sh'}
x = findall_files(dct_find)
lst_sync = x.get_files()

for sync in lst_sync:
    job_dir = os.path.dirname(sync)
    os.chdir(job_dir)
    print sync
    run_command('bash',sync)
