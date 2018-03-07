#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
from datetime import datetime

import numpy as np
from glob import glob

my_dir = os.path.abspath(os.path.dirname(__file__))


#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from plot.SOP import *
from data.check_bad_lines import check_bad_lines
from mylib.run_command import run_command
from mylib.FindAllFiles import *


#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
#  ---------------------------------------------------------  #
# import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
# print 'backend:',matplotlib.get_backend()
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
# fig = plt.figure(0)

#  ---------------------------------------------------------  #
#  Import Data! (2/4)                                         #
#  ---------------------------------------------------------  #
result_type = 'gsop' # sop | sopnucleo | gsop | namd
plot_type = 'indentation3' # fe | tension | rmsd | rdf

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
    parser.add_argument("-r","--round_name",help="round_name: 1,2,3 .. -> 02",type=int)
    parser.add_argument("-m","--multi",help="multi: defaults to None, any other")
    parser.add_argument("-f","--function",help="function: run,rename(default)")
    parser.add_argument("-p","--program",help="program: emol3n, pfbend")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
option = args['option']
data_name = args['dataname']
if data_name == None:
    data_name = 'all'
round_name = str(args['round_name']).zfill(2)
multi = args['multi']

print "option:",option,"data:",data_name,"round:",round_name
combined_name = '%s_%s_%s_%s' % (result_type, plot_type,round_name,data_name)

function = args['function']
prog = args['program']

# gs = GridSpec(1,1)
# ax1 = plt.subplot(gs[0,:])
# # ax2 = plt.subplot(gs[1,:-1])
# ax = [ax1]
# if multi != None:
#     ax2 = ax1.twiny()
#     ax3 = ax1.twiny()
#     ax = [ax1,ax2,ax3]


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
    set9 = x.dct
    # x.dct (last pos.)
    # set9 = x.sort_dirname(-1,x.dct)
    # x.print_ [query,class]
    # x.query_ [dirname,file,filename](searchstring,pos,dct)
    # x.remove_[dirname,file,filename](searchstring,pos,dct)
    # x.print_query(set9)
    # print len(set9.keys()),'of',x.total
    # sys.exit()
    # return set9
    set9 = x.remove_dirname('fail',None,set9)
    set9 = x.remove_dirname('builder',None,set9)
    set9 = x.remove_filename('_new.dat',set9)
    set9 = x.remove_filename('_bac.dat',set9)
    set9 = x.remove_dirname('dat',-1,set9)

    print len(set9.keys()),'of',x.total
    set9 = x.sort_dirname(-1,set9)
    return set9

def get_round(dct,round_name):
    print 'files entered:',len(dct.keys())
    x = FindAllFiles()
    print round_name

    set9 = x.query_dirname(round_name,-3,dct)
    if(len(set9.keys()) == 0):
        set9 = x.query_dirname(round_name,-4,dct)

    # if ((round_name == 'round_16') and (len(set9.keys()) == 0)):
    #     set9 = x.query_dirname(round_name,-4,dct)

    set9 = x.sort_dirname(-1,set9)
    print 'file returned: (round) ',len(set9.keys())
    return set9

def get_bydata(dct,data_name):
    print 'files entered:',len(dct.keys())
    x = FindAllFiles()
    print data_name
    set9 = x.query_dirname(data_name,-2,dct)
    lst = set9.keys()
    return sorted(lst)
    # set9 = x.sort_dirname(-1,set9)
    # print 'file returned:',len(set9.keys())
    # return set9

def get_doz(dct,data_name):
    print 'files entered:',len(dct.keys())
    x = FindAllFiles()
    print data_name
    set9 = x.query_dirname(data_name,-2,dct)
    set9 = x.sort_dirname(-2,set9)
    # lst = set9.keys()
    # return sorted(lst)
    # return lst
    return set9


# available dictionaries:
dct_dat = load_dct(my_dir,'*indent*.dat')
print 'total entries:',len(dct_dat.keys())
# for k,v in dct_dat.iteritems():
#     print k,v['dirname']

dct_plot = get_round(dct_dat,'round_%s' % round_name)

for k,v in dct_plot.iteritems():
    print k,v['dirname']




