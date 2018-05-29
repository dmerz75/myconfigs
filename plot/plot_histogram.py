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
from plot.SETTINGS import *
import argparse

from plot.SETTINGS import *

#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
#  ---------------------------------------------------------  #
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def new_fig():
    fig = plt.figure(0)
    gs = GridSpec(1,1)
    ax1 = plt.subplot(gs[0,:])
    ax = [ax1]

    fig.set_size_inches(7,5)
    plt.subplots_adjust(left=0.180,right=0.950,top=0.940,bottom=0.22)
    dct_font = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'14'}
    matplotlib.rc('font',**dct_font)
    return ax


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
if args['topology'] != None:
    topology = args['topology'].split(',')
else:
    topology = None
if args['position'] != None:
    position = args['position'].split(',')
else:
    position = None

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

    lst = []
    for k,v in set9.items():
        lst.append(v['file'])
    return lst
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)
    # print len(set9.keys()),'of',x.total
    # sys.exit()
    # return set9
    # return x.dct

# dct_hist = load_dct(os.path.join(my_dir,'results.crit_breaks'),'rev_*.out')
# dct_hist = load_dct(os.path.join(my_dir,'results.crit_breaks'),'pname_*.out')
# for k,v in dct_hist.iteritems():
#     print k,v['filename']
# sys.exit()

def get_data_dep(datafile,topology,position=None):
    print "Processing data."
    print datafile
    print topology,position
    lst_data = []
    with open(datafile,'r+') as fp:
        for line in fp:
            # print line
            # print position
            if (topology != None and position != None):
                if ((re.search(topology,line) != None) and
                    (re.search(position,line) != None)):
                    # print line
                    lst_data.append(float(line.split()[2]))
            elif (topology != None):
                if (re.search(topology,line) != None):
                    # print line
                    lst_data.append(float(line.split()[2]))
            elif (position != None):
                # print position
                if (re.search(position,line) != None):
                    # print line
                    # print position,"Found!"
                    lst_data.append(float(line.split()[2]))
            else:
                # print line.split()
                lst_data.append(float(line.split()[2]))

    lst_data = sorted(lst_data)
    data = np.array(lst_data)
    print "Returning array:",data.shape
    return data

def get_lst_tup_data(datafile,**kwargs):
    """
    Topolgy and Position
    [lists]
    """
    # if kwargs['topology'] != None:
    #     top = list(kwargs['topology'])
    # if 'position' in kwargs:
    #     pos = list(kwargs['position'])

    lst_tupdata = []

    with open(datafile,'r+') as fp:

        for line in fp:
            values = tuple(line.split())
            # lst_data.append(float(line.split()[2]))
            lst_tupdata.append((values[0],values[1],float(values[2])))

    lst_data = sorted(lst_tupdata,key=lambda x: x[2])
    # lst_data = sorted(lst_data)
    # data = np.array(lst_data)
    # for obj in lst_data:
    #     print obj
    return lst_data

def get_pertinent_data(lst,keyword=None):
    """
    Topology and Position
    """
    print "Searching for %s" % keyword
    if keyword == None:
        return lst

    lst_data = []

    for i,v in enumerate(lst):

        # print v[0]

        for key in keyword:
            result = re.search(key,v[0])
            print key,v[0],result
            if result != None:
            # if re.search(key,v[0]) != None:
                # print key,v[0]
                # lst.remove(v)
                lst_data.append(v)

        # print len(lst)



    return lst_data









    #         if kwargs['topology'] != None:
    #             # for
    #             # if re.search(kwargs['topology'],line) == None:
    #             for t in top:
    #                 if re.search(t,line) != None:
    #                     lst_data.append(float(line.split()[2]))

    #                     # no match found.
    #                     # continue

    #         if kwargs['position'] != None:

    #             # if re.search(kwargs['position'],line) == None:
    #             for p in pos:
    #                 if re.search(p,line) == None:
    #                     # continue


    #         lst_data.append(float(line.split()[2]))

    # lst_data = sorted(lst_data)
    # data = np.array(lst_data)
    # print "Returning array:",data.shape
    # return data


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

    return cdf

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

