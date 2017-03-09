#!/usr/bin/env python
import sys
import os
import time
from glob import *
import re
import numpy as np

#  ---------------------------------------------------------  #
#  Directions:                                                #
#  ./run_2_tension.py -r1 1                                   #
#                     -r2 383                                 #
#                     -f1 400                                 #
#                     -f2 900                                 #
#                     -seed 788912                            #
#                     -nuc ATP | ADP                          #
#                     -run_type gsop | sopnucleo              #
#                     -pdb 2KHO | 4B9Q                        #
#  Result:                                                    #
#  tension_coords/interim<frame1>.pdb will be written!        #
n#  ---------------------------------------------------------  #

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-r1","--resid1",help="first resid",type=int)
    parser.add_argument("-r2","--resid2",help="last resid",type=int)
    parser.add_argument("-f1","--frame1",help="first frame",type=int)
    parser.add_argument("-f2","--frame2",help="last frame",type=int)
    parser.add_argument("-seed","--seed",help="Langevin seed used in trajectory acquisition",type=int)
    parser.add_argument("-nuc","--nucleotide",help="nucleotide, either ADP or ATP")
    parser.add_argument("-t","--run_type",help="for what type of analysis is this, gsop or sopnucleo")
    parser.add_argument("-p","--pdb",help="PDB code, i.e. 2KHO,4B9Q")
    args = vars(parser.parse_args())
    # return parser.parse_args()
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''

# for k,v in args.iteritems():
#     print k,v
# sys.exit()

frame_first = args['frame1']
frame_last  = args['frame2']
resid_first = args['resid1']
resid_last  = args['resid2']
nucleotide  = args['nucleotide']
seed = args['seed']
run_type = args['run_type']
pdb = args['pdb']


my_dir = os.path.abspath(os.path.dirname(__file__))

import subprocess

def run_command(invocation):
    pipe=subprocess.Popen(invocation,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr


# def write_interim_coords():
#     # write interim coords
#     if run_type == 'sopnucleo':
#         print 'writing coordinates for SOPNUCLEO, running ...'
#         command = ['./run_mda_write_interimcoord.py','-f1',str(frame_first),\
#                    '-f2',str(frame_last),'-nuc',nucleotide,'-seed',str(seed),\
#                    '-t',run_type,'-p',pdb,'-r1',str(resid_first),'-r2',str(resid_last)]
#         # run_command(['./run_mda_write_interimcoord.py',str(frame_first),str(frame_last),nucleotide])
#         run_command(command)

# def get_tension(fn_tension):
#     for path in lst_coords_files:
#         dir_tension_coords = os.path.dirname(path)
#         fn_molecule = os.path.basename(path)
#         # print path
#         # print dir_tension_coords
#         # print fn_molecule
#         cp_file(dir_tension_coords,fn_molecule,my_dir,fn_molecule)

#         if run_type == 'sopnucleo':
#             command_list = ['run_tension',str(resid_first),str(resid_last), \
#                             'pdb%s4B9Q.pdb' % nucleotide,fn_molecule]
#         elif run_type == 'gsop':
#             # command_list = ['./run_tension',str(resid_first),str(resid_last), \
#                             # 'pdb%s.pdb' % pdb,fn_molecule]
#             command_list = ['run_tension',str(resid_first),str(resid_last), \
#                             '2kho_nbd.pdb',fn_molecule]

#             print command_list
#         run_command(command_list)
# np.savetxt(fn_tension,averages,fmt='%2.4f')
