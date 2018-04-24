#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# libraries:
from mylib.FindAllFiles import *
from plot.microtubule import *
from plot.SETTINGS import *

# Figures:
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


#  ---------------------------------------------------------  #
#  Plots                                                      #
#  ---------------------------------------------------------  #
def make_plots():
    fig = plt.figure(0)
    gs = GridSpec(1,1)
    ax1 = plt.subplot(gs[0,:])
    ax = [ax1]

    dct_font = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'16'}
    matplotlib.rc('font',**dct_font)
    gs = GridSpec(8,24)
    fig.set_size_inches(15.0,13.0)
    plt.subplots_adjust(left=0.12,right=0.96,top=0.960,bottom=0.08,hspace=1.3,wspace=0.3)


    # Row 1: Force-Indentation, N,S
    ax1 = plt.subplot(gs[0:2,0:8])
    ax3 = plt.subplot(gs[0:2,10:16])
    ax5 = plt.subplot(gs[0:2,18:24])

    # Row 2: Contacts, W,E
    ax2 = plt.subplot(gs[2:4,0:8])
    ax4 = plt.subplot(gs[2:4,10:16])
    ax6 = plt.subplot(gs[2:4,18:24])

    axtop6 = [ax1,ax2,ax3,ax4,ax5,ax6]

    # Row 3,4: PFBend, Angles
    ax71 = plt.subplot(gs[4:6,0:3])
    ax72 = plt.subplot(gs[4:6,3:6])
    ax73 = plt.subplot(gs[4:6,6:9])
    ax74 = plt.subplot(gs[4:6,9:12])
    ax75 = plt.subplot(gs[4:6,12:15])
    ax76 = plt.subplot(gs[4:6,15:18])
    ax77 = plt.subplot(gs[4:6,18:21])
    ax78 = plt.subplot(gs[4:6,23:24]) # colorbar
    ax7s = [ax71,ax72,ax73,ax74,ax75,ax76,ax77]
    ax7 = [ax71,ax72,ax73,ax74,ax75,ax76,ax77,ax78]

    ax81 = plt.subplot(gs[6:8,0:3])
    ax82 = plt.subplot(gs[6:8,3:6])
    ax83 = plt.subplot(gs[6:8,6:9])
    ax84 = plt.subplot(gs[6:8,9:12])
    ax85 = plt.subplot(gs[6:8,12:15])
    ax86 = plt.subplot(gs[6:8,15:18])
    ax87 = plt.subplot(gs[6:8,18:21])
    ax88 = plt.subplot(gs[6:8,23:24]) # colorbar
    ax8s = [ax81,ax82,ax83,ax84,ax85,ax86,ax87]
    ax8 = [ax81,ax82,ax83,ax84,ax85,ax86,ax87,ax88]

    ax_bottom = plt.subplot(gs[4:8,0:24])

    axes_all = [ax1,ax2,ax3,ax4,ax5,ax6] + ax7 + ax8
    # axes_plotted = axtop6 + ax7s + ax8s
    axes_plotted = axtop6 + ax8s
    axes_lower = ax7 + ax8
    axes_beta = ax7[:-1] + ax8[:-1]

    return axes_all


#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    Options:
    args['makefile']
    args['procs']
    args['node'])
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--string1",help="input string")
    parser.add_argument("-n","--node",help="select node",type=int)
    parser.add_argument("-rnd","--rnd",help="select round",type=int)
    parser.add_argument("-psf","--psf",help="select psffile")
    parser.add_argument("-nd","--num_dimers",help="number of dimers, 104, 156")
    parser.add_argument("-ff","--forceframecontacts",help="select plot trajectories file")
    parser.add_argument("-pf","--num_protofilaments",help="Number of Protofilaments")

    args = vars(parser.parse_args())
    return args
args = parse_arguments()
rnd = args['rnd']
psffile = args['psf']
ffile = args['forceframecontacts']
num_dimers = int(args['num_dimers'])

try:
    num_pf = int(args['num_protofilaments'])
except:
    num_pf = 13

option = None
result_type = 'gsop'
plot_type = 'ffc'


# Rounds: 16, 17 only

#  ---------------------------------------------------------  #
#  sorting                                                    #
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
    set9 = x.remove_dirname('example',None,set9)
    set9 = x.remove_dirname('tops_extra',None,set9)

    # if((rnd == '10') or (rnd == '11')):
    #     set9 = x.remove_dirname('_nop_',None,set9)
    #     set9 = x.remove_dirname('_rev_',None,set9)
    set9 = x.query_dirname("round_%d" % rnd,None,set9)
    set9 = x.sort_dirname(-1,set9)
    print 'dct_matches:',len(set9.keys())
    return set9


def get_retraction_dct(dct):

    set9 = dct
    print len(set9.keys())
    x = FindAllFiles()
    set_rev = x.query_dirname("_rev_",None,set9)
    set_nop = x.query_dirname("_nop_",None,set9)
    set10 = x.merge_dct([set_rev,set_nop])
    print len(set10.keys())

    set_for = x.remove_dirname("_rev_",None,set9)
    set_for = x.remove_dirname("_nop_",None,set_for)
    print len(set_for.keys())

    lst_forward_names = []

    for k,v in set10.iteritems():
        # print k,v['dirname'].split('/')[-1]
        # print v
        proj_name = v['dirname'].split('/')[-1]
        forwards = proj_name.split('_nop_')[0]

        lst_forward_names.append(forwards)


    lst_tup_for_retract = []

    for name in lst_forward_names:
        # print name


        for k,v in set_for.iteritems():

            if re.search(name,v['dirname']) != None:

                # print k,name
                f1 = k
                break

        for k,v in set10.iteritems():

            if re.search(name,v['dirname']) != None:

                lst_tup_for_retract.append((f1,k))
                break


    for tup in lst_tup_for_retract:
        # print tup
        pass

    print len(lst_tup_for_retract)
    return lst_tup_for_retract
    # # indices:
    # for name in lst_forward_names:

    #     for k,v in set10.iteritems():
    #         if re.search(name,v['dirname']) != None:

    #             print name,k #,v['dirname']
    #             break


