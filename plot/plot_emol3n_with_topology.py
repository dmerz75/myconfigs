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
from glob import glob

my_dir = os.path.abspath(os.path.dirname(__file__))

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.FindAllFiles import *
from microtubule import *

#  ---------------------------------------------------------  #
#  Begin.argparse                                             #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--round",help="the round: 16, 17",type=int)
    parser.add_argument("-psf","--psf",help="psf: file")
    parser.add_argument("-nd","--nd",help="num_dimers: 104, 156",type=int)
    parser.add_argument("-o","--option",help="options .. show")
    parser.add_argument("-x","--xtraj",help="select trajectory .. x",type=int)
    parser.add_argument("-ctype","--ctype",help="ctype: 3 3n None")
    parser.add_argument("-e","--emol",help=
                        "for plotting emol_mtcontacts_by_subdomain \n \
                        or emol_mtcontacts_by_subdomain3(n), \n \
                        None/0-off,1-on,2-emol3n,4-emol-6x3-dimer-regions \n \
                        other ..",
                        type=int)
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
proj_round = args['round']
xtraj = args['xtraj']
ctype = args['ctype']

if ctype == '3':
    cstring = "emol_mtcontacts_by_subdomain3_top.dat"
elif ctype == '3n':
    cstring = "emol_mtcontacts_by_subdomain3n_top.dat"
else:
    cstring = "emol_mtcontacts_by_subdomain_top.dat"


def load_dct(cwd=my_dir,pattern='*_top.dat'):
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
    set9 = x.remove_dirname('tops_extra',None,set9)
    set9 = x.query_dirname("round_%d" % proj_round,None,set9)
    set9 = x.sort_dirname(-1,set9)
    return set9

# Find all mt_analysis.dat files.
dct_traj = load_dct(os.path.join(my_dir,'indentation'),'*3n_top.dat')
print len(dct_traj.keys())

# M = Microtubule()

#  ---------------------------------------------------------  #
#  Preparatory Functions:                                     #
#  ---------------------------------------------------------  #
def build_mt(mt):
    # mt_list[i].get_mtanalysis()
    # mt_list[i].get_dimers()
    # mt_list[i].get_integersndentation()
    # mt_list[i].get_force_by_time_series()
    # mt_list[i].get_analysis_by_time_series()
    # mt.set_attributes(v)

    mt.setupdirs()
    # mt.find_psf(my_dir,psffile)
    mt.find_psf('%s/structural' % my_dir,psffile)
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

    mt.get_emol_mtcontacts_3n(mt.emoltop3nfile,num_dimers)
    mt.get_emol_mtcontacts_3(mt.emoltop3file,num_dimers)


#  ---------------------------------------------------------  #
#  Plot Here:                                                 #
#  ---------------------------------------------------------  #
def plot_emol_3n(mt):
    '''
    Provide n the index in mt_list for plotting.
    Provide dimers, a list from "get_dimers."
    Use with -e 2 (flag)
    '''
    import matplotlib
    # default - Qt5Agg
    # print matplotlib.rcsetup.all_backends
    # matplotlib.use('GTKAgg')
    # matplotlib.use('TkAgg')
    print 'backend:',matplotlib.get_backend()
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from cycler import cycler

    # print emolfile
    # build_mt(mt)
    # mt.get_dimers()

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
    plot_type = 'bysubdomain_top' # fe | tension | rmsd | rdf

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
        subcolors = ['k','r','g','b','c','m','lime','darkorange','sandybrown','hotpink']

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
            save_fig(my_dir,0,'fig/emol3top','%s_%s_%s_%ddimer' % (result_type,plot_type,
                                                                   data_name,iv[0]),option)
            # plt.clf()



        for dim,iv in enumerate(mt_var[:10]):
            plot_7(iv)
            # break
        plot_7(mt_var[0])

    else:
        data_name = mt.dirname.split('/')[-1]
        save_fig(my_dir,0,'fig','%s_%s_%s' % (result_type,plot_type,
                                              data_name),option)
        plt.clf()




#  ---------------------------------------------------------  #
#  Run Here:                                                  #
#  ---------------------------------------------------------  #
print args

for k,v in dct_traj.iteritems():
    f_select = os.path.join(v['dirname'],cstring)
    mtname = v['dirname'].split('/')[-1]
    print '%3d' % k,mtname,'\t',cstring

print 'Selecting ..'

for k,v in dct_traj.iteritems():
    if xtraj != None:
        if k != xtraj:
            continue
    os.chdir(v['dirname'])
    # print k,v['dirname']
    # lst_files = glob(os.path.join(v['dirname'],'*_top.dat'))
    # f_select = [ff for ff in lst_files if re.search(cstring,ff) != None][0]
    f_select = os.path.join(v['dirname'],cstring)
    # print k,f_select,
    mtname = v['dirname'].split('/')[-1]
    print '%3d' % k,mtname,'\t',cstring

    mt = Microtubule(mtname)
    mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
    mt.emol_topology_based_contact_files(None)
    build_mt(mt)

    # print mt.emoltopfile
    # print mt.emoltop3file
    # print mt.emoltop3nfile
    print mt.emoltopfilename
    print mt.emoltop3filename
    print mt.emoltop3nfilename


    # mt.get_emol_mtcontacts_3n(mt.emoltop3nfile,num_dimers)
    plot_emol_3n(mt)
    # mt.emol_topology_contact(mt.emoltopfile,num_dimers)
    # creates emol3top
    # mt.plot_emol3top(my_dir,option,mt.dimers)
