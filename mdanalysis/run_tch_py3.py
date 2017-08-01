#!/usr/bin/python2
# #!/usr/bin/env python
import sys
import os
import time
from glob import glob
import re
import numpy as np
# import subprocess

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
from mylib.run_command import run_command
from mdanalysis.MoleculeUniverse import MoleculeUniverse

# sys.path.append(os.path.join(my_library,'mdtraj'))
from MDTraj.MDTraj import *

# run_command(['ls','-l'])
# sys.exit()

# #  ---------------------------------------------------------  #
# #  subprocess                                                 #
# #  ---------------------------------------------------------  #
# def run_command(invocation):
#     pipe=subprocess.Popen(invocation,stdin=subprocess.PIPE,
#                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     stdout,stderr = pipe.communicate()
#     print 'stdout >> ',stdout
#     print 'stderr >> ',stderr


#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--ignore",help="num_chains_ignored",type=int)
    parser.add_argument("-c","--chains",help="num_chains",type=int)
    parser.add_argument("-r1","--resid1",help="first resid",type=int)
    parser.add_argument("-r2","--resid2",help="last resid",type=int)
    parser.add_argument("-h1","--hresid1",help="first resid for hsa",type=int)
    parser.add_argument("-h2","--hresid2",help="last resid for hsa",type=int)
    parser.add_argument("-f1","--frame1",help="first frame",type=int)
    parser.add_argument("-f2","--frame2",help="last frame",type=int)
    parser.add_argument("-seed","--seed",help="Langevin seed used in trajectory acquisition",type=int)
    parser.add_argument("-nuc","--nucleotide",help="nucleotide, either ADP or ATP")
    parser.add_argument("-t","--run_type",help="for what type of analysis is this, gsop or sopnucleo")
    parser.add_argument("-p","--pdb",help="PDB code, i.e. 2KHO,4B9Q")
    parser.add_argument("-step","--step",help="step by frames",type=int)
    parser.add_argument("-o","--option",help="run options: clean, all, tension, chi, hsa, debug")
    parser.add_argument("-psf","--psf",help="psf")
    parser.add_argument("-dcd","--dcd",help="dcd")
    parser.add_argument("-sel","--selection",help="valid MDAnalysis selection")
    args = vars(parser.parse_args())
    # return parser.parse_args()
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
num_chains = args['chains']
num_chains_i = args['ignore']
frame_first = args['frame1']
frame_last  = args['frame2']
resid_first = args['resid1']
resid_last  = args['resid2']
hresid_first = args['hresid1']
hresid_last  = args['hresid2']
nucleotide  = args['nucleotide']
seed = args['seed']
run_type = args['run_type']
pdb = args['pdb']
step = args['step']
option = args['option']
sel = args['selection']
sel = re.sub("_"," ",sel)


# print 'option:',option
# sys.exit()

# my_dir
my_dir = os.path.abspath(os.path.dirname(__file__))


# interim_coord
if not os.path.exists(os.path.join(my_dir,'interim_coord')):
    os.makedirs(os.path.join(my_dir,'interim_coord'))

# tension
# tension_output
# if not os.path.exists(os.path.join(my_dir,'tension_coords')):
#     os.makedirs('tension_coords')
# if not os.path.exists(os.path.join(my_dir,'tension_output')):
#     os.makedirs('tension_output')

# clean out the directories: tension_output, interim_coord
if option == 'clean':
    for path in os.listdir('tension_output'):
        fp_path = os.path.join(my_dir,'tension_output',path)
        os.remove(fp_path)
    for path in os.listdir('interim_coord'):
        fp_path = os.path.join(my_dir,'interim_coord',path)
        os.remove(fp_path)
    print("cleaned tension_output, interim_coord")
    sys.exit()

print(args['psf'])

if args['psf'] != None:
    psf = os.path.normpath(os.path.join(my_dir,args['psf']))
    print('the psf is now:',psf)
if args['dcd'] != None:
    dcd = os.path.normpath(os.path.join(my_dir,args['dcd']))
# sys.exit()

if args['hresid1'] == None and args['hresid2'] == None:
    hresid_first = args['resid1']
    hresid_last  = args['resid2']
    try:
        print('using resid1,2 %d,%d instead of hresid1,2 ...' % (args['resid1'],args['resid2']))
    except TypeError:
        pass


