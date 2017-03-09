#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time
import numpy as np
import numpy.ma as ma
import re
import pickle

my_dir = os.path.abspath(os.path.dirname(__file__))

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *
from microtubule import *
# libraries:
# from mylib.FindAllFiles import *
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
# from mylib.run_command import run_command


#  ---------------------------------------------------------  #
#  Begin.argparse                                             #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="options .. show")
    parser.add_argument("-b","--both",help="plot contacts and force-indentation")
    parser.add_argument("-i","--integers",help="force-indenation: give integer")
    parser.add_argument("-n","--nesw",help="NESW: contacts by north,south,east,west..")
    parser.add_argument("-f","--force",help="force plot: (off) or on",type=int)
    parser.add_argument("-ff","--forceframecontacts",help=" \
    ff: ff.file line: seamup_doz5_fix2_top56_6_nop_00,250,400 \
                        <name>,<first-break>,<second-break>")
    parser.add_argument("-e","--emol",help=
                        "for plotting emol_mtcontacts_by_subdomain \n \
                        or emol_mtcontacts_by_subdomain3(n), \n \
                        None/0-off,1-on,2-emol3n,4-emol-6x3-dimer-regions \n \
                        other ..",
                        type=int)
    # parser.add_argument("-e","--emol",help=
    #                     "for plotting emol_mtcontacts_by_subdomain \n \
    #                     or emol_mtcontacts_by_subdomain3(n), \n \
    #                     None/0-off,1-on,2-emol3n ..",
    #                     type=int)
    parser.add_argument("-c","--contacts",help="contact plot: (off) or on")
    parser.add_argument("-psf","--psf",help="psf: file")
    parser.add_argument("-nd","--nd",help="num_dimers: 104, 156",type=int)
    parser.add_argument("-r","--run",help="the run commands: (0-both,1-forcei,2-Qn/Contacts) plot_everything, 1-78,83 prints",type=int)
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
option = args['option']
psffile = args['psf']
num_dimers = args['nd']


if args['integers']:
    if re.search(',',args['integers']):
        args['integers'] = [int(x) for x in args['integers'].split(',')]
    else:
        args['integers'] = [int(args['integers'])]
# print args['integers'],type(args['integers'])

def load_dct(cwd=my_dir,pattern='*.dat'):
    # FindAllFiles
    print 'cwd:',cwd
    print 'pattern:',pattern
    dct_find = {'cwd':cwd,'pattern':pattern}
    x = FindAllFiles(dct_find)
    x.get_files()
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    set9 = x.remove_dirname('fail',None,x.dct)
    set9 = x.remove_dirname('example',None,set9)
    return set9

# Find all mt_analysis.dat files.
dct_traj = load_dct(os.path.join(my_dir,'indentation'),'mt_analysis.dat')
print len(dct_traj.keys())



#  ---------------------------------------------------------  #
#  Classify microtubules.                                     #
#  ---------------------------------------------------------  #
mt_list = []

count = 0
for k,v in dct_traj.iteritems():
    count += 1
    # print k,v['dirname']
    name = v['dirname'].split('/')[-1]
    mt = Microtubule(name)
    mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
    # mt.print_class()
    # continue

    mt.my_dir = my_dir
    mt.setupdirs()
    '''
    self.datdir = os.path.join(self.dirname,'dat')
    self.dcddir = os.path.join(self.dirname,'dcd')
    self.indentationdir = os.path.join(self.dirname,'indentation')
    self.outputdir = os.path.join(self.dirname,'output')
    self.topdir = os.path.join(self.dirname,'topologies')
    '''
    mt.set_attributes(v)
    mt.find_psf(my_dir,psffile)
    mt.find_dcd()
    mt.get_frame_count()
    mt.get_analysis_file()
    mt.get_indentation_file()
    mt.get_pdbs()
    mt.get_direction_info() # forward or reverse:
    mt.get_plate_info() # with plate or without:
    mt.get_reversal_frame()
    mt.get_sop_file()
    mt.get_sop_info()
    mt_list.append(mt)

# ^^ Run no matter what.



def build_1st_mt(dct):

    mt_list = []
    count = 0

    for k,v in dct.iteritems():
        count += 1
        # print k,v['dirname']
        name = v['dirname'].split('/')[-1]
        mt = Microtubule(name)
        mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
        # mt.print_class()
        # continue

        mt.my_dir = my_dir
        mt.setupdirs()
        '''
        self.datdir = os.path.join(self.dirname,'dat')
        self.dcddir = os.path.join(self.dirname,'dcd')
        self.indentationdir = os.path.join(self.dirname,'indentation')
        self.outputdir = os.path.join(self.dirname,'output')
        self.topdir = os.path.join(self.dirname,'topologies')
        '''
        mt.set_attributes(v)
        mt.find_psf(my_dir,psffile)
        mt.find_dcd()
        mt.get_frame_count()
        mt.get_analysis_file()
        mt.get_indentation_file()
        mt.get_pdbs()
        mt.get_direction_info() # forward or reverse:
        mt.get_plate_info() # with plate or without:
        mt.get_reversal_frame()
        mt.get_sop_file()
        mt.get_sop_info()
        mt_list.append(mt)

    return mt_list


# print len(mt_list)
# for i,mt in enumerate(mt_list):
#     # print i,mt.dirname
#     # print i,mt.name
#     if re.search('round_16',mt.dirname) != None:
#         print mt.name,' ',mt.total_frames,'\t\t    # max-%d' % mt.total_frames
#         # print dir(mt)
# # sys.exit()


def build_mt(mt):
    # mt_list[i].get_mtanalysis()
    # mt_list[i].get_dimers()
    # mt_list[i].get_integersndentation()
    # mt_list[i].get_force_by_time_series()
    # mt_list[i].get_analysis_by_time_series()

    if not hasattr(mt,'ext_raw'):
        mt.get_forceindentation()

    if not hasattr(mt,'contacts'):
        mt.get_mtanalysis(num_dimers)

    if not mt.dimers: # defaults to empty list
        mt.get_dimers()

    if not hasattr(mt,'force'):
        mt.get_force_by_time_series()

    if not hasattr(mt,'analysis'):
        mt.get_analysis_by_time_series()


# def print_lists(string1):
#     for i,mt in enumerate(mt_list):
#         if re.search(string1,mt.dirname) != None:
#             print mt.name
def print_lst_args(*args):
    lst = []
    for a in args:
        print a
    for i,mt in enumerate(mt_list):
        lst_ans = [re.search(a,mt.dirname) for a in args]
        # print lst_ans
        if None in lst_ans:
            continue
        else:
            lst.append(mt.name)
            # print mt.name
    return lst


# PRINT ALL: 16-17-AHM-LHM-top56-REG
# Creates the original pickle.
if 0:
    dct_crit = {}
    dct_crit['round_16'] = {}
    # dct_crit[('round_16','AHM')] = {}
    # dct_crit[('round_16','LHM')] = {}
    # dct_crit[('round_16','reg')] = {}
    # dct_crit[('round_16','top56')] = {}
    dct_crit['round_17'] = {}
    # dct_crit[('round_17','AHM')] = {}
    # dct_crit[('round_17','LHM')] = {}
    # dct_crit[('round_17','reg')] = {}
    # dct_crit[('round_17','top56')] = {}

    for k,v in dct_crit.iteritems():
        print k
        if type(k) == str:
            lst = print_lst_args(k)
        else:
            lst = print_lst_args(*k)
        dct_crit[k] = sorted(lst)


    # for tup in lst_tup:
    print 'results:'
    for k,v in dct_crit.iteritems():
        if type(k) == str:
            the_key = k
        else:
            the_key = '-'.join(s for s in k)
        print '%s:' % the_key

        for m in v:
            print m

    print 'Pickling ..'
    pickle.dump(dct_crit,open(os.path.join(my_dir,'dct_1617.pkl'),'w+'))
    sys.exit()

if 0:
    print 'hello'
    dct_crit = pickle.load(open('dct_1617.pkl','r'))

    for k,v in dct_crit.iteritems():
        if type(k) == str:
            the_key = k
        else:
            the_key = '-'.join(s for s in k)
        print '%s:' % the_key

        for m in v:
            print m
            try:
                print dct_crit[m]['first']
            except:
                pass
            # try:
            #     print m['first']
            #     print m['second']
            # except:
            #     pass
            # try:
            #     print m['first']
            #     print m['second']
            #     print m['third']
            # except:
            #     pass
    sys.exit()





#  ---------------------------------------------------------  #
#  Sorting.                                                   #
#  ---------------------------------------------------------  #
print len(mt_list)
for i,mt in enumerate(mt_list):
    # print i,mt.dirname
    print i,mt.name

def print_1617_sort():
    print len(mt_list)
    lst_16 = []
    lst_16names = []
    lst_17 = []
    lst_17names = []

    for i,mt in enumerate(mt_list):
        if re.search('round_17',mt.dirname) != None:
            print mt.name
            lst_17.append(i)
            lst_17names.append(mt.name)
        if re.search('round_16',mt.dirname) != None:
            print mt.name
            lst_16.append(i)
            lst_16names.append(mt.name)

    # print '16:'
    # for i in lst_16:
    #     print mt_list[i].name

    # print '17:'
    # for i in lst_17:
    #     print mt_list[i].name

    print '16-names:'
    for f in sorted(lst_16names):
        print f

    print '17-names:'
    for f in sorted(lst_17names):
        print f

    sys.exit()
# print_1617_sort()


# need forward.
# need reversals w/ plate.
# need reversals w/o plate.
lst_forward = [i for i,m in enumerate(mt_list) if m.direction == 'forward']
print 'forward:'
print lst_forward
# sys.exit()


dct_rev = {} # SORTING Dictionary!

for i in lst_forward:
    dct_rev[i] = {}
    dct_rev[i]['plate'] = []
    dct_rev[i]['noplate'] = []

    for j,m in enumerate(mt_list):

        if re.search(mt_list[i].name,mt_list[j].name) != None:
            if (mt_list[j].plate == 'yes'):

                if j != i:
                    dct_rev[i]['plate'].append(j)
            else:
                if j != i:
                    dct_rev[i]['noplate'].append(j)

lst_com = []