def do_sorting():
    lst_dcts = [get_doz(dct_plot,'doz%d' % x) for x in [1,2,3,4,5]]

    for dct1 in lst_dcts: # lst of integers
        # for k,v in dct_plot.iteritems():
        for k,v in dct1.iteritems():
            # if k not in dct1:
            #     continue
            # print k,v.keys()
            print k,'\t',v['dirname'].split('/')[-2]

        # print type(dct1)
        # print len(dct1)
        # for xd in dct1:
            # print type(xd)

        # for k,v in dct1.iteritems():
        #     # print k,v.keys()
        #     print k,'\t',v['dirname'].split('/')[-2]


print 'sorting...'
do_sorting()
# sys.exit()

# for k,v

# rounds:
# 0: ningxi, 1:nolongrange 2: gb-w-longrange  3: longi-later-fail
# 2,5,8, gb
# 4:6 sasa, 5:6-gb, 6:6-, 7:4-, 8:6-gb, 9:6-;
# 4,6,7,9
# 13:18: lat1,lat2,lat3,lon1,lon2,lon3; down,up;
# lst_plot = get_list(round_name)
# print lst_plot

if data_name != 'all':
    lst_plot = get_bydata(dct_plot,data_name)
else:
    lst_plot = dct_plot.keys()
print lst_plot
# sys.exit()


# ____check file integrity_____
# for k,v in dct_plot.iteritems():
#     check_bad_lines(v['file'])
#     # check_bad_lines(v['file'],'new')
#     check_bad_lines(v['file'],'write')
#     continue
# sys.exit()



for k,v in dct_plot.iteritems():
    # print k,v['file']
    # print os.path.basename(v['dirname'])
    # ddir = ('/').join(os.path.split(v['dirname']))
    ddir = '/' + ('/').join(v['dirname'].split('/')[1:-1])

    if 1:
        print 'checking here:',ddir
        os.chdir(ddir)
        pdb = glob.glob('*.ref.pdb')[0]
        if not os.path.exists('pdbref.ent'):
            command1 = ['ln','-s',pdb,'pdbref.ent']
            run_command(command1)
        pdb = 'pdbref.ent'
        # dcd = glob.glob('dcd/*pull.dcd')[0]
        dcd = glob.glob('dcd/*.dcd')[0]

        # tops = glob.glob('*.top')[0]
        if re.search('AHM',ddir) != None:
            # ../../../../tops/MT_AHM.top
            # ../../../../tops/MT_PF56.top
            # ../../../../tops/MT_LHM.top
            # ../../../../tops/MT_regular.top
            command2 = ['ln','-s','../../../../tops/MT_AHM.top','top_this.top']
        elif re.search('LHM',ddir) != None:
            command2 = ['ln','-s','../../../../tops/MT_LHM.top','top_this.top']
        elif re.search('top56',ddir) != None:
            command2 = ['ln','-s','../../../../tops/MT_PF56.top','top_this.top']
        elif re.search('_reg_',ddir) != None:
            command2 = ['ln','-s','../../../../tops/MT_regular.top','top_this.top']

        if ((re.search('mt8doz',ddir) != None) or (re.search('mt8nop',ddir) != None)):
            command2 = ['ln','-s','../mt.top','top_this.top']
        print command2
        run_command(command2)
        # try:
        #     run_command(commmand2)
        # except:
        #     pass
        # sys.exit(0)

        # OPTION
        # command = ['emol_mtcontacts',pdb,dcd,'0','5000','1']

        if prog == 'emol3n':
            command = ['emol_mtcontacts3n',pdb,dcd,'0','5000','1']
            datfile = 'emol_mtcontacts_by_subdomain3n.dat'
        elif prog == 'pfbend':
            command = ['emol_mtpfbend3',pdb,dcd,'2','5000','10']
            datfile = 'emol_mtpfbending_angle.dat'

        # command = ['emol_mtcontacts_topo',pdb,dcd,'3','903','3','top_this.top']
        # if int(round_name) < 15:
        #     command = ['run_segment_dcd_dimermap_mt',pdb,dcd,'209','1','0','5000','1']
        # else:
        #     command = ['run_segment_dcd_dimermap_mt',pdb,dcd,'313','1','0','5000','1']
        # command = ['run_segment_dcd',pdb,dcd,'209','1','0','5000','5']

        # datfiles = glob.glob('emol_mtcontacts.dat')
        # num_datfile = len(datfiles)

        # datfile = 'emol_mtcontacts.dat'
        # datfile = 'emol_mtcontacts_top.dat'
        # print datfiles
        # print num_datfile
        # sys.exit()

        if function == 'run':
            if os.path.exists(datfile):
            # OPTION
            # if 0:
                print 'emol_contacts.dat must be renamed first. not running!'
            else:
                print 'running:  ',os.path.basename(ddir)
                print command
                run_command(command)

        if function == 'rename':
            if os.path.exists(datfile):
                print 'renaming.'
                time_ext = datetime.fromtimestamp(os.path.getmtime(datfile)).strftime('%Y_%m%d_%I%M')
                fcn = os.path.splitext(datfile)[0]
                new_name = fcn + '_' + time_ext + '.dat'
                print 'renaming:',new_name,'in',os.path.basename(ddir)
                os.rename(datfile,new_name)
            # else:
            #     pass
            # else:
            #     print 'no emol_contacts.dat found.'
            #     print 'found emol_contacts*.dat',num_datfile
            #     print datfiles


        # if ((not os.path.exists(datfile)) and (function == 'run')):
        #     print command
        #     run_command(command)
        # else:
        #     print'mt_analysis.dat exists!!'
        #     # time_ext = time.strftime("%Y_%m%d_%I%M")
        #     time_ext = datetime.fromtimestamp(os.path.getmtime(datfile)).strftime('%Y_%m%d_%I%M')
        #     fcn = os.path.splitext(datfile)[0]
        #     new_name = fcn + '_' + time_ext + '.dat'
        #     print 'renaming:',new_name,'in',os.path.basename(ddir)
        #     os.rename(datfile,new_name)


