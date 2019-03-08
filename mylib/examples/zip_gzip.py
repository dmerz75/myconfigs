#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import re
from glob import glob
import shutil
from pathlib import *

print(sys.version)

# usage:
# ./convert.py -d incomplete/

# mylib:
my_library = os.path.expanduser('~/.myconfigs')
sys.path.append(my_library)

# libraries:
# from mylib.FindAllFiles import *
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
# from mylib.myargs import parse_arguments
from mylib.run_command import run_command

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    '''
    Parse script's arguments.
    Options:
    args['makefile']
    args['procs']
    args['node'])
    '''
    parser = argparse.ArgumentParser()
    # parser.add_argument("-r","--range",help="range for running")
    parser.add_argument("-d","--subdir",help="subdirectory provided")
    parser.add_argument("-o","--outdir",help="output directory")
    parser.add_argument("-f","--nfile",help="notebook file")
    args = vars(parser.parse_args())
    return args
args = parse_arguments()

my_dir = os.path.dirname(os.path.abspath('__file__'))
print(my_dir)
print(os.getcwd())
# curr_path = Path(".")
# print(curr_path)
# sys.exit()

# lst_files = glob(os.path.join(my_dir,'*.ZIP'))
lst_files = glob('*.ZIP')
CWD = Path('.')
print('cwd:',CWD)

# shutil.rmtree('temp_file/*')
if os.path.exists('temp_file'):
    # os.removedirs('temp_file')
    shutil.rmtree('temp_file')
    os.makedirs('temp_file')


for i,fp in enumerate(lst_files):
    print('fp:',fp)
    fp_path = PurePath(fp)
    fp_base = fp_path.stem
    fp_gzip = fp_base + '.gz'
    # fp_zip = list(CWD.glob('./temp_file/**'))
    # fp_zip = glob('./temp_file/*')
    # temp_file = PurePath('temp_file',fp_gzip)

    print(fp_path)
    print(fp_base)
    # print('unzip:',fp_zip)
    print('gz:',fp_gzip)



    run_command(['unzip','-d','temp_file',fp])

    temp_file = os.listdir('temp_file')[0]

    print('temp_file:',temp_file)

    run_command(['gzip',os.path.join('temp_file',temp_file)])

    # gzip_file = os.listdir('temp_file')[0]
    gzip_file = glob(os.path.join(os.getcwd(),'temp_file/*'))[0]
    print(gzip_file)

    # break
    dest_file = os.path.join(os.getcwd(),'nielsen_gzip',fp_gzip)

    # break
    shutil.move(gzip_file,dest_file)

    os.remove(fp)