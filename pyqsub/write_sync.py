#!/usr/bin/env python
import sys
import os
import time
from glob import *
import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))

import subprocess

def run_command(invocation,script):
    pipe=subprocess.Popen([invocation,script],stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr


for path in glob(os.path.join(my_dir,'a*/job.pbs')):
    o = open(path,'r+')
    lines = o.readlines()
    shebang = lines[0]
    beginning = lines[4:9]
    ending = lines[-3:]
    sync_contents = []
    sync_contents.append(shebang) 
    sync_contents += beginning + ending
    # print sync_contents
    o.close()
    
    # # print os.path.dirname(path)
    new_file = os.path.join(os.path.dirname(path),'sync1.sh')

    # write
    with open(new_file,'w+') as fp:
        [fp.write(obj) for obj in sync_contents]

    run_command('bash',new_file)
            
    

