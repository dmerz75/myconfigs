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
    parser.add_argument("-bar","--bar",help="bars: 0-off, 1-on",type=int)
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

if args['rnd'] != None:
    rnd = args['rnd'].split(',')
else:
    rnd = None

fnum = args['filenumber']
nbins = args['nbins']
cdf_on_off = args['cdf']
bars_on_off = args['bar']

# print rnd
# sys.exit()

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
def load_angle_dct(cwd=my_dir,pattern='*.dat'):
    # FindAllFiles
    print 'cwd:',cwd
    print 'pattern:',pattern
    dct_find = {'cwd':cwd,'pattern':pattern}
    x = FindAllFiles(dct_find)
    # print x.pattern
    x.get_files()
    # x.print_query(x.dct)
    print "Grand total:",len(x.dct.keys()),'of',x.total
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)

    lst_dct = []
    print "Rounds:",rnd
    # if rnd == None:
    #     rnd = []

    if rnd != None:
        for r in rnd:
            set9 = x.query_dirname("round_%s" % r,None,x.dct)
            lst_dct.append(set9)
            # x.print_query(set9)
            print "subtotal:",len(set9.keys()),'of',x.total
            # print len(set9.keys())

        set7 = x.merge_dct(lst_dct)
        # x.print_query(set7)
        print "subtotals:",len(set7.keys()),'of',x.total

    lst_dct = []
    print "Positions:",position
    # if position == None:
    #     position = []

    if position != None:
        for p in position:
            set9 = x.query_dirname(p,-1,x.dct)
            lst_dct.append(set9)
            # x.print_query(set9)
            print "subtotal:",len(set9.keys()),'of',x.total
            # print len(set9.keys())

        set8 = x.merge_dct(lst_dct)
        # x.print_query(set8)
        print "subtotals:",len(set8.keys()),'of',x.total


    if ((rnd != None) and (position != None)):
        set9 = x.get_overlapping_entries(set7,set8)
    elif (rnd != None):
        set9 = set7
    elif (position != None):
        set9 = set8
    else:
        set9 = x.dct

    print "Overlaps:",len(set9.keys()),'of',x.total
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)

    # x.print_query(set9)
    # sys.exit()
    return set9
    # return x.dct

def build_angle_hist_class(dct,rnd,pos):
    """
    Build the cdf class.
    rnd = rounds 10,11,16,26,17
    pos = positions: 1,2,3,4,5
    """
    print "Rounds:",rnd
    print "Positions:",pos

    lst_class = []
    for k,v in dct.iteritems():

        # matchr = 0
        # matchp = 0
        # trajectory = v['dirname'].split('/')[-1]

        # if rnd == None:
        #     matchr = 1
        # else:
        #     for r in rnd:
        #         if re.search(r,trajectory) != None:
        #             matchr = 1
        # if pos == None:
        #     matchp = 1
        # else:
        #     for p in pos:
        #         if re.search(p,trajectory) != None:
        #             matchp = 1

        # # print v
        # if((matchr == 0) and (matchp == 0)):
        #     continue

        x = np.loadtxt(v['file'])
        # print k,trajectory
        # print x.shape
        C = myCDF(x)
        lst_class.append(C)
        # print l,
    return lst_class

def build_exp_angle_hist_class(lst):
    """
    Lst of floats.
    """
    lst_class = []

    for l in lst:
        # print len(l)
        x = np.array(l)
        # print x.shape
        # print x[::,0]
        # print x[::,1]
        # print x[::,]

        C = myCDF(x[::,1])
        lst_class.append(C)

    return lst_class

def build_exp_angle_hist_class100n50(fn):
    """
    Lst of floats.
    """
    x = np.array(fn)
    C = myCDF(x)
    return [C]


def sort_routine1(dct):
    x = FindAllFiles()
    print 'files entered:',len(dct.keys())


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
            # print key
            if re.search(key,v[0]) != None:
                # lst.remove(v)
                lst_data.append(v)
        # print len(lst)



    return lst_data


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