def legend_settings(lst,**kwargs):

    print 'Legend_settings:'
    for k,v in kwargs.iteritems():
        print k,v
    if 'location' in kwargs:
        loc = kwargs['location']
    # if 'upper_limit' in kwargs:
    #     upper_limit = kwargs['upper_limit']

    # legend
    # 1:
    # handles, labels = ax1.get_legend_handles_labels()
    # ax1.legend(handles, labels,prop={'size':10})
    # 2:
    # lst_labels = ['','',]
    ax1.legend(lst,loc=loc,prop={'size':18})
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
# sys.exit()



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

if args['sel'] == 170:
    # RUN
    # cd ~/ext2/completed_mt/ && ./plot_histogram.py -fn 13 -p doz5 -sel 170
    # 13 rev_crit_breaks_16.maxvalue.final0.out nop   magenta
    # 14 rev_crit_breaks_17.maxvalue.final0.out plate green

    # for k,v in dct_hist.iteritems():
    #     print k,v
    # print 'selected:',fnum,dct_hist[fnum].items()
    # sys.exit()

    # 16-nop-magenta
    # 17-plate-green
    data1 = get_data(dct_hist[13]['file'],topology,position)
    data2 = get_data(dct_hist[14]['file'],topology,position)
    # get_cdf(data1,'g',False)
    # get_cdf(data2,'m',False)

    cdf1 = get_cdf(data1,'m',True,
                   lower_limit=0.44,upper_limit=0.85,
                   nbins=6,alpha=0.6,pattern='--') # //
    cdf2 = get_cdf(data2,'g',True,
                   lower_limit=0.44,upper_limit=0.85,
                   nbins=6,alpha=0.6,pattern='\\') # //

    # axis_settings()
    legend_settings(['No Plate','Plate'],location=2)

    cdf1.plot_cdf(color='m')
    cdf2.plot_cdf(color='g')

    ax[0].set_xlim(0.31,.88)
    # ax[0].set_xlim(cdf.lower_limit,cdf.upper_limit)
    ax[0].set_ylim(-0.02,1.05)
    ax[0].set_xlabel('Forces (nN)',fontsize=24)
    # ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    ax[0].set_ylabel('Norm. Freq.',fontsize=24)

    data_name = data_name + '_%s' % args['sel']


    if topology != None:
        data_name = data_name + '_%s' % topology
    if position != None:
            data_name = data_name + '_%s' % position
    data_name = data_name + '_rnd%s' % rnd

    from plot.SETTINGS import *

    P = SaveFig(my_dir,
                'hist_%s_%s' % (result_type,data_name),
                destdirname='fig/histogramCDF/compare16nop17plateg-2')
    sys.exit()

if args['sel'] == 171:
    # RUN
    # cd ~/ext2/completed_mt/ && ./plot_histogram.py -fn 13 -p doz5 -sel 170
    # 12 rev_crit_breaks_16.first.final0.out nop   magenta
    # 15 rev_crit_breaks_17.first.final0.out plate green

    # for k,v in dct_hist.iteritems():
    #     print k,v
    # print 'selected:',fnum,dct_hist[fnum].items()
    # sys.exit()

    # 16-nop-magenta
    # 17-plate-green
    data1 = get_data(dct_hist[12]['file'],topology,position)
    data2 = get_data(dct_hist[15]['file'],topology,position)
    # get_cdf(data1,'g',False)
    # get_cdf(data2,'m',False)

    cdf1 = get_cdf(data1,'m',True,
                   lower_limit=0.20,upper_limit=0.60,
                   nbins=6,alpha=0.6,pattern='--') # //
    cdf2 = get_cdf(data2,'g',True,
                   lower_limit=0.20,upper_limit=0.60,
                   nbins=6,alpha=0.6,pattern='\\') # //

    # axis_settings()
    legend_settings(['No Plate','Plate'],location=2)

    cdf1.plot_cdf(color='m')
    cdf2.plot_cdf(color='g')

    ax[0].set_xlim(0.18,.62)
    # ax[0].set_xlim(cdf.lower_limit,cdf.upper_limit)
    ax[0].set_ylim(-0.02,1.05)
    ax[0].set_xlabel('Forces (nN)',fontsize=24)
    # ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    ax[0].set_ylabel('Norm. Freq.',fontsize=24)

    data_name = data_name + '_%s' % args['sel']


    if topology != None:
        data_name = data_name + '_%s' % topology
    if position != None:
            data_name = data_name + '_%s' % position
    data_name = data_name + '_rnd%s' % rnd

    from plot.SETTINGS import *

    P = SaveFig(my_dir,
                'hist_%s_%s' % (result_type,data_name),
                destdirname='fig/histogramCDF/compare16nop17plateg-2')
    sys.exit()


