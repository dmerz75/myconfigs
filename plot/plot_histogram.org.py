#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time
import glob
import re

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

fig.set_size_inches(7,5)
plt.subplots_adjust(left=0.140,right=0.960,top=0.920,bottom=0.20)
# fig.set_size_inches(8.5,5.1)
# plt.subplots_adjust(left=0.160,right=0.960,top=0.950,bottom=0.20)
# font_prop_large = matplotlib.font_manager.FontProperties(size='large')
# for k in matplotlib.rcParams.keys():
#     print k
dct_font = {'family':'sans-serif',
            'weight':'normal',
            'size'  :'20'}
matplotlib.rc('font',**dct_font)
# matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rcParams['figure.dpi'] = 900
# print matplotlib.rcParams['figure.dpi']

# ax[0].set_xticklabels([],size=20)
# ax[0].set_yticklabels([],size=20)


#  ---------------------------------------------------------  #
#  Import Data! (2/4)                                         #
#  ---------------------------------------------------------  #
result_type = 'force' # sop | sopnucleo | gsop | namd
plot_type = 'histogram' # fe | tension | rmsd | rdf
data_name = 'round_16_17'
option = None

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    # parser.add_argument("-o","--option",help="select None,publish,show")
    # parser.add_argument("-d","--dataname",help="data name: run280, 76n")
    # parser.add_argument("-f","--filename",help="filename: data file")
    parser.add_argument("-t","--topology",help="topology: all, reg, AHM, LHM, or top56")
    parser.add_argument("-p","--position",help="position: doz1,doz2,doz3,doz4,doz5")
    args = vars(parser.parse_args())
    return args


args = parse_arguments()
topology = args['topology']
position = args['position']


# option = args['option']
# data_name = args['dataname']


#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #
# lst_files = args['filename'].split(',')
# print sys.argv
lst_files = sys.argv[1:]
print lst_files
# sys.exit()

def get_data(datafile,topology,position):
    lst_data = []
    with open(datafile,'r+') as fp:
        for line in fp:

            if (topology != None and position != None):
                if ((re.search(topology,line) != None) and
                    (re.search(position,line) != None)):
                    print line
                    lst_data.append(float(line.split()[1]))
            elif (topology != None):
                if (re.search(topology,line) != None):
                    print line
                    lst_data.append(float(line.split()[1]))
            elif (position != None):
                if (re.search(position,line) != None):
                    print line
                    lst_data.append(float(line.split()[1]))

    data = np.array(lst_data)
    print data.shape
    return data

def plot_hist(data,color='b'):
    ''' Manual creation of a histogram.
    '''
    print min(data),max(data)

    bins = np.linspace(0.30,0.65,7)
    width = bins[1] - bins[0]
    hist = np.histogram(data,bins=bins) # normed, density, still hits 10
    norm = hist[0] / np.linalg.norm(hist[0])

    print 'width:',width
    print 'hist:'
    print hist
    print hist[0],len(hist[0])
    print hist[1],len(hist[1])
    print 'norm:'
    print norm

    # ax[0].bar(bins[:-1],hist[0],width,color=color,alpha=0.6)
    ax[0].bar(bins[:-1],norm,width,color=color,alpha=0.6)

    ax[0].set_xlim(bins[0],bins[-1])
    ax[0].set_xlabel('Forces',fontsize=24)
    ax[0].set_ylabel('Frequency',fontsize=24)
    return bins

def plot_hist4(data,bins,color='b'):
    '''
    Manual creation of a histogram. Normalized.
    '''
    print min(data),max(data)
    # binmax = 5
    # bins = np.linspace(min(data),max(data),binmax)
    width = bins[1] - bins[0]
    # while width > 0.05:
    #     binmax += 1
    #     bins = np.linspace(min(data),max(data),binmax)
    #     width = bins[1] - bins[0]
    # print 'binmax:',binmax

    hist = np.histogram(data,bins=bins) # normed, density, still hits 10
    norm = hist[0] / np.linalg.norm(hist[0])

    print 'width:',width
    print 'hist:'
    print hist
    print hist[0],len(hist[0])
    print hist[1],len(hist[1])
    print 'norm:'
    print norm

    # CDF-1
    cumulative = np.cumsum(norm)

    ax[0].bar(bins[:-1],norm,width,color=color,alpha=0.6)

    # CDF-2
    plt.plot(bins[:-1],cumulative,color=color)

    # ax[0].set_xlim(bins[0],bins[-1])

    # CDF-3
    if 1:
        # with:
        ax[0].set_ylim(-0.05,2.8)
        ax[0].set_xlim(0.22,1.30)
    else:
        # without:
        ax[0].set_ylim(-0.05,1.12)
        ax[0].set_xlim(0.30,1.30)

    ax[0].set_xlabel('Forces',fontsize=24)
    # ax[0].set_ylabel('Frequency',fontsize=24)
    ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    return bins

def plot_cdf(data,color='b'):
    '''
    With the cumulative distribution function, CDF.
    '''
    values,base = np.histogram(data,bins=len(bins))
    cumulative = np.cumsum(values)
    plt.plot(base[:-1],cumulative,color=color)



# TYPE 1:
if 0:
    colors = ['blue','red']
    for i,ff in enumerate(lst_files):
        print ff
        data = get_data(ff)
        bins = plot_hist(data,colors[i])
    lst_labels = ['No-Plate','With-Plate']
    ax[0].legend(lst_labels,loc=1,prop={'size':18})


# TYPE 2:
if 1:
    # lst_files = glob.glob(os.path.join(my_dir,'ff.file','*.out'))
    # lst_files = [os.path.join(my_dir,'crit_breaks','crit_breaks_*.out'),
    #              os.path.join(my_dir,'crit_breaks','crit_breaks_')
    lst_files = ['cur_crit_breaks_16.first.out',
                 'cur_crit_breaks_16.maxvalue.out',
                 'cur_crit_breaks_17.first.out',
                 'cur_crit_breaks_17.maxvalue.out']
  #   cur_crit_breaks_16.first.out
  # cur_crit_breaks_16.maxvalue.out
  # cur_crit_breaks_17.first.out
  # cur_crit_breaks_17.maxvalue.out
    lst_files = [os.path.join(my_dir,'crit_breaks',x) for x in lst_files]
    print lst_files

    # dct = {}
    # dct['16'] = {}
    # dct['17'] = {}
    # dct['16']['first'] = {}
    # dct['16']['maxvalue'] = {}
    # dct['17']['first'] = {}
    # dct['17']['maxvalue'] = {}
    # for k,v in dct.iteritems():

    colors = ['red','m','blue','cyan']

    for i,f in enumerate(lst_files):
        # topology: all, AHM, reg, LHM, top56
        # position: doz1,2,3,4,5
        data = get_data(f,topology,position)
        if ((i==0) or (i==2)):
            bins = np.linspace(0.30,0.65,7)
        else:
            bins = np.linspace(0.60,1.10,7)
        # if (i>1):
            # break
        plot_hist4(data,bins,color=colors[i])
        # plot_cdf(data,color=colors[i])

    # legend
    # 16-NoPlate
    # 17-Plate
    lst_labels = ['NoPlate-1st','NoPlate-Crit','Plate-1st','Plate-Crit']
    ax[0].legend(lst_labels,loc=1,prop={'size':16})




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

if topology != None:
    data_name = data_name + '_%s' % topology
if position != None:
    data_name = data_name + '_%s' % position

from plot.SETTINGS import *
save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)
# mpl_myargs_end
