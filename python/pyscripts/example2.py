#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
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
plot_type = 'contacts' # fe | tension | rmsd | rdf

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

x = np.linspace(0,10,11)
y = x**2

print x,y


ax1.plot(x,y)

#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_rc
# mpl_font
# mpl_label
# mpl_xy
# mpl_ticks
# mpl_tick
# mpl_minorticks
# mpl_legend
# combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)
from plot.SETTINGS import *

# Save a matplotlib figure.
# REQ:
# (1) cwd = saves here, else provide 'destdirname'
# (2) name = filename without suffix. eg. 'png' (def), 'svg'
# OPT:
# (3) destdirname: eg. 'fig/histograms'
# (4) dpi: (optional) 120 (default), 300, 600, 1200
# (5) filetypes: ['png','svg','eps','pdf']

# P = SaveFig(cwd,name,destdirname*,dpi*,filetypes*)
# print plt.gcf().canvas.get_supported_filetypes()

P = SaveFig(my_dir,
            'hist_%s_%s' % (result_type,data_name),
            destdirname='fig/')
