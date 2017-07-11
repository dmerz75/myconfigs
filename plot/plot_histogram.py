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
# print my_dir
# sys.exit()

#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from plot.cdf import *
from mylib.FindAllFiles import *

#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
#  ---------------------------------------------------------  #
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
ax = [ax1]

fig.set_size_inches(7,5)
plt.subplots_adjust(left=0.180,right=0.950,top=0.940,bottom=0.22)
dct_font = {'family':'sans-serif',
            'weight':'normal',
            'size'  :'20'}
matplotlib.rc('font',**dct_font)

#  ---------------------------------------------------------  #
#  Import Data! (2/4)                                         #
#  ---------------------------------------------------------  #
result_type = 'force' # sop | sopnucleo | gsop | namd
plot_type = 'hist' # fe | tension | rmsd | rdf
data_name = 'cdf'
option = None

#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--topology",help="topology: all, reg, AHM, LHM, or top56")
    parser.add_argument("-p","--position",help="position: doz1,doz2,doz3,doz4,doz5")
    parser.add_argument("-fn","--filenumber",help="filenumber: 0,1,2 ..",type=int)
    parser.add_argument("-rnd","--rnd",help="round: 13, 14, 16, 17")
    parser.add_argument("-nb","--nbins",help="number of bins: 3,4,5,6..",type=int)
    parser.add_argument("-cdf","--cdf",help="cdf-line: 0-off, 1-on",type=int)
    parser.add_argument("-sel","--sel",help="select: 100,101,102..",type=int)
    args = vars(parser.parse_args())
    return args


args = parse_arguments()
topology = args['topology']
position = args['position']
rnd = args['rnd']
fnum = args['filenumber']
nbins = args['nbins']
cdf_on_off = args['cdf']
# MY ARGS:
# topology: all, AHM, reg, LHM, top56
# position: doz1,2,3,4,5


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
    set9 = x.remove_dirname('fail',None,x.dct)
    # set9 = x.query_filename(rnd,set9)
    set9 = x.sort_filename(set9)
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)
    # print len(set9.keys()),'of',x.total
    # sys.exit()
    return set9
    # return x.dct

dct_hist = load_dct(os.path.join(my_dir,'results.crit_breaks'),'rev_*.out')
for k,v in dct_hist.iteritems():
    print k,v['filename']
# sys.exit()

def get_data(datafile,topology,position):
    print datafile
    lst_data = []
    with open(datafile,'r+') as fp:
        for line in fp:
            # print line
            # print position
            if (topology != None and position != None):
                if ((re.search(topology,line) != None) and
                    (re.search(position,line) != None)):
                    # print line
                    lst_data.append(float(line.split()[1]))
            elif (topology != None):
                if (re.search(topology,line) != None):
                    # print line
                    lst_data.append(float(line.split()[1]))
            elif (position != None):
                # print position
                if (re.search(position,line) != None):
                    # print line
                    lst_data.append(float(line.split()[1]))
            else:
                print line.split()
                lst_data.append(float(line.split()[1]))

    data = np.array(lst_data)
    print data.shape
    return data


def get_cdf(data,color='b',fill=True,**kwargs):
    '''
    '''
    if 'lower_limit' in kwargs:
        lower_limit = kwargs['lower_limit']
    else:
        lower_limit = min(data)

    if 'upper_limit' in kwargs:
        upper_limit = kwargs['upper_limit']
    else:
        upper_limit = max(data)

    if 'nbins' in kwargs:
        nbins = kwargs['nbins']
    else:
        nbins = 3

    if 'alpha' in kwargs:
        alpha = kwargs['alpha']
    else:
        alpha = 1.0

    if 'pattern' in kwargs:
        pattern = kwargs['pattern']
    else:
        pattern = None

    print 'nbins:',nbins
    # sys.exit()
    cdf = myCDF(data)
    # cdf.print_class()

    # cdf.determine_bins(lower_limit=0.3,upper_limit=0.6,nbins=3) # set
    # cdf.determine_bins_limits(lower_limit=0.3,upper_limit=0.6,nbins=)
    cdf.determine_bins_limits(lower_limit=lower_limit,
                              upper_limit=upper_limit,
                              nbins=nbins) # set


    # print cdf.bins
    # print alpha
    # sys.exit()

    # cdf.get_hist(bins=cdbins)
    cdf.get_hist()
    cdf.print_values()
    cdf.plot_bars(color=color,fill=fill,alpha=alpha,pattern=pattern)

    if cdf_on_off != None:
        cdf.plot_cdf(color=color)

    # cdf.plot_hist4(data,bins,color='b')
    # cdf.plot_cdf(data,color='b')

    # stats:
    cdf.print_stats()

    # if re.search('max',v['file']) != None:
    #     data_name = data_name + '_max'
    # elif re.search('first',v['file']) != None:
    #     data_name = data_name + '_first'

    # if re.search('2pts',v['file']) != None:
    #     data_name = data_name + '_2pts'
    # elif re.search('1pts',v['file']) != None:
    #     data_name = data_name + '_1pts'


