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

# Figures:
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


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


def write_crit_file(dct,suffix='.out',value='firstvalue'):

    lst_stat = []

    for k,v in dct.iteritems():
        print k
        try:
            lst_stat.append((k,v[value]))
        except:
            pass

    for stat in lst_stat:
        print stat[0],stat[1]
        lst_stat.sort(key=lambda x: x[1])

    outfile = os.path.join(my_dir,args['forceframecontacts'] + suffix)
    print "Writing:",outfile

    with open(outfile,'w+') as fp:
        # for k,v in dct_sortedstat.iteritems():
        # print k,v
        for stat in lst_stat:
            print stat[0],stat[1]
            fp.write("%s   %7.5f\n" % (stat[0],stat[1]))


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
    x.print_query(x.dct)
    print len(x.dct.keys()),'of',x.total
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
    return x.dct

dct_dat = load_dct(my_dir,'mt_analysis.dat')
print 'dict obtained',len(dct_dat.keys())

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

for i,mt in enumerate(mt_list):
    print i,mt.name


# /home/dmerz3/ext2/completed_mt/results.crit_breaks/rev_crit_breaks_13
# print ffile


# plt.clf()
# fig = plt.figure(0)
# gs = GridSpec(2,1)
# ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:])
# ax = [ax1,ax2]
# fig.set_size_inches(8.0,10.0)
# plt.subplots_adjust(left=0.2,right=0.78,top=0.960,bottom=0.10,hspace=0.4)


with open(os.path.join(my_dir,ffile)) as fp:

    firsts = []
    criticals = []
    dct_stat = {}

    for line in fp:
        if line.startswith('#'):
            continue
        # print line

        fig = plt.figure(0)
        plt.title(mt.name)
        dct_font = {'family':'sans-serif',
                    'weight':'normal',
                    'size'  :'16'}
        matplotlib.rc('font',**dct_font)
        gs = GridSpec(8,24)
        fig.set_size_inches(15.0,10.0)
        plt.subplots_adjust(left=0.12,right=0.96,top=0.930,bottom=0.08,hspace=1.3,wspace=0.3)

        # Row 1: Force-Indentation, N,S
        ax1 = plt.subplot(gs[0:2,0:8])
        ax3 = plt.subplot(gs[0:2,10:16])
        ax5 = plt.subplot(gs[0:2,18:24])

        # Row 2: Contacts, W,E
        ax2 = plt.subplot(gs[2:4,0:8])
        ax4 = plt.subplot(gs[2:4,10:16])
        ax6 = plt.subplot(gs[2:4,18:24])

        # Row 3,4: PFBend, Angles
        ax71 = plt.subplot(gs[4:6,0:3])
        ax72 = plt.subplot(gs[4:6,3:6])
        ax73 = plt.subplot(gs[4:6,6:9])
        ax74 = plt.subplot(gs[4:6,9:12])
        ax75 = plt.subplot(gs[4:6,12:15])
        ax76 = plt.subplot(gs[4:6,15:18])
        ax77 = plt.subplot(gs[4:6,18:21])
        ax78 = plt.subplot(gs[4:6,23:24]) # colorbar
        ax7 = [ax71,ax72,ax73,ax74,ax75,ax76,ax77,ax78]

        ax81 = plt.subplot(gs[6:8,0:3])
        ax82 = plt.subplot(gs[6:8,3:6])
        ax83 = plt.subplot(gs[6:8,6:9])
        ax84 = plt.subplot(gs[6:8,9:12])
        ax85 = plt.subplot(gs[6:8,12:15])
        ax86 = plt.subplot(gs[6:8,15:18])
        ax87 = plt.subplot(gs[6:8,18:21])
        ax88 = plt.subplot(gs[6:8,23:24]) # colorbar
        ax8 = [ax81,ax82,ax83,ax84,ax85,ax86,ax87,ax88]

        axes_all = [ax1,ax2,ax3,ax4,ax5,ax6] + ax7 + ax8
        axes_lower = ax7 + ax8

        print line
        mtname = line.split()[0]
        frame1 = int(line.split()[1])
        frame2 = int(line.split()[2])
        print mtname,frame1,frame2

        for i,mt in enumerate(mt_list):
            if mt.name != mtname:
                continue
            print mt.name
            mt.get_mtanalysis(num_dimers)
            # mt.get_dimers(0.33,0.70)
            # mt.get_dimers(0.48,0.68)
            # mt.get_dimers(0.05,0.1)
            mt.get_dimers(0.45,0.70)

            mt.get_forceindentation()
            mt.get_force_by_time_series()
            e1,f1 = mt.get_force_at_frame(frame1)
            e2,f2 = mt.get_force_at_frame(frame2)
            print frame1,e1,f1
            print frame2,e2,f2

            # mt.plot_forceindentation(ax1) # with "Full indent," "partial"
            mt.plot_forceframe(ax1)
            mt.plot_contacts(ax2,mt.dimers)
            # mt.get_mtpf(ax2)

            # plot N,S,E,W contacts.
            minfn = mt.plot_contact_interface(ax3,'n')
            minfs = mt.plot_contact_interface(ax4,'s')
            minfw = mt.plot_contact_interface(ax5,'w')
            minfe = mt.plot_contact_interface(ax6,'e')
            mt.plot_vertlines(ax1,[minfn,minfw])
            mt.plot_vertlines(ax2,[minfn,minfw])

            # plot the mtpf global, local.
            # mt.get_mtpf()
            # mt.plot_mtpf(ax7)
            # mt.plot_mtpf_local(ax8)

            # Now..
            # Get the frame of first lateral break,
            # frame of the first significant longitudinal break.
            # save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
            #          '%s_%s_%s_rnd%d_total' % (result_type,plot_type,
            #                                    mtname,rnd),option)

            # savedir = os.path.join(self.my_dir,'contacts_full/%s' % (self.rnd))

            for ax in axes_all[2:]:
                # ax.axis('off')
                # ax.tick_params('')
                # ax.tick_params()
                ax.tick_params(axis='both',labelsize=12)

            # for ax in axes_lower:
                # ax.

            P = SaveFig(mt.my_dir,mt.name,
                        destdirname='fig/contacts_full/%s' % mt.rnd)

            # mt1 = mt
            # mt2 = mt
            # mt1.reversal_frame = frame1
            # mt1.truncation_by_percent(frame1)
            # mt2.reversal_frame = frame2
            # mt2.truncation_by_percent(frame2)
            dct_stat[mt.name] = {}
            dct_stat[mt.name]['dirname'] = mt.dirname
            dct_stat[mt.name]['first'] = f1
            dct_stat[mt.name]['second'] = f2
            firsts.append(f1)
            criticals.append(f2)


        # save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
        #          '%s_%s_%s_rnd%d_total' % (result_type,plot_type,
        #                                    mtname,rnd),option)
        # plt.clf()

        # # MTPF
        # mt.get_mtpf()
        # save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
        #          '%s_%s_%s_rnd%d_mtpf' % (result_type,plot_type,
        #                                    data_name,rnd),option)
    # end of line loop.

    for i in range(len(firsts)):
        print i,firsts[i],criticals[i]

    for k,v in dct_stat.iteritems():
        print k,v['first'],v['second']


    # Write First, and Maxvalue:
    write_crit_file(dct_stat,'.first.out','first')
    write_crit_file(dct_stat,'.maxvalue.out','second')




