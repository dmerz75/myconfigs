#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

print ("Hello from main script!")

my_dir = os.path.abspath(os.path.dirname(__file__))


sys.path.append(os.path.join(my_dir,'pylib'))
# print (sys.path)

from pylib.ForceIndentation import ForceIndentation

X = ForceIndentation()
