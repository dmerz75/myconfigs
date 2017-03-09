#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))


my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
from mylib.run_command import *
# from plot.WLC import WormLikeChain
from plot.SOP import *
# from mdanalysis.MoleculeUniverse import MoleculeUniverse


#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-d","--dataname",help="dataname")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
option = args['option']
dataname = args['dataname']


#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
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
plot_type = 'fe' # fe | tension | rmsd | rdf
data_name = dataname # seed #
# save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)



#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #
# mylib
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *

# FindAllFiles
dct_find = {'cwd':my_dir,'pattern':'.dat'}
x = FindAllFiles(dct_find)
x.get_files()
set9 = x.dct
# x.print_query(set9)
set9 = x.remove_filename('curvature',set9)
set9 = x.remove_filename('distance_proto_',set9)
set9 = x.remove_dirname('fail',-2,set9)
set9 = x.remove_filename('LOG',set9)
set9 = x.remove_filename('contact',set9)
set9 = x.remove_filename('mt_angles',set9)
set9 = x.remove_filename('indices',set9)
set9 = x.remove_filename('tubulin_inter',set9)
# x.print_query(set9)
set9 = x.query_dirname('3kinesin13',-3,set9)
# set9 = x.sort_dirname(-2,set9)
# x.print_query(set9)
# sys.exit()

# projects: 123, 134, 145
set9 = x.query_dirname(dataname,-2,set9)
set9 = x.sort_dirname(-2,set9)
x.print_query(set9)

point_start = 0
# (3000001, 7) -- confirmed
point_end = 5000000
ma_value = 2500
step = 10
ts = 20.00
nav = 1000
dcdfreq = 100000
d = PlotSop('gsop',point_start,point_end,ma_value,step,ts,nav,dcdfreq)


for i in range(len(set9.keys())):
    path = set9[i]['file']
    print i,path
    label = dataname + '-' + str(i)
    d.load_data(path)
    d.describe_data(1)
    # plt.plot(d.ext,d.force)
    plt.plot(d.time,d.force,label=label)
    # plt.plot(d.time,d.force)




#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_rc
# mpl_font
# mpl_label

plt.ylabel('Force (pN)')
plt.xlabel('Time | Frame')



# mpl_xy: set_xlim,set_ylim,xticks,yticks

# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])

# mpl_ticks
# mpl_tick
# mpl_minorticks
# legend
# 1:
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels,prop={'size':12},loc=2)
# 2:
# lst_labels = ['','',]
# ax1.legend(lst_labels,loc=2,prop={'size':18})
# 3:
# lst_labels = ['','',]
leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(2.5)

# some lines in legend!
# print len(ax1.lines),ax1.lines
# lst_labels = ['0.3','0.4','0.5','0.6','0.7']
# for i,line in enumerate(ax1.lines[2:7]):
#     print lst_labels[i]
#     line.set_label(lst_labels[i])
# ax1.legend()

# save_fig

from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)
# mpl_myargs_end