# if args['run'] == 1:
if 1:
    for k,v in dct_rev.iteritems():
        print k,mt_list[k].name
        # print '  ',mt_list[k].max_x20,' ',mt_list[k].max_y20
        if v['plate']:
            print 'plate:',v['plate']
            for rtraj in v['plate']:
                print '\t',rtraj,mt_list[rtraj].name
                # print "./plot_everything.py -c %d,%d" % (k,rtraj)
        if v['noplate']:
            print 'noplate:',v['noplate']
            for rtraj in v['noplate']:
                print '\t',rtraj,mt_list[rtraj].name
                # print "./plot_everything.py -c %d,%d" % (k,rtraj)

        if v['plate']:
            for v1 in v['plate']:
                # print (k,v1)
                lst_com.append((k,v1))
        if v['noplate']:
            for v1 in v['noplate']:
                # print (k,v1)
                lst_com.append((k,v1))
        # print (k,)


if args['run'] in [0,1,2,3]:
    for k,v in dct_rev.iteritems():
        # print k,mt_list[k].name
        # print '  ',mt_list[k].max_x20,' ',mt_list[k].max_y20
        if v['plate']:
            # print 'plate:',v['plate']
            for rtraj in v['plate']:
                # print '\t',rtraj,mt_list[rtraj].name

                if ((args['run'] == 1) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -f 1" % (k,rtraj)
                if ((args['run'] == 2) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -c 1" % (k,rtraj)
                if ((args['run'] == 3) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -b 1" % (k,rtraj)
        if v['noplate']:
            # print 'noplate:',v['noplate']
            for rtraj in v['noplate']:
                # print '\t',rtraj,mt_list[rtraj].name
                if ((args['run'] == 1) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -f 1" % (k,rtraj)
                if ((args['run'] == 2) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -c 1" % (k,rtraj)
                if ((args['run'] == 3) or (args['run'] == 0)):
                    print "./plot_everything.py -i %d,%d -b 1" % (k,rtraj)
        if v['plate']:
            for v1 in v['plate']:
                # print (k,v1)
                lst_com.append((k,v1))
        if v['noplate']:
            for v1 in v['noplate']:
                # print (k,v1)
                lst_com.append((k,v1))
        # print (k,)


print 'forwards:',lst_forward
# print 'forwards:',dct_rev.keys()
# print 'reverse w/plate:',[i for i in dct_rev.keys() if len(dct_rev[i]['plate']) > 0]
# print 'reverse w/o plate:',[i for i in dct_rev.keys() if len(dct_rev[i]['noplate']) > 0]


#  ---------------------------------------------------------  #
#  Combine Classes.                                           #
#  ---------------------------------------------------------  #
def combine_classes(m1,m2):

    # print type(m1),type(m2)
    # sys.exit()
    i1 = mt_list.index(m1)
    i2 = mt_list.index(m2)

    newid = str('%d_%d' % (i1,i2))
    print 'newid:',newid
    cmt = Microtubule('%s' % newid)

    cmt.dimers = m1.dimers
    print 'cmt-dimers:',cmt.dimers

    combines = ['frames','numfixedbeads','numsteps','plate','steps','tipx',
                'tipy','tipz','total_frames','analysis','angles','curvature',
                'data','deltax','direction','end_to_end','ext_raw',
                'externalcontacts','f_nano','f_pico','force','max_x20',
                'max_y20','contacts']

    # print getattr(m1,'ext_raw')[::100]
    # print getattr(m2,'ext_raw')[::100]
    # print getattr(m1,'force').shape
    # print getattr(m1,'force')[::10,1]
    # # [::10,]
    # print getattr(m2,'force').shape
    # print getattr(m2,'force')[::10,1]
    # [::10,]
    # sys.exit()


    # for obj in dir(cmt):
    for obj in combines:
        # print obj
        value = ''

        if obj == 'frames':
            ar1 = getattr(m1,obj)
            ar2 = getattr(m2,obj)
            ar2mod = ar2 + ar1[-1] + 1
            value = np.concatenate((ar1,ar2mod),axis=0)

        # equal
        # if ((obj == 'numfixedbeads') or (obj == 'plate')):
        if ((obj == 'numfixedbeads')):
            if getattr(m1,obj) != getattr(m2,obj):
                print getattr(m1,obj),getattr(m2,obj)
                print obj,'failed'
                sys.exit(1)
        # NOT equal
        if ((obj == 'direction')):
            if getattr(m1,obj) == getattr(m2,obj):
                print obj,'failed'
                sys.exit(1)

        # add
        if ((obj == 'steps') or (obj == 'total_frames')):
            value = getattr(m1,obj) + getattr(m2,obj)

        # continue array
        if ((obj == 'ext_raw') or (obj == 'end_to_end')):
            m2arr = getattr(m2,obj) + getattr(m1,obj)[-1]
            value = np.concatenate((getattr(m1,obj),m2arr))

        # analysis --> i t f.
        if (obj == 'analysis'):
            # print m1.analysis
            # print m1.analysis.shape
            # print m2.analysis.shape
            # print m2.analysis

            # print m1.analysis[-1,0]
            # print m1.analysis[-1,1]
            # print m1.analysis[-1,2]

            arr0 = m2.analysis[::,0] + m1.analysis[-1,0] # ext/indentation.
            arr1 = m2.analysis[::,1] + m1.analysis[-1,1] # time
            arr2 = m2.analysis[::,2] + m1.analysis[-1,2] # frame
            arr = np.transpose(np.vstack((arr0,arr1,arr2)))

            setattr(cmt,'reversal_ind',m1.analysis[-1,0])
            setattr(cmt,'reversal_time',m1.analysis[-1,0])
            setattr(cmt,'reversal_frame',m1.analysis[-1,2])


            # print arr[-1,::]
            # arr[-1,::] = m1.analysis[-1,::]
            # print arr[-1,::]
            # print arr.shape
            # print arr
            # print m2.analysis
            # sys.exit()
            # value = np.concatenate((getattr(m1,obj),getattr(m1,obj)[-1,::],arr[1:,::]))
            value = np.concatenate((getattr(m1,obj),arr))

        # concatenate
        # if ((obj == 'f_nano') or (obj == 'f_pico') or (obj == 'force') or
        if ((obj == 'f_nano') or (obj == 'f_pico') or
            (obj == 'curvature') or (obj == 'angles')):
            # print obj
            # print getattr(m1,obj).shape
            # print getattr(m2,obj).shape
            value = np.concatenate((getattr(m1,obj),getattr(m2,obj)))
            # print value.shape
            # print value[::100]

        # force gets special treatment. itf in the 1,2,3 are itf .. need
        # to be used as the full extension...
        if ((obj == 'force')):
            # print getattr(m1,'ext_raw')[::100]
            # print getattr(m1,'ext_raw')[-1]
            # print getattr(m2,'ext_raw')[::100]
            # print getattr(m2,'ext_raw')[-1]
            # print getattr(cmt,'ext_raw')[-1]
            # print getattr(m1,'force').shape
            # print getattr(m1,'force')[::10,1]
            # # [::10,]
            # print getattr(m2,'force').shape
            # print getattr(m2,'force')[::10,1]
            # nums = getattr(m1,obj).shape[0] + getattr(m2,obj).shape[0]
            value = np.concatenate((getattr(m1,obj),getattr(m2,obj)))
            nums = value.shape[0]
            forces = np.linspace(0,cmt.ext_raw[-1],nums)
            value[::,1] = forces
            # sys.exit()


        # if ((obj == 'contacts') or (obj == 'externalcontacts')):
        if ((obj == 'externalcontacts')):
            # print m2.contacts.shape
            arr = getattr(m2,obj)[2,::]
            # print arr
            m2.contacts[0,::] = arr
            value = np.concatenate((getattr(m1,obj),getattr(m2,obj)))
            # sys.exit()
            # value = np.concatt


        # ---SET---
        setattr(cmt,obj,value)


    # get contacts for forward/reverse.
    # cmt.externalcontacts
    # maxc = np.linspace(-1,-1,len(cmt.externalcontacts[1]))
    # # max over all frames  ---- no looping through frames.
    # for d in range(cmt.externalcontacts.shape[1]):
    #     # print d
    #     # print cmt.externalcontacts.shape
    #     maxc[d] = max(cmt.externalcontacts[::,d])


    # OVERWRITE
    # print len(m1.externalcontacts)
    # print len(m2.externalcontacts)
    # cmt.contacts = cmt.externalcontacts / maxc


    cmt.contacts = cmt.externalcontacts / cmt.externalcontacts[0,::]
    # print len(cmt.externalcontacts)

    # end for loop, return class.
    return cmt


#  ---------------------------------------------------------  #
#  Begin Plotting.                                            #
#  ---------------------------------------------------------  #
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
# gs = GridSpec(1,1)
gs = GridSpec(2,1)
ax1 = plt.subplot(gs[0,:])
ax = [ax1]

from cycler import cycler
# print matplotlib.rcParams['axes.prop_cycle']
mycolors = ['k', 'r', 'g', 'b','c','m','lime','darkorange','sandybrown','hotpink']
ax1.set_prop_cycle(cycler('color',mycolors))


def plot_forceindentation(mt):
    '''
    Class. use -fi (integer)
    '''
    # import matplotlib.patches as mpatches
    # c = mpatches.ArrowStyle("simple", head_length=.4, head_width=.4, tail_width=.4)
    # c = mpatches.ArrowStyle((0.5, 0.5), 0.25, facecolor="green",
    #                     edgecolor="red", linewidth=3)
    # ax1.gca().add_patch(c)
    # plt.legend([c], ["An ellipse, not a rectangle"])

    build_mt(mt)
    # mt.get_forceindentation()

    # ax1.set_prop_cycle(cycler('color',mycolors))
    # for n,i in enumerate(lst):
    #     print n,i

    x = mt.ext_raw[1:]
    y = mt.f_nano[1:]

    if args['force'] != None:
        if ((mt.direction == 'forward') and (mt.truncated == 'no')):
            ax1.plot(x,y,'k-',label='Full Indent')
        elif ((mt.direction == 'forward') and (mt.truncated == 'yes')):
            ax1.plot(x,y,'r-',label='Partial Indent')
        else:
            ax1.plot(x,y,'g-',label='Retracting')
        # break

        if mt.truncated == 'yes':
            ax1.axvline(mt.reversal_ind,color='r',linestyle='-',linewidth=1.5)

    else:
        ax1.plot(x,y,label=mt.name)


    ax1.set_xlim(-1,31)
    ax1.set_xticks([0,10,20,30])
    ax1.set_ylim(-.20,.905)
    ax1.set_yticks([0,.2,.4,.6,.8])
    ax1.set_ylim(-0.04,0.94)

    ax1.set_xlabel('Indentation Depth X/nm')
    ax1.set_ylabel('Indentation Force F/nN')

    # legend
    handles,labels = ax1.get_legend_handles_labels()
    ax1.legend(handles,labels,prop={'size':14},loc=2)

def plot_forceframe(mt):
    '''
    Class. use -fi (integer)
    '''
    # build_mt(mt)
    # mt.print_class()
    # return

    # x = mt.fnrame_array
    # x = mt.frames
    x = np.linspace(mt.frames[0],mt.frames[-1],len(mt.f_nano[1:]))
    y = mt.f_nano[1:]

    # print "FRAMES:::"
    # print x,len(x)
    # print len(mt.f_nano[1:])

    ax1.plot(x,y,label=mt.name)

    # ax1.set_xlim(-1,31)
    ax1.set_xlim(x[0],x[-1])
    # ax1.set_xticks([0,10,20,30])
    # ax1.set_ylim(-.20,.905)
    ax1.set_yticks([0,.2,.4,.6,.8])
    ax1.set_ylim(-0.04,0.94)
    # ax1.set_xlabel('Indentation Depth X/nm')
    # ax1.set_xlabel('Frame #')
    ax1.set_ylabel('Indentation Force F/nN')

    # legend
    handles,labels = ax1.get_legend_handles_labels()
    ax1.legend(handles,labels,prop={'size':14},loc=2)

def plot_forceindentation_group(mt,**kwargs):
    '''
    Class. use -fi (integer)
    '''

    if kwargs is not None:
        for k,v in kwargs.iteritems():
            print k,v

    if 'linetype' in kwargs:
        linetype = kwargs['linetype']
    if 'label' in kwargs:
        label = kwargs['label']
    # return

    dct_font = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'18'}
    matplotlib.rc('font',**dct_font)

    # mt.get_forceindentation()

    x = mt.ext_raw[1:]
    y = mt.f_nano[1:]

    ax1.plot(x,y,linetype,label=label)

    ax1.set_xlim(-1,31)
    ax1.set_xticks([0,10,20,30])
    ax1.set_ylim(-.20,.905)
    ax1.set_yticks([0,.2,.4,.6,.8])
    ax1.set_ylim(-0.04,0.94)

    ax1.set_xlabel('Indentation Depth X/nm')
    ax1.set_ylabel('Indentation Force F/nN')

    # legend
    handles,labels = ax1.get_legend_handles_labels()
    ax1.legend(handles,labels,prop={'size':14},loc=2)

# def plot_both(mt,dimers=mt.dimers,shift=0):

#     # fig.set_size_inches(8.5,5.5)
#     plt.subplots_adjust(left=0.14,right=0.81,top=0.960,bottom=0.18)

#     ax1

#     ax1.set_prop_cycle(cycler('color',mycolors))

#     dct_font = {'family':'sans-serif',
#                 'weight':'normal',
#                 'size'  :'20'}
#     matplotlib.rc('font',**dct_font)


#     plot_forceindentation(mt)

#     ax2.set_prop_cycle(cycler('color',mycolors))

#     x1 = mt.frames[1::]
#     x1 = x1 + shift
#     y1 = mt.contacts[1::,::]

#     print dimers
#     for d in dimers:
#         ax2.plot(x1,y1[::,d],label=str(d*2))

#     ax2.set_xlabel("Frame #")
#     ax2.set_ylabel("Qn")

#     ax2.set_xlim(x1[0],1320)
#     ax2.set_xticks([0,200,400,600,800,1000,1200])
#     ax2.set_ylim(0.36,1.02)
#     ax2.set_yticks([0.40,0.55,0.70,0.85,1.00])

#     # legend
#     # 1:
#     handles, labels = ax2.get_legend_handles_labels()
#     ax2.legend(bbox_to_anchor=(1.02, 1),loc=2,borderaxespad=0.0,fontsize=18)

#     if hasattr(mt,'reversal_frame'):
#         print 'reversal_frame:',mt.reversal_frame
#         ax2.axvline(mt.reversal_frame,color='r',linestyle='-',linewidth=1.5)

def plot_emol(mt):
    '''
    Provide n the index in mt_list for plotting.
    Provide dimers, a list from "get_dimers."
    '''
    # print emolfile
    build_mt(mt)
    mt.get_dimers()
    mt.get_emol_mtcontacts(num_dimers)


    def new_fig():
        fig = plt.figure(0)
        gs = GridSpec(3,5,wspace=0.0,hspace=0.0)

        ax1 = plt.subplot(gs[0,0])
        ax2 = plt.subplot(gs[0,1])
        ax3 = plt.subplot(gs[0,2])
        ax4 = plt.subplot(gs[0,3])
        ax5 = plt.subplot(gs[0,4])

        ax6 = plt.subplot(gs[1,0])
        ax7 = plt.subplot(gs[1,1])
        ax8 = plt.subplot(gs[1,2])
        ax9 = plt.subplot(gs[1,3])
        ax10 = plt.subplot(gs[1,4])

        ax11 = plt.subplot(gs[2,0])
        ax12 = plt.subplot(gs[2,1])
        ax13 = plt.subplot(gs[2,2])
        ax14 = plt.subplot(gs[2,3])
        ax15 = plt.subplot(gs[2,4])

        # ax = [ax2,ax4,ax6,ax7,ax8,ax9,ax10,
        #       ax12,ax14]
        ax = [ax7,ax9,ax8,ax6,ax12,ax2,ax10,
              ax14,ax4]

        ax1.axis('off')
        ax3.axis('off')
        ax5.axis('off')
        ax11.axis('off')
        ax13.axis('off')
        ax15.axis('off')



        for axes in ax:
            axes.tick_params(labelsize=8.0)
            axes.set_xticks([])
            axes.set_yticks([])
            # axes.set_xlim([0,1.2])
            axes.set_ylim([0,1.2])

        return ax



    #  ---------------------------------------------------------  #
    #  Import Data! (2/4)                                         #
    #  ---------------------------------------------------------  #
    result_type = 'emolcontacts' # sop | sopnucleo | gsop | namd
    plot_type = 'bysubdomain' # fe | tension | rmsd | rdf

    # mpl_myargs_begin

    #  ---------------------------------------------------------  #
    #  Import Data! (3/4)                                         #
    #  ---------------------------------------------------------  #

    ##            NN  NM   NC  MN  MM  MC     CN           CM           CC
    subcolors = ['r', 'g', 'b','c','m','lime','darkorange','sandybrown','hotpink']


    for d in mt.dimers:

        ax = new_fig()

        print d
        print mt.emol[::,d,0,::] # 0 is the
        f0 = mt.emol[0,d,0,::]
        print 'f0:',f0
        print 'subd:'
        subd_name = ['alpha','beta','intra-dimer',
                     'a-south','a-east','a-west',
                     'b-north','b-east','b-west']

        mesk = ma.masked_less(mt.emol,1.0)
        # mesk1 = np.log(mesk)

        # n = 0
        for n in range(0,9):


            # x = mesk[::,d,n,0]/mesk[0,d,n,0]
            print 'mt.emol:'
            print mt.emol[0,d,n,::]

            x = mt.emol[::,d,n,0]/mt.emol[0,d,n,0]
            # print x,x.shape
            ax[n].plot(x,'k-',linewidth=1.0)

            ax[n].set_prop_cycle(cycler('color',subcolors))

            for nn in range(1,10):
                xn = mt.emol[::,d,n,nn] / mt.emol[0,d,n,0]
                # print xn
                ax[n].plot(xn,color=subcolors[nn-1],linewidth=0.5,linestyle='-')


        data_name = mt.dirname.split('/')[-1]
        save_fig(my_dir,0,'fig','%s_%s_%s_%dmer' % (result_type,plot_type,
                                                 data_name,d),option)
        plt.clf()


        # break
        # for f in range(mt.emol.shape[0]):
        #     for n in range(0,9):
        # continue

        # for f in range(mt.emol.shape[0]):
        #     for n in range(0,9):
        #         for nn in range(0,10):

        #             pass
        #             # print mesk[f,d,n,::]
        # break


        # print mesk
        # mt.emol = np.log(mt.emol)

        # for f in range(mt.emol.shape[0]):
        #     for n in range(0,9):

        #         print mt.emol[f,d,n,::]
        #         # mt.emol[f,d,n,::] = mt.emol[f,d,n,::] / mt.emol[0,d,n,::]
        #         # print mt.emol[f,d,n,::]

        #         for nn in range(0,10):
        #             print mt.emol[f,d,n,nn]
        #             # tot_size = mt.emol[f,d,n,0]
        #             # sizes = mt.emol[f,d,n,nn]
        #             # plt.plot
        #             # print np.log(mt.emol)



        #         #     if mt.emol[0,d,n,nn] == 0:
        #         #         print 'zeroes.'
        #         #     else:
        #         #         mt.emol[f,d,n,nn] = mt.emol[f,d,n,nn] / mt.emol[0,d,n,nn]

        # f = 0
        # n = 0
        # nn = 0
        # print '-----------'

        # for f in range(mt.emol.shape[0]):
        #     for n in range(0,9):
        #         for nn in range(0,10):
        #             # print mt.emol[f,d,n,nn]
        #             print mt.emol[f,d,n,::]


        # print '-----------'
        #     # for n in range(0,9):
        #     #     print mt.emol[f,d,0,::]


        # break



        # for f in range(mt.emol.shape[0]):
        #     print f
        #     for sdiv in range(0,9):
        #         print "%s:" % subd_name[sdiv]
        #         print mt.emol[f,d,sdiv,::]


        # for sdiv in range(0,9):
        #     print "%s:" % subd_name[sdiv]


        #     continue

        #     for nmc in range(0,9):
        #         print "%d:" % nmc
        #         print mt.emol[::,d,sdiv,nmc]


        # break


    # for d in mt.dimers():
    #     print d
        # print mt.emol[::,d,0,::]

    # plt.plot(mt.emol[::,])



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
    # from plot.SETTINGS import *
    # data_name = mt.dirname.split('/')[-1]
    # save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,data_name),option)
    # mpl_myargs_end


def plot_emol_3n(mt):
    '''
    Provide n the index in mt_list for plotting.
    Provide dimers, a list from "get_dimers."
    Use with -e 2 (flag)
    '''
    # print emolfile
    build_mt(mt)
    # mt.get_dimers()
    mt.get_emol_mtcontacts_3n(num_dimers)
    mt.get_emol_mtcontacts_3(num_dimers)

    def new_fig():
        fig = plt.figure(0)
        gs = GridSpec(1,1)
        ax1 = plt.subplot(gs[0,:])
        ax = [ax1]
        return ax

    def fig8():
        fig = plt.figure(0)
        fig.set_size_inches(14,5)
        plt.subplots_adjust(left=0.10,right=0.95,top=0.96,bottom=0.18,hspace=0.1,wspace=0.4)

        gs = GridSpec(3,6)
        ax1 = plt.subplot(gs[0:3,0:2])
        ax2 = plt.subplot(gs[0,2])
        ax3 = plt.subplot(gs[1,2])
        ax4 = plt.subplot(gs[2,2])

        ax5 = plt.subplot(gs[0:3,4:6])
        ax6 = plt.subplot(gs[0,3])
        ax7 = plt.subplot(gs[1,3])
        ax8 = plt.subplot(gs[2,3])

        ax = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]


        # ax1.set_xticklabels([30,60,90,120,150],size=12)

        ax1.tick_params(labelsize=12)
        ax5.tick_params(labelsize=12)
        # ax5.set_yticks([20,])

        for axe in [ax1,ax5]:
            axe.set_xticks([20,50,80,110,140])
            axe.set_yticks([20,120,220,320,420])
            # ax1.set_xticklabels([30,60,90,120,150],size=12)
            # ax1.set_xticklabels([30,60,90,120,150],size=12)
            # axe.set_xticklabels([],size=12)
            # axe.set_yticklabels([],size=12)
            # axe.set_yticks(fontsize=12)
            pass

        for axe in [ax2,ax3,ax4,ax6,ax7,ax8]:
            # axe.axis('off')
            axe.set_yticks([])
            axe.set_xticks([])
            axe.set_xticklabels((),size=12)
            axe.set_yticklabels((),size=12)
            pass

        return ax

    def fig7():
        # fig.clf()
        plt.clf()
        fig = plt.figure(0)
        fig.set_size_inches(14,6)
        plt.subplots_adjust(left=0.14,right=0.93,top=0.950,bottom=0.15,wspace=1.0,hspace=0.8)

        # print matplotlib.rcParams.keys()
        # matplotlib.rcParams['legend.fontsize'] = 16
        # matplotlib.rcParams[''] =
        # handles,labels = ax.get_legend_handles_labels()
        # ax.legend(bbox_to_anchor=(1.4,1.0))
        # ax.legend(handles,labels,prop={'size':8})
        # fig.set_size_inches(8.5,5.1)
        # plt.subplots_adjust(left=0.160,right=0.960,top=0.950,bottom=0.20)
        # font_prop_large = matplotlib.font_manager.FontProperties(size='large')

        # for k in matplotlib.rcParams.keys():
        #     print k
        dct_font = {'family':'sans-serif',
                    'weight':'normal',
                    'size'  :'24'}
        matplotlib.rc('font',**dct_font)

        gs = GridSpec(12,9)
        ax1 = plt.subplot(gs[1:11,0:5])

        # SEW
        ax2 = plt.subplot(gs[9:12,6:8])
        ax3 = plt.subplot(gs[6:9,7:9])
        ax4 = plt.subplot(gs[6:9,5:7])
        # NEW
        ax5 = plt.subplot(gs[0:3,6:8])
        ax6 = plt.subplot(gs[3:6,7:9])
        ax7 = plt.subplot(gs[3:6,5:7])

        ax = [ax1,ax2,ax3,ax4,ax5,ax6,ax7]
        # ax = [ax1]

        for axe in [ax2,ax3,ax4,ax5,ax6,ax7]:
            # axe.axis('off')
            axe.set_yticks([])
            axe.set_xticks([])
            axe.set_xticklabels(())
            axe.set_yticklabels(())

        yticks = [0,100,200,300]
        ax1.set_yticks(yticks)
        # ax1.set_yticklabels(yticks,fontsize=18)
        # ax1.set_y
        # for axe in ax:
        #     # axe.set_ylim(0,340)
        #     axe.set_linewidth(1.0)

        return ax


    #  ---------------------------------------------------------  #
    #  Import Data! (2/4)                                         #
    #  ---------------------------------------------------------  #
    result_type = 'emolcontacts_3n' # sop | sopnucleo | gsop | namd
    plot_type = 'bysubdomain' # fe | tension | rmsd | rdf

    #  ---------------------------------------------------------  #
    #  Import Data! (3/4)                                         #
    #  ---------------------------------------------------------  #
    ##            NN  NM   NC  MN  MM  MC     CN           CM           CC
    # subcolors = ['r', 'g', 'b','c','m','lime','darkorange','sandybrown','hotpink']

    ax = new_fig()
    print mt.emol3n.shape

    # for f in range(mt.emol3n.shape[0]):
    #     for d in range(mt.emol3n.shape[1]):
    #         print mt.emol3n[f,d,::]
    # print mt.emol3n[0:5,0,::]

    # d_interest = []
    # for d in range(mt.emol3n.shape[1]):

    #     # 12,16,20,24,28,32
    #     # ext = np.sum(mt.emol3n[::,d,12:36:4],axis=0)

    #     # print mt.emol3n[::,d,12:36:4].shape
    #     # print np.sum(mt.emol3n[::,d,12:36:4],axis=1).shape
    #     # print np.sum(mt.emol3n[::,d,12:36:4],axis=1)
    #     d_interest.append((d,np.var(np.sum(mt.emol3n[::,d,12:36:4],axis=1))))

    #     # ext = np.sum(mt.emol3n[::,d,12:36:4],axis=1)
    #     # print ext
    #     # ext = mt.emol3n[::,d,12] + mt.emol3n[::,d,16] + \
    #     #       mt.emol3n[::,d,20] + mt.emol3n[::,d,24] + \
    #     #       mt.emol3n[::,d,28] + mt.emol3n[::,d,32]
    #     # print ext
    #     # break
    # d_interest.sort(key=lambda x: x[1])
    # print d_interest[-10:]


    # array:
    # contacts_ext = mt.emol3n[::,::,13:]
    # contacts_ext = np.delete(mt.emol3n,np.s_[::,::,:13],axis=2)

    # contacts_ext = np.delete(mt.emol3n,0,axis=2)
    contacts_ext = mt.emol3n[::,::,12:36:4]
    external = np.sum(contacts_ext,axis=2)
    external_max = np.array([max(external[::,x]) for x in range(external.shape[1])])
    externaln = np.divide(external,external_max)

    print "contacts_shape:\n",contacts_ext.shape
    print "external_shape:\n",external.shape # [f,dimers]
    print "external_max:\n",external_max
    print "externaln:\n",externaln
    print 'externaln.shape:',externaln.shape


    mt_var = []

    if 1:
        # contacts, not normalized.
        for d in range(external.shape[1]):
            # print d
            # print external[0:10,d]
            v = np.var(external[::,d])
            mt_var.append((d,v))
        # sys.exit()
    else:
        for f in range(externaln.shape[1]):
            # print externaln[f,::]
            v = np.var(externaln[f,::])
            mt_var.append((f,v))
            # pass

    mt_var.sort(key=lambda x: x[1],reverse=True)

    for v in mt_var[:26]:
        print v[0],'\t\t',v[1]
    # sys.exit()

    if 0:
        # Get All West:
        ax = fig8()
        cmap = plt.set_cmap('rainbow')
        vmin = 0
        vmax = 1

        if args['emol'] >= 6:
            # 6: south/north
            # 7: east
            # 8: west

            if args['emol'] == 8:
                # west
                arr_a = mt.emol3n[::,::,20:24]
                arr_b = mt.emol3n[::,::,32:36]

            if args['emol'] == 7:
                # east
                arr_a = mt.emol3n[::,::,16:20]
                arr_b = mt.emol3n[::,::,28:32]

            if args['emol'] == 6:
                # south/north
                arr_a = mt.emol3n[::,::,12:16]
                arr_b = mt.emol3n[::,::,24:28]

            ax[0].imshow(arr_a[::,::,0],aspect='auto',clim=(vmin,vmax))
            ax[1].imshow(arr_a[::,::,1],aspect='auto',clim=(vmin,vmax))
            ax[2].imshow(arr_a[::,::,2],aspect='auto',clim=(vmin,vmax))
            ax[3].imshow(arr_a[::,::,3],aspect='auto',clim=(vmin,vmax))

            ax[4].imshow(arr_b[::,::,0],aspect='auto',clim=(vmin,vmax))
            ax[5].imshow(arr_b[::,::,1],aspect='auto',clim=(vmin,vmax))
            ax[6].imshow(arr_b[::,::,2],aspect='auto',clim=(vmin,vmax))
            ax[7].imshow(arr_b[::,::,3],aspect='auto',clim=(vmin,vmax))


    if args['emol'] == 4:
        # Get ..
        # subcolors = ['r', 'g', 'b','c','m','lime','darkorange','sandybrown','hotpink',]
        subcolors = ['k','r','g','b','c','m','lime','darkorange','sandybrown','hotpink']

        # ax = fig7()
        # plt.clf()
        def plot_7(iv):
            '''
            iv:
            '''
            print 'iv:',iv
            print 'iv[0]:',iv[0],' (dimer)'
            print '\t tuple of dimer-id,variance.'

            ax = fig7()
            ax[0].set_prop_cycle(cycler('color',subcolors))

            for v in mt_var[:10]:
                if v == iv:
                    ax[0].plot(external[::,v[0]],linewidth=3.5,label=str(iv[0]))
                else:
                    ax[0].plot(external[::,v[0]],linewidth=0.9)

            # print v[0]
            # contacts_extsub = mt.emol3n[::,v[0],12:36]

            ax1xticks = ax[0].get_xticks()[1::2]
            ax1xticks = [int(x) for x in ax1xticks]

            for i in range(1,7):
                # get columns: l-first position.
                #              h-final position.
                l = (i-1)*4 + 12
                h = i*4 + 12
                print 'bounds: ',i,l,h-1

                # if i != 1:
                #     continue

                # Description:
                # REMEMBER: this h-1
                # 0: main
                #      4    4:24-27
                # NEW 6 5   5:28-31, 6:32-35
                # SEW 3 2   2:16-19, 3:20-23
                #      1    1:12-15
                #
                csub = mt.emol3[::,iv[0],l:h]
                x = np.arange(0,csub.shape[0])
                # print x
                # print csub.shape
                yt = csub[::,0]
                y1 = csub[::,1]
                y2 = csub[::,1] + csub[::,2]
                # y3 = csub[::,1] + csub[::,2] + csub[::,3]

                print 'DIMER:',iv[0]
                # print yt
                # print y1
                # print y2
                # print y3
                # print 'y123-t:'
                # print y1[0:5],'red'
                # print y2[0:5],'red + green'
                # print y3[0:5],'red + green + blue'
                print yt[0:5],'total'

                # ax[i].fill_between(x,0,y1,where=y1>0,facecolor='r',alpha=0.3,interpolate=True)
                # ax[i].fill_between(x,y1,y2,where=y2>y1,facecolor='g',alpha=0.3,interpolate=True)
                # ax[i].fill_between(x,y2,y3,where=y3>y2,facecolor='b',alpha=0.3,interpolate=True)
                # ax[i].fill_between(x,0,y1,where=y1>0,color='k',facecolor='r',alpha=0.6)
                # ax[i].fill_between(x,y1,y2,where=y2>y1,color='k',facecolor='g',alpha=0.6)
                # ax[i].fill_between(x,y2,y3,where=y3>y2,color='k',facecolor='b',alpha=0.6)
                # ax[i].fill_between(x,0,y1,where=y1>0,color='k',linewidth=0.4,facecolor='r',alpha=0.6)
                ax[i].fill_between(x,0,y1,where=y1>0,color='k',linewidth=0.4,facecolor='r',alpha=0.6)
                ax[i].fill_between(x,y1,y2,where=y2>y1,color='k',linewidth=0.4,facecolor='g',alpha=0.6)
                # ax[i].fill_between(x,y2,y3,where=y3>y2,color='k',linewidth=0.4,facecolor='b',alpha=0.6)
                ax[i].fill_between(x,y2,yt,where=yt>y2,color='k',linewidth=0.4,facecolor='b',alpha=0.6)



                # print 'x[-1]:',x[-1]
                # print 'max-y3:',max(y3)
                ax[i].set_xlim(0,x[-1])
                if max(yt) > 50:

                    if max(yt) < 100:
                        ax[i].set_ylim(0,110)
                    else:
                        ax[i].set_ylim(0,max(yt)+10)

                    ax[i].set_yticks([100])
                    ax[i].set_yticklabels([100],fontsize=14)

                else:
                    ax[i].set_ylim(0,60)
                    ax[i].set_yticks([50])
                    ax[i].set_yticklabels([50],fontsize=14)


                if i == 1:
                    ax[i].set_xticks(ax1xticks)
                    ax[i].set_xticklabels(ax1xticks,fontsize=14)
                    ax[i].set_xlabel('Frame #')
                else:
                    ax1xticks = ax[0].get_xticks()[1::2]
                    ax[i].set_xticks(ax1xticks)
                    ax[i].set_xticklabels([],fontsize=14)


            # legend
            # 1:
            # print dim
            handles,labels = ax[0].get_legend_handles_labels()
            ax[0].legend(handles,labels,prop={'size':20},
                         # markerscale=5.0,
                         borderaxespad=0.6,
                         handlelength=3.0,
                         handleheight=2.0)
            # ax[0].set_xticklabels(fontsize=16)
            # ax[0].set_yticklabels(fontsize=16)
            ax[0].set_xlabel('Frame #')
            ax[0].set_ylabel('Contacts')


            data_name = mt.dirname.split('/')[-1]
            save_fig(my_dir,0,'fig/emol3n','%s_%s_%s_%ddimer' % (result_type,plot_type,
                                                          data_name,iv[0]),option)
            # plt.clf()


        for dim,iv in enumerate(mt_var[:10]):
            plot_7(iv)
            # break
        plot_7(mt_var[0])
        # sys.exit()

    # if args['emol'] != 4:
    else:
        data_name = mt.dirname.split('/')[-1]
        save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,
                                              data_name),option)
        plt.clf()


def plot_contacts(mt,dimers=mt.dimers,shift=0,limit=None):
    '''
    Provide n the index in mt_list for plotting.
    Provide dimers, a list from "get_dimers."
    limit = 1320
    '''
    build_mt(mt)
    # fig.set_size_inches(8.5,5.5)
    # plt.subplots_adjust(left=0.14,right=0.81,top=0.960,bottom=0.18,hspace=0.3)

    ax2.set_prop_cycle(cycler('color',mycolors))

    dct_font = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'18'}
    matplotlib.rc('font',**dct_font)

    # ax2 = ax2.twiny()
    # ax3 = ax2.twiny()
    # ax = [ax2,ax2]
    ax = [ax2]

    # print 'shape:'
    # shape:
    # (348,)
    # (348, 104)
    # print mt.frames.shape
    # print mt.contacts.shape
    # sys.exit()

    x1 = mt.frames[1::]
    x1 = x1 + shift
    y1 = mt.contacts[1::,::]

    # print x1[::75]
    # print y1[::75]
    # sys.exit()
    # y1 = np.linspace(0,0,len(x1))

    # x2 = mt.analysis[1::,2]
    # y2 = np.linspace(0,0,len(x2))

    # line1 = ax1.plot(x1,y1,visible=False)
    # line2 = ax2.plot(x2,y2,visible=False)

    print dimers
    for d in dimers:
        # print d
        # ax2.plot(mt.frames[1::],mt.contacts[1::,d])
        ax2.plot(x1,y1[::,d],label=str(d*2))

    # ax1.set_xlim(x1[0],x1[-1])
    # ax2.set_xlim(x2[0],x2[-1])

    # fig.text(0.02,0.125,'Time (ms)',color='b',size=16)
    # ax2.spines['bottom'].set_color('b')
    # ax2.spines['bottom'].set_position(('outward',65.0))
    # ax2.spines['bottom'].set_bounds(x2[0],x2[-1])
    # ax2.xaxis.set_ticks_position('bottom')
    # for tick in ax2.xaxis.get_major_ticks():
    #     tick.label.set_fontsize(14)

    # fig.text(0.02,0.050,'Frame #',color='m',size=16)
    # ax2.spines['bottom'].set_color('m')
    # ax2.spines['bottom'].set_position(('outward',70.0))
    # ax2.spines['bottom'].set_bounds(x2[0],x2[-1])
    # ax2.xaxis.set_ticks_position('bottom')
    # for tick in ax2.xaxis.get_major_ticks():
    #     tick.label.set_fontsize(14)




    # print type(mt.reversal_ind)
    # print mt.reversal_ind
    # print mt.reversal_time
    # print mt.reversal_frame



    # if hasattr(mt,'reversal_time'):
    #     print 'reversal_time:',mt.reversal_time
    #     ax1.axvline(mt.reversal_time,color='m',linestyle='-',linewidth=1.5)


    # if hasattr(mt,'reversal_time'):
    #     ax1.axvline(mt.reversal_time,color='r',linestyle='-',linewidth=1.5)
    # sys.exit()

    ax2.set_xlabel("Frame #")
    # ax1.set_ylabel("Contacts")
    ax2.set_ylabel("Qn")

    # ax2.set_xlim(x1[0],x1[-1])
    # if limit:
        # ax2.set_xlim(x1[0],limit)
    if limit != None:
        ax2.set_xlim(x1[0],1320)
        ax2.set_xticks([0,200,400,600,800,1000,1200])
    else:
        ax2.set_xlim(x1[0],limit)
        # ax2.set_xlim(x1[0],limit)

    # ax2.set_ylim(90,410)
    ax2.set_ylim(0.36,1.02)
    ax2.set_yticks([0.40,0.55,0.70,0.85,1.00])
    # ax2.set_yticks([0.35,0.50,0.65,0.80,0.95])
    # ax2.set_yticks([100,200,300,400])

    # legend
    # 1:
    handles, labels = ax2.get_legend_handles_labels()
    # ax2.legend(loc='upper right',bbox_to_anchor=(1,1))

    # ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
    #        ncol=2, mode="expand", borderaxespad=0.)

    ax2.legend(bbox_to_anchor=(1.02, 1),loc=2,borderaxespad=0.0,fontsize=12)

    if hasattr(mt,'reversal_frame'):
        print 'reversal_frame:',mt.reversal_frame
        ax2.axvline(mt.reversal_frame,color='r',linestyle='-',linewidth=1.5)


    # ax2.legend(handles, labels,prop={'size':10},loc=3)

    # leg = plt.gca().get_legend()
    # for label in leg.get_lines():
    #     label.set_linewidth(2.5)

    # some lines in legend!
    # print len(ax2.lines),ax1.lines
    # lst_labels = ['0.3','0.4','0.5','0.6','0.7']
    # for i,line in enumerate(ax1.lines[2:7]):
    #     print lst_labels[i]
    #     line.set_label(lst_labels[i])
    # ax1.legend()