if args['sel'] == 2000:
    # RUN
    # 0 pname_framebreaks_13.maxvalue.out
    # 1 pname_framebreaks_13.first.out
    # 2 pname_framebreaks_14.first.out
    # 3 pname_framebreaks_14.maxvalue.out
    # 4 pname_framebreaks_17.maxvalue.out
    # 5 pname_framebreaks_17.first.out       # plate
    # 6 pname_framebreaks_1626.first.out     # no plate
    # 7 pname_framebreaks_1626.maxvalue.out

    # cd ~/ext2/completed_mt/ && ./plot_histogram.py -fn 13 -p doz5 -sel 170
    # 12 rev_crit_breaks_16.first.final0.out nop   magenta
    # 15 rev_crit_breaks_17.first.final0.out plate green

    # for k,v in dct_hist.iteritems():
    #     print k,v
    # print 'selected:',fnum,dct_hist[fnum].items()
    # sys.exit()

    # 16-nop-magenta
    # 17-plate-green
    # 0 pname_framebreaks_13.maxvalue.out
    # 1 pname_framebreaks_13.first.out
    # 2 pname_framebreaks_14.first.out
    # 3 pname_framebreaks_14.maxvalue.out
    # 4 pname_framebreaks_16.first.out
    # 5 pname_framebreaks_16.maxvalue.out
    # 6 pname_framebreaks_17.maxvalue.out
    # 7 pname_framebreaks_17.first.out
    # 8 pname_framebreaks_26.first.out
    # 9 pname_framebreaks_26.maxvalue.out
    # 10 pname_framebreaks_1626.first.out
    # 11 pname_framebreaks_1626.maxvalue.out
    # round_13_freeplus
    # round_14_pushmid
    # round_16_mtdoz_complete_nop
    # round_17_mtdozplate
    # round_26_mtdoz
    # round_27_mtdozplate
    if args['sel'] == 2001:
        data1 = get_data(dct_hist[2]['file'],topology)
        data2 = get_data(dct_hist[7]['file'],topology,position)
        name1 = '8-dimer (1st)'
        name2 = '12-dimer, with plate'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 6
    elif args['sel'] == 2002:
        data1 = get_data(dct_hist[2]['file'],topology)
        data2 = get_data(dct_hist[10]['file'],topology,position)
        name1 = '8-dimer (1st)'
        name2 = '12-dimer, no plate'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 6
    elif args['sel'] == 2005:
        data1 = get_data(dct_hist[3]['file'],topology)
        data2 = get_data(dct_hist[6]['file'],topology,position)
        name1 = '8-dimer (crit)'
        name2 = '12-dimer, with plate'
        lower_limit = 0.40
        upper_limit = 0.90
        nbins = 6
    elif args['sel'] == 2006:
        data1 = get_data(dct_hist[3]['file'],topology)
        data2 = get_data(dct_hist[11]['file'],topology,position)
        name1 = '8-dimer (crit)'
        name2 = '12-dimer, no plate'
        lower_limit = 0.40
        upper_limit = 0.90
        nbins = 6

        # FEBRUARY 10th.
    elif args['sel'] == 2007:
        # 10: 0,1 - plate  8s
        # 11: 3,2 - noplate 8s
        desc = 'nop-plate-8s'
        data1 = get_data(dct_hist[3]['file'],topology)
        data2 = get_data(dct_hist[0]['file'],topology,position)
        name1 = '8-dimer (no plate)'
        name2 = '8-dimer (plate)'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 10
    elif args['sel'] == 2008:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        desc = 'nop-plate-8s'
        data1 = get_data(dct_hist[2]['file'],topology)
        data2 = get_data(dct_hist[1]['file'],topology,position)
        name1 = '8-dimer (no plate)'
        name2 = '8-dimer (plate)'
        lower_limit = 0.50
        upper_limit = 0.95
        nbins = 9
        # sys.exit()
    elif args['sel'] == 2009:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'nop-plate-12s'
        data1 = get_data(dct_hist[14]['file'],topology)
        data2 = get_data(dct_hist[10]['file'],topology,position)
        name1 = '12-dimer (no plate)'
        name2 = '12-dimer (plate)'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 10
        # sys.exit()
    elif args['sel'] == 2010:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'nop-plate-12s'
        data1 = get_data(dct_hist[15]['file'],topology)
        data2 = get_data(dct_hist[11]['file'],topology,position)
        name1 = '12-dimer (no plate)'
        name2 = '12-dimer (plate)'
        lower_limit = 0.50
        upper_limit = 0.95
        nbins = 9
        # sys.exit()
    elif args['sel'] == 2011:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'plate-first-8v12s'
        data1 = get_data(dct_hist[0]['file'],topology)
        data2 = get_data(dct_hist[10]['file'],topology,position)
        name1 = '8-dimer (plate)'
        name2 = '12-dimer (plate)'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 10
    elif args['sel'] == 2012:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'plate-crit-8v12s'
        data1 = get_data(dct_hist[1]['file'],topology)
        data2 = get_data(dct_hist[11]['file'],topology,position)
        name1 = '8-dimer (plate)'
        name2 = '12-dimer (plate)'
        lower_limit = 0.50
        upper_limit = 0.95
        nbins = 9
    elif args['sel'] == 2013:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'nop-first-8v12s'
        data1 = get_data(dct_hist[14]['file'],topology)
        data2 = get_data(dct_hist[3]['file'],topology,position)
        name1 = '8-dimer (no plate)'
        name2 = '12-dimer (no plate)'
        lower_limit = 0.20
        upper_limit = 0.60
        nbins = 10
    elif args['sel'] == 2014:
        # 10: 0,1 - plate
        # 11: 3,2 - noplate
        # 17: 10,11 - plate       (12s)
        # 1626: 14, 15 - noplate  (12s)
        # second: plate
        desc = 'nop-crit-8v12s'
        data1 = get_data(dct_hist[15]['file'],topology)
        data2 = get_data(dct_hist[2]['file'],topology,position)
        name1 = '8-dimer (no plate)'
        name2 = '12-dimer (no plate)'
        lower_limit = 0.50
        upper_limit = 0.95
        nbins = 9
        # sys.exit()

    # def plot_distributions(**kwargs):
    #     data1 = get_data(dct_hist[kwargs['nop']],topology,position)
    #     data2 = get_data(dct_hist[kwargs['plate']],topology,position)
        # name1 = '12-dimer



    # get_cdf(data1,'g',False)
    # get_cdf(data2,'m',False)

    cdf1 = get_cdf(data1,'m',True,
                   lower_limit=lower_limit,upper_limit=upper_limit,
                   nbins=nbins,alpha=0.6,pattern='--') # //
    cdf2 = get_cdf(data2,'g',True,
                   lower_limit=lower_limit,upper_limit=upper_limit,
                   nbins=nbins,alpha=0.6,pattern='\\') # //

    cdf1.plot_cdf(color='m')
    cdf2.plot_cdf(color='g')

    # axis_settings()
    legend_settings([name1,name2],location=2)

    ax[0].set_xlim(lower_limit - 0.05,upper_limit + 0.05)
    # ax[0].set_xlim(cdf.lower_limit,cdf.upper_limit)
    ax[0].set_ylim(-0.02,1.05)
    ax[0].set_xlabel('Forces (nN)',fontsize=24)
    # ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
    ax[0].set_ylabel('Norm. Freq.',fontsize=24)

    data_name = data_name + '_%s' % args['sel']

    if topology != None:
        data_name = data_name + '_%s' % topology
    if position != None:
        data_name = data_name + '_%s' % position
    data_name = data_name + '_d%s' % desc

    from plot.SETTINGS import *

    P = SaveFig(my_dir,
                'hist_%s_%s' % (result_type,data_name),
                destdirname='fig/histogramCDF_force')
    sys.exit()


