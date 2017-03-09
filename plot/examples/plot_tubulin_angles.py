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
# mylib
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *
from mylib.moving_average import *
# mpl_moving_average
# mpl_forcequench
# mpl_worm

#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
#  ---------------------------------------------------------  #
import matplotlib
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
# plot_type = 'proto_angles_3centroid' # fe | tension | rmsd | rdf
plot_type = 'tubulin_angles' # fe | tension | rmsd | rdf
# data_name = '3kin_2' # seed #
# save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
# combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--number",help="line_number, i.e. 196",type=int)
    parser.add_argument("-d","--data_name",help="so far: 4-1",type=int)
    parser.add_argument("-a","--angle",help="angle: n or e")
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-b","--barrier",help="barrier 15.0 deg",type=float)
    parser.add_argument("-t","--t",help="trajectory/trial number, 0,1,2,4,5 ..",type=int)
    parser.add_argument("-e","--evenodd",help="even by default, even(2), odd(1)",type=int)
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
line_size = args['number']
data_name = args['data_name']
angle = args['angle']
option = args['option']
barrier = args['barrier']
trajectory = args['t']

if args['evenodd'] == None:
    evenodd = 1
else:
    evenodd = args['evenodd']
if evenodd != 1:
    evenodd = 2
print 'evenodd:',evenodd

# evenodd = args['evenodd']

# ./plot_proto_angles_from3centroid.py -n 10 -d 123
# ./plot_proto_angles_from3centroid.py -d 123 -x 0  [1,2,3]
# ./plot_tubulin_angles.py -d 123 -t 1 -e 2

if line_size == None: # 10
    line_size = 10

#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #
# FindAllFiles
dct_find = {'cwd':my_dir,'pattern':'dat'}
x = FindAllFiles(dct_find)
x.get_files()
# x.print_query(x.dct)
set9 = x.dct
print len(x.dct.keys()),'of',x.total
# sys.exit()
# x.dct (last pos.)
# x.sort_dirname
# x.print_query,_class
# x.query_ [dirname,file,filename](searchstring,pos,dct)
# x.remove_[dirname,file,filename](searchstring,pos,dct)
set9 = x.query_dirname('3kinesin',-3)
set9 = x.query_filename('tubulin',set9)
set9 = x.remove_dirname('fail',-2,set9)
set9 = x.remove_dirname('contact_maps',-1,set9)
set9 = x.sort_dirname(-2,set9)
# x.print_query(set9)
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

def get_data(filename,line_size):
    data = np.loadtxt(filename)
    # nr,nc = x.shape
    # print nr,nc
    # data = x.reshape(nr/line_size,line_size,4)
    print data.shape
    return data


# color cycle
# from cycler import cycler
# ax1.set_prop_cycle(cycler('color',colors))
import itertools
colors = ['k','r','g','b','c','m',\
          'darkgoldenrod','darksalmon',\
          'darkmagenta','chartreuse','darkturquoise']
# marker = ['.','^','s','o','p']
color = itertools.cycle((['k','r','g','b','c','m',\
                          'darkgoldenrod','darksalmon',\
                          'darkmagenta','chartreuse','darkturquoise']))
marker = itertools.cycle(('.','^','s','o','p'))


for k in set9.keys():
    data = get_data(set9[k]['file'],line_size) # 10 is ma_value

    for a in range(data.shape[1]):
        if evenodd == 2:
            if a % 2 != 0:
                continue
        else:
            if a % 2 == 0:
                continue

        print a
        # color = colors[a]
        # ms = marker[a]
        # print color,ms
        # continue

        lw = int(a+1)
        le = int(a+2)
        label = str(lw) + '-' + str(le)

        d1 = moving_average(data[::,a],25)
        print d1.shape
        mcount = int(d1.shape[0] / 80)
        x = np.linspace(0,d1.shape[0]*5*0.001,d1.shape[0])
        # plt.plot(x,d1,label=label,marker=ms,markevery=mcount,linestyle='None',markersize=5)
        plt.plot(x,d1,label=label,color=color.next(),
                 marker=marker.next(),markevery=mcount,linewidth=1,markersize=5) #***


#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_rc
# mpl_font
# mpl_label
# mpl_xy

plt.ylabel("Angle (deg.)")
plt.xlabel("Frame (x1000)")

# plt.yticks([20,40,60])


# plt.yticks([15,30,45])
# plt.xticks([250,500,750,1000])
plt.yticks([0,30,60,90,120,150])
plt.xticks(np.linspace(0,14,8))
plt.ylim([-2,170])
plt.xlim([-0.05,15.1])

# 1:
handles, labels = ax1.get_legend_handles_labels()

# handles = handles[0:10]
# labels = labels[0:10]

if 'i' not in str(data_name):
    handles = handles[-10:]
    labels = labels[-10:]
else:
    handles = handles[-11:]
    labels = labels[-11:]

if 'odd' in str(data_name):
    handles = handles[-5:]
    labels = labels[-5:]
else:
    handles = handles[-6:]
    labels = labels[-6:]


ax1.legend(handles, labels,prop={'size':12},loc=2)
leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(2.5)

data_name = str(data_name) + '_' + str(trajectory)
# data_name = str(data_name) + '_' + str(trajectory) + '_' + unit
# save_fig
from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)
# mpl_myargs_end