def plot_nesw_contacts(mt,obj,dimers=mt.dimers,shift=0):
    '''
    Provide n the index in mt_list for plotting.
    Provide dimers, a list from "get_dimers."
    '''
    build_mt(mt)


    dct_font = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'20'}
    matplotlib.rc('font',**dct_font)

    # fig.set_size_inches(8.5,5.5)
    # plt.subplots_adjust(left=0.14,right=0.81,top=0.960,bottom=0.18,wspace=0.0,hspace=0.0)
    plt.subplots_adjust(left=0.14,right=0.97,top=0.970,bottom=0.18)

    ax1 = plt.subplot(gs[0,0]) # col1
    ax2 = plt.subplot(gs[1,0]) # W
    ax3 = plt.subplot(gs[2,0])

    ax4 = plt.subplot(gs[0,1]) # col2, N
    ax5 = plt.subplot(gs[1,1])
    ax6 = plt.subplot(gs[2,1]) # S

    ax7 = plt.subplot(gs[0,2]) # col3
    ax8 = plt.subplot(gs[1,2]) # E
    ax9 = plt.subplot(gs[2,2])

    ax = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9]

    for axe in [ax1,ax3,ax5,ax7,ax9]:
        axe.axis('off')
        axe.set_prop_cycle(cycler('color',mycolors))

    # ax2 = ax1.twiny()
    # ax3 = ax1.twiny()
    # ax = [ax1,ax2]
    ax = [ax1]

    x1 = mt.frames[1::]
    x1 = x1 + shift

    obj = obj[0]
    dir_obj = '%scontacts' % obj
    y1 = getattr(mt,dir_obj)[1::,::]

    print dimers
    for d in dimers:
        # print d
        # ax1.plot(mt.frames[1::],mt.contacts[1::,d])

        # npm = np.var(y1[::,d])
        npm = min(y1[10:-10,d])
        # print npm
        criterion = 1.0

        if obj == 'n':
            if npm > criterion:
                # ax4.plot(x1,y1[::,d],label=str(d*2),visible='false')
                ax4.plot(x1,y1[::,d],label=str(d*2),alpha=0.1)
            else:
                ax4.plot(x1,y1[::,d],label=str(d*2))
        elif obj == 'e':
            if npm > criterion:
                ax8.plot(x1,y1[::,d],label=str(d*2),alpha=0.1)
            else:
                ax8.plot(x1,y1[::,d],label=str(d*2))
            # ax8.plot(x1,y1[::,d],label=str(d*2))
        elif obj == 's':
            if npm > criterion:
                # ax6.plot(x1,y1[::,d],label=str(d*2),visible='false')
                ax6.plot(x1,y1[::,d],label=str(d*2),alpha=0.1)
            else:
                ax6.plot(x1,y1[::,d],label=str(d*2))
            # ax6.plot(x1,y1[::,d],label=str(d*2))
        elif obj == 'w':
            if npm > criterion:
                # ax2.plot(x1,y1[::,d],label=str(d*2),visible='false')
                ax2.plot(x1,y1[::,d],label=str(d*2),alpha=0.1)
            else:
                ax2.plot(x1,y1[::,d],label=str(d*2))
            # ax2.plot(x1,y1[::,d],label=str(d*2))



    ax6.set_xlabel("Frame #")
    ax2.set_ylabel("Qn")

    for axe in [ax2,ax4,ax6,ax8]:

        axe.set_xlim(x1[0],1320)
        axe.set_xticks([0,200,400,600,800,1000,1200])

        axe.set_ylim(-0.1,1.1)
        axe.set_yticks([0.40,0.55,0.70,0.85,1.00])

        # axe.tick_params(labelsize=12)
        plt.setp(axe.get_xticklabels(),rotation=45,fontsize=10)
        plt.setp(axe.get_yticklabels(),fontsize=10)

        # handles, labels = ax1.get_legend_handles_labels()
        # axe.legend(bbox_to_anchor=(1.02, 1),loc=2,borderaxespad=0.0,fontsize=18)

        if hasattr(mt,'reversal_frame'):
            print 'reversal_frame:',mt.reversal_frame
            axe.axvline(mt.reversal_frame,color='r',linestyle='-',linewidth=1.5)




    # legend
    # 1:


def plot_angles(n,dimers):
    '''
    Plot the angles (of the dimers that lost the most contacts.)
    '''
    build_mt(n)

    ax1.set_prop_cycle(cycler('color',mycolors))

    xstep = int(float(len(mt_list[n].ext_raw)) / len(mt_list[n].externalcontacts))
    x = mt_list[n].ext_raw[::xstep]
    x = x[:len(mt_list[n].externalcontacts)]
    y = mt_list[n].angles
    print len(y),len(x)

    for d in dimers:
        ax1.plot(x,y[::,d[0],2])

    ax1.set_xlim(-1,41)
    ax1.set_xticks([0,10,20,30,40])
    ax1.set_ylim(165,183)
    ax1.set_yticks([168,172,176,180])


    result_type = 'angles' # sop | sopnucleo | gsop | namd
    plot_type = mt_list[n].name # fe | tension | rmsd | rdf
    data_name = 'one'

    save_fig(my_dir,0,'fig/anglesE','%s_%s_%s' % (result_type,plot_type,data_name),None)
    plt.cla()
    plt.clf()




def plot_multiplot2(mt,dimers=mt.dimers):
    '''
    ...
    '''
    plot_forceindentation(mt)




def plot_multiplot(mt,dimers=mt.dimers):
    '''
    Multiplot..
    '''
    fig = plt.figure(0)

    fig.set_size_inches(7.0,8.5)
    # matplotlib.rcParams[''] =
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


    fig = plt.figure(0)
    gs = GridSpec(2,1)
    ax1 = plt.subplot(gs[0,:])
    ax2 = plt.subplot(gs[1,:],sharex=ax1)

    ax3 = ax1.twiny()
    ax4 = ax1.twiny()
    ax = [ax1,ax2,ax3,ax4]

    for axe in ax:
        axe.set_prop_cycle(cycler('color',mycolors))

    x1 = mt.force[::,1]
    x3 = mt.force[::,2]
    x4 = mt.force[::,3]
    y1 = mt.force[::,0]

    print 'x1:',x1
    print 'y1:',y1
    ax1.plot(x1,y1)

    # x is the monomer/dimer.
    # y == contacts,angles,curvature
    x2 = mt.analysis[::,0]
    # x2 =

    # print mt.externalcontacts.shape

    for d in dimers:
        # ax2.plot(x2,mt.externalcontacts[::,d])
        ax2.plot(x2,mt.contacts[::,d])
        # ax2.plot(x1,mt.contacts[::,d])

    # ax1.set_xlim(0,1.0)
    # ax1.set_xticks([0.3,0.5,0.7,0.9])
    ax1.set_ylabel('Force (nN)')
    ax1.set_ylim(-0.01,1.0)
    ax1.set_yticks([0.1,0.3,0.5,0.7,0.9])
    ax1.set_xlim(x1[0],x1[-1])
    # make these tick labels invisible
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2.set_ylabel('Contacts #')
    ax2.set_xlabel('Indentation (nm)',fontsize=18)
    ax2.set_xlim(x2[0],x2[-1])
    # ax2.set_xticks([])
    # ax2.set_ylim(0,400)
    ax2.set_ylim(0.33,1.02)
    ax2.set_yticks([0.40,0.55,0.70,0.85,1.00])
    # ax2.set_yticks([100,200,300])

    line3 = ax3.plot(x3,y1,visible=False)
    ax3.set_xlim(x3[0],x3[-1])
    line4 = ax4.plot(x4,y1,visible=False)
    ax4.set_xlim(x4[0],x4[-1])

    # line3.visible('False')
    # delete(line3);
    # delete(line4);
    # set((line3,'Visible','off'));  # Make it invisible
    # set(line4,'Visible','off');  # Make it invisible


    fig.text(0.03,0.095,'Time (ms)',color='b',size=14)
    ax3.spines['bottom'].set_color('b')
    ax3.spines['bottom'].set_position(('outward',290.0))
    ax3.spines['bottom'].set_bounds(x3[0],x3[-1])
    ax3.xaxis.set_ticks_position('bottom')
    for tick in ax3.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)

    fig.text(0.03,0.045,'Frame #',color='m',size=14)
    ax4.spines['bottom'].set_color('m')
    ax4.spines['bottom'].set_position(('outward',322.0))
    ax4.spines['bottom'].set_bounds(x4[0],x4[-1])
    ax4.xaxis.set_ticks_position('bottom')
    for tick in ax4.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)


    plt.subplots_adjust(left=0.20,right=0.960,top=0.950,bottom=0.200,hspace=0.0)
    # result_type = 'multiaxis' # sop | sopnucleo | gsop | namd
    # plot_type = mt_list[i].name # fe | tension | rmsd | rdf
    # data_name = 'one'
    # save_fig(my_dir,0,'fig/multiaxis','%s_%s_%s' % (result_type,plot_type,data_name),None)




