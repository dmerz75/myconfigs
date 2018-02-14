#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

import numpy as np
import math
from scipy.stats import maxwell
import matplotlib.pyplot as plt

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# insert Example here about how to build your own python library.
# Example 1: write: ~/.pylib/mylib/cp.py
#            touch ~/.pylib/mylib/__init__.py
#            gets compiled: ~/.pylib/mylib/cp.pyc
#            Done. (importable!)
# libraries:
# from mylib.cp import *
# from mylib.moving_average import *
# from mylib.FindAllFiles import *
# from mylib.regex import reg_ex
# from mylib.run_command import run_command


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
result_type = 'maxwell' # sop | sopnucleo | gsop | namd
plot_type = 'distribution' # fe | tension | rmsd | rdf

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
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
option = args['option']
data_name = args['dataname']


#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #


mean, var, skew, kurt = maxwell.stats(moments='mvsk')

if 0:
    x = np.linspace(maxwell.ppf(0.0001),
                    maxwell.ppf(0.9999),1000)
    y = 16 * maxwell.pdf(x)
else:
    a = 1
    x = np.linspace(0.00001,4.9,1000)
    y2 =  -1 * a * x**2
    yf = a * x**2
    y = yf * np.exp(y2)
    x = np.linspace(1,250000,1000)
    # y1 = x**2
    # ye = np.exp((-1 * y1) * 0.5)
    # y = np.sqrt(((2/math.pi) * y1)) * ye



mb = ax1.plot(x,y,'r-', lw=5, alpha=0.6, label='maxwell pdf')

ax1.fill_between(x,0,y,where=y>0,facecolor='green',interpolate=True,alpha=0.2)





#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# Section 1.
# print matplotlib.rcParams.keys()
# matplotlib.rcParams['legend.fontsize'] = 16
# matplotlib.rcParams[''] =
# handles,labels = ax.get_legend_handles_labels()
# ax.legend(bbox_to_anchor=(1.4,1.0))
# ax.legend(handles,labels,prop={'size':8})

# Section 2.
# fig.set_size_inches(8.5,5.1)
# plt.subplots_adjust(left=0.160,right=0.960,top=0.950,bottom=0.20)
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

# Section 3.
# mpl_label
# mpl_xy: set_xlim,set_ylim,xticks,yticks
# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])

# mpl_ticks
# mpl_tick
# mpl_minorticks

# Section 4.
# legend
# 1:
# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles, labels,prop={'size':10})
# 2:
# lst_labels = ['','',]
# ax1.legend(lst_labels,loc=2,prop={'size':18})
# 3:
# lst_labels = ['','',]
# leg = plt.gca().get_legend()
# for label in leg.get_lines():
#     label.set_linewidth(2.5)

# some lines in legend!
# print len(ax1.lines),ax1.lines
# lst_labels = ['0.3','0.4','0.5','0.6','0.7']
# for i,line in enumerate(ax1.lines[2:7]):
#     print lst_labels[i]
#     line.set_label(lst_labels[i])
# ax1.legend()

# combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)
# save_fig
plt.savefig("fig/maxwell_distribution_1.png")
plt.savefig("fig/maxwell_distribution_1.eps")
plt.savefig("fig/maxwell_distribution_1.pdf")
plt.savefig("fig/maxwell_distribution_1.svg")
# from plot.SETTINGS import *
# save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)

# mpl_myargs_end
