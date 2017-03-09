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
from mylib.moving_average import moving_average
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
plot_type = 'curv_local' # fe | tension | rmsd | rdf

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-d","--dataname",help="dataname",type=int)
    parser.add_argument("-t","--trajectory",help="trajectory",type=int)
    parser.add_argument("-u","--unit",help="monomer,dimer")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
option = args['option']
data_name = args['dataname']
trajectory = args['trajectory']
if args['unit'] == None:
    unit = 'dimer'
else:
    unit = args['unit']



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
print len(x.dct.keys()),'of',x.total
set9 = x.remove_dirname('fail',-2,x.dct)
set9 = x.query_file('curvature_local',set9)
set9 = x.sort_dirname(-2,set9)
print len(set9.keys()),'of',x.total
# sys.exit()

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


def get_data(filename,ma_value):
    # add in first (1)
    # data = np.loadtxt(values['file'])
    data = np.loadtxt(filename)
    data2 = np.array(moving_average(data[::,0],ma_value))
    for i in range(0,data.shape[1]):
        # print i
        if unit == 'dimer':
            if i % 2 == 0:
                continue
        # print min(data[::,i])
        # print max(data[::,i])
        d1 = moving_average(data[::,i],ma_value)
        # d2 = np.histogram(d1,bins=10,range=(40.0,80.0))
        # d2 = np.histogram(d1,bins=(0,45,50,55,60,70,500))
        # print d2
        # sys.exit()
        # print d1.shape
        # do stacking (2)
        data2 = np.vstack((data2,d1))
        # data2 = np.vstack((data2,d2))
    # print data2.shape
    # remove first (3)
    data2 = data2[1:,::]
    # print data2.shape
    data2 = np.transpose(data2)
    print data2.shape
    data2 = data2[::,::-1]
    print data2.shape
    # sys.exit()
    return data2


# protofilament
lst_mon = np.linspace(0.75,6.25,12)
print lst_mon
# sys.exit()
ms = 27
for i,mon in enumerate(lst_mon):
    if i % 2 == 0:
        if i % 4 == 0:
            plt.plot(2,mon,'o',color='orange',markersize=ms)
        else:
            plt.plot(2,mon,'o',color='orange',markersize=ms)
    else:
        if (i+1) % 4 == 0:
            plt.plot(2,mon,'co',markersize=ms)
        else:
            plt.plot(2,mon,'co',markersize=ms)

# kinesins
for d in str(data_name):
    # plt.plot(1,int(d),'r8',markersize=25)
    plt.plot(1.4,int(d),'r>',markersize=30)




# key = set9.keys()[0]
# data = get_data(set9[key]['file'],ma_value=20)

for k in set9.keys():
    # print dir(set9)
    # print set9.values()
    data = get_data(set9[k]['file'],10) # 10 is ma_value
    data = np.transpose(data)
    cmap = plt.get_cmap('magma') # tried afmhot_r,
    v = np.linspace(20,380,4)
    plt.imshow(data,aspect='auto',extent=[0,data.shape[1]*5*0.001,1,data.shape[0]+1],\
               cmap=cmap,\
               interpolation='none',\
               clim=(0.00,400.0))
    x = plt.colorbar(ticks=v)


#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_rc
# mpl_font
# mpl_label
# mpl_xy
plt.subplots_adjust(bottom=0.24)
ax1.set_yticks([1.5,2.5,3.5,4.5,5.5])
ax1.set_ylim(0.75,6.25)

ax1.set_ylabel('Dimer Interfaces')
ax1.set_xlabel('Frame #')

# mpl_ticks
# mpl_tick
# mpl_minorticks
# mpl_legend
# combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)
# data_name = str(data_name) + '_' + str(trajectory)
data_name = str(data_name) + '_' + str(trajectory) + '_' + unit
# save_fig
from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)

# mpl_myargs_end
