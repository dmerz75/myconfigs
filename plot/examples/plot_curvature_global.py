#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))


#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
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
plot_type = 'curv_global' # fe | tension | rmsd | rdf

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-d","--dataname",help="data name: 123,134,145,156",type=int)
    parser.add_argument("-t","--trajectory",help="trajectory: 0,1,2,3...",type=int)
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
option = args['option']
data_name = args['dataname']
trajectory = args['trajectory']

#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #
# mylib
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *

# FindAllFiles
dct_find = {'cwd':my_dir,'pattern':'curvature_global.dat'}
x = FindAllFiles(dct_find)
x.get_files()
# x.print_query(x.dct)
# print len(x.dct.keys()),'of',x.total
# sys.exit()
# x.dct (last pos.)
# x.sort_dirname
# x.print_query,_class
# x.query_ [dirname,file,filename](searchstring,pos,dct)
# x.remove_[dirname,file,filename](searchstring,pos,dct)
set9 = x.remove_dirname('fail',-2,x.dct)
# set9 = x.sort_dirname(-1,set9)
# x.print_query(set9)
# print len(set9.keys()),'of',x.total

# data_name
set9 = x.query_dirname(str(data_name),-2,set9)
set9 = x.sort_dirname(-1,set9)
x.print_query(set9)
print len(set9.keys()),'of',x.total

# trajectory
set9 = x.query_dirname(str(trajectory),-1,set9)
set9 = x.sort_dirname(-1,set9)
x.print_query(set9)
print len(set9.keys()),'of',x.total
# sys.exit()

def get_data(values):
    data = np.loadtxt(values['file'])
    print 'data,load,shape:',data.shape
    return data


for k in set9.keys():
    # print dir(set9)
    # print set9.values()
    data = get_data(set9[k])
    data = data * 0.1
    x = np.linspace(0,data.shape[0]*5,data.shape[0])
    print x.shape
    plt.plot(x,data)



#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_rc
# fig.set_size_inches(8.5,5.1)
# plt.subplots_adjust(left=0.160,right=0.960,top=0.950,bottom=0.20)
# plt.subplots_adjust(left=0.20)
# ,right=0.960,top=0.950,bottom=0.20)
# font_prop_large = matplotlib.font_manager.FontProperties(size='large')

# for k in matplotlib.rcParams.keys():
#     print k
# dct_font = {'family':'sans-serif',
#             'weight':'normal',
#             'size'  :'28'}
# matplotlib.rc('font',**dct_font)
# matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rcParams['figure.dpi'] = 900
# print matplotlib.rcParams['figure.dpi']

# mpl_label
# mpl_xy: set_xlim,set_ylim,xticks,yticks

ax1.set_xlim(0,11000)

# plt.gca().invert_yaxis()
ax1.set_yticks([10,20,30,40])
ax1.set_ylim(2,42)

ax1.set_ylabel('Global Curvature (nm)')
ax1.set_xlabel('Frame #')

# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])

# mpl_ticks
# mpl_tick
# mpl_minorticks
# mpl_legend
# combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)
data_name = str(data_name) + '_' + str(trajectory)
# save_fig
from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)

# mpl_myargs_end
