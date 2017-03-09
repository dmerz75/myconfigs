^#!/usr/bin/env python
import sys
import os
import time
from glob import *
import re
import numpy as np
import subprocess

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
#  ---------------------------------------------------------  #

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
from mdanalysis.MoleculeUniverse import MoleculeUniverse

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

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
    parser.add_argument("-step","--step",help="step by frames",type=int)
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
step = args['step']

my_dir = os.path.abspath(os.path.dirname(__file__))

# clean out the directories
if not os.path.exists(os.path.join(my_dir,'interim_coord')):
    os.makedirs(os.path.join(my_dir,'interim_coord'))
for path in os.listdir('interim_coord'):
    fp_path = os.path.join(my_dir,'interim_coord',path)
    os.remove(fp_path)


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



#  ---------------------------------------------------------  #
#  workflow                                                   #
#  ---------------------------------------------------------  #
# 1. call run_mda_write_interimcoord.py
#    write_interim_coords with appropriate residues
# 2. call pulchra
# 3. call run_area
# 4. extract/collect surface areas as 2d array: frame_number | hsa


def call_write_coords():
    # dcd = os.path.expanduser('~/ext/completed/sopnucleo/hsp70nbd_unsignedint/atp/sopnuc_atp_unsigned_sopnucleo__07-01-2014__131_1098398/Coord/ATP4B9Q.dcd')
    # psf = os.path.expanduser('~/ext/completed/sopnucleo/ATP4B9Q.psf')
    dcd = os.path.expanduser('~/ext/completed/sopnucleo/hsp70nbd_2bil_int/too-large-int-atpadp-defaults/adp-default/adp-def_runsopnuc__84__04-17-2014_0014__84_621235/Coord/ADP4B9Q.dcd')
    psf = os.path.expanduser('~/ext/completed/sopnucleo/ADP4B9Q.psf')
    # dcd = os.path.expanduser('~/ext/completed/gsop/gsop_nbd_doubled-4-11-139-169/nbd_orig2x4-11-139-169__2kho__280_7743741__09-03-2014_1021/dcd/2KHO_D30_pull.dcd')
    # psf = os.path.expanduser('~/ext/completed/gsop/psfgsop2KHO.psf')
    print psf,dcd
    # def __init__(self,workdir,psf,dcd,destdir,idn):
    x = MoleculeUniverse(my_dir,psf,dcd,my_dir,'hsa')
    # def write_coords(self,resid_first,resid_last,start=0,stop=-1,step=1):
    x.write_coords(resid_first,resid_last,frame_first,frame_last,step)

call_write_coords()

def call_pulchra():
    # os.chdir(os.path.join(my_dir,'interim_coord'))
    os.chdir('interim_coord')
    # lst_interim_coords = glob(os.path.join(my_dir,'interim_coord/interim_*'))
    # lst_interim_coords = glob('interim_coord/interim_*')
    lst_interim_coords = glob('interim_*')
    # print lst_interim_coords
    [lst_interim_coords.pop(i) for i,item in enumerate(lst_interim_coords) if re.search('rebuilt',item) != None]
    # print lst_interim_coords
    for coord in lst_interim_coords:
        run_command(['pulchra',coord])

call_pulchra()

def call_run_area():
    os.chdir(os.path.join(my_dir,'interim_coord'))
    lst_rebuilts = glob(os.path.join('interim_*.rebuilt.*'))
    for coord in lst_rebuilts:
        run_command(['run_area',coord])

call_run_area()

def get_ratio():
    lst_hydro = []
    lst_frames= []
    lst_zipped = []
    os.chdir(os.path.join(my_dir,'interim_coord'))
    lst_ratios = glob(os.path.join('Ratio_*'))
    print lst_ratios
    for i,ratio in enumerate(lst_ratios,frame_first):
        print i,ratio
        # print ratio.split('.')[1]
        o = open(ratio,'r+')
        final_line = o.readlines()[-1]
        hydrophobes_exposed = final_line.split()[-1]
        print final_line,hydrophobes_exposed,'\n'
        o.close()
        frame = int(re.search('_f(\d+)',ratio).groups(1)[0])
        # lst_frames.append(int(i))
        lst_frames.append(frame)
        # print frame
        # sys.exit()
        lst_hydro.append(float(hydrophobes_exposed))
    lst_zipped = zip(lst_frames,lst_hydro)

    # sys.exit()

    # arr_frames = np.array(lst_frames)
    # arr_hydro = np.array(lst_hydro)
    # hsa_data = np.transpose(np.vstack([arr_frames,arr_hydro]))
    hsa_data = np.array(sorted(lst_zipped))
    # print arr_zip,arr_zip.shape
    # print hsa_data,hsa_data.shape
    # sys.exit()
    script_args = (' ').join(sys.argv)
    os.chdir(my_dir)
    np.savetxt('hsa_r%d-%d_f%d-%d.dat' % (resid_first,resid_last,frame_first,frame_last),hsa_data,\
               fmt='%0.0f %0.3f',header=script_args)

get_ratio()


# 84: run_hsa.py - part-a
# f: 2350 - 2450 r: 1-343 *
# f: 4940 - 5040 r: 1-169 *
# f: 7400 - 7500 r: 1-145 *
# f: 19250 - 19350 r: 188-346 *
# f: 24700 - 24800 r: 187-225

# 84: run_hsa.py - part-b
# f: 2250 r: 1-343
# f: 5170 r: 1-170 (might be better as 1-343)
# f: 6200 r: 1-145
# f: 8020 r: 1-115
# f: 19400 r: 187-346
# f: 26500 r: 187-225 ***

# 84: run_hsa.py - part-c - 400
# f: 2000 r: 1-343
# f: 5000 r: 1-170 (might be better as 1-343)
# f: 6000 r: 1-145
# f: 7800 r: 1-115
# f: 19200 r: 187-346
