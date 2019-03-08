#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time

my_dir = os.path.abspath(os.path.dirname('__file__'))
out_dir = os.path.join(my_dir,'nielsen_gzip2')

try:
    from FileConverter import *
except:
    sys.path.append(os.path.expanduser('~/.myconfigs/mylib'))
    from FileConverter import *


F = FileConverter(my_dir,'ZIP',out_dir,'gz')
F.FindFiles()
F.CopyFiles()