def plot_all(ax,dfiles,**kwargs):
    '''
    Plot all.
    '''
    print "Plotting."
    colors = ['m','g']

    if 'description' in kwargs:
        description = kwargs['description']
    if 'lower_limit' in kwargs:
        lower_limit = kwargs['lower_limit']
    else:
        lower_limit = 0.2
    if 'upper_limit' in kwargs:
        upper_limit = kwargs['upper_limit']
    else:
        upper_limit = 0.6
    if 'nbins' in kwargs:
        nbins = kwargs['nbins']
    else:
        nbins = 6
        # nbins = 10
    if 'topology' in kwargs:
        topology = kwargs['topology']
    else:
        topology = None
    if 'position' in kwargs:
        position = kwargs['position']
    else:
        position = None


    nbins = 12
    print dfiles
    # sys.exit()
    if re.search('.critical.',dfiles[0]) != None:
        lower_limit = 0.48
        upper_limit = 0.96
    else:
        lower_limit = 0.24
        upper_limit = 0.60
    print upper_limit,lower_limit
    # sys.exit()


    str_name = ''
    lst_cdf = []

    patterns = ['-','\\']

    for i,dfile in enumerate(dfiles):

        label = ''
        tdata = get_lst_tup_data(dfile)
        print len(tdata)
        lst_tdata = get_pertinent_data(tdata,topology)
        print len(lst_tdata)
        print "position",position
        lst_tdata = get_pertinent_data(lst_tdata,position)
        print len(lst_tdata)
        data = np.array(sorted([v[2] for v in lst_tdata]))
        avg = np.mean(data)
        print avg
        if ((avg > 0.60) and (avg < 0.90)):
            lower_limit = 0.48
            upper_limit = 0.96
        elif ((avg < 0.60) and (avg > 0.20)):
            lower_limit = 0.24
            upper_limit = 0.62
        # print data.shape
        # print data
        # sys.exit()
        cdf = myCDF(data)
        cdf.name = ('.').join(dfile.split('/')[-1].split('.')[2:6])
        print cdf.name
        # for t in lst_tdata:
        #     print t
        cdf.get_meanstdev()
        # str_name = str_name + cdf.name
        # print str_name
        cdf.determine_bins_limits(nbins=nbins,
                                  lower_limit=lower_limit,
                                  upper_limit=upper_limit) # nbins,lower_limit,upper_limit
        cdf.get_hist() # none,processing
        # cdf.plot_bars(color=color,fill=fill,alpha=alpha,pattern=pattern)
        # cdf.plot_bars(ax,color=colors[i],alpha=0.6,label=cdf.name) # color,fill,alpha,pattern,label
        entity = re.search("Dimers(\d+)",cdf.name)
        # numD = [int(i) for i in re.findall(r'\d+',entity.group())]
        numD = re.findall(r'\d+',entity.group())
        print "entity:",entity.group()
        print "numD:",numD
        label = label + "%sD" % numD[0]
        # sys.exit()

        if re.search("NoPlate",cdf.name) != None:
            label = label + ", No Plate"
            pattern = patterns[i]
        else:
            label = label + ", Plate"
            pattern = patterns[i]
        # label = cdf.name
        cdf.plot_bars(ax,color=colors[i],alpha=0.6,label=label) # color,fill,alpha,pattern,label
        # cdf.plot_bars(ax,color=colors[i],alpha=0.6,label=label,pattern=pattern)
        cdf.plot_cdf(ax,color=colors[i])
        # print 'limits initially: ',cdf.lower_limit,cdf.upper_limit
        # print 'nbins:',nbins
        cdf.print_values()
        lst_cdf.append(cdf)



    # Kolmogorov–Smirnov test
    lst_KStups = []
    for i in range(0,len(lst_cdf),2):
        f = i + 1
        print lst_cdf[i].name," vs. ",lst_cdf[f].name
        print lst_cdf[i].data
        print lst_cdf[f].data
        Result = "Uncertain."

    # d,p = scipy.stats.ks_2samp(data1,data2)
        d,p = Kolmogorov_Smirnov_Test(lst_cdf[i].data,lst_cdf[f].data)
        print """ The null hypothesis is that the distributions of the two
        samples are the same. If the K-S value is small or the p-value is high,
        then reject the null hypothesis."""
        print "K-S value:",d
        print "two-tailed p-value:",p

        # if p < 0.01:
        #     print "We reject the null hypothesis. (a different distribution)"
        #     print "Reject."
        #     Result = 'Reject. diff dist.'
        # elif p > 0.1:
        #     print "We cannot reject the null hypothesis. (more/less the same dist.)"
        #     print "Do Not Reject."
        #     Result = 'Do Not Reject. (same dist.)'
        # else:
        #     print p,"It is uncertain whether we can reject the null hypothesis. Reject. ?"


        if p < 0.05:
            print "We reject the null hypothesis. (a different distribution)"
            print "Reject."
            Result = 'Reject. diff dist.'
        else:
            print "We cannot reject the null hypothesis. (more/less the same dist.)"
            Result = 'Do Not Reject. (same dist.)'
            print Result

        print args

        lst_KStups.append((lst_cdf[i].name,lst_cdf[f].name,d,p,Result))
    # sys.exit()

    # print "KS-results:"
    # for tup in lst_KStups:
    #     print tup[0],tup[1],tup[2],tup[3],tup[4]

    lst_global_ks.append(lst_KStups)

    # Data Name:
    data_name = cdf.name
    # print data_name
    # sys.exit()
    if topology != None:
        data_name = data_name + '_%s' % topology
    if position != None:
        pos_name = ('-').join(position)
        print 'pos_name:',pos_name
        data_name = data_name + '_%s' % pos_name
    if rnd != None:
        data_name = data_name + '_%s' % rnd
    # if description:
    #     description = re.sub(" ","",description)
    #     description = re.sub(",","_",description)
    #     data_name = data_name + '_%s' % description
    data_name = data_name + str_name

    # ax.set_label(fontsize=14)
    ax.tick_params(axis='both',labelsize=18)
    # ax.axis(size=14)

    ax.set_xlabel('Force (nN)',fontsize=20)
    ax.set_ylabel('Normalized Freq.',fontsize=20)

    P = SaveFig(my_dir,
                'hist_%s_%s' % (result_type,data_name),
                destdirname='fig/histogramCDF_force')
    plt.clf()


