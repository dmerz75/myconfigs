#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import shutil

import numpy as np
from cycler import cycler
import glob


# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *
# imports from my_library
# from mylib.cp import *
# from mylib.regex import *
from mylib.run_command import *
# from plot.WLC import WormLikeChain
# from plot.SOP import *
# from mdanalysis.MoleculeUniverse import MoleculeUniverse
from plot.SETTINGS import *
from MDTraj.MDTraj3 import MDTraj3

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    # parser.add_argument("-m","--makefile_arg",help="supply Makefile argument")
    parser.add_argument("-p","--peptide",help="is there a peptide? pep,nopep")
    parser.add_argument("-o","--option",help="option: None,show,publish")
    parser.add_argument("-st","--stage",help="stage 1,14,...",type=int)
    parser.add_argument("-t","--trajectory",help="trajectory 0,1,...",type=int)
    parser.add_argument("-c","--commandrun",help="None,1-hsa,2-check+hsa_dir(creates hsa_current),3-Remove interim_coord,4-plot,5-rename-current-new_dir",type=int)
    parser.add_argument("-n","--new_dir",help="New directory (-c 2)")
    # parser.add_argument("-s","--section",help="Section 0,1,2... [(397,603),(397,501),(510,603)]",type=int)
    parser.add_argument("-s","--section",help="Section 0,1,2,3..segments (397,460)(397,501)(510,600)(532,600)", \
                        type=int)
    # parser.add_argument("-n","--node",help="type of node for computation")
    args = vars(parser.parse_args())
    return args


args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
peptide = args['peptide']
option = args['option']
traj = args['trajectory']
commandrun = args['commandrun']
stage = args['stage']
section = args['section']
new_dir = args['new_dir']

# segments = [()] - 4
segments = [(0,170),(186,381),(393,456),(457,497),(393,497),(506,596),(528,596)]
segment = segments[section]
selection = "resid %d to %d" % (segment[0],segment[1])

if commandrun == 1:
    print(section)
    if section == None:
        print('must select a section: 0,1,2,3 .. segments')
        sys.exit(1)


def get_stage_dir(stage,cwd=my_dir):
    '''Get traj dir.
    '''
    print('stage:',stage)
    print('cwd:',cwd)
    dir_traj = os.path.join(cwd,'gsop_traj')
    print('dir_traj:',dir_traj)

    stages = [d for d in os.listdir(dir_traj)
              if os.path.isdir(os.path.join(dir_traj,d))]

    # dir_stages = [os.path.join(dir_traj,d) for d in stages]
    # print('stages:',stages)
    # print('dir_stages:',dir_stages)

    for s in stages:
        # print(s)
        if s.startswith(str(stage).zfill(2)):
            break
    sel_stage = s
    print('selected_stage:',sel_stage)

    dir_stage = os.path.join(dir_traj,sel_stage)
    return dir_stage

def write_frame_limit_file(dir_traj,l1,l2):
    '''Write the FRAME.f1.f2
    '''
    os.chdir(dir_traj)
    f = open("FRAME.%d.%d" % (l1,l2),"w+")
    f.write("#")
    f.close()
    os.chdir(my_dir)
    return



def load_dct(cwd=my_dir,pattern='*.dat'):
    # FindAllFiles
    print('cwd:',cwd)
    print('pattern:',pattern)
    dct_find = {'cwd':cwd,'pattern':pattern}
    x = FindAllFiles(dct_find)
    x.get_files()
    dct9 = x.sort_dirname(-1,x.dct)
    print(len(dct9.keys()),'of',x.total)
    return dct9