# debug
if option == 'debug':
    print('frame_first:',frame_first)
    print('frame_last:',frame_last)
    print('resid_first:',resid_first)
    print('resid_last:',resid_last)
    print('hresid_first:',hresid_first)
    print('hresid_last:',hresid_last)
    print('nucleotide:',nucleotide)
    print('seed:',seed)
    print('run_type:',run_type)
    print('pdb:',pdb)
    print('step:',step)
    print('psf:',psf)
    print('dcd:',dcd)
    print('exiting ...')
    sys.exit()
else:
    try:
        print(psf)
        print(dcd)
    except NameError:
        pass



#  ---------------------------------------------------------  #
#  workflow-hsa                                               #
#  ---------------------------------------------------------  #
# 1. call run_mda_write_interimcoord.py
#    write_interim_coords with appropriate residues
# 2. call pulchra
# 3. call run_area
# 4. extract/collect surface areas as 2d array: frame_number | hsa


def call_write_coords():
    # dcd = os.path.expanduser('~/ext/completed/sopnucleo/hsp70nbd_unsignedint/atp/sopnuc_atp_unsigned_sopnucleo__07-01-2014__131_1098398/Coord/ATP4B9Q.dcd')
    # psf = os.path.expanduser('~/ext/completed/sopnucleo/ATP4B9Q.psf')
    # dcd = os.path.expanduser('~/ext/completed/sopnucleo/hsp70nbd_2bil_int/too-large-int-atpadp-defaults/adp-default/adp-def_runsopnuc__84__04-17-2014_0014__84_621235/Coord/ADP4B9Q.dcd')
    # psf = os.path.expanduser('~/ext/completed/sopnucleo/ADP4B9Q.psf')
    # dcd = os.path.expanduser('~/ext/completed/gsop/gsop_nbd_doubled-4-11-139-169/nbd_orig2x4-11-139-169__2kho__280_7743741__09-03-2014_1021/dcd/2KHO_D30_pull.dcd')
    # psf = os.path.expanduser('~/ext/completed/gsop/psfgsop2KHO.psf')
    # dcd = os.path.expanduser('~/ext/completed_sbd/gsop/5.alpha158/sbd_a158__2khosbd__153_1635976__01-26-2015_1834/dcd/2khosbd_D30_pull.dcd')
    # psf = os.path.expanduser('~/ext/completed_sbd/gsop/sbd_gsop.psf')
    # ~/ext/completed_sbd/gsop/sbd_gsop.psf
    print(psf)
    print(dcd)
    x = MoleculeUniverse(my_dir,psf,dcd,my_dir,option)
    x.write_coords(resid_first,resid_last,frame_first,frame_last,step,sel)
    # if (option != 'mtcon'):
    #     x.write_coords(resid_first,resid_last,frame_first,frame_last,step,sel)
    # else:
    #     x.write_coords_(resid_first,resid_last,frame_first,frame_last,step,sel)

def call_mdtraj():
    pdb = glob('*.ref*.pdb')[0]
    dcd = glob('*/*pull*dcd')[0]
    x = MDTraj(my_dir,my_dir,dcd,pdb,sel)
    x.print_class()
    start = frame_first
    stop = frame_last
    x.write_traj(start,stop,step)
    # x = MoleculeUniverse(my_dir,psf,dcd,my_dir,option)
    # x.write_coords(resid_first,resid_last,frame_first,frame_last,step,sel)
    # if (option != 'mtcon'):
    #     x.write_coords(resid_first,resid_last,frame_first,frame_last,step,sel)
    # else:
    #     x.write_coords_(resid_first,resid_last,frame_first,frame_last,step,sel)


