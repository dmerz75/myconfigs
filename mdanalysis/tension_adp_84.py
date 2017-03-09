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
#  ---------------------------------------------------------  #

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


# make tension directories
if not os.path.exists(os.path.join(my_dir,'tension_coords')):
    os.makedirs('tension_coords')
if not os.path.exists(os.path.join(my_dir,'tension_output')):
    os.makedirs('tension_output')
# if not os.path.exists(os.path.join(my_dir,'pytension')):
#     os.makedirs('pytension')

# clean out the directories
# for path in os.listdir('tension_coords'):
#     fp_path = os.path.join(my_dir,'tension_coords',path)
#     os.remove(fp_path)
for path in os.listdir('tension_output'):
    fp_path = os.path.join(my_dir,'tension_output',path)
    os.remove(fp_path)

# for path in os.listdir('pytension'):
#     fp_path = os.path.join(my_dir,'pytension',path)
#     os.remove(fp_path)



lst_coords_files = ['tension_coords/interimcoord%d.pdb' % i for i in range(frame_first,frame_last+1)]

def write_interim_coords():
    # write interim coords
    if run_type == 'sopnucleo':
        print 'writing coordinates for SOPNUCLEO, running ...'
        command = ['./run_mda_write_interimcoord.py','-f1',str(frame_first),\
                   '-f2',str(frame_last),'-nuc',nucleotide,'-seed',str(seed),\
                   '-t',run_type,'-p',pdb,'-r1',str(resid_first),'-r2',str(resid_last)]
        # run_command(['./run_mda_write_interimcoord.py',str(frame_first),str(frame_last),nucleotide])
        run_command(command)

    elif run_type == 'gsop':
        print 'writing coordinates for GSOP, running ...'
        command = ['./run_mda_write_interimcoord.py','-f1',str(frame_first),\
                   '-f2',str(frame_last),'-t',run_type,'-p',pdb]
        # run_command(['./run_mda_write_interimcoord.py',str(frame_first),str(frame_last),run_type])
        run_command(command)

    else:
        print 'failed execute run_mda_write_interimcoord.py'
        sys.exit(1)
        # sys.exit()

for coord_file in lst_coords_files:
    if os.path.exists(coord_file) != True:
        write_interim_coords()



# run_tension on interimcoord(s)
# for path in sorted(glob(os.path.join(my_dir,'tension_coords/interimcoord*.pdb'))):
def get_tension(fn_tension):
    for path in lst_coords_files:
        dir_tension_coords = os.path.dirname(path)
        fn_molecule = os.path.basename(path)
        # print path
        # print dir_tension_coords
        # print fn_molecule
        cp_file(dir_tension_coords,fn_molecule,my_dir,fn_molecule)

        if run_type == 'sopnucleo':
            command_list = ['run_tension',str(resid_first),str(resid_last), \
                            'pdb%s4B9Q.pdb' % nucleotide,fn_molecule]
        elif run_type == 'gsop':
            # command_list = ['./run_tension',str(resid_first),str(resid_last), \
                            # 'pdb%s.pdb' % pdb,fn_molecule]
            command_list = ['run_tension',str(resid_first),str(resid_last), \
                            '2kho_nbd.pdb',fn_molecule]

            print command_list
        run_command(command_list)

        # break
        os.remove(os.path.join(my_dir,fn_molecule))
        # sys.exit()

    #  ---------------------------------------------------------  #
    #  get average!                                               #
    #  ---------------------------------------------------------  #
    dct_average = {}
    # lst_average = []
    for path in sorted(glob(os.path.join(my_dir,'tension_output/*.dat'))):
        # print path
        fn_base = os.path.basename(path)
        result = re.search('(?<=_)\d+',fn_base)
        num = result.group(0)
        data = np.loadtxt(path)

        # print 'data:',data.shape # if its 2800 to 3000, (201,11)
        # force = data[0:resid_last-1:,2] # ARRAY SIZE,column
        force = data[::,2] # ARRAY SIZE,column
        # print 'force:',force.shape # (201,)
        force_avg = np.mean(force)
        dct_average[int(num)] = force_avg

    #  ---------------------------------------------------------  #
    #  savefile                                                   #
    #  ---------------------------------------------------------  #
    lst_average = []
    for k,v in sorted(dct_average.iteritems()):
        # print 'building list','\t --->',k,v
        lst_average.append(v)
        averages = np.array(lst_average)

    # # print averages
    # if run_type == 'sopnucleo':
    #     np.savetxt('tensionaverage_%s_%d_%d_%d.dat' % (nucleotide,seed,frame_first,frame_last, \
    #                                                ),averages,fmt='%2.4f')
    # elif run_type == 'gsop':
    #     np.savetxt('tensionaverage_%s_%d_%d_%d.dat' % (pdb,seed,frame_first,frame_last, \
    #                                                ), averages,fmt='%2.4f')

    np.savetxt(fn_tension,averages,fmt='%2.4f')


# print averages
if run_type == 'sopnucleo':
    fn_tension = 'tensionaverage_%s_%d_%d_%d.dat' % (nucleotide,seed,frame_first,frame_last)
