#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *

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

def sort_routine1(dct):
    x = FindAllFiles()
    print 'files entered:',len(dct.keys())

dct_dat = load_dct("%s/Documents" % my_dir,'one.dat')
dct_1 = sort_routine1(dct_dat)


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
result_type = 'one' # sop | sopnucleo | gsop | namd
plot_type = 'type' # fe | tension | rmsd | rdf

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

for k,v in dct_dat.iteritems():
    data = np.loadtxt(v['file'])
    print data.shape

    plt.plot(data)


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
# save_fig
from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)

# mpl_myargs_end