def call_pulchra(code=0):
    '''
    Writes interim_f1_r-4-385.pdb -> interim_f1_r-4-385.rebuilt.pdb if rebuilt has not been written.
    '''
    # print sys.args[::]
    print(args)
    # sys.exit()
    if os.getcwd().split('/')[-1] != 'interim_coord':
        os.chdir('interim_coord')
    if code == 7:
        lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,1,604) for i in range(frame_first,frame_last+1,step)]
        # lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,1,604) for i in range(frame_first,frame_last+1,step)]
    elif code == 603:
        lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,383,603) for i in range(frame_first,frame_last+1,step)]
    elif code == 24:
        lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,389,604) for i in range(frame_first,frame_last+1,step)]
    else:
        # print '<call_pulchra>',resid_first,resid_last
        print('<call_pulchra>',resid_first,resid_last)
        lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # print lst_interim_coords

    # temp_coord_list = []
    # for i,coord in enumerate(lst_interim_coords):
    #     print coord
    #     temp_coord_file = re.sub('\.pdb','-temp.pdb',coord)
    #     print temp_coord_file
    #     if not os.path.exists(temp_coord_file):
    #         with open(temp_coord_file,'w+') as fw:
    #             with open(coord,'r+') as fp:
    #                 for line in fp.readlines():
    #                     if line.startswith('ATOM'):
    #                         fw.write(line)
    #             fw.write("END\n")
    #     # temp_coord_file = ['interim_f%d_r-%d-%d-temp.pdb']
    #     temp_coord_list.append(temp_coord_file)
    # # sys.exit()

    for i,coord in enumerate(lst_interim_coords):
    # for i,coord in enumerate(temp_coord_list):
        # rebuilt_coord = re.sub('-temp\.pdb','rebuilt.pdb',coord)
        rebuilt_coord = re.sub('pdb','rebuilt.pdb',coord)
        # print rebuilt_coord
        # print os.listdir(os.getcwd())
        # continue
        if not os.path.exists(rebuilt_coord):
        # os.remove(rebuilt_coord)
        # if 1:
            run_command(['which','pulchra'])
            print('building with pulchra..',rebuilt_coord)
            # print i,os.getcwd()
            run_command(['pulchra','-v',coord])
        else:
            run_command(['which','pulchra'])
            print('previously built:',rebuilt_coord)


def call_run_contacts():
    '''
    Writes interim_f1_r-4-385.pdb
    '''
    os.chdir('interim_coord')

    if not os.path.exists(os.path.join(my_dir,'contact_maps')):
        os.makedirs(os.path.join(my_dir,'contact_maps'))

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    for i,coord in enumerate(lst_interim_coords,frame_first):
        # print i
        # print os.getcwd()
        run_command(['run_contacts_calpha_res_count',coord,str(resid_last-resid_first+1)])
        # os.rename('Contact_map_residue_index_array.dat','Contact_map_residue_index_array_f%d.dat' % i)
        cp_file(os.getcwd(),'Contact_map_residue_index_array.dat',os.path.join(my_dir,'contact_maps'),\
                'Contact_map_residue_index_array_f%d.dat' % i)


def call_run_new_contacts():
    '''
    Writes interim_f1_r-4-385.pdb
    '''
    os.chdir('interim_coord')
    # print my_dir
    contact_dir = os.path.join(my_dir,'contact_maps_new')
    interim_dir = os.path.join(my_dir,'interim_coord')
    # sys.exit()

    if not os.path.exists(os.path.join(my_dir,'contact_maps_new')):
        os.makedirs(os.path.join(my_dir,'contact_maps_new'))

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    for i,coord in enumerate(lst_interim_coords,frame_first):
        # print i
        os.chdir(contact_dir)
        cp_file(interim_dir,coord,contact_dir,coord)
        print("check the call_run_new_contacts function for the correct reference coords")
        # run_command(['run_contacts_new','pdbref.ent',coord]) # MAY 28th.
        # run_command(['run_analyze','pdbref.ent',coord]) # August 8, 2015.
        run_command(['run_segment_contact','pdbref.ent',coord,str(num_chains),str(num_chains_i)])
        print(coord)
        os.remove(coord)
        # cp_file(os.getcwd(),'Contact_map_residue_index_array.dat',os.path.join(my_dir,'contact_maps'),\
        #         'Contact_map_residue_index_array_f%d.dat' % i)

def call_bond_vector_angle():
    '''
    Writes interim_f1_r-4-385.pdb
    '''
    os.chdir('interim_coord')
    # print my_dir
    contact_dir = os.path.join(my_dir,'contact_maps_new')
    interim_dir = os.path.join(my_dir,'interim_coord')
    # sys.exit()

    if not os.path.exists(os.path.join(my_dir,'contact_maps_new')):
        os.makedirs(os.path.join(my_dir,'contact_maps_new'))

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    for i,coord in enumerate(lst_interim_coords,frame_first):
        # print i
        os.chdir(contact_dir)
        cp_file(interim_dir,coord,contact_dir,coord)
        # print "check the call_run_new_contacts function for the correct reference coords"
        # run_command(['run_contacts_bond_vector_angle','pdbref.ent',coord]) # May 28th.
        run_command(['run_analyze_orig','pdbref.ent',coord])
        print(coord)
        os.remove(coord)
        # cp_file(os.getcwd(),'Contact_map_residue_index_array.dat',os.path.join(my_dir,'contact_maps'),\
        #         'Contact_map_residue_index_array_f%d.dat' % i)