def run_hsa_analysis(dct):
    for i,k in enumerate(dct.keys()):
        if traj != None:
            if i != traj:
                continue
        print(i,k)
        print('dir:',dct[i]['dirname'])
        os.chdir(dct[i]['dirname'])
        # print os.listdir(os.getcwd())

        pdb = glob.glob('*.ref.*')[0]
        dcd = glob.glob('dcd/*pull.dcd')[0]
        print(pdb)
        print(dcd)


        try:
            frames = glob.glob('FRAME.*')[0]
        except IndexError:
            print('FRAME.* not found.')
            write_frame_limit_file(dct[i]['dirname'],0,25000)
            sys.exit(1)

        if frames.split('.')[0] == 'FRAME':
            frame1 = frames.split('.')[1]
            frame2 = frames.split('.')[2]
        else:
            print('need a FRAME.2.5004 file')
            sys.exit(1)

        step = 50

        resid1 = segment[0]
        resid2 = segment[1]

        if not os.path.exists('run_tch.py'):
            print('linking run_tch.py')
            tch_path = os.path.expanduser('~/.pylib/mdanalysis/run_tch.py')
            print(tch_path)
            run_command(['ln','-s',tch_path,'.'])

        if peptide == 'nopep':
            # resid1 = 383
            # resid2 = 603
            command = ['./run_tch.py','-o','hsa','-seed','1',
                       '-t sbd','-r1',str(resid1),'-r2',str(resid2),'-f1',frame1,
                       '-f2',frame2,'-step',str(step),'-c','1','-i','0',
                       '-psf',psf,'-dcd',dcd,
                       '-sel','resid_%d:%d' % (resid1,resid2)]

        elif peptide == 'pep':
            # resid1 = 389
            # resid2 = 604
            command = ['./run_tch.py','-o','hsa','-seed','1',
                       '-t sbd','-r1',str(resid1),'-r2',str(resid2),'-f1',frame1,
                       '-f2',frame2,'-step',str(step),'-c','2','-i','1',
                       '-psf',psf,'-dcd',dcd,
                       '-sel','resid_%d:%d' % (resid1,resid2)]
        print(command)
        # run_command(['echo','hello'])
        if commandrun == 1:
            run_command(command)

def check_hsa_analysis(dct):
    for i,k in enumerate(dct.keys()):

        os.chdir(dct[k]['dirname'])


        # FindAllFiles
        dct_hsa = {'cwd':dct[k]['dirname'],'pattern':'*.dat'}
        H = FindAllFiles(dct_hsa)
        set9 = H.get_files()
        # H.query_ [dirname,file,filename](searchstring,pos,dct)
        # H.remove_[dirname,file,filename](searchstring,pos,dct)
        set9 = H.query_file('hsa',set9)
        set9 = H.sort_dirname(-1,set9)
        H.print_query(set9)
        # set9
        print(len(set9.keys()),'of',H.total)

        # if ((not os.path.exists('hsa_current')) and (len(set9.keys()) != 0)):
        # if (not os.path.exists('hsa_%s' % new_dir)):
        if ((dct[traj]['dirname'] == dct[k]['dirname']) and (not os.path.exists('hsa_current'))):
            print('making hsa_current')
            os.makedirs('hsa_current')

        # hcount = 0
        for h in set9.keys():
            # print h
            if os.path.basename(set9[h]['dirname']) == os.path.basename(dct[k]['dirname']):
                new_hsa_cur = os.path.join(dct[k]['dirname'],'hsa_current',set9[h]['filename'])
                # print 'moving to hsa_current:',new_hsa_cur
                # hcount += 1
                os.rename(set9[h]['file'],new_hsa_cur)

        lst_hsa = glob.glob('hsa_current/hsa*.dat') # 1

        if len(lst_hsa) > 0:
            print('base:',os.path.basename(dct[k]['dirname']))
            print(lst_hsa)


def rename_current_hsadir(dct):
    for i,k in enumerate(dct.keys()):
        os.chdir(dct[k]['dirname'])

        if os.path.exists('hsa_current'):
            # print 'making hsa_current'
            # os.makedirs('hsa_current')
            print(dct[k]['dirname'])
            print('renaming hsa_current to hsa_%s' % new_dir)
            shutil.move('hsa_current','hsa_%s' % new_dir)