def axis_settings(axes,plot_type='forces',**kwargs):

    for ax in axes:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        ax.tick_params(axis='both',labelsize=18.0)

        if plot_type == 'forces':

            ax.set_xlabel('Forces (nN)',fontsize=20)
            ax.set_ylabel('Norm. Freq.',fontsize=20)

            if xlim[1] < 0.7:
                ax.set_xlim(0.15,0.65)
                ax.set_ylim(-0.01,1.01)
            else:
                ax.set_xlim(0.49,1.01)
                ax.set_ylim(-0.01,1.01)

        if plot_type == 'angle':

            ax.set_xlabel(r"Bending Angle$^\circ$",fontsize=20)
            # ax.set_xlabel('Angle',fontsize=20)
            ax.set_ylabel('Normalized Freq.',fontsize=20)



def legend_settings(ax,lst,**kwargs):

    print 'Legend_settings:'
    for k,v in kwargs.iteritems():
        print k,v
    if 'location' in kwargs:
        loc = kwargs['location']

    ax.legend(lst,loc=loc,prop={'size':18})

    leg = plt.gca().get_legend()
    for label in leg.get_lines():
        label.set_linewidth(2.5)


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






if args['sel'] == 170:
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
    if 'topology' in kwargs:
        topology = kwargs['topology']
    else:
        topology = None
    if 'position' in kwargs:
        position = kwargs['position']
    else:
        position = None


    nbins = 8
    if re.search('critical',dfiles[0]) != None:
        lower_limit = 0.48
        upper_limit = 0.96
    else:
        lower_limit = 0.24
        upper_limit = 0.60



    str_name = ''
    lst_cdf = []
    for i,dfile in enumerate(dfiles):

        tdata = get_lst_tup_data(dfile)
        print len(tdata)
        lst_tdata = get_pertinent_data(tdata,topology)
        lst_tdata = get_pertinent_data(lst_tdata,position)
        data = np.array(sorted([v[2] for v in lst_tdata]))
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
        cdf.plot_bars(ax,color=colors[i],alpha=0.6,label=cdf.name) # color,fill,alpha,pattern,label
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
            print "Do Not Reject."
            Result = 'Do Not Reject. (same dist.)'

        lst_KStups.append((lst_cdf[i].name,lst_cdf[f].name,d,p,Result))
    # sys.exit()

    print "KS-results:"
    for tup in lst_KStups:
        print tup[0],tup[1],tup[2],tup[3],tup[4]

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
    ax.tick_params(axis='both',labelsize=14)
    # ax.axis(size=14)
    ax.set_xlabel('Breaking Force',fontsize=16)
    ax.set_ylabel('Normalized Freq.',fontsize=16)

    P = SaveFig(my_dir,
                'hist_%s_%s' % (result_type,data_name),
                destdirname='fig/histogramCDF')
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


# dct_hist = load_dct(os.path.join(my_dir,'results.crit_breaks'),'rev_*.out')

def process_experimental_angles(fp):
    """
    Process Experimental Angle Data.
    """
    print fp

    lst_numbers = []
    numbers = []

    fo = open(fp,'r')
    line1 = [float(f) for f in fo.readline().split()]
    line_num = 0

    with open(fp,'r') as fp:

        for line in fp:

            if line_num == 0:
                line_num += 1
                previous_line = line1
                numbers.append(previous_line)
                continue

            current_line = [float(f) for f in line.split()]

            # print previous_line[0],current_line[0]

            index1 = float(current_line[0])
            index2 = float(previous_line[0])
            irange = 12.0

            if ((index1 >= index2 - irange) and
                (index1 <= index2 + irange)):
                numbers.append(current_line)
                # print numbers
            else:
                lst_numbers.append(numbers)
                numbers = []
                numbers.append(current_line)


            previous_line = current_line

    # for i in range(1,len(lines)): # line
    #     prev_line = fp[i-1].split()
    #     numbers = fp[i].split()
    #     # numbers = line.split()
    #     print prev_line,numbers

    # print "Groups:",len(lst_numbers)
    # for sec in lst_numbers:
    #     print len(sec)
    #     print sec

    return lst_numbers

    f = open(fp,'r')
    file_contents = f.read()
    # entries = file_contents.split("t:")
    entries = file_contents.split("\t")

    lst_numbers = []
    numbers = []

    print len(entries)


    for string in entries:
        # print string.split()
        # break

        # if int(string) != 0:
        try:
            numbers.append(float(string))
        except ValueError:
            pass

        if re.search("tif",string) != None:

            lst_numbers.append(numbers)
            numbers = []

    for arr in lst_numbers:
        print arr