def call_proto_angle():
    '''
    Writes interim_f1_r-4-385.pdb
    '''
    os.chdir('interim_coord')
    # print my_dir
    contact_dir = os.path.join(my_dir,'contact_maps_new')
    interim_dir = os.path.join(my_dir,'interim_coord')
    # sys.exit()

    if not os.path.exists(os.path.join(my_dir,'contact_maps_new')):
        os.makedirs(os.path.join(my_dir,'contact_maps_new'))

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    for i,coord in enumerate(lst_interim_coords,frame_first):
        # print i
        os.chdir(contact_dir)
        cp_file(interim_dir,coord,contact_dir,coord)
        # print "check the call_run_new_contacts function for the correct reference coords"
        # run_command(['run_contacts_bond_vector_angle','pdbref.ent',coord]) # May 28th.
        run_command(['run_analyze_proto',coord,'14','2','14','257'])
        print(coord)
        os.remove(coord)
        # cp_file(os.getcwd(),'Contact_map_residue_index_array.dat',os.path.join(my_dir,'contact_maps'),\
        #         'Contact_map_residue_index_array_f%d.dat' % i)

def call_mtcon():
    '''
    Writes interim_f1_r-4-385.pdb
    '''
    os.chdir('interim_coord')
    contact_dir = os.path.join(my_dir,'contact_maps_new')
    interim_dir = os.path.join(my_dir,'interim_coord')

    if not os.path.exists(os.path.join(my_dir,'contact_maps_new')):
        os.makedirs(os.path.join(my_dir,'contact_maps_new'))

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    for i,coord in enumerate(lst_interim_coords,frame_first):
        # print i
        os.chdir(contact_dir)
        cp_file(interim_dir,coord,contact_dir,'timelater.pdb')
        print(coord)
        run_command(['run_segment_mtcon','ref.pdb','timelater.pdb',str(num_chains),str(num_chains_i)])
        # os.remove(coord)