def print_data_sets(d):
    for k,v in d.items():
        print k,v['file']

def merge_dct(d1,d2):
    print d1
    sys.exit()
    dct = d1.copy()
    dct.update(d2)
    return dct
    # for d in lst:
    #     dct.update(d)
    # return dct


# plt.clf()
# plot_all('lat',topology,position)
# plot_all('lat',position)

# round_10_mt8doz
# round_11_mt8nop
# round_13_freeplus
# round_14_pushmid
# round_16_mtdoz_complete_nop
# round_17_mtdozplate
# round_26_mtdoz
# print_data_sets(files_lat)
# print_data_sets(files_lon)
# print_data_sets(files_first)
# 0 /home/dmerz3/ext/completed_mt/results_breaks/march_firstbreaks/ALL.v1.first.16.out
# 1 /home/dmerz3/ext/completed_mt/results_breaks/march_firstbreaks/ALL.v1.first.17.out
# 2 /home/dmerz3/ext/completed_mt/results_breaks/march_firstbreaks/ALL.v1.first.10.out
# 3 /home/dmerz3/ext/completed_mt/results_breaks/march_firstbreaks/ALL.v1.first.11.out
# ALL.v1.first.10d8plate.out
# ALL.v1.first.11d8nop.out
# ALL.v1.first.16d12nop.out
# ALL.v1.first.17d12plate.out