elif run_type == 'gsop':
    fn_tension = 'tensionaverage_%s_%d_%d_%d.dat' % (pdb,seed,frame_first,frame_last)

if not os.path.exists(fn_tension):
    get_tension(fn_tension)
else:
    print 'tension already computed!'
    time.sleep(1)


#  ---------------------------------------------------------  #
#  Chi_analysis                                               #
#  ---------------------------------------------------------  #
def run_chi_analysis(tup_resids):
    print 'running chi_analysis'

    fn_chi = 'chi_%s_frames_%d_%d_resids_%d_%d.dat' % (run_type,frame_first,frame_last,tup_resids[0],tup_resids[1])
    if os.path.exists(fn_chi):
        print fn_chi,'exists!!'
        return

    for path in lst_coords_files:
        # continue
        dir_tension_coords = os.path.dirname(path)
        fn_molecule = os.path.basename(path)
        # print path
        # print dir_tension_coords
        # print fn_molecule
        result = re.search('\d+',fn_molecule)
        num = int(result.group(0)) # file_01.dat => 01
        # print num
        # lst_coord_nums.append(num)
        # continue
        cp_file(dir_tension_coords,fn_molecule,my_dir,fn_molecule)

        if run_type == 'sopnucleo':
            # command_list = ['run_chi',str(resid_first),str(resid_last), \
            #                 str(resid_first),str(resid_last),
            #                 'pdb%s4B9Q.pdb' % nucleotide,fn_molecule]
            command_list = ['run_chi',str(tup_resids[0]),str(tup_resids[1]), \
                            str(tup_resids[0]),str(tup_resids[1]),
                            'pdb%s4B9Q.pdb' % nucleotide,fn_molecule]
        elif run_type == 'gsop':
            # command_list = ['run_chi',str(resid_first),str(resid_last), \
            #                 str(resid_first),str(resid_last),
            #                 '2kho_nbd.pdb',fn_molecule]
            command_list = ['run_chi',str(tup_resids[0]),str(tup_resids[1]), \
                            str(tup_resids[0]),str(tup_resids[1]),
                            '2kho_nbd.pdb',fn_molecule]

        print command_list
        # time.sleep(0.14)
        run_command(command_list)

        # break
        os.remove(os.path.join(my_dir,fn_molecule))
        # sys.exit()
    print 'ran chi_analysis for %d to %d' % (tup_resids[0],tup_resids[1])
    time.sleep(2)

    # Chi_residue_117.dat*  Chi_residue_144.dat*  Chi_residue_18.dat*   Chi_residue_45.dat*
    lst_chi_files = glob(os.path.join(my_dir,'Chi_residue*'))
    dct_chi_files = {}

    for path in lst_chi_files:
        fn_base = os.path.basename(path)
        print fn_base
        result = re.search('(?<=_)\d+',fn_base)
        num = int(result.group(0))
        print num,type(num)
        data = np.loadtxt(path)
        print data.shape
        avg_chi_value = np.mean(data)
        dct_chi_files[num] = {}
        dct_chi_files[num]['fn'] = fn_base
        dct_chi_files[num]['fp'] = path
        dct_chi_files[num]['chi'] = avg_chi_value
        os.remove(path)

    lst_chi_avg = []
    for k,v in sorted(dct_chi_files.iteritems()):
        # print k,v['fp'],v['fn']
        print k,v['fn'],v['chi']
        lst_chi_avg.append(v['chi'])


    chi = np.array(lst_chi_avg)
    # np.savetxt('chi_%s_frames_%d_%d_resids_%d_%d.dat' % (run_type,frame_first,frame_last,\
    #                                                      tup_resids[0],tup_resids[1]),chi,fmt='%0.6f')
    np.savetxt(fn_chi,chi,fmt='%0.6f')


# C-Term 187-340,340-383
# N-Term 40 - 115,1-39,116-169
# Linker 170 - 187
segments = [(1,39),(40,115),(116,169),(170,187),(188,340),(341,382)]
[run_chi_analysis(t) for t in segments]
# run_chi_analysis((341,382))


#  ---------------------------------------------------------  #
#  pytension                                                  #
#  ---------------------------------------------------------  #
sys.exit()

py_averages = []
for path in sorted(glob(os.path.join(my_dir,'pytension/*.dat'))):
    # print path
    fn_base = os.path.basename(path)
    result = re.search('(?<=_)\d+',fn_base)
    num = result.group(0)
    data = np.loadtxt(path)
    py_averages.append(data[::,2])
    # force = data[0:resid_last-1:,2]       # ARRAY SIZE,column
    # force_avg = np.mean(force)
    # dct_average[int(num)] = force_avg
pyav = np.array(py_averages)
print pyav.shape
# sys.exit()
# pymean = np.mean(pyav,axis=1)
pymean = np.mean(pyav,axis=0)
print pymean.shape
# print len(py_averages)
# for it in py_averages:
#     print it
#     print it.shape
# sys.exit()
np.savetxt('pyten_%s_%d_%d_%d.dat' % (pdb,seed,frame_first,frame_last, \
                                                ), pymean,fmt='%2.6f')