if 0:
    with open(os.path.join(my_dir,ffile)) as fp:

        firsts = []
        criticals = []
        dct_stat = {}

        for line in fp:
            if line.startswith('#'):
                continue
            # print line

            fig = plt.figure(0)
            gs = GridSpec(2,1)
            ax1 = plt.subplot(gs[0,:])
            ax2 = plt.subplot(gs[1,:])
            ax = [ax1,ax2]
            fig.set_size_inches(8.0,10.0)
            plt.subplots_adjust(left=0.2,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

            print line
            # mtname = line.split(' ')[0]
            mtname = line.split()[0]
            frame1 = int(line.split()[1])
            frame2 = int(line.split()[2])
            print mtname,frame1,frame2

            for i,mt in enumerate(mt_list):
                if mt.name != mtname:
                    continue
                print mt.name
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
                mt.get_mtpf()
                # e1,f1 = mt.get_force_at_frame(frame1)
                # e2,f2 = mt.get_force_at_frame(frame2)
                # print frame1,e1,f1
                # print frame2,e2,f2
                # mt1 = mt
                # mt2 = mt
                # mt1.reversal_frame = frame1
                # mt1.truncation_by_percent(frame1)
                # mt2.reversal_frame = frame2
                # mt2.truncation_by_percent(frame2)
                # dct_stat[mt.name] = {}
                # dct_stat[mt.name]['dirname'] = mt.dirname
                # dct_stat[mt.name]['first'] = f1
                # dct_stat[mt.name]['second'] = f2
                # firsts.append(f1)
                # criticals.append(f2)
                data_name = mt.name


            save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
                     '%s_%s_%s_rnd%d_mtpf' % (result_type,plot_type,
                                               data_name,rnd),option)
            plt.clf()



# 26
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -rnd 26 -psf ~/ext/completed_mt/structural/mt12_plate.psf -nd 156 -ff results.crit_breaks/pname_framebreaks_16

# 11
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -nd 104 -psf structural/mt8nop.psf -ff results.crit_breaks/pname_framebreaks_11 -rnd 11

# 10
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -nd 104 -psf structural/mt8doz.psf -ff results.crit_breaks/pname_framebreaks_10 -rnd 10
