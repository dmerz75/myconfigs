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

    # Axes4
    ax1 = plt.subplot(gs[0:4,0:11]) # 1 3
    ax2 = plt.subplot(gs[4:8,0:11]) # 2 4

    ax3 = plt.subplot(gs[0:2,13:24])
    ax4 = plt.subplot(gs[2:4,13:24])
    ax5 = plt.subplot(gs[4:6,13:24])
    ax6 = plt.subplot(gs[6:8,13:24])

    axes = [ax1,ax2,ax3,ax4,ax5,ax6]
    return axes


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
    x.get_files()
    # print len(x.dct.keys()),'of',x.total
    set9 = x.remove_dirname('fail',None,x.dct)
    set9 = x.remove_dirname('example',None,set9)
    set9 = x.remove_dirname('tops_extra',None,set9)

    # if((rnd == '10') or (rnd == '11')):
    #     set9 = x.remove_dirname('_nop_',None,set9)
    #     set9 = x.remove_dirname('_rev_',None,set9)
    set9 = x.query_dirname("round_%d" % rnd,None,set9)
    set9 = x.sort_dirname(-1,set9)
    # x.print_query(set9)
    # sys.exit()
    print 'dct_matches:',len(set9.keys())
    return set9


def get_retraction_dct(dct):

    set9 = dct
    print len(set9.keys())
    x = FindAllFiles()

    if rnd == 16:
        set_nop = x.remove_dirname("_nop_00",None,set9)
    else:
        set_nop = x.query_dirname("_nop_",None,set9)

    set_rev = x.query_dirname("_rev_",None,set9)
    set10 = x.merge_dct([set_rev,set_nop])

    # print "Lengths:"
    # print len(set_rev.keys())
    # print len(set_nop.keys())
    # print len(set10.keys())
    # sys.exit()

    if rnd == 16:
        set_for = x.query_dirname("_nop_00",None,set9)
    else:
        set_for = x.remove_dirname("_rev_",None,set9)
        set_for = x.remove_dirname("_nop_",None,set_for)

    # print "Forwards:"
    # print len(set_for.keys())
    # sys.exit()

    # lst_forward_names = []
    # for k,v in set10.iteritems():
    #     # print k,v['dirname'].split('/')[-1]
    #     # print v
    #     proj_name = v['dirname'].split('/')[-1]
    #     forwards = proj_name.split('_nop_')[0]
    #     lst_forward_names.append(forwards)


    lst_tup_for_retract = []

    # print set_for.keys()
    # print set10.keys()

    for k,v in set_for.iteritems():

        # print k,v['name']

        for k1,v1 in set10.iteritems():

            if rnd == 16:
                name_ser = v['name'].split('_nop_')[0]
                if re.search(name_ser,v1['name']) != None:
                    # print v['name'],v1['name']
                    # print (k,k1)
                    lst_tup_for_retract.append((k,k1))
            else:
                if re.search(v['name'],v1['name']) != None:
                    # print v['name'],v1['name']
                    # print (k,k1)
                    lst_tup_for_retract.append((k,k1))


    # for name in lst_forward_names:
    #     # print name

    #     for k,v in set_for.iteritems():

    #         if re.search(name,v['dirname']) != None:
    #             # print k,name
    #             f1 = k
    #             break
    #     try:
    #         print f1
    #     except:
    #         continue

    #     for k,v in set10.iteritems():

    #         if re.search(name,v['dirname']) != None:

    #             if (f1,k) not in lst_tup_for_retract:
    #                 lst_tup_for_retract.append((f1,k))
    #             break


    # for tup in lst_tup_for_retract:
    #     print tup
    #     pass

    print "retractions:",len(lst_tup_for_retract)
    # sys.exit()
    return lst_tup_for_retract



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
    mt.get_analysis_by_time_series() # ??
    mt.get_emol_mtcontacts(num_dimers)



    # Screening for early low dimer loss:
    # print "before:",mt.dimers
    mt.remove_early_contact_losses('n')
    mt.remove_early_contact_losses('s')
    mt.remove_early_contact_losses('w')
    mt.remove_early_contact_losses('e')

    return mt