def call_run_area(code=0):
    # lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    # print os.getcwd().split('/')[-1]
    # sys.exit()
    if os.getcwd().split('/')[-1] != 'interim_coord':
        os.chdir('interim_coord')
    if code == 0:
        lst_interim_coords = ['interim_f%d_r-%d-%d.rebuilt.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # lst_interim_coords = ['interim_f%d_r-%d-%d.rebuilt.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # for coord in lst_interim_coords:
        #     area_atom = 'Area_atom.' + coord
        #     area_aa = 'Area_aa.' + coord
        #     ratio_aa = 'Ratio_aa.' + coord
            # if (not os.path.exists(area_atom) or not os.path.exists(area_aa) or not os.path.exists(ratio_aa)):
            #     print 'run_area:',coord
            #     # run_command(['run_area',coord]) # run_area_orig
            #     # has the 4 385 (NBD) -> 1 382 effect 4-4+1, 385-4+1
            #     run_command(['run_area',coord,str(hresid_first-resid_first+1),str(hresid_last-resid_first+1)])
    elif (code == 7 or code == 603):
        if code == 7:
            lst_interim_coords = ['interim_f%d_r-%d-%d.rebuilt.pdb' % (i,1,604) for i in range(frame_first,frame_last+1,step)]
        if code == 603:
            lst_interim_coords = ['interim_f%d_r-%d-%d.rebuilt.pdb' % (i,383,603) for i in range(frame_first,frame_last+1,step)]
        # for coord in lst_interim_coords:
        #     area_atom = 'Area_atom.' + coord
        #     area_aa = 'Area_aa.' + coord
        #     ratio_aa = 'Ratio_aa.' + coord
            # if not os.path.exists(area_atom) or not os.path.exists(area_aa) or not os.path.exists(ratio_aa):
            #     print 'run_area:',coord
            #     # run_command(['run_area',coord]) # run_area_orig
            #     # has the 4 385 (NBD) -> 1 382 effect 4-4+1, 385-4+1
            #     run_command(['run_area',coord,str(hresid_first-resid_first+1),str(hresid_last-resid_first+1)])
    else:
        # lst_interim_coords = ['interim_f%d_r-%d-%d.rebuilt.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        print('trying to run on non-rebuilt structures??')
        sys.exit(1)
        # lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]

        # for coord in lst_interim_coords:
        #     # area_atom = 'Area_atom.' + coord
        #     # area_aa = 'Area_aa.' + coord
        #     # ratio_aa = 'Ratio_aa.' + coord
        #     # if not os.path.exists(area_atom) or not os.path.exists(area_aa) or not os.path.exists(ratio_aa):
        #     #     print 'run_area:',coord
        #     #     # run_command(['run_area',coord]) # run_area_orig
        #     #     # has the 4 385 (NBD) -> 1 382 effect 4-4+1, 385-4+1
        #     print 'run_area',coord,str(hresid_first-resid_first+1),str(hresid_last-resid_first+1)
        #     run_command(['run_area',coord,str(hresid_first-resid_first+1),str(hresid_last-resid_first+1)])


    # final.
    for coord in lst_interim_coords:
        area_atom = 'Area_atom.' + coord
        area_aa = 'Area_aa.' + coord
        ratio_aa = 'Ratio_aa.1.%s.' % (str(resid_last-resid_first+1)) + coord
        #           Ratio_aa.1.65.interim_f8805_r-397-461.rebuilt.pdb
        print(ratio_aa)
        print(resid_last,resid_last - resid_first)
        # sys.exit()
        # if (not os.path.exists(area_atom) or not os.path.exists(area_aa) or not os.path.exists(ratio_aa)):
        if not os.path.exists(ratio_aa):
            print('run_area:',coord)
            # run_command(['run_area',coord]) # run_area_orig
            # has the 4 385 (NBD) -> 1 382 effect 4-4+1, 385-4+1
            run_command(['run_area',coord,str(hresid_first-resid_first+1),str(hresid_last-resid_first+1)])
        else:
            print('run_area:',coord,'done previously.')

    # for coord in lst_interim_coords:
    #     rebuilt_coord = re.sub('pdb','rebuilt.pdb',coord)
    #     if not os.path.exists(rebuilt_coord):
    #         run_command(['pulchra',coord])


def get_hsa(code):
    lst_hydro = []
    lst_frames= []
    lst_zipped = []
    os.chdir(os.path.join(my_dir,'interim_coord'))

    # builds exact set required for analysis
    if code == 90:
        lst_ratios = ['Ratio_aa.%d.90.interim_f%d_r-%d-%d.pdb' % (hresid_first-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    elif code == 7:
        # print hresid_last-resid_first+1
        # sys.exit()
        # lst_ratios = ['Ratio_aa.%d.%d.interim_f%d_r-%d-%d.rebuilt.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        lst_ratios = ['Ratio_aa.%d.%d.interim_f%d_r-1-604.rebuilt.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i) for i in range(frame_first,frame_last+1,step)]
        # Ratio_aa.1.216.interim_f7001_r-1-604.rebuilt.pdb
        # Ratio_aa.1.7.interim_f7001_r-1-604.rebuilt.pdb
    elif code == 603:
        lst_ratios = ['Ratio_aa.%d.%d.interim_f%d_r-383-603.rebuilt.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i) for i in range(frame_first,frame_last+1,step)]
    else:
        lst_ratios = ['Ratio_aa.%d.%d.interim_f%d_r-%d-%d.rebuilt.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # lst_ratios = ['Ratio_aa.%d.%d.interim_f%d_r-%d-%d.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # lst_ratios = ['interim_f%d_r-%d-%d.pdb' % (hresid_first-resid_first+1,hresid_last-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # NOTE -4
        # lst_ratios = ['Ratio_aa.%d.203.interim_f%d_r-%d-%d.pdb' % (hresid_first-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # lst_ratios = ['Ratio_aa.%d.102.interim_f%d_r-%d-%d.pdb' % (hresid_first-resid_first+1,i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
        # lst_ratios.pop(0)
        #                         CHANGE!!!
    # print lst_ratios
    for i,ratio in enumerate(lst_ratios,frame_first):
        print(i,ratio)
        o = open(ratio,'r+')
        final_line = o.readlines()[-1]
        hydrophobes_exposed = final_line.split()[-1]
        print(final_line,hydrophobes_exposed,'\n')
        o.close()
        frame = int(re.search('_f(\d+)',ratio).groups(1)[0])
        lst_frames.append(frame)
        lst_hydro.append(float(hydrophobes_exposed))
    lst_zipped = zip(lst_frames,lst_hydro)

    hsa_data = np.array(sorted(lst_zipped))
    script_args = (' ').join(sys.argv)
    os.chdir(my_dir)
    # np.savetxt('hsa_r%d-%d_f%d-%d.dat' % (resid_first,resid_last,frame_first,frame_last),hsa_data,\
    #            fmt='%0.0f %0.3f',header=script_args)
    np.savetxt('hsa_r%d-%d_h%d-%d_f%d-%d.dat' % (resid_first,resid_last,hresid_first,hresid_last,frame_first,frame_last),\
               hsa_data,fmt='%0.0f %0.3f',header=script_args)

# get_hsa()


#  ---------------------------------------------------------  #
#  tension                                                    #
#  ---------------------------------------------------------  #
def get_tension(fn_tension):
    # must clean out tension_output when you run tension
    os.chdir(my_dir)
    lst_tension_output = glob(os.path.join(my_dir,'tension_output/*'))
    for path in lst_tension_output:
        # print path
        os.remove(path)
    # for path in os.listdir(os.path.join(my_dir,'tension_output')):
    #     print path
    #     # fp_path = os.path.join(my_dir,'tension_output',path)
    #     os.remove(fp_path)

    # sys.path.append('~/sop_dev/tension')
    # print sys.path
    # lst_interim_coords = glob('interim_coord/interim_*')
    # [lst_interim_coords.pop(i) for i,item in enumerate(lst_interim_coords) if re.search('rebuilt',item) != None]

    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]
    # print lst_interim_coords
    # sys.exit()
    # interim_f800_r-383-603.pdb

    for interim_coord in lst_interim_coords:
        # break
        dir_coord = os.path.join(my_dir,'interim_coord')
        coord = os.path.basename(interim_coord)
        # print coord
        # print dir_coord
        cp_file(dir_coord,coord,my_dir,coord)
        # sys.exit()

        if run_type == 'sopnucleo':
            command_list = ['run_tension',str(resid_first),str(resid_last), \
                            'pdb%s4B9Q.pdb' % nucleotide,coord]

        elif run_type == 'gsop':
            command_list = ['run_tension',str(resid_first),str(resid_last), \
                            '2kho_nbd.pdb',coord]

        elif run_type == 'sbd':
            if not os.path.exists(os.path.join(my_dir,'2khosbd.pdb')):
                os.system('ln -s /home/dale/sop_dev/molecules/hsp70/pdb2khosbd_CA.ent 2khosbd.pdb')
                # cp_file(os.path.expanduser('~/sop_dev/molecules'),'2kho_sbd.pdb',my_dir,'2kho_sbd.pdb')
            command_list = ['run_tension',str(resid_first),str(resid_last),
                            '2khosbd.pdb',coord]
            # command_list = ['run_tension',str(resid_first),str(resid_last),
            #                 '~/sop_dev/tension/2kho_sbd.pdb',coord]
                    # 2kho_sbd.pdb

        print('tension_command_list:',command_list)
        # print os.getcwd()
        run_command(command_list)
        os.remove(coord)

    #  ---------------------------------------------------------  #
    #  get average!                                               #
    #  ---------------------------------------------------------  #
    dct_average = {}
    lst_tensions = glob(os.path.join(my_dir,'tension_output/*.dat'))
    # print len(lst_tensions)
    # lst_tensions = ['tension_output/tension_%d.dat' % i for i in range(resid_first,resid_last)]
    # print len(lst_tensions)
    # sys.exit()
    if len(lst_tensions) == 0:
        print('no tension files found!')
        sys.exit()
        # for path in sorted(glob(os.path.join(my_dir,'tension_output/*.dat'))):
    # print sorted(lst_tensions)
    time.sleep(3)
    for path in sorted(lst_tensions):
        # print path
        fn_base = os.path.basename(path)
        result = re.search('(?<=_)\d+',fn_base)
        num = result.group(0)
        data = np.loadtxt(path)
        force = data[::,2] # ARRAY SIZE,column
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

    np.savetxt(fn_tension,averages,fmt='%2.4f')


#  ---------------------------------------------------------  #
#  Chi_analysis                                               #
#  ---------------------------------------------------------  #
def run_chi_analysis(tup_resids):
    print('running chi_analysis')

    fn_chi = 'chi_%s_frames_%d_%d_resids_%d_%d.dat' % (run_type,frame_first,frame_last,tup_resids[0],tup_resids[1])
    if os.path.exists(fn_chi):
        print(fn_chi,'exists!!')
        return

    # lst_interim_coords = glob('interim_coord/interim_*')
    # [lst_interim_coords.pop(i) for i,item in enumerate(lst_interim_coords) if re.search('rebuilt',item) != None]
    lst_interim_coords = ['interim_f%d_r-%d-%d.pdb' % (i,resid_first,resid_last) for i in range(frame_first,frame_last+1,step)]


    for path in lst_interim_coords:
        dir_coords = os.path.join(my_dir,'interim_coord')
        fn_molecule = os.path.basename(path)
        # print path
        # print dir_coords
        # print fn_molecule
        result = re.search('\d+',fn_molecule)
        num = int(result.group(0)) # file_01.dat => 01


        # copy rebuit coord file into my_dir
        cp_file(dir_coords,fn_molecule,my_dir,fn_molecule)


        if run_type == 'sopnucleo':
            print('need right molecule!?')
            # find the molecule
            sys.exit()
            command_list = ['run_chi',str(tup_resids[0]),str(tup_resids[1]), \
                            str(tup_resids[0]),str(tup_resids[1]),
                            'pdb%s4B9Q.pdb' % nucleotide,fn_molecule]

        elif run_type == 'gsop':
            if not os.path.exists(os.path.join(my_dir,'2kho_nbd.pdb')):
                cp_file(os.path.expanduser('~/sop_dev/tension'),'2kho_nbd.pdb',my_dir,'2kho_nbd.pdb')
            command_list = ['run_chi',str(tup_resids[0]),str(tup_resids[1]), \
                            str(tup_resids[0]),str(tup_resids[1]),
                            '2kho_nbd.pdb',fn_molecule]

        elif run_type == 'sbd':
            # if not os.path.exists(os.path.join(my_dir,'2kho_sbd.pdb')):
            if not os.path.exists(os.path.join(my_dir,'2khosbd.pdb')):
                os.system('ln -s /home/dale/sop_dev/molecules/hsp70/pdb2khosbd_CA.ent 2khosbd.pdb')
                # cp_file(os.path.expanduser('~/sop_dev/tension'),'2kho_sbd.pdb',my_dir,'2kho_sbd.pdb')
            command_list = ['run_chi',str(tup_resids[0]-382),str(tup_resids[1]-382), \
                            str(tup_resids[0]-382),str(tup_resids[1]-382),
                            '2khosbd.pdb',fn_molecule]
        # elif run_type == 'sbd':
        #     if not os.path.exists(os.path.join(my_dir,'2khosbd.pdb')):
        #         os.system('ln -s /home/dale/sop_dev/molecules/hsp70/pdb2khosbd_CA.ent 2khosbd.pdb')
        #         # cp_file(os.path.expanduser('~/sop_dev/molecules'),'2kho_sbd.pdb',my_dir,'2kho_sbd.pdb')
        #     command_list = ['run_tension',str(resid_first),str(resid_last),
        #                     '2khosbd.pdb',coord]


        # print command_list
        run_command(command_list)
        os.remove(os.path.join(my_dir,fn_molecule))


    print('ran chi_analysis for %d to %d' % (tup_resids[0],tup_resids[1]))

    # All Chi_residue files used in calculation but they get deleted in next for loop!
    # Chi_residue_117.dat*  Chi_residue_144.dat*  Chi_residue_18.dat*   Chi_residue_45.dat*
    lst_chi_files = glob(os.path.join(my_dir,'Chi_residue*'))


    # extra dictionary before, going to list
    dct_chi_files = {}
    for path in lst_chi_files:
        fn_base = os.path.basename(path)
        print(fn_base)
        result = re.search('(?<=_)\d+',fn_base)
        num = int(result.group(0))
        print(num,type(num))
        data = np.loadtxt(path)
        print(data.shape)

        # average computed
        avg_chi_value = np.mean(data)
        dct_chi_files[num] = {}
        dct_chi_files[num]['fn'] = fn_base # extra, gets deleted ... 3 line later
        dct_chi_files[num]['fp'] = path
        dct_chi_files[num]['chi'] = avg_chi_value
        os.remove(path)

    # from dictionary to list ... averages compiled, saved
    lst_chi_avg = []
    for k,v in sorted(dct_chi_files.iteritems()):
        # print k,v['fp'],v['fn']
        print(k,v['fn'],v['chi'])
        lst_chi_avg.append(v['chi'])
    chi = np.array(lst_chi_avg)

    np.savetxt(fn_chi,chi,fmt='%0.6f')

def compute_tension():
    call_write_coords()
    # print averages
    if run_type == 'sopnucleo':
        fn_tension = 'tensionaverage_%s_%d_%d_%d.dat' % (nucleotide,seed,frame_first,frame_last)
    elif run_type == 'gsop':
        fn_tension = 'tensionaverage_%s_%d_%d_%d.dat' % (pdb,seed,frame_first,frame_last)
    elif run_type == 'sbd':
        fn_tension = 'tensionaverage_%s_%d_%d_%d.dat' % (pdb,seed,frame_first,frame_last)

    if not os.path.exists(fn_tension):
        get_tension(fn_tension)
    else:
        print('tension already computed!')


def compute_chi():
    call_write_coords()
    # C-Term 187-340,340-383
    # N-Term 40 - 115,1-39,116-169
    # Linker 170 - 187
    if (run_type == 'gsop') or (run_type == 'sopnucleo'):
        segments = [(1,39),(40,115),(116,169),(170,187),(188,340),(341,382)]
    elif run_type == 'sbd':
        # segments = [(383,399),(400,491),(492,522),(523,603)] - previous
        segments = [(383,398),(399,460),(461,501),(502,531),(532,597)] #- new proposed, (598-603) excluded;
    [run_chi_analysis(t) for t in segments]


def compute_hsa():
    # call_write_coords()
    # # call_pulchra() # ATOMISTIC
    # call_run_area(1) # ATOMISTIC, use 1
    # get_hsa(1)

    # gsop
    call_write_coords()
    call_pulchra(0) # ATOMISTIC
    # call_run_area(0) # ATOMISTIC, use 1
    call_run_area(0) # ATOMISTIC, use 1
    get_hsa(0)

def compute_csu():
    print(pdb)
    # print psf
    # x = MoleculeUniverse(my_dir,psf,pdb,my_dir,option)
    # x.print_resids(resid_first,resid_last,1)
    for i in range(resid_first,resid_last+1,1):
        print(i)
        command_list = ["resc",pdb,str(i),"Y"]
        print('\n--------',command_list,'-----\n')
        run_command(command_list)


print('option:',option)
if option == 'all':
    print('running tension, chi and hsa')
    compute_tension()
    compute_chi()
    compute_hsa()
    compute_contacts()
    # compute_new_contacts()
    compute_bond_vector_angle() # if this, then no tension | costheta | contacts elsewhere
elif option == 'tension':
    compute_tension()
elif option == 'chi':
    compute_chi()
elif option == 'hsa':
    compute_hsa()
    # # gsop::
    # call_write_coords()
    # call_pulchra(0) # ATOMISTIC
    # call_run_area(0) # ATOMISTIC, use 1
    # get_hsa(0)
elif option == 'nopephsa':
    call_write_coords() # 1,604
    call_pulchra(603) # uses 1,604
    call_run_area(603) # run_tch.sh with 1 7, 383 604
    get_hsa(603)
elif option == 'pephsa':
    call_write_coords() # 1,604
    call_pulchra(7) # uses 1,604
    call_run_area(7) # run_tch.sh with 1 7, 389 604
    get_hsa(7)
elif option == 'mdtraj':
    call_mdtraj()
elif option == 'contacts':
    call_write_coords()
    call_run_contacts()
elif option == 'new_contacts':
    call_write_coords()
    call_run_new_contacts()
elif option == 'bond_vector_angle':
    # new_contacts, costheta, tension
    call_write_coords()
    call_bond_vector_angle()
elif option == 'hsab':
    compute_hsa()
    compute_bond_vector_angle() # if this, then no tension | costheta | contacts elsewhere
elif option == 'csu':
    compute_csu()
elif option == 'coords':
    call_write_coords()
elif option == 'proto':
    call_write_coords()
    call_proto_angle()
elif option == 'mtcon':
    call_write_coords()
    call_mtcon()
