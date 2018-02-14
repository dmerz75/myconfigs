#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# libraries:
from mylib.FindAllFiles import *
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
# from mylib.run_command import run_command
from plot.microtubule import *
from plot.SETTINGS import *

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    Options:
    args['makefile']
    args['procs']
    args['node'])
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--string1",help="input string")
    parser.add_argument("-n","--node",help="select node",type=int)
    parser.add_argument("-rnd","--rnd",help="select round",type=int)
    parser.add_argument("-psf","--psf",help="select psffile")
    parser.add_argument("-nd","--num_dimers",help="number of dimers, 104, 156")
    parser.add_argument("-ff","--forceframecontacts",help="select plot trajectories file")

    args = vars(parser.parse_args())
    return args
args = parse_arguments()
rnd = args['rnd']
psffile = args['psf']
ffile = args['forceframecontacts']
num_dimers = int(args['num_dimers'])

option = None
result_type = 'gsop'
plot_type = 'ffc'

#  ---------------------------------------------------------  #
#  sorting                                                    #
#  ---------------------------------------------------------  #
def load_dct(cwd=my_dir,pattern='*.dat'):
    # FindAllFiles
    print 'cwd:',cwd
    print 'pattern:',pattern
    dct_find = {'cwd':cwd,'pattern':pattern}
    x = FindAllFiles(dct_find)
    # print x.pattern
    x.get_files()
    # x.print_query(x.dct)
    # print len(x.dct.keys()),'of',x.total
    set9 = x.remove_dirname('fail',None,x.dct)
    set9 = x.remove_dirname('example',None,set9)
    set9 = x.remove_dirname('tops_extra',None,set9)
    set9 = x.query_dirname("round_%d" % rnd,None,set9)
    set9 = x.sort_dirname(-1,set9)
    return set9
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)
    # print len(set9.keys()),'of',x.total
    # sys.exit()
    # return set9
    # return x.dct

dct_dat = load_dct(my_dir,'mt_analysis.dat')
# print 'dict obtained',len(dct_dat.keys())



def build_mt(dct):
    mt_list = []
    count = 0

    for k,v in dct.iteritems():
        count += 1
        # print k,v['dirname']
        name = v['dirname'].split('/')[-1]
        mt = Microtubule(name)
        mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
        # mt.print_class()
        # continue

        mt.my_dir = my_dir
        mt.setupdirs()
        '''
        self.datdir = os.path.join(self.dirname,'dat')
        self.dcddir = os.path.join(self.dirname,'dcd')
        self.indentationdir = os.path.join(self.dirname,'indentation')
        self.outputdir = os.path.join(self.dirname,'output')
        self.topdir = os.path.join(self.dirname,'topologies')
        '''
        mt.set_attributes(v)
        mt.rnd = rnd
        mt.find_psf('%s/structural' % my_dir,psffile)
        mt.find_dcd()
        mt.get_frame_count()
        mt.get_analysis_file()
        mt.get_indentation_file()
        mt.get_pdbs()
        mt.get_direction_info() # forward or reverse:
        mt.get_plate_info() # with plate or without:
        mt.get_reversal_frame()
        mt.get_sop_file()
        mt.get_sop_info()
        mt_list.append(mt)

    return mt_list

mt_list = build_mt(dct_dat)

    # def print_class(self):
    # def set_attributes(self,dct):
    # def setupdirs(self):
    # def find_psf(self,psfdir,psf):
    # def find_dcd(self,dcddir=None):
    # def get_reversal_frame(self):
    # def get_frame_count(self):
    # def get_analysis_file(self):
    # def get_sop_file(self):
    # def get_indentation_file(self):
    # def get_pdbs(self):
    # def get_direction_info(self):
    # def get_plate_info(self):
    # def get_sop_info(self):
    # def get_dimers(self):
    # def get_forceindentation(self):
    # def get_emol_mtcontacts(self,total_num_dimers):
    # def get_emol_mtcontacts_3(self,fp,total_num_dimers):
    # def get_emol_mtcontacts_3n(self,fp,total_num_dimers):
    # def get_mtanalysis(self,num_dimers=104,step=5):
    # def get_force_by_time_series(self):
    # def get_reverse_abscissa(self,xt):
    # def get_analysis_by_time_series(self):
    # def truncation_by_percent(self,reversal_frame):
    # def combine_contacts_and_frames(self,arr_contacts,arr_frames,rev_frame):
    # def combine_nesw_contacts(self,obj,arr_contacts,arr_frames,rev_frame):
    # def combine_force_and_indentation(self,arr_force,arr_indentation,rev_ind):
    # def emol_topology_based_contact_files(self,dirname):
    # def emol_topology_contact(self,fp,num_dimers):
    # def plot_emol3top(self,my_dir,option,dimers=[]):

# for k,v in dct_dat.iteritems():
#     print k,v['dirname'].split('/')[-1]

# for i,mt in enumerate(mt_list):
#     print i,mt.name

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


with open(os.path.join(my_dir,ffile)) as fp:

    for line in fp:
        if line.startswith('#'):
            continue
        # print line
        # fig = plt.figure(0)
        # gs = GridSpec(2,1)
        # ax1 = plt.subplot(gs[0,:])
        # ax2 = plt.subplot(gs[1,:])
        # ax = [ax1,ax2]
        # fig.set_size_inches(8.0,10.0)
        # plt.subplots_adjust(left=0.2,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

        # print line
        # mtname = line.split(' ')[0]
        mtname = line.split()[0]
        frame1 = int(line.split()[1])
        frame2 = int(line.split()[2])
        print mtname,frame1,frame2

        for i,mt in enumerate(mt_list):
            if mt.name != mtname:
                continue
            # print mt.name
            mt.get_mtanalysis(num_dimers)
            mt.get_dimers(0.72)
            mt.get_forceindentation()
            mt.get_force_by_time_series()
            # mt.plot_forceindentation(ax1) # with "Full indent," "partial"
            # mt.plot_forceframe(ax1)
            # mt.plot_contacts(ax2,mt.dimers)
            # mt.plot_vertlines(ax1,[frame1,frame2])
            # mt.plot_vertlines(ax2,[frame1,frame2])
            # mt.get_mtpf(ax2)
            # mt.get_mtpf()
            mt.plot_mtpf()
            P = SaveFig(my_dir,
                        '%s_%s' % (mt.name,mt.rnd),
                        destdirname='fig/mtpfbending_global')
            plt.clf()

            mt.plot_mtpf_local()

            P = SaveFig(my_dir,
                        '%s_%s' % (mt.name,mt.rnd),
                        destdirname='fig/mtpfbending_local')
            plt.clf()



# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -rnd 26 -psf ~/ext/completed_mt/structural/mt12_plate.psf -nd 156 -ff results.crit_breaks/pname_framebreaks_16