#  ---------------------------------------------------------  #
#  Combine Classes.                                           #
#  ---------------------------------------------------------  #
def combine_classes(m1,m2):
    """
    Consider just modifying m1.
    """
    m1.truncation_by_percent(m2.reversal_frame)
    m1.combine_ext_raw(m2.ext_raw) # concatenates to m1.ext_raw, m2.ext_raw
    m1.combine_force(m2.f_nano)

    print "combining contacts and frames."
    m1.combine_contacts_and_frames(m2.contacts,
                                   m2.frames,
                                   m2.reversal_frame)

    # print 'combining NESW contacts.'
    # m1.combine_nesw_contacts('n',m2.ncontacts,
    #                          m2.frames,
    #                          m2.reversal_frame)
    # m1.combine_nesw_contacts('s',m2.ncontacts,
    #                          m2.frames,
    #                          m2.reversal_frame)
    # m1.combine_nesw_contacts('e',m2.ncontacts,
    #                          m2.frames,
    #                          m2.reversal_frame)
    # m1.combine_nesw_contacts('w',m2.ncontacts,
    #                          m2.frames,
    #                          m2.reversal_frame)

    m1.combine_contacts(ncontacts=m2.ncontacts)
    m1.combine_contacts(econtacts=m2.econtacts)
    m1.combine_contacts(scontacts=m2.scontacts)
    m1.combine_contacts(wcontacts=m2.wcontacts)

    m1.combine_contacts(wcontacts_raw=m2.wcontacts_raw)
    m1.combine_contacts(econtacts_raw=m2.econtacts_raw)
    # sys.exit()




dct_total = load_dct(my_dir,'mt_analysis.dat')
# for k,v in dct_total.iteritems():
#     print k,v['dirname'].split('/')[-1]
# sys.exit()
lst_retractpairs = get_retraction_dct(dct_total)
# print lst_retractpairs
# print len(lst_retractpairs)

for tup in lst_retractpairs:
    print tup
    label = ('_').join([str(i) for i in tup])

    namef = dct_total[tup[0]]['dirname'].split('/')[-1]
    namer = dct_total[tup[1]]['dirname'].split('/')[-1]
    # namer = re.sub(namef,'',namef)

    # print namef
    # print namer
    # continue

    # if (tup[0] != 59):
    #     continue
    # if (tup[1] != 63):
    #     continue


    # print tup
    # continue

    # print type(label),label
    # continue
    # print 'Forward:',dct_total[tup[0]]['dirname'].split('/')[-1]
    # print "Reverse:",dct_total[tup[1]]['dirname'].split('/')[-1]

    mtf = build_mt(dct_total[tup[0]])
    mtr = build_mt(dct_total[tup[1]])

    # mtf.print_class()
    # mtr.print_class()

    print mtf.direction,':',mtf.name
    print mtr.direction,':',mtr.name

    combine_classes(mtf,mtr)

    print mtf.ext_raw.shape
    print mtf.f_nano.shape

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
    mtf.plot_forceindentation(axes[0])
    mtf.plot_contacts(axes[1],mtf.dimers,loc=3)

    mtf.plot_contact_interface(axes[2],ncontacts=mtf.ncontacts)
    mtf.plot_contact_interface(axes[3],scontacts=mtf.scontacts)
    mtf.plot_contact_interface(axes[4],econtacts=mtf.econtacts)
    mtf.plot_contact_interface(axes[5],wcontacts=mtf.wcontacts)
    mtf.plot_vertlines(axes,[mtr.reversal_frame],color='r')

    mtf.get_work()


    # determine if the retraction permits recovery.
    contact_count = mtf.get_min_lateral_contacts()

    # maxcount,mincount = mtf.get_min_lateral_contacts()
    # contact_count = min(np.concatenate([mtf.econtacts_raw,mtf.wcontacts_raw]))
    # break

    # print mincount,maxcount,maxcount - mincount
    # break


    # str1 = '# %s %s %s (kcal/mol ~600/(200-300)contacts)' % (label, namef, namer)
    str1 = '# %s %s %s %s' % (label, namef, namer,mtf.bool_recovers)
    str2 = "%6.2f  %6.2f  %6.2f  %3d" % (mtf.work_indentation,
                                           mtf.work_retraction,
                                           mtf.work_total,contact_count)
    print str1
    print str2
    # break


    fn = 'results_work_%s.dat' % rnd
    fp = os.path.join(my_dir,fn)
    f = open(fp,'a+')
    f.write(str1)
    f.write("\n")
    f.write(str2)
    f.write("\n")
    # f.write("# %s\n" % mtf.bool_recovers)
    f.close()
    # lst_work.append(w)
    # break



    P = SaveFig(my_dir,
                'ret_%s_%s' % (rnd,label),
                destdirname='fig/retractions')
    # break