def remove_interim_dir(dct):
    for i,k in enumerate(dct.keys()):
        os.chdir(dct[k]['dirname'])
        if os.path.exists(os.path.join(dct[k]['dirname'],'interim_coord')):
            # os.makedirs(new_dir)
            print('removing interim_coord')
            shutil.rmtree('interim_coord')

def plot_hsa(dct):
    print('inside PLOT')
    #  ---------------------------------------------------------  #
    #  Start matplotlib (1/4)                                     #
    #  ---------------------------------------------------------  #
    fig = plt.figure(0)

    gs = GridSpec(1,1)
    ax1 = plt.subplot(gs[0,:])
    # ax2 = plt.subplot(gs[1,:-1])
    ax = [ax1]

    #  ---------------------------------------------------------  #
    #  Import Data! (2/4)                                         #
    #  ---------------------------------------------------------  #
    result_type = 'gsop' # sop | sopnucleo | gsop | namd
    # plot_type = 'hsa_r460' # fe | tension | rmsd | rdf
    plot_type = 'hsa_%s' % new_dir # fe | tension | rmsd | rdf
    # data_name = peptide + str(traj) + str(segment[0]) + str(segment[1])
    data_name = peptide + '_stage%s_' % str(stage) + str(traj)
    print(data_name)

    #  ---------------------------------------------------------  #
    #  Import Data! (3/4)                                         #
    #  ---------------------------------------------------------  #
    for i,k in enumerate(dct.keys()):
        print(i,k)
        if traj != i:
            continue
        print('changing to:',dct[k]['dirname'])
        os.chdir(dct[k]['dirname'])
        # lst_hsa = sorted(glob.glob('hsa*.dat')) # 2
        print('new_dir:',new_dir)
        lst_hsa = sorted(glob.glob('hsa_%s/hsa*.dat' % new_dir))
        print(lst_hsa)
        if not lst_hsa:
            print("no hsa files found.")
            sys.exit(1)

        s = plt.axhline(0.5,color='blue',linewidth=3.0)

        for fh in lst_hsa:
            print('fh:',fh)
            resids = re.search('_h(\d+)-(\d+)',fh.split('/')[-1])
            # print resids.group(0)
            print('groups:',resids.groups())

            print('stage:',stage,type(stage))

            h1 = int(resids.groups()[0])
            h2 = int(resids.groups()[1])
            print(h1,h2)
            # segments = [(397,426),(430,460),(397,460),(397,481)]
            # segments = [(397,426),(430,460),(397,460),(397,501)]
            # segments = [(397,460),(397,491),(397,501),(510,600),(532,600)]
            # segments = [(397,426),(430,460),(397,501),(510,600),(532,600)]

            # segments = [(397,426),(430,460),(461,501),(397,501),(510,600),(532,600)]

            # segments = [(397,460),(461,501),(397,501),(510,600),(532,600)]

            if ((h1 == 397) and (h2 == 426)):
                color = 'lime'
                linestyle = '--'
            elif ((h1 == 430) and (h2 == 460)):
                color = 'lime'
                linestyle = '-.'

            elif ((h1 == 397) and (h2 == 460)):
                color = 'lime'
                linestyle = '-'
            elif ((h1 == 461) and (h2 == 501)):
                color = 'mediumseagreen'
                linestyle = '-'
            elif ((h1 == 397) and (h2 == 501)):
                color = 'g'
                linestyle = '-'
            elif ((h1 == 510) and (h2 == 600)):
                color = 'r'
                linestyle = '-'
            elif ((h1 == 532) and (h2 == 600)):
                color = 'r'
                linestyle = '--'


            print('ls:',linestyle,'color:',color)
            res_label = ('-').join(resids.groups())
            print(res_label)
            data = np.loadtxt(fh)
            data[::,0] = data[::,0] * 0.001
            print(data.shape)
            # x = data[::,0]
            # y = data[::,1]


            # PLOT only 460
            # if (resids.groups()[1]) == '460':
            #     # or resids.groups()[0] == '532'):
            #     plt.plot(data[::,0],data[::,1],label=res_label,color=color,\
            #              linestyle=linestyle,linewidth=3.0)

            plt.plot(data[::,0],data[::,1],label=res_label,color=color,\
                     linestyle=linestyle,linewidth=3.0)


    #  ---------------------------------------------------------  #
    #  Make final adjustments: (4/4)                              #
    #  mpl - available expansions                                 #
    #  ---------------------------------------------------------  #
    ax1.set_ylabel("HSA Ratio")
    ax1.set_xlabel("Frame # (x 1000)")
    ax1.set_ylim(-0.1,1.1)
    ax1.set_xlim(0,data[-1,0])

    handles,labels = ax1.get_legend_handles_labels()
    ax1.legend(handles[::],labels[::],prop={'size':20},loc=4)
    leg = plt.gca().get_legend()
    for label in leg.get_lines():
        label.set_linewidth(3.0)


    # Save a matplotlib figure.
    # REQ:
    # (1) cwd = saves here, else provide 'destdirname'
    # (2) name = filename without suffix. eg. 'png' (def), 'svg'
    # OPT:
    # (3) destdirname: eg. 'fig/histograms'
    # (4) dpi: (optional) 120 (default), 300, 600, 1200
    # (5) filetypes: ['png','svg','eps','pdf']
    result_type = ''
    data_name = ''

    P = SaveFig(my_dir,
                'hsa_%s_%s' % (result_type,data_name),
                destdirname='fig/hsa')

    # save_fig(my_dir,0,'fig/hsa/%s%d' % (peptide,stage),'%s_%s_%s' %
    # (result_type,plot_type,data_name),option)