#  ---------------------------------------------------------  #
#  Run Here.                                                  #
#  ---------------------------------------------------------  #
if (args['emol']) == 1:
    x = FindAllFiles()
    set9 = x.remove_dirname('fail',None,dct_traj)
    set9 = x.remove_dirname('example',None,set9)
    set9 = x.query_dirname('round_17',None,set9)

    # mt_list = set9.keys()
    # print mt_list

    mt_list = build_1st_mt(set9)
    # print mt_list

    print 'num_dimers:',num_dimers
    for m in mt_list:
        plot_emol(m)

        break


if (args['emol']) >= 2:
    # emol_3n: 2,8,..
    x = FindAllFiles()
    set9 = x.remove_dirname('fail',None,dct_traj)
    set9 = x.remove_dirname('example',None,set9)
    # set9 = x.query_dirname('round_17',None,set9)
    set9 = x.query_dirname('round_16',None,set9)

    mt_list = build_1st_mt(set9)

    print 'num_dimers:',num_dimers

    # investigate dimer 79,80,
    # searching seamup_doz2_fix2_LHM_1_nop_00
    plot_emol_3n(mt_list[10])

    # for m in mt_list:
    #     print m.name
    #     pass
        # plot_emol_3n(m)
        # break
    sys.exit()


if ((args['forceframecontacts'])):
    # x = FindAllFiles()
    # set9 = x.remove_dirname('fail',None,dct_traj)
    # set9 = x.remove_dirname('example',None,set9)
    # # set9 = x.query_dirname('round_17',None,set9)
    # print len(dct_traj.keys())
    # print len(set9.keys())
    # for k,v in set9.iteritems():
    #     print k,v['dirname'].split('/')[-1]
    # # sys.exit()

    dct_plot = {}
    dct_stat = {}
    print 'cwd:',my_dir

    def get_one_dct(n):
        dct_crit = pickle.load(open('dct_1617.pkl','r'))
        return dct_crit[n]


    def get_crit_breaks(ffile):
        with open(ffile) as fp:
            for line in fp.readlines():
                if line.startswith('#'):
                    continue

                line_val = line.split()
                line_len = len(line_val)

                plotthis = line_val[0]
                print plotthis

                for i in range(len(mt_list)):
                    if mt_list[i].name == plotthis:
                        print i,mt_list[i].name
                        dct_plot[i] = {}
                        dct_plot[i]['name'] = plotthis
                        dct_plot[i]['data'] = mt_list[i]
                        dct_plot[i]['dirname'] = mt_list[i].dirname

                        # print len(line.split())
                        # sys.exit()

                        # line_val = line.split()

                        # by FRAME:
                        if line_len == 3:
                            dct_plot[i]['first'] = int(line_val[1])
                            dct_plot[i]['second'] = int(line_val[2])
                            dct_plot[i]['max'] = int(line_val[2])
                        elif line_len == 5:
                            dct_plot[i]['first'] = int(line_val[1])
                            dct_plot[i]['second'] = int(line_val[2])
                            dct_plot[i]['third'] = int(line_val[3])
                            if line_val[4] == '2':
                                dct_plot[i]['max'] = int(line_val[2])
                            elif line_val[4] == '3':
                                dct_plot[i]['max'] = int(line_val[3])
                        else:
                            pass

                        break

                print 'Max value obtained:',dct_plot[i]['max']


                        # for z in range(len(line.split())):
                        # try:
                        #     dct_plot[i]['first'] = int(line.split()[1])
                        # except:
                        #     pass
                        # try:
                        #     dct_plot[i]['second'] = int(line.split()[2])
                        # except:
                        #    pass
                        # try:
                        #     dct_plot[i]['third'] = int(line.split()[3])
                        # except:
                        #     pass


    # sys.exit()
    get_crit_breaks(os.path.join(my_dir,args['forceframecontacts']))
    print dct_plot.keys()
    # sys.exit()

    # get_crit_breaks(os.path.join(my_dir,'ff.file/ff.file.16'))
    # tup_use = ('round_16')
    # lst_cb = get_one_dct(tup_use)
    # # get_crit_breaks(os.path.join(my_dir,'ff.file/ff.file.17'))
    # # tup_use = ('round_17')
    # # lst_cb = get_one_dct(tup_use)


    # dct_cb = {}
    # for k in lst_cb:
    #     for i,v1 in dct_plot.iteritems():
    #         if v1['name'] == k:
    #             dct_cb[k] = {}
    #             try:
    #                 dct_cb[k]['first'] = v1['first']
    #             except:
    #                 pass
    #             try:
    #                 dct_cb[k]['second']= v1['second']
    #             except:
    #                pass
    #             try:
    #                 dct_cb[k]['third'] = v1['third']
    #             except:
    #                 pass
    # print "New_Dict:"
    # for k,v in dct_cb.iteritems():
    #     print k,v

    # # dct_crit = pickle.load(open('dct_1617.pkl','r'))
    # # dct_crit[tup_use] = {}
    # # dct_crit[tup_use] = dct_cb
    # pickle.dump(dct_cb,open(os.path.join(my_dir,'dct_16_wf.pkl'),'w+'))
    # for k,v in dct_cb.iteritems():
    #     print k,v
    # sys.exit()


    def compare_dct():
        # dct_1617.pkl
        # dct_1617.pkl.bak
        # dct_16_wf.pkl
        # dct_17_wf.pkl
        # ORIGINAL
        db = pickle.load(open(os.path.join(my_dir,'dct_1617.pkl'),'r'))

        # tup_use = ('round_16')
        # di = pickle.load(open(os.path.join(my_dir,'dct_16_wf.pkl'),'r'))

        tup_use = ('round_17')
        di = pickle.load(open(os.path.join(my_dir,'dct_17_wf.pkl'),'r'))

        print 'Comparing..'
        # print type(db[tup_use])

        for t in db[tup_use]:
            if t in di.keys():
                if len(di[t].keys()) == 3:
                    print t,di[t]['first'],di[t]['second'],di[t]['third']
                elif len(di[t].keys()) == 2:
                    print t,di[t]['first'],di[t]['second']
                else:
                    pass
            else:
                print t,"-----not here-----"


        # for k,v in db.iteritems():

        #     if k in di.iteritems():
        #         print k,v
        #     else:
        #         print 'not here: ',k

    # PICKLE
    # compare_dct()
    # sys.exit()


    for k,v in dct_plot.iteritems():
        print k,v
        # print dct_traj[k]

        result_type = 'gsop' # sop | sopnucleo | gsop | namd
        plot_type = 'ffc'
        data_name = v['name'] + "_%d" % k
        dct_stat[data_name] = {}

        # name = v['dirname'].split('/')[-1]
        def new_mt(v):
            name = v['name']
            mt = Microtubule(name)
            mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
            mt.my_dir = my_dir
            mt.setupdirs()
            mt.set_attributes(v)
            mt.find_psf(my_dir,psffile)
            mt.find_dcd()
            mt.get_frame_count()
            mt.get_analysis_file()
            mt.get_indentation_file()
            mt.get_pdbs()
            mt.get_direction_info() # forward or reverse:
            mt.get_plate_info() # with plate or without:
            mt.get_reversal_frame()
            mt.get_sop_file()
            mt.get_sop_info()
            mt_list.append(mt)
            # break
            mt.file = v['data'].file
            # mt.print_class()
            build_mt(mt)
            return mt

        mt = new_mt(v)

        fig = plt.figure(0)
        gs = GridSpec(2,1)
        ax1 = plt.subplot(gs[0,:])
        ax2 = plt.subplot(gs[1,:],sharex=ax1)
        ax = [ax1,ax2]
        fig.set_size_inches(7.0,8.0)
        plt.subplots_adjust(left=0.18,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

        try:
            mt.reversal_frame = v['third']
            mt.truncation_by_percent(v['third'])
            # dct_stat[data_name]['thirdvalue'] = mt.f_nano[-1]
            dct_stat[data_name]['thirdvalue'] = max(mt.f_nano)

            plot_forceframe(mt)
            plot_contacts(mt,mt.dimers)
            save_fig(my_dir,0,'fig/both_fi_contact_dim12f','%s_%s_%s_THIRD' % (result_type,plot_type,data_name),option)
            plt.clf()
        except:
            pass

        mt = new_mt(v)

        fig = plt.figure(0)
        gs = GridSpec(2,1)
        ax1 = plt.subplot(gs[0,:])
        ax2 = plt.subplot(gs[1,:],sharex=ax1)
        ax = [ax1,ax2]
        fig.set_size_inches(7.0,8.0)
        plt.subplots_adjust(left=0.18,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

        try:
            mt.reversal_frame = v['second']
            mt.truncation_by_percent(v['second'])
            # dct_stat[data_name]['secondvalue'] = mt.f_nano[-1]
            dct_stat[data_name]['secondvalue'] = max(mt.f_nano)

            plot_forceframe(mt)
            plot_contacts(mt,mt.dimers)
            save_fig(my_dir,0,'fig/both_fi_contact_dim12f','%s_%s_%s_SECOND' % (result_type,plot_type,data_name),option)
            plt.clf()
        except:
            pass

        mt = new_mt(v)

        fig = plt.figure(0)
        gs = GridSpec(2,1)
        ax1 = plt.subplot(gs[0,:])
        ax2 = plt.subplot(gs[1,:],sharex=ax1)
        ax = [ax1,ax2]
        fig.set_size_inches(7.0,8.0)
        plt.subplots_adjust(left=0.18,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

        try:
            mt.reversal_frame = v['first']
            mt.truncation_by_percent(v['first'])
            # dct_stat[data_name]['firstvalue'] = mt.f_nano[-1]
            dct_stat[data_name]['firstvalue'] = max(mt.f_nano)

            plot_forceframe(mt)
            plot_contacts(mt,mt.dimers)
            save_fig(my_dir,0,'fig/both_fi_contact_dim12f','%s_%s_%s_FIRST' % (result_type,plot_type,data_name),option)
            plt.clf()
        except:
            pass

        print v
        # sys.exit()
        if v['max'] == v['second']:
            dct_stat[data_name]['maxvalue'] = dct_stat[data_name]['secondvalue']
        elif v['max'] == v['third']:
            dct_stat[data_name]['maxvalue'] = dct_stat[data_name]['thirdvalue']

    # MAX VALUE:
    # maxval = 0.0
    # for k,v in dct_stat.iteritems():
    #     print k
    #     maxval = v['secondvalue']
    #     try:
    #         if (v['thirdvalue'] > maxval):
    #             maxval = v['thirdvalue']
    #             print 'Using third value!'
    #     except:
    #         pass
    #     dct_stat[k]['maxvalue'] = maxval

    print '---start of print---'
    for k,v in dct_stat.iteritems():
        print k,'\t',v['firstvalue'],'\t',v['maxvalue']
    print '---end of print---'

    def write_crit_file(dct,suffix='.out',value='firstvalue'):
        lst_stat = []
        for k,v in dct.iteritems():
            print k
            lst_stat.append((k,v[value]))
        for stat in lst_stat:
            print stat[0],stat[1]
        lst_stat.sort(key=lambda x: x[1])

        outfile = os.path.join(my_dir,args['forceframecontacts'] + suffix)
        print "Writing:",outfile

        with open(outfile,'w+') as fp:
            # for k,v in dct_sortedstat.iteritems():
            # print k,v
            for stat in lst_stat:
                print stat[0],stat[1]
                fp.write("%s   %7.5f\n" % (stat[0],stat[1]))

    # Write First, and Maxvalue:
    write_crit_file(dct_stat,'.first.out','firstvalue')
    write_crit_file(dct_stat,'.maxvalue.out','maxvalue')
    sys.exit()


    # mt_list = [mt_list[m] for m in plot_list]
    # print mt_list[0].name

    # for i in range(len(mt_list)):
    #     print i,mt_list[i].name
    # if ((args['integers'])) != None:
    #     mt_list = [mt_list[m] for m in args['integers']]


    # print "about_to_build:"
    # for i in range(len(mt_list)):
    #     print i,mt_list[i].name

    # print "now_building:"
    # for i in range(len(mt_list)):
    #     print i,mt_list[i].name
    #     build_mt(mt_list[i])

    # forceframecontacts
    # sys.exit()



if ((args['integers'])):
    # plot_forceindentation(mt_list[0])
    # plot_forceindentation(mt_list[1])

    # print args['force'],type(args['force'])
    # sys.exit()
    if args['force'] == 0:

        fig = plt.figure(0)
        gs = GridSpec(1,1)
        ax1 = plt.subplot(gs[0,:])
        ax = [ax1]
        fig.set_size_inches(7.0,4.0)
        # plt.subplots_adjust(left=0.18,right=0.78,top=0.960,bottom=0.10,hspace=0.4)
        # plt.subplots_adjust(left=0.20,right=0.960,top=0.950,bottom=0.200,hspace=0.0)


        for n in args['integers']:
            print n,type(n)
            build_mt(mt_list[n])

            if n in [54,55,56]: # pushmid, seamdown, fixedends
                plot_forceindentation_group(mt_list[n],linetype='k-',label=str(n))
            elif n in [57,58,65]: # pushmid, seamdown, freeplus, btnproto
                plot_forceindentation_group(mt_list[n],linetype='r-',label=str(n))

            elif n in [81,103,104]: # pushmid, seamup, fixedends
                plot_forceindentation_group(mt_list[n],linetype='r-',label=str(n))
            elif n in [72,82]: # pushmid, seamup, freeplus, leftalpha
                plot_forceindentation_group(mt_list[n],linetype='r-',label=str(n))
            elif n in [73,74,75]: # pushmid, seamup, freeplus, rightbeta
                plot_forceindentation_group(mt_list[n],linetype='g-',label=str(n))
            elif n in [78,79,99]: # pushmid, seamup, fixedends, latcenter,loncenter
                plot_forceindentation_group(mt_list[n],linetype='b-',label=str(n))




        result_type = 'fei' # sop | sopnucleo | gsop | namd
        plot_type = 'forceI'
        data_name = ''.join(map(str,args['integers']))
        save_fig(my_dir,0,'fig/forceIonly','%s_%s_%s' % (result_type,plot_type,data_name),option)
        sys.exit()

    if (args['force'] or args['contacts'] or args['nesw'] or args['both']):
        for n in args['integers']:
            print 'Running the Builder.'
            build_mt(mt_list[n])

    if (args['force'] or args['both']):
        print "Plotting Force-Indentation."

        if args['force']:
            plot_forceindentation(mt_list[args['integers'][0]])


    c1 = args['integers'][0]

    # print args['nesw']
    # sys.exit()

    if (args['force'] or args['contacts'] or args['nesw'] or args['both']):
        if len(args['integers']) == 2:
            c2 = args['integers'][1]

            if args['force']:
                print 'getting reverse abscissa'
                mt_list[c1].truncation_by_percent(mt_list[c2].reversal_frame)
                mt_list[c2].get_reverse_abscissa(mt_list[c1].ext_raw[-1])

            if args['contacts']:
                print 'combining contacts and frames..'
                mt_list[c1].combine_contacts_and_frames(mt_list[c2].contacts,
                                                        mt_list[c2].frames,
                                                        mt_list[c2].reversal_frame)
                print mt_list[c1].contacts.shape
                print mt_list[c1].frames.shape
                print mt_list[c1].reversal_frame


            if args['nesw']:
                print 'combining NESW contacts.'
                mt_list[c1].combine_nesw_contacts('n',mt_list[c2].ncontacts,
                                                  mt_list[c2].frames,
                                                  mt_list[c2].reversal_frame)
                mt_list[c1].combine_nesw_contacts('s',mt_list[c2].scontacts,
                                                  mt_list[c2].frames,
                                                  mt_list[c2].reversal_frame)
                mt_list[c1].combine_nesw_contacts('e',mt_list[c2].econtacts,
                                                  mt_list[c2].frames,
                                                  mt_list[c2].reversal_frame)
                mt_list[c1].combine_nesw_contacts('w',mt_list[c2].wcontacts,
                                                  mt_list[c2].frames,
                                                  mt_list[c2].reversal_frame)

            if args['both']:
                print 'plotting both.'
                mt_list[c1].truncation_by_percent(mt_list[c2].reversal_frame)
                mt_list[c2].get_reverse_abscissa(mt_list[c1].ext_raw[-1])

                mt_list[c1].combine_contacts_and_frames(mt_list[c2].contacts,
                                                        mt_list[c2].frames,
                                                        mt_list[c2].reversal_frame)
                print mt_list[c1].contacts.shape
                print mt_list[c1].frames.shape
                print mt_list[c1].reversal_frame

            # cmt = combine_classes(c1,c2)
            # cmt = combine_classes(mt_list[c1],mt_list[c2])


    plot_type = mt_list[args['integers'][0]].name # fe | tension | rmsd | rdf
    data_name1 = ''.join(map(str,args['integers']))
    if len(args['integers']) == 2:
        data_name2 = '_%s' % (mt_list[c2].plate)
        data_name = '%s%s' % (data_name1,data_name2)
    else:
        data_name = data_name1
    print data_name

    if (args['force'] or args['both']):
        for n in args['integers']:
            plot_forceindentation(mt_list[n])

        result_type = 'fei' # sop | sopnucleo | gsop | namd
        save_fig(my_dir,0,'fig/forceI_12dimd','%s_%s_%s' % (result_type,plot_type,data_name),option)

    # print len(args['contacts'])
    # sys.exit()
    # if ((args['contacts']) and (len(args['integers']) > 1)):
    #     print 'Plot Contacts.'
    #     print args['integers']
    #     # for n in args['integers']:
    #     #     plot_contacts(mt_list[n],mt_list[args['integers'][0]].dimers)
    #     plot_contacts(cmt,cmt.dimers)
    # else:
    #     print 'plotting single array of contacts'
    #     mt_list[c1].print_class()
    #     plot_contacts(mt_list[c1],mt_list[c1].dimers)

    if args['contacts']:
        # for n in args['integers']:
        plt.subplots_adjust(left=0.14,right=0.81,top=0.960,bottom=0.18)
        plot_contacts(mt_list[c1],mt_list[c1].dimers)

        result_type = 'contacts' # sop | sopnucleo | gsop | namd
        save_fig(my_dir,0,'fig/see11_contactsE','%s_%s_%s' % (result_type,plot_type,data_name),option)

    if args['nesw']:

        gs = GridSpec(3,3)

        plot_nesw_contacts(mt_list[c1],'n',mt_list[c1].dimers)
        plot_nesw_contacts(mt_list[c1],'e',mt_list[c1].dimers)
        plot_nesw_contacts(mt_list[c1],'s',mt_list[c1].dimers)
        plot_nesw_contacts(mt_list[c1],'w',mt_list[c1].dimers)

        result_type = 'nesw_contacts' # sop | sopnucleo | gsop | namd
        save_fig(my_dir,0,'fig/see11_nesw_contactsE','%s_%s_%s' % (result_type,plot_type,data_name),option)


    if args['both']:

        fig.set_size_inches(7.0,8.0)
        plt.subplots_adjust(left=0.18,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

        # ax1 = plt.subplot(gs[0,:])
        ax2 = plt.subplot(gs[1,:])
        # plot_forceindentation

        plot_contacts(mt_list[c1],mt_list[c1].dimers)
        result_type = 'both2' # sop | sopnucleo | gsop | namd
        save_fig(my_dir,0,'fig/both_fi_contact_dim12d','%s_%s_%s' % (result_type,plot_type,data_name),option)


# ALL single plot, force-extension.
if 0:

    fig = plt.figure(1)
    gs = GridSpec(1,1)
    ax1 = plt.subplot(gs[0,:])
    ax = [ax1]


    print lst_forward
    # lst_forward = []
    # lst_forward = [112,113,115]
    # print args['integers']
    # lst_forward = args['integers']

    # mycolors = ['k', 'r', 'g', 'b','c','m','lime','darkorange','sandybrown','hotpink']
    mycolors = ['k', 'r', 'g','c','c','m','lime','darkorange','sandybrown','hotpink']
    ax1.set_prop_cycle(cycler('color',mycolors))

    # sys.exit()
    for i in lst_forward:

        # print dir(mt_list[i])
        # mt_list[i].print_class()
        print 'name:',mt_list[i].name

        # fig = plt.figure(0)
        # gs = GridSpec(1,1)
        # ax1 = plt.subplot(gs[0,:])
        # ax = [ax1]

        plot_forceindentation(mt_list[i])
        print i,mt_list[i].dirname
        print mt_list[i].name
        print mt_list[i].max_x20,mt_list[i].max_y20

        result_type = 'fei' # sop | sopnucleo | gsop | namd
        plot_type = mt_list[i].name # fe | tension | rmsd | rdf
        data_name = 'one'
# cd ~/ext2/completed_mt/ && ./plot_everything.py -psf ~/ext2/completed_mt/mt12_lev.psf -i 118,116,114,126 -nd 156
    # 2:
    lst_labels = ['1','2','3','5']
    # lst_labels = ['1','2','3','4','2']
    ax1.legend(lst_labels,loc=2,prop={'size':18})

    leg = plt.gca().get_legend()
    for label in leg.get_lines():
        label.set_linewidth(2.5)
    # ax1.set_ylim(-0.05,1.05)
    save_fig(my_dir,0,'fig/forceI','%s_%s_%s' % (result_type,plot_type,data_name),None)
    plt.clf()
    sys.exit()


# sys.exit()
# plt.cla()


if 0:
    plot_contacts(mt_list[1])
    sys.exit()

if 0:
    ####  DIMERS changed!
    plot_angles(mt_list[1],dimers) # beta lon angle
    plot_multiplot(mt_list[1],dimers)

if 0:
    for i,cc in enumerate(lst_cc):
        print i,cc.name

        fig = plt.figure(0)
        gs = GridSpec(1,1)
        ax1 = plt.subplot(gs[0,:])
        ax = [ax1]

        idn = int(cc.name.split('_')[0])
        print type(cc)
        print dir(cc)
        print mt_list[idn].dimers
        # plot_contacts(cc,mt_list[idn].dimers)
        plot_multiplot(cc,mt_list[idn].dimers)

        result_type = 'normcontacts' # sop | sopnucleo | gsop | namd
        plot_type = cc.name # fe | tension | rmsd | rdf
        data_name = 'tiger'

        save_fig(my_dir,0,'fig/multiaxis','%s_%s_%s' % (result_type,plot_type,data_name),None)
        # plt.cla()
        plt.clf()


# #  ---------------------------------------------------------  #
# #  Truncation by percent / combine classes                    #
# #  ---------------------------------------------------------  #
# if args['combine']:
# # if 1:
# # for c
#     fig = plt.figure(0)
#     gs = GridSpec(1,1)
#     ax1 = plt.subplot(gs[0,:])
#     ax = [ax1]

#     tup = tuple([int(x) for x in args['combine'].split(',')])
#     print tup

#     for p in lst_com:
#         print p
#         if p != tup:
#             continue

#         mt_list[p[0]].truncation_by_percent(mt_list[p[1]].reversal_frame)
#         cmt = combine_classes(mt_list[p[0]],mt_list[p[1]])
#         # break
#         # lst_cc.append(cmt)

#         result_type = 'combinedcon' # sop | sopnucleo | gsop | namd
#         plot_type = mt_list[p[0]].name # fe | tension | rmsd | rdf
#         data_name = '_%d_%d_round1' % (p[0],p[1])

#         if 1:
#             plot_multiplot(cmt)
#             save_fig(my_dir,0,'fig/multiaxis','%s_%s_%s' % (result_type,plot_type,data_name),None)
#         elif 0:
#             plot_contacts(cmt)
#             ax1.axvline(mt_list[p[0]].ext_raw[-1],color='r',linewidth=1,linestyle='--')
#             save_fig(my_dir,0,'fig/externalcontactsE','%s_%s_%s' % (result_type,plot_type,data_name),None)
#         elif 0:
#             plot_forceindentation(cmt)
#             save_fig(my_dir,0,'fig/forceI','%s_%s_%s' % (result_type,plot_type,data_name),None)


#     # plt.cla()
#     plt.clf()



# for k in lst_forward:
#     # mt_list[k].get_forceindentation()
#     print k,mt_list[k].name,mt_list[k].max_x20,mt_list[k].max_y20
#     # print 'plate:',dct_rev[k]['plate']
#     # for k1 in dct_rev[k]['plate']:
#     #     print k1,mt_list[k1].max_x20,mt_list[k1].max_y20
#     # print 'noplate:',dct_rev[k]['noplate']
#     # for k2 in dct_rev[k]['noplate']:
#     #     print k2,mt_list[k2].max_x20,mt_list[k2].max_y20

# sys.exit()


# print len(lst_cc)
# print lst_cc