# min_x = 0.0
# max_x = 0.0

# for k,v in dct_plot.iteritems():
#     if k not in lst_plot:
#         continue
#     print 'plotting ',k

#     # D = PlotSop('MT',point_start=0,point_stop=8040,ma_value=20,step=1,\
#     #             ts=20,nav=100,dcdfreq=1000000,seam='down',outputtiming=100000)
#     D = PlotSop('MT',point_start=0,point_stop=20000,ma_value=20,step=1,\
#                 ts=20,nav=100,dcdfreq=1000000,seam='down',outputtiming=100000)

#     D.load_data(v['file'])

#     print 'HERE!'
#     e8 = D.extension[-1] * 0.05
#     t8 = D.time[-1] * 0.05
#     f8 = D.frame[-1] * 0.05
#     print e8
#     print t8
#     print f8

#     newmin_x = D.extension[0]-e8
#     newmax_x = D.extension[-1]+e8
#     print newmin_x,newmax_x
#     if min_x > newmin_x:
#         min_x = newmin_x
#     if max_x < newmax_x:
#         max_x = newmax_x
#     print "XMIN,XMAX:",min_x,max_x
#     ax1.set_xlim(min_x,max_x)

#     if multi != None:
#         # eline = ax1.plot(D.extension,D.force,'k-',linewidth=2.0)
#         eline = ax1.plot(D.extension,D.force,'k-')


#         ax2.set_xlim(D.time[0]-t8,D.time[-1]+t8)
#         tline = ax2.plot(D.time,D.force,'b')

#         fig.text(0.01,0.135,'Time (ms)',color='b',size=16)
#         ax2.spines['bottom'].set_color('b')
#         ax2.spines['bottom'].set_position(('outward',70.0))
#         ax2.xaxis.set_ticks_position('bottom')
#         for tick in ax2.xaxis.get_major_ticks():
#             tick.label.set_fontsize(16)


#         ax3.set_xlim(D.frame[0]-f8,D.frame[-1]+f8)
#         fline = ax3.plot(D.frame,D.force,'m')

#         fig.text(0.01,0.050,'Frame #',color='m',size=16)
#         ax3.spines['bottom'].set_color('m')
#         ax3.spines['bottom'].set_position(('outward',110.0))
#         ax3.xaxis.set_ticks_position('bottom')
#         for tick in ax3.xaxis.get_major_ticks():
#             tick.label.set_fontsize(16)
#         break
#     else:
#         plt.plot(D.extension,D.force)
#         ax1.set_ylim(-0.05,0.75)
#         ax1.set_xlabel("Indentation Depth (nm)")
#         ax1.set_ylabel("Force (nN)")







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
# save_fig(my_dir,0,'fig/indentation','%s_%s_%s' % (result_type,plot_type,data_name),option)
# save_fig(my_dir,0,'fig/indentation','%s' % (combined_name),option)

# mpl_myargs_end