def axis_settings(**kwargs):
    xlim = ax[0].get_xlim()
    ylim = ax[0].get_ylim()

    ax[0].tick_params(axis='both',labelsize=18.0)
    ax[0].set_xlabel('Forces (nN)',fontsize=20)
    ax[0].set_ylabel('Norm. Freq.',fontsize=20)

    if xlim[1] < 0.7:
        ax[0].set_xlim(0.15,0.65)
        ax[0].set_ylim(-0.01,1.01)
    else:
        ax[0].set_xlim(0.49,1.01)
        ax[0].set_ylim(-0.01,1.01)

    # try:
    #     ax[0].set_xlim(0.18,1.2)
    #     # ax[0].set_xlim(cdf.lower_limit,cdf.upper_limit)
    #     ax[0].set_ylim(-0.01,1.01)
    #     ax[0].set_xlabel('Forces',fontsize=24)
    #     # ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    #     ax[0].set_ylabel('Norm. Freq.',fontsize=24)
    # except NameError:
    #     pass

def legend_settings(lst):

    # legend
    # 1:
    # handles, labels = ax1.get_legend_handles_labels()
    # ax1.legend(handles, labels,prop={'size':10})
    # 2:
    # lst_labels = ['','',]
    ax1.legend(lst,loc=1,prop={'size':18})
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
if 0:
    # colors = ['red','blue','m','cyan']
    colors = ['firebrick','red','blue','cyan']
    colors = ['blue']

    # Get myCDF
    # for i,f in enumerate(lst_files):
    for k,v in dct_hist.iteritems():

        if fnum != k:
            continue

        # data = get_data(f,topology,position)
        # print v['file']
        data = get_data(v['file'],topology,position)
        cdf = myCDF(data)
        # cdf.print_class()

        # cdf.determine_bins(lower_limit=0.3,upper_limit=0.6,nbins=3) # set
        cdf.determine_bins_limits(nbins=nbins) # set
        # print cdf.bins

        # cdf.get_hist(bins=cdbins)
        cdf.get_hist()
        cdf.print_values()

        cdf.plot_bars(color='b')

        if cdf_on_off != None:
            cdf.plot_cdf(color='b')

        # cdf.plot_hist4(data,bins,color='b')
        # cdf.plot_cdf(data,color='b')

        # stats:
        cdf.print_stats()

        if re.search('max',v['file']) != None:
            data_name = data_name + '_max'
        elif re.search('first',v['file']) != None:
            data_name = data_name + '_first'

        if re.search('2pts',v['file']) != None:
            data_name = data_name + '_2pts'
        elif re.search('1pts',v['file']) != None:
            data_name = data_name + '_1pts'




for k,v in dct_hist.iteritems():
    print k,v


# 0 rev_crit_breaks_mt8_combined.maxvalue.out
# 1 rev_crit_breaks_mt8_combined.first.out
# 2 rev_crit_breaks_mt12_np.maxvalue.out
# 3 rev_crit_breaks_mt12_p.maxvalue.out
# 4 rev_crit_breaks_mt12_p.first.out
# 5 rev_crit_breaks_mt12_np.first.out
# 6 rev_crit_breaks_13.maxvalue.out
# 7 rev_crit_breaks_13.first.out
# 8 rev_crit_breaks_14.2pts.first.out
# 9 rev_crit_breaks_14.2pts.maxvalue.out
# 10 rev_crit_breaks_14.1pts.maxvalue.out
# 11 rev_crit_breaks_14.1pts.first.out
# 12 rev_crit_breaks_16.first.final0.out
# 13 rev_crit_breaks_16.maxvalue.final0.out
# 14 rev_crit_breaks_17.maxvalue.final0.out
# 15 rev_crit_breaks_17.first.final0.out

if args['sel'] == 100:
    data_name = data_name + '_812plate_main_first'
    colors = ['r','b']
    fillval= [False,False]

    data = get_data(dct_hist[1]['file'],topology,position)
    get_cdf(data,'r',True,
            lower_limit=0.2,upper_limit=0.6,
            nbins=6,alpha=0.6,pattern='--') # //

    data = get_data(dct_hist[4]['file'],topology,position)
    get_cdf(data,'b',True,
            lower_limit=0.2,upper_limit=0.6,
            nbins=6,alpha=0.4,pattern='\\')

    axis_settings()
    legend_settings(['8-dimer','12-dimer'])