def build_mt(v):

    name = v['dirname'].split('/')[-1]
    # print v['dirname']
    # print name

    mt = Microtubule(name)
    mt.set_attributes(v) # dirname, file, filename, name, type(mt_analysis.dat)
    # mt.print_class()

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
    mt.rnd = rnd
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


    # additions:
    mt.get_forceindentation()
    mt.get_force_by_time_series()
    mt.get_mtanalysis(num_dimers)
    mt.get_dimers()
    mt.get_analysis_by_time_series()
    mt.get_emol_mtcontacts(num_dimers)



    # Screening for early low dimer loss:
    # print "before:",mt.dimers
    mt.remove_early_contact_losses('n')
    mt.remove_early_contact_losses('s')
    mt.remove_early_contact_losses('w')
    mt.remove_early_contact_losses('e')
    # print "after:",mt.dimers
    # sys.exit()

    print "SHape:"
    print mt.analysis.shape


    return mt

    # extras:
    # def print_class(self):

    # not yet ..
    # def setupdirs(self):
    # def get_emol_mtcontacts(self,total_num_dimers):
    # def get_emol_mtcontacts_3(self,fp,total_num_dimers):
    # def get_emol_mtcontacts_3n(self,fp,total_num_dimers):


#  ---------------------------------------------------------  #
#  Combine Classes.                                           #
#  ---------------------------------------------------------  #
def combine_classes(m1,m2):

    cmt = Microtubule('combined')
    cmt.dimers = m1.dimers
    print 'cmt-dimers:',cmt.dimers

    combines = ['frames','numfixedbeads','numsteps','plate','steps','tipx',
                'tipy','tipz','total_frames','analysis','angles','curvature',
                'data','deltax','direction','end_to_end','ext_raw',
                'externalcontacts','f_nano','f_pico','force','max_x20',
                'max_y20','contacts']


    # mt_list[c1].truncation_by_percent(mt_list[c2].reversal_frame)
    m1.truncation_by_percent(m2.reversal_frame)

    # mt_list[c2].get_reverse_abscissa(mt_list[c1].ext_raw[-1])
    m2.get_reverse_abscissa(xt=m1.ext_raw[-1])


    # Extras:
    # def combine_force_and_indentation(self,arr_force,arr_indentation,rev_ind):
    # def emol_topology_based_contact_files(self,dirname):
    # def emol_topology_contact(self,fp,num_dimers):
    # def plot_emol3top(self,my_dir,option,dimers=[]):


    # cmt or m1


    print "combining contacts and frames."
    m1.combine_contacts_and_frames(m2.contacts,
                                   m2.frames,
                                   m2.reversal_frame)

    print 'combining NESW contacts.'
    m1.combine_nesw_contacts('n',m2.ncontacts,
                             m2.frames,
                             m2.reversal_frame)
    m1.combine_nesw_contacts('s',m2.ncontacts,
                             m2.frames,
                             m2.reversal_frame)
    m1.combine_nesw_contacts('e',m2.ncontacts,
                             m2.frames,
                             m2.reversal_frame)
    m1.combine_nesw_contacts('w',m2.ncontacts,
                             m2.frames,
                             m2.reversal_frame)


    # cmt.absorb(m1)

    # Combine m1, m2
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




dct_total = load_dct(my_dir,'mt_analysis.dat')
# for k,v in dct_total.iteritems():
#     print k,v['dirname'].split('/')[-1]
lst_retractpairs = get_retraction_dct(dct_total)

for tup in lst_retractpairs:
    print tup
    # print 'Forward:',dct_total[tup[0]]['dirname'].split('/')[-1]
    # print "Reverse:",dct_total[tup[1]]['dirname'].split('/')[-1]

    mtf = build_mt(dct_total[tup[0]])
    mtr = build_mt(dct_total[tup[1]])

    # mtf.print_class()
    # mtr.print_class()

    print mtf.direction,':',mtf.name
    print mtr.direction,':',mtr.name

    cmt = combine_classes(mtf,mtr)

    axes = make_plots()


    # Screening for early low dimer loss:
    # print "before:",cmt.dimers
    # cmt.remove_early_contact_losses('n')
    # cmt.remove_early_contact_losses('s')
    # cmt.remove_early_contact_losses('w')
    # cmt.remove_early_contact_losses('e')
    # print "after:",cmt.dimers
    # sys.exit()

    # cmt.get_forceindentation()
    # cmt.get_force_by_time_series()
    # cmt.get_first_break_events()
    # cmt.get_crit_break_events()
    # cmt.manual_override_first_crit_break_frames(ffile)
    # sys.exit()


    # cmt.plot_forceindentation(ax1) # with "Full indent," "partial"


    # PLOT: contacts
    # cmt.plot_forceframe(axes[0])
    cmt.plot_forceindentation(axes[0])
    cmt.plot_contacts(axes[1],cmt.dimers)

    # cmt.plot_contact_interface(axes[2],'n')
    # cmt.plot_contact_interface(axes[3],'s')
    # cmt.plot_contact_interface(axes[4],'w')
    # cmt.plot_contact_interface(axes[5],'e')
    # print "The Breaking Pattern: ",cmt.breaking_pattern

    P = SaveFig(my_dir,
                'ret_%s' % (rnd),
                destdirname='fig/retractions')
    break
