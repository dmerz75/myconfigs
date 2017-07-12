#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *
from plot.gsop import PlotSop
from plot.SETTINGS import *
# mpl_moving_average
# mpl_forcequench
# mpl_worm

#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
#  ---------------------------------------------------------  #
import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])
ax = [ax1]

#  ---------------------------------------------------------  #
#  Import Data! (2/4)                                         #
#  ---------------------------------------------------------  #
result_type = 'gsop' # sop | sopnucleo | gsop | namd
plot_type = 'all' # fe | tension | rmsd | rdf

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-d","--dataname",help="data name: run280, 76n")
    parser.add_argument("-rnd","--rnd",help="select round",type=int)
    parser.add_argument("-x","--x",help="select trajectory x",type=int)

    parser.add_argument("-f","--f",help="select trajectory x",type=int)
    parser.add_argument("-i","--i",help="select trajectory x",type=int)
    parser.add_argument("-t","--t",help="select trajectory x",type=int)
    parser.add_argument("-c","--c",help="select trajectory x",type=int)
    args = vars(parser.parse_args())
    return args


args = parse_arguments()
rnd = str(args['rnd']).zfill(2)
traj = args['x']
plot_force = args['f']
plot_chi = args['i']
plot_tension = args['t']
plot_contacts = args['c']
# option = args['option']
# data_name = args['dataname']


#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
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
    print len(x.dct.keys()),'of',x.total
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)
    # print len(set9.keys()),'of',x.total
    # sys.exit()
    # return x.dct
    set9 = x.remove_dirname('fail',-1,x.dct)
    return set9

def get_round(dct,rnd):
    x = FindAllFiles()
    set9 = x.query_dirname(rnd,-2,dct)
    print 'files entered:',len(dct.keys())
    print 'files returned, round %s:' % rnd,len(set9.keys())
    set9 = x.sort_dirname(-1,set9)
    return set9

dct_all = load_dct(my_dir,'pull.*.dat')
dct_sel1 = get_round(dct_all,'01')
dct_sel2 = get_round(dct_all,'02')
if rnd != None:
    dct_sel = get_round(dct_all,rnd)


#  ---------------------------------------------------------  #
#  Notes:                                                     #
#  ---------------------------------------------------------  #
# 1. steps:       4.8/5.2 billion
# 2. velocity: 2680.0  nm/s
# 3. timestep:   18.64 ps
# 4. time:       89.4  ms
# 5. distance:  240.0  nm


if rnd == '01':
    point_start = 0
    point_end = 2500000000
    ma_value = 100
    step = 10
    ts = 20.0
    nav = 1000
    dcdfreq = 10000000
    outputtiming = 10000000
if rnd == '02':
    point_start = 0
    point_end = 2500000000
    ma_value = 100
    step = 10
    ts = 20.0
    nav = 1000
    dcdfreq = 10000000
    outputtiming = 10000000


for k,v in dct_sel.items():
    if traj != None:
        if k != traj:
            continue

    print v.keys()

    F = PlotSop(job_type='gsop',nav=nav,start=point_start,stop=point_end,ma=ma_value,\
                ts=ts,dcdfreq=dcdfreq,outputtiming=outputtiming,step=step)

    # begin:
    print k,v['dirname'].split('/')[-1]
    just_dirname = v['dirname'].split('/')[-1]
    os.chdir(v['dirname'])
    cwd = os.getcwd()

    F.load_data(v['file'])
    F.process_data(2.0)
    # F.describe_data()
    # 'barrier',
    # 'data',
    # 'dcdfreq',
    # 'describe_data',
    # 'end_to_end','ext','ext_linear','ext_raw','ext_short','extension',
    # 'f70','f_pico','f_raw','force',
    # 'frame',
    # 'job_type',
    # 'load_data',
    # 'ma',
    # 'nav','outputtiming',
    # 'start', 'step', 'stop', 'time', 'time_array_ms', 'ts'
    # 'print_class',
    # 'process_data',

    # print dir(F)
    # sys.exit()

    # print dir(F)

    # print F.data_chi.shape
    # print F.data_tension.shape
    # print F.data_costheta.shape
    # print F.data_contacts_intra.shape
    # print F.data_contacts_residue.shape


    #  ---------------------------------------------------------  #
    #  Analysis                                                   #
    #  ---------------------------------------------------------  #
    # F.plot()
    # F.plot_colorline()

    # 1. Force-Extension Curves:
    if plot_force == 1:
        F.Plot_Multi()
        P = SaveFig(my_dir,
                    'multi_%s_%s' % (rnd,just_dirname),
                    destdirname='fig/round_%s' % rnd)
        plt.clf()

    # 2. Force-Extension Curves:
    if plot_force == 2:
        colors = ['g','m','b']
        for i,t in enumerate(['ext','frame','time']):
            F.Plot_Fext(t,colors[i])
            P = SaveFig(my_dir,
                        'fe_%s_%s_%s' % (t,rnd,just_dirname),
                        destdirname='fig/round_%s' % rnd)
            plt.clf()

    # Tension:
    if plot_tension == 1:
        F.get_analysis(v['dirname'],'tension')
        F.Plot_Tension()
        P = SaveFig(my_dir,
                    'ten_%s_%s' % (rnd,just_dirname),
                    destdirname='fig/round_%s' % rnd)
        plt.clf()

    # Chi:
    if plot_chi == 1:
        F.get_analysis(v['dirname'],'chi')
        F.Plot_Chi()
        P = SaveFig(my_dir,
                    'chi_%s_%s' % (rnd,just_dirname),
                    destdirname='fig/round_%s' % rnd)
        plt.clf()

    # Contacts:
    if plot_contacts == 1:
        F.get_analysis(v['dirname'],'contacts')
        F.Plot_Contacts()
        P = SaveFig(my_dir,
                    'contacts_%s_%s' % (rnd,just_dirname),
                    destdirname='fig/round_%s' % rnd)
        plt.clf()

    # Costheta:
    if plot_tension == 1:
        F.get_analysis(v['dirname'],'costheta')
        F.Plot_Costheta()
        P = SaveFig(my_dir,
                    'costheta_%s_%s' % (rnd,just_dirname),
                    destdirname='fig/round_%s' % rnd)
        plt.clf()