if args['sel'] == 101:
    data_name = data_name + '_812plate_main_crit'
    colors = ['r','b']
    fillval= [False,False]

    data = get_data(dct_hist[0]['file'],topology,position)
    get_cdf(data,'r',True,
            lower_limit=0.6,upper_limit=1.0,
            nbins=6,alpha=0.6,pattern='--') # //

    data = get_data(dct_hist[3]['file'],topology,position)
    get_cdf(data,'b',True,
            lower_limit=0.6,upper_limit=1.0,
            nbins=6,alpha=0.4,pattern='\\')

    axis_settings()
    legend_settings(['8-dimer','12-dimer'])

if args['sel'] == 102:
    data_name = data_name + '_812noplate_main_first'
    colors = ['r','b']
    fillval= [False,False]

    data = get_data(dct_hist[1]['file'],topology,position)
    get_cdf(data,'r',True,
            lower_limit=0.2,upper_limit=0.6,
            nbins=6,alpha=0.6,pattern='--') # //

    data = get_data(dct_hist[5]['file'],topology,position)
    get_cdf(data,'b',True,
            lower_limit=0.2,upper_limit=0.6,
            nbins=6,alpha=0.4,pattern='\\')

    axis_settings()
    legend_settings(['8-dimer','12-dimer'])

if args['sel'] == 103:
    data_name = data_name + '_812noplate_main_crit'
    colors = ['r','b']
    fillval= [False,False]

    data = get_data(dct_hist[0]['file'],topology,position)
    get_cdf(data,'r',True,
            lower_limit=0.6,upper_limit=1.0,
            nbins=6,alpha=0.6,pattern='--') # //

    data = get_data(dct_hist[2]['file'],topology,position)
    get_cdf(data,'b',True,
            lower_limit=0.6,upper_limit=1.0,
            nbins=6,alpha=0.4,pattern='\\')

    axis_settings()
    legend_settings(['8-dimer','12-dimer'])



if 0:
    data_name = data_name + '_812plate_main'
    colors = ['g','b','orange','r']
    fillval= [False,False,True,True]
    limits = [(0.22,0.5),(0.48,0.9),(0.22,0.5),(0.48,0.9)]
    for i,k in enumerate([1,0,4,3]): # 8 first, max, 12p first, max
        data = get_data(dct_hist[k]['file'],topology,position)
        get_cdf(data,colors[i],fillval[i],
                lower_limit=limits[i][0],
                upper_limit=limits[i][1])

    axis_settings()
    legend_settings(['mt8-first','mt8-crit','mt12-plate-first','mt12-plate-crit'])
# else:
if 0:
    data_name = data_name + '_8_12noplate'
    colors = ['g','b','orange','r']
    fillval= [False,False,True,True]
    limits = [(0.22,0.5),(0.48,0.9),(0.22,0.5),(0.48,0.9)]
    for i,k in enumerate([1,0,5,2]): # 8 first, max, 12np first, max
        data = get_data(dct_hist[k]['file'],topology,position)
        # get_cdf(data,colors[i],fillval[i])
        get_cdf(data,colors[i],fillval[i],
                lower_limit=limits[i][0],
                upper_limit=limits[i][1])

    axis_settings()
    legend_settings(['mt8-first','mt8-crit','mt12-noplate-first','mt12-noplate-crit'])


if 0:
    for k in [1,0,5,2]: # 8 first, max, 12np first, max
        pass

    data1 = get_data(dct_hist[0]['file'],topology,position)
    data2 = get_data(dct_hist[1]['file'],topology,position)
    get_cdf(data1,'b',False)
    get_cdf(data2,'g',False)


    data1 = get_data(dct_hist[0]['file'],topology,position)
    data2 = get_data(dct_hist[1]['file'],topology,position)
    get_cdf(data1,'b',False)
    get_cdf(data2,'g',False)


    # data_name =

    # Plot Adjustments:

    try:
        ax[0].set_xlim(0.18,1.2)
        # ax[0].set_xlim(cdf.lower_limit,cdf.upper_limit)
        ax[0].set_ylim(-0.01,1.01)
        ax[0].set_xlabel('Forces',fontsize=24)
        ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    except NameError:
        pass

    # legend
    # 16-NoPlate
    # 17-Plate
    # lst_labels = ['NoPlate-1st','NoPlate-Crit','Plate-1st','Plate-Crit']
    # ax[0].legend(lst_labels,loc=1,prop={'size':16})



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
data_name = data_name + '_rnd%s' % rnd

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
            destdirname='fig/histogramCDF')