# plot_all(ax[0],files1,description='nop,plate 12',
#          nbins=8,lower_limit=0.16,upper_limit=0.56)
files_lat = load_dct(my_dir,"ALL.v1.lat*") # lat,lon,first
files_lon = load_dct(my_dir,"ALL.v1.lon*") # lat,lon,first
files_first = load_dct(my_dir,"ALL.v1.first*") # lat,lon,first

if ((args['sel'] >= 700) and (args['sel'] <= 725)):

    files1 = [files_first[2],files_first[3]] # 11-10, nop, plate, 8
    files2 = [files_first[0],files_first[1]] # 16,17, nop, plate, 12
    files3 = [files_first[2],files_first[0]] # 11-16, nop, 8-12
    files4 = [files_first[3],files_first[1]] # 10-17, plate, 8-12

    print files1
    print files2
    print files3
    print files4

    nbins = 8
    lower_limit = 0.18
    upper_limit = 0.50

    ax = new_fig() # 12noplate, 12plate
    plot_all(ax[0],files1,
             nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)

    ax = new_fig() # 8nop, 8plate
    plot_all(ax[0],files2,
             nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)

    ax = new_fig() # description='nop, 8v12')
    plot_all(ax[0],files3,
             nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)

    ax = new_fig() # description='plate, 8v12')
    plot_all(ax[0],files4,
             nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)