def get_total_histogram(lst,color='b'):
    """
    Plot the total histograms.
    Combined.
    """

    if len(lst) > 1:
        x = np.concatenate((lst[0].data,lst[1].data))
    else:
        x = lst[0].data

    for i in range(2,len(lst)):
        x = np.concatenate((x,lst[i].data))
    print x.shape


    if rnd != None:
        round_name = ('.').join(rnd)
    else:
        round_name = 'all'

    if position != None:
        position_name = ('.').join(position)
    else:
        position_name = 'all'

    filename = 'array_%s_%s.dat' % (round_name,position_name)
    outfile = os.path.join(my_dir,'results_breaks',filename)
    np.savetxt(outfile,x,fmt='%5.2f')
    # sys.exit()

    cdf = myCDF(x)
    cdf.get_meanstdev()
    cdf.determine_bins_limits(lower_limit=0,upper_limit=80,nbins=81) # set
    cdf.get_hist()
    print "------------------------------------------------"
    cdf.print_values()


    # high_point = 0.0
    # if ax[0].get_ylim()[1] > high_point:
    #     ax[0].set_ylim(0,ax[0].set_ylim()[1] + 0.1 * ax[0].set_ylim()[1])
    #     high_point = ax[0].set_ylim()[1]

    if max(cdf.norm) > ax[0].get_ylim()[1]:
        ax[0].set_ylim(0,max(cdf.norm)+0.1*max(cdf.norm))

    if bars_on_off == 1:
        cdf.plot_bars(ax[0],color=color,alpha=0.8)
        ax[0].set_xlim(-1,72)
        ax[0].set_ylim(0,0.094)

    if (cdf_on_off == 1) and (bars_on_off == 1):
        cdf.plot_cdf(ax[0],color=color,multiplier=0.09)
    elif ((cdf_on_off == 1) and (bars_on_off != 1)):
        cdf.plot_cdf(ax[0],color=color,multiplier=1.0)
        ax[0].set_xlim(-1,72)
        ax[0].set_ylim(-0.02,1.02)


    axis_settings(ax,'angle')
    # if cdf_on_off != None:
        # first one is the hist/cdf
        # second is for cdf only
        # third is for single hist/cdf
        # cdf.plot_cdf(ax[0],color=color,multiplier=ax[0].get_ylim()[1])
        # cdf.plot_cdf(ax[0],color=color)
        # cdf.plot_cdf(ax[0],color=color,multiplier=max(cdf.norm))

    # legend_settings(ax[0],lst=[names])
    # sys.exit()
    # ax[0].set_ylim(0,1.05)

    # if max(cdf.norm) > ax[0].get_ylim()[1]:
    #     ax[0].set_ylim(0,max(cdf.norm)+0.1*max(cdf.norm))
    # ax[0].set_ylim(0,max(cdf.norm)+0.1*max(cdf.norm))





    # if rnd:
    #     P = SaveFig(my_dir,
    #                 'hist_%s_%s' % (result_type,data_name),
    #                 destdirname='fig/histogramCDFangles')
    # else:
    #     P = SaveFig(my_dir,
    #                 'hist_%s_%s' % ('angles',str(rnd)),
    #                 destdirname='fig/histogramCDFangles')

    return x


# Experimental Histogram:
# filename = 'Angles_highsalt_mod.txt'
# filename = 'Angles_highsalt_modkate.txt'
# filename = 'Angles_highsalt_modkate.txt.unix.txt'

# filename = 'highsalt_angles.curated_may24.dat'
# fpath = os.path.join(my_dir,'experimental/',filename)
# Edata = process_experimental_angles(fpath)
# lst_ExpAngles2 = build_exp_angle_hist_class(Edata)
# # sys.exit()

# filename = 'control.dat'
# fpath = os.path.join(my_dir,'experimental/',filename)
# Edata = process_experimental_angles(fpath)
# lst_ExpAnglesC = build_exp_angle_hist_class(Edata)


# Angle Histograms:
dct_anglehist = load_angle_dct(my_dir,"max_angle_criticalbreak_array.dat")
print len(dct_anglehist)
lst_SimAngles = build_angle_hist_class(dct_anglehist,rnd,position)
# print len(lst_Angles)
# sizes = []
# for lst in lst_Angles:
#     sizes.append(lst.data.shape[0])
# print np.mean(np.array(sizes))