#  ---------------------------------------------------------  #
#  End of Functions.                                          #
#  ---------------------------------------------------------  #
dir_stage = get_stage_dir(stage)
print('dir_stage:',dir_stage)
dct_targets = load_dct(dir_stage,'pull.*.dat')
# print(len(dct_targets.keys()))

# PSF:
psfdir = os.path.join(my_dir,'psf')
psf = glob.glob(os.path.join(psfdir,'%s.psf' % str(stage).zfill(2)))[0]
print(psf)

print("Building MDTraj3")

# Run directories:
for k,v in dct_targets.items():
    if k != traj:
        continue

    print(k,v['dirname'])
    os.chdir(v['dirname'])

    pdb = glob.glob('*.ref.*')[0]
    dcd = glob.glob('dcd/*pull.dcd')[0]

    print('pdb:',pdb)
    print('dcd:',dcd)

    M = MDTraj3(pdb,dcd,v['dirname'])
    # M.print_class()
    # print(segment)
    # print(selection)

    M.sel = selection

    # remove_interim_coords: all or rebuilt
    # M.remove_interim_coords('all')
    # M.remove_interim_coords('rebuilt')

    M.write_pdb(3,25000,800)
    # M.print_interim_coord_files()
    M.run_pulchra()
    M.run_hsa()
    M.get_hsa() # requires .write_pdb





# sys.exit()

# # Run command:
# if commandrun == 1:
#     run_hsa_analysis(dct_targets)

# if commandrun == 2:
#     check_hsa_analysis(dct_targets)

# if commandrun == 3:
#     remove_interim_dir(dct_targets)

# if commandrun == 4:
#     import matplotlib
#     # default - Qt5Agg
#     # print matplotlib.rcsetup.all_backends
#     # matplotlib.use('GTKAgg')
#     # matplotlib.use('TkAgg')
#     print('backend:',matplotlib.get_backend())
#     import matplotlib.pyplot as plt
#     from matplotlib.gridspec import GridSpec
#     from plot.SETTINGS import *
#     plot_hsa(dct_targets)

# if commandrun == 5:
#     print('renaming current hsadir')
#     rename_current_hsadir(dct_targets)