if ((args['sel'] >= 750) and (args['sel'] <= 759)):

    # files_first
    # search_dir = os.path.join(my_dir,'results_breaks/r7.manualcuratedbreaks2')
    # files_first = load_dct(search_dir,"ALL.v1.*.out") # lat,lon,first
    # files_first = sorted(files_first)

    # print files_first
    # for f in files_first:
    #     print f
    # sys.exit()
    files_first = [
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.11.Dimers8.NoPlate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.10.Dimers8.Plate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.16.Dimers12.NoPlate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.17.Dimers12.Plate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.11.Dimers8.NoPlate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.10.Dimers8.Plate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.16.Dimers12.NoPlate.out',
        '/home/dmerz3/ext/completed_mt/results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.17.Dimers12.Plate.out']
    # results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.10.Dimers8.Plate.out     results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.10.Dimers8.Plate.out
    # results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.11.Dimers8.NoPlate.out   results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.11.Dimers8.NoPlate.out
    # results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.16.Dimers12.NoPlate.out  results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.16.Dimers12.NoPlate.out
    # results_breaks/r7.manualcuratedbreaks2/ALL.v1.critical.17.Dimers12.Plate.out    results_breaks/r7.manualcuratedbreaks2/ALL.v1.first.17.Dimers12.Plate.out
    # for f in files_first:
    #     print f
    # sys.exit()

    # nbins = 6
    # lower_limit = 0.18
    # upper_limit = 0.50

    tup_files = [(0,1),(2,3),(4,5),(6,7),(0,2),(1,3),
                 (4,6),(5,7)]

    lst_global_ks = []
    for t in range(len(tup_files)):
        files = [files_first[tup_files[t][0]],
                 files_first[tup_files[t][1]]]
        print "New_Set:",t
        print files
        ax = new_fig()
        plot_all(ax[0],files,nbins=nbins,topology=topology,position=position)
        axis_settings()


    # def print_this()
    for lst in lst_global_ks:
        # print (' ').join([str(obj) for obj in lst])
        for tup in lst:
            print tup[0],tup[1]
        # for tup in lst:
        #     print '%5.3f' % tup[2], '%5.3f' % tup[3],tup[4]

    for lst in lst_global_ks:
        # print (' ').join([str(obj) for obj in lst])
        # for tup in lst:
        #     print tup[0],tup[1]
        for tup in lst:
            print '%5.3f' % tup[2], '%5.3f' % tup[3],tup[4]

    sys.exit()

    positions = ['oz1','oz2','oz3','oz4','oz5']


    for t in range(len(tup_files)):
        files = [files_first[tup_files[t][0]],
                 files_first[tup_files[t][1]]]
        print files
        for i in range(5):
            ax = new_fig()
            plot_all(ax[0],files,
                     nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit,
                     position=positions[i])

    # ax = new_fig() # 8nop, 8plate
    # plot_all(ax[0],files2,
    #          nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)

    # ax = new_fig() # description='nop, 8v12')
    # plot_all(ax[0],files3,
    #          nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)

    # ax = new_fig() # description='plate, 8v12')
    # plot_all(ax[0],files4,
    #          nbins=nbins,lower_limit=lower_limit,upper_limit=upper_limit)