# high salt
filename = 'highsalt_angles.curated.dat'
fpath = os.path.join(my_dir,'experimental/',filename)
Sdata = process_experimental_angles(fpath)
lst_ExpHighSalt = build_exp_angle_hist_class(Sdata)


# control
filename = 'angles_controlMTs.curated.dat'
fpath = os.path.join(my_dir,'experimental/',filename)
Cdata = process_experimental_angles(fpath)
lst_ExpCtrl = build_exp_angle_hist_class(Cdata)

filename = 'angles_100nM_fromNan.dat'
fpath = os.path.join(my_dir,'experimental/',filename)
data100 = process_experimental_angles(fpath)
lst_Exp100 = build_exp_angle_hist_class100n50(data100)
# print lst_Exp100
# cdf = lst_Exp100[0]
# print dir(cdf)
# print cdf.data

# filename = 'angles_50nM_fromNan.dat'
# fpath = os.path.join(my_dir,'experimental/',filename)
# data50 = process_experimental_angles(fpath)
# lst_Exp50 = build_exp_angle_hist_class(data50)


# sys.exit()



# New Figure. Get Histograms. (Return Data)
ax = new_fig()
# d,p = Kolmogorov_Smirnov_Test(dataA,dataE)
# dataSim = get_total_histogram(lst_SimAngles,'b')
# dataSalt = get_total_histogram(lst_ExpHighSalt,'r')
# dataCtrl = get_total_histogram(lst_ExpCtrl,'g')

# 1
# dataSim = get_total_histogram(lst_SimAngles,'b')
# dataSalt = get_total_histogram(lst_ExpHighSalt,'r')
# KS = KSTest(dataSim,dataSalt)
# dir_pic = 'simsalt'

# 2
# dataSim = get_total_histogram(lst_SimAngles,'b')
# dataCtrl = get_total_histogram(lst_ExpCtrl,'g')
# KS = KSTest(dataSim,dataCtrl)
# dir_pic = 'simctrl'

# 3
# dataSalt = get_total_histogram(lst_ExpHighSalt,'r')
# dataCtrl = get_total_histogram(lst_ExpCtrl,'g')
# KS = KSTest(dataSalt,dataCtrl)
# dir_pic = 'saltctrl'

# 4
data100s = get_total_histogram(lst_Exp100,'m')
dataSim = get_total_histogram(lst_SimAngles,'b')
KS = KSTest(data100s,dataSime)
dir_pic = 'sim100s'




# print "Doc:"
# print KS.__doc__
KS.print_description()
# basically 80, but going with 60
# KS.compute_KS_and_p_value(size1=60,size2=60)
KS.compute_KS_and_p_value()
KS.evaluate_hypothesis()
KS.print_result()
KS.plot_KS_result(ax[0],color='r',pos=(50,0.05))


filename = "results_angle_histograms_%s.txt" % dir_pic
with open(filename,"a+") as fp:
    fp.write("----\n")
    try:
        fp.write("Rnd: %s\n" % args['rnd'])
    except KeyError:
        pass
    try:
        fp.write("Pos: %s\n" % args['position'])
        # for pos in args['position']:
            # fp.write("Pos: %s\n  " % pos)
    except KeyError:
        pass

    fp.write("%s\n" % KS.Results[0][1])
    fp.write("%s\n" % KS.Results[0][0])

print args
if ('rnd' in args):
    print "Rnd:",args['rnd']
if ('pos' in args):
    print "Pos:",args['position']

print KS.Results[0][1]
print KS.Results[0][0]




if rnd != None:
    round_name = ('.').join(rnd)
else:
    round_name = 'all'

if position != None:
    position_name = ('.').join(position)
else:
    position_name = 'all'

if (cdf_on_off == 1):
    extra_name = 'cdf'
else:
    extra_name = ''
if (bars_on_off == 1):
    extra_name = extra_name + '_bar'

P = SaveFig(my_dir,
            'hist_%s_%s_%s' % (round_name,position_name,extra_name),
            destdirname='fig/histogramCDF_angles/salt_and_control_curated/%s'
            % dir_pic)


'''
What it does:
load_angle             | grabs all of the max_angle_critical_breaks.
                       | (all located in the local trajectory directories)
build_angle_hist_class | returns a list of the angle entries
get_total_histogram    | concatenates the arrays. prints them to file.
                       | then it builds the CDF
'''