# dfiles1 = update_dct(files1)
# for k,v in dfiles1.items():
#     print k,v
# # files2 = [files_]

# # print datafiles
# # datafiles1 =
# plot_all(ax[0],dfiles1,None,None)
# -----------------

if (args['sel'] >= 5000):

    # print my_dir
    files_forces = glob.glob(os.path.join(my_dir,"results_breaks/r10.*/*.out"))
    files_first = sorted(files_forces)
    # for f in files_forces:
    #     print f
    # 0  ALL.v1.critical.10.Dimers8.Plate.out
    # 1  ALL.v1.critical.11.Dimers8.NoPlate.out
    # 2  ALL.v1.critical.16.Dimers12.NoPlate.out
    # 3  ALL.v1.critical.17.Dimers12.Plate.out
    # 4  ALL.v1.first.10.Dimers8.Plate.out
    # 5  ALL.v1.first.11.Dimers8.NoPlate.out
    # 6  ALL.v1.first.16.Dimers12.NoPlate.out
    # 7  ALL.v1.first.17.Dimers12.Plate.out
    # sys.exit()
    # tup_files = [(4,0),(5,1),(6,2),(7,3)] # first,crit
    tup_files = [(0,1),(3,2),(4,5),(7,6),
                 (0,3),(1,2),(4,7),(5,6)] # Plate,NOP

    lst_global_ks = []
    for t in range(len(tup_files)):
        files = [files_first[tup_files[t][0]],
                 files_first[tup_files[t][1]]]
        ax = new_fig()
        plot_all(ax[0],files,nbins=nbins,topology=topology,position=position)
        axis_settings()


    # def print_this()
    print "Final_KS_Results:"
    for lst in lst_global_ks:
        # print (' ').join([str(obj) for obj in lst])
        for tup in lst:
            print tup[0],tup[1]
        # for tup in lst:
        #     print '%5.3f' % tup[2], '%5.3f' % tup[3],tup[4]

    for lst in lst_global_ks:
        # print (' ').join([str(obj) for obj in lst])
        # for tup in lst:
        #     print tup[0],tup[1]
        for tup in lst:
            # print tup[0],tup[1]
            print '%5.3f' % tup[2], '%5.3f' % tup[3],tup[4]

    sys.exit()
