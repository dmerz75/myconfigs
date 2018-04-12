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
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
# from mylib.run_command import run_command
from plot.microtubule import *
from plot.SETTINGS import *

# Figures:
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


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


if 0:
    with open(os.path.join(my_dir,ffile)) as fp:

        firsts = []
        criticals = []
        dct_stat = {}

        for line in fp:
            if line.startswith('#'):
                continue
            # print line

            fig = plt.figure(0)
            gs = GridSpec(2,1)
            ax1 = plt.subplot(gs[0,:])
            ax2 = plt.subplot(gs[1,:])
            ax = [ax1,ax2]
            fig.set_size_inches(8.0,10.0)
            plt.subplots_adjust(left=0.2,right=0.78,top=0.960,bottom=0.10,hspace=0.4)

            print line
            # mtname = line.split(' ')[0]
            mtname = line.split()[0]
            frame1 = int(line.split()[1])
            frame2 = int(line.split()[2])
            print mtname,frame1,frame2

            for i,mt in enumerate(mt_list):
                if mt.name != mtname:
                    continue
                print mt.name
                mt.get_mtanalysis(num_dimers)
                mt.get_dimers(0.72)
                mt.get_forceindentation()
                mt.get_force_by_time_series()
                # mt.plot_forceindentation(ax1) # with "Full indent," "partial"
                # mt.plot_forceframe(ax1)
                # mt.plot_contacts(ax2,mt.dimers)
                # mt.plot_vertlines(ax1,[frame1,frame2])
                # mt.plot_vertlines(ax2,[frame1,frame2])
                # mt.get_mtpf(ax2)
                mt.get_mtpf()
                # e1,f1 = mt.get_extNforce_at_frame(frame1)
                # e2,f2 = mt.get_extNforce_at_frame(frame2)
                # print frame1,e1,f1
                # print frame2,e2,f2
                # mt1 = mt
                # mt2 = mt
                # mt1.reversal_frame = frame1
                # mt1.truncation_by_percent(frame1)
                # mt2.reversal_frame = frame2
                # mt2.truncation_by_percent(frame2)
                # dct_stat[mt.name] = {}
                # dct_stat[mt.name]['dirname'] = mt.dirname
                # dct_stat[mt.name]['first'] = f1
                # dct_stat[mt.name]['second'] = f2
                # firsts.append(f1)
                # criticals.append(f2)
                data_name = mt.name


            save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
                     '%s_%s_%s_rnd%d_mtpf' % (result_type,plot_type,
                                               data_name,rnd),option)
            plt.clf()





def write_crit_file(dct,value='firstvalue',rnd=0):

    dct_names = {}
    dct_names[10] = "Dimers8.Plate"
    dct_names[11] = "Dimers8.NoPlate"
    dct_names[17] = "Dimers12.Plate"
    dct_names[16] = "Dimers12.NoPlate"
    dct_names[26] = "Dimers12.NoPlate"

    lst_stat = []
    for k,v in dct.iteritems():
        print k
        try:
            lst_stat.append((k,v['breaking_pattern'],v[value]))
        except:
            pass

    # lst_stat_first = dct.values().sort(key=lambda x: x['first'])
    # lst_stat_crit =
    # print lst_stat_first
    # sys.exit()

    for stat in lst_stat:
        print stat[0],stat[1],stat[2]
        lst_stat.sort(key=lambda x: x[2])


    outfile = os.path.join(my_dir,args['forceframecontacts'] +
                           '.' + value + '.' + str(rnd) +
                           '.%s' % dct_names[rnd] +
                           '.out')

    print "Writing:",outfile

    with open(outfile,'w+') as fp:
        # for k,v in dct_sortedstat.iteritems():
        # print k,v
        for stat in lst_stat:
            print stat[0],stat[1],stat[2]
            fp.write("%s     %s   %6.4f\n" % (stat[0],stat[1],stat[2]))


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

    if((rnd == '10') or (rnd == '11')):
        set9 = x.remove_dirname('_nop_',None,set9)
        set9 = x.remove_dirname('_rev_',None,set9)


    set9 = x.query_dirname("round_%d" % rnd,None,set9)
    set9 = x.sort_dirname(-1,set9)
    print 'dct_matches:',len(set9.keys())
    return set9
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

def build_mt(dct):
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
        mt_list.append(mt)

    return mt_list


def get_plotted(fp):

    dct_plotfile = {}
    lst_plotfile = []

    with open(os.path.join(my_dir,ffile)) as fh:
        for line in fh:
            if line.startswith('#'):
                continue

            if re.search('round_%s' % str(rnd),line) == None:
                continue
            # sys.exit()

            # print line
            plotfileline = line.split('/')[1:-1]
            path = ('/').join(line.split('/')[0:-1])
            # print plotfileline

            if len(plotfileline) == 2:
                # ['round_11_mt8nop', 'seamup_poz5_fix2_reg_1001']
                f_round = int(plotfileline[0].split('_')[1])
                f_pos = plotfileline[1].split('_')[1]
                f_name = plotfileline[1]
                # print f_round,f_name,f_pos
            elif len(plotfileline) == 3:
                #['round_16_mtdoz_complete_nop','ahm','seamup_doz5_fix2_AHM_6_nop_00']
                f_round = int(plotfileline[0].split('_')[1])
                f_pos = plotfileline[2].split('_')[1]
                f_name = plotfileline[2]
                # print f_round,f_name,f_pos

            dct_plotfile[f_name] = {}
            dct_plotfile[f_name]['path'] = path
            dct_plotfile[f_name]['pos'] = f_pos
            dct_plotfile[f_name]['round'] = f_round
            lst_plotfile.append(f_name)

    print 'lst_matches:',len(lst_plotfile)
    return lst_plotfile,dct_plotfile

    # def print_class(self):
    # def set_attributes(self,dct):
    # def setupdirs(self):
    # def find_psf(self,psfdir,psf):
    # def find_dcd(self,dcddir=None):
    # def get_reversal_frame(self):
    # def get_frame_count(self):
    # def get_analysis_file(self):
    # def get_sop_file(self):
    # def get_indentation_file(self):
    # def get_pdbs(self):
    # def get_direction_info(self):
    # def get_plate_info(self):
    # def get_sop_info(self):
    # def get_dimers(self):
    # def get_forceindentation(self):
    # def get_emol_mtcontacts(self,total_num_dimers):
    # def get_emol_mtcontacts_3(self,fp,total_num_dimers):
    # def get_emol_mtcontacts_3n(self,fp,total_num_dimers):
    # def get_mtanalysis(self,num_dimers=104,step=5):
    # def get_force_by_time_series(self):
    # def get_reverse_abscissa(self,xt):
    # def get_analysis_by_time_series(self):
    # def truncation_by_percent(self,reversal_frame):
    # def combine_contacts_and_frames(self,arr_contacts,arr_frames,rev_frame):
    # def combine_nesw_contacts(self,obj,arr_contacts,arr_frames,rev_frame):
    # def combine_force_and_indentation(self,arr_force,arr_indentation,rev_ind):
    # def emol_topology_based_contact_files(self,dirname):
    # def emol_topology_contact(self,fp,num_dimers):
    # def plot_emol3top(self,my_dir,option,dimers=[]):

# for k,v in dct_dat.iteritems():
#     print k,v['dirname'].split('/')[-1]



# /home/dmerz3/ext2/completed_mt/results.crit_breaks/rev_crit_breaks_13
# print ffile


# plt.clf()
# fig = plt.figure(0)
# gs = GridSpec(2,1)
# ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:])
# ax = [ax1,ax2]
# fig.set_size_inches(8.0,10.0)
# plt.subplots_adjust(left=0.2,right=0.78,top=0.960,bottom=0.10,hspace=0.4)


# with open(os.path.join(my_dir,ffile)) as fp:

def plot_all(mt_list,lst_plot):
    firsts = []
    criticals = []
    dct_stat = {}
    # print name
    # sys.exit()
    # print len(lst),lst
    # for name in lst:
    # for line in fp:
        # if line.startswith('#'):
            # continue
        # print line

    for i,mt in enumerate(mt_list):
        mt.num_pf = num_pf
        mt.num_dimers = num_dimers

        if mt.name not in lst_plot:
            # print "out",mt.name
            continue
        print mt.name

        # if i > 0:
        #     break


        # print "in",mt.name

        # if mt.name != name:
        #     continue
        # print mt.name
        # continue

        fig = plt.figure(0)
        plt.title(mt.name)
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

        # print line
        # mtname = line.split()[0]
        # frame1 = int(line.split()[1])
        # frame2 = int(line.split()[2])
        # print mtname,frame1,frame2

        # for i,mt in enumerate(mt_list):
            # if mt.name != mtname:
                # continue
            # print mt.name

        mt.get_mtanalysis(num_dimers)

        # Contact at percent frame evaluation:
        # mt.get_dimers(0.33,0.70)
        # mt.get_dimers(0.48,0.68)
        # mt.get_dimers(0.05,0.1)
        mt.get_dimers(0.45,0.70)

        # Screening for early low dimer loss:
        # print "before:",mt.dimers
        mt.remove_early_contact_losses('n')
        mt.remove_early_contact_losses('s')
        mt.remove_early_contact_losses('w')
        mt.remove_early_contact_losses('e')
        # print "after:",mt.dimers
        # sys.exit()

        mt.get_forceindentation()
        mt.get_force_by_time_series()
        mt.get_first_break_events()
        mt.get_crit_break_events()
        mt.manual_override_first_crit_break_frames(ffile)
        # sys.exit()


        # mt.get_break_events('n')
        # mt.get_break_events('s')
        # mt.get_break_events('e')
        # mt.get_break_events('w')
        # mt.process_break_events()


        # mt.plot_forceindentation(ax1) # with "Full indent," "partial"


        # PLOT: contacts
        mt.plot_forceframe(ax1)
        mt.plot_contacts(ax2,mt.dimers)
        mt.plot_contact_interface(ax3,'n')
        mt.plot_contact_interface(ax4,'s')
        mt.plot_contact_interface(ax5,'w')
        mt.plot_contact_interface(ax6,'e')
        print "The Breaking Pattern: ",mt.breaking_pattern


        # P = SaveFig(mt.my_dir,mt.name,
        #             destdirname='fig/contacts_full/%s' % mt.rnd)
        # sys.exit()

        # mt.get_mtpf(ax2)
        # plot N,S,E,W contacts.    OLD
        # minfn = mt.plot_contact_interface(ax3,'n')
        # minfs = mt.plot_contact_interface(ax4,'s')
        # minfw = mt.plot_contact_interface(ax5,'w')
        # minfe = mt.plot_contact_interface(ax6,'e')


        # mt.determine_early_late_contact_changes()
        # Get maxforceframes. Store in maxforceframes
        # mt.get_maxforceframe() # Get after mt.break_first


        # print minfn,minfs,minfw,minfe
        # sys.exit()
        # mt.plot_vertlines(ax1,[min([minfn,minfs]),min([minfw,minfs])])
        # mt.plot_vertlines(ax2,[min([minfn,minfs]),min([minfw,minfs])])
        # mt.plot_vertlines(ax2,[minfn,minfw])
        # minframe_lat = min([minfw,minfe])
        # minframe_lon = min([minfn,minfs])
        # print minframes
        # sys.exit()


        # PLOT MTPF - global, local.
        mt.get_mtpf()
        mt.process_mtpf()
        mt.plot_mtpf_global(ax7)

        # mt.plot_mtpf_local(ax8)

        # mt.get_cendist()
        # mt.plot_cendist(ax_bottom)

        # beta angle.
        # mt.get_beta_angle()
        # mt.plot_beta_angle(axes_beta)

        # point4ab
        # mt.get_point4ab()
        # mt.plot_point4ab(ax8)

        # entire PF ang:
        mt.get_entire_PF_ang()
        mt.plot_entire_PF_ang(ax_bottom)
        mt.plot_vertlines([ax_bottom],[mt.break_first],color='g')
        mt.plot_vertlines([ax_bottom],[mt.break_critical],color='r')



        # Draw Vertical Lines for First, Critical Breaks.
        # mt.plot_vertlines([ax1,ax2],[mt.break_first],color='g')
        # mt.plot_vertlines([ax1,ax2],[mt.break_critical],color='r')
        mt.plot_vertlines(axes_plotted,[mt.break_first],color='g')
        mt.plot_vertlines(axes_plotted,[mt.break_critical],color='r')
        # mt.plot_vertlines(ax1,[mt.break_first],color='g')
        # mt.plot_vertlines(ax2,[mt.break_first],color='g')



        e1,f1 = mt.get_extNforce_at_frame(mt.break_first)
        e2,f2 = mt.get_extNforce_at_frame(mt.break_critical)
        # e0,f0 = mt.get_extNforce_at_frame(min([minframe_lat,minframe_lon]))
        # e1,f1 = mt.get_extNforce_at_frame(minframe_lat)
        # e2,f2 = mt.get_extNforce_at_frame(minframe_lon)

        # print frame1,e1,f1
        # print frame2,e2,f2


        # Now..
        # Get the frame of first lateral break,
        # frame of the first significant longitudinal break.
        # save_fig(my_dir,0,'fig/both_fi_contact_dim12vert/%s' % rnd,
        #          '%s_%s_%s_rnd%d_total' % (result_type,plot_type,
        #                                    mtname,rnd),option)

        # savedir = os.path.join(self.my_dir,'contacts_full/%s' % (self.rnd))

        # for ax in axes_all[2:]:
            # ax.axis('off')
            # ax.tick_params('')
            # ax.tick_params()
            # ax.tick_params(axis='both',labelsize=12)
        P = SaveFig(mt.my_dir,mt.name,
                    destdirname='fig/contacts_full/%s' % mt.rnd)

        # mt1 = mt
        # mt2 = mt
        # mt1.reversal_frame = frame1
        # mt1.truncation_by_percent(frame1)
        # mt2.reversal_frame = frame2
        # mt2.truncation_by_percent(frame2)

        dct_stat[mt.name] = {}
        dct_stat[mt.name]['dirname'] = mt.dirname
        # dct_stat[mt.name]['first'] = f1
        # dct_stat[mt.name]['first'] = min([minframe_lat + minframe_lon])
        # dct_stat[mt.name]['lat'] = minframe_lat
        # dct_stat[mt.name]['lon'] = minframe_lon

        dct_stat[mt.name]['first'] = f1
        dct_stat[mt.name]['critical'] = f2
        dct_stat[mt.name]['breaking_pattern'] = mt.breaking_pattern


        # dct_stat[mt.name]['first'] = f0
        # dct_stat[mt.name]['lat'] = f1
        # dct_stat[mt.name]['lon'] = f2


        # dct_stat[mt.name]['second'] = f2
        # dct_stat[mt.name]['second'] = f2
        # firsts.append(f1)
        # criticals.append(f2)

    # for i in range(len(firsts)):
    #     print i,firsts[i],criticals[i]
    # for k,v in dct_stat.iteritems():
    #     print k,v['first'],v['second']

    # Write First, and Maxvalue:
    # write_crit_file(dct_stat,'.first.out','first')
    # write_crit_file(dct_stat,'.maxvalue.out','second')

    # March decision:
    # write_crit_file(dct_stat,'first',rnd)
    # write_crit_file(dct_stat,'lat',rnd)
    # write_crit_file(dct_stat,'lon',rnd)

    # Final decision:
    write_crit_file(dct_stat,'first',rnd)
    write_crit_file(dct_stat,'critical',rnd)


# End all
dct_dat = load_dct(my_dir,'mt_analysis.dat')
# for tracking:
for k,v in dct_dat.items():
    # print k,v
    print v['dirname']
# sys.exit()
lst_plotfile,dct_plotfile = get_plotted(ffile)
mt_list = build_mt(dct_dat)
plot_all(mt_list,lst_plotfile)

# dct_dat = load_dct(path_pf,'mt_analysis.dat')
# for i,mt in enumerate(mt_list):
#     print i,mt.name
# for lpf in lst_plotfile:
    # /home/dmerz3/ext/completed_mt/indentation/round_10_mt8doz/seamup_poz1_fix2_reg_1001
    # indentation/round_10_mt8doz/seamup_poz1_fix2_reg_1001
    # seamup_poz1_fix2_reg_1001
    # 10
    # poz1
    # path_pf = os.path.join(my_dir,dct_plotfile[lpf]['path'])
    # print path_pf
    # print dct_plotfile[lpf]['path']
    # print lpf
    # print dct_plotfile[lpf]['round']
    # print dct_plotfile[lpf]['pos']
    # break

# for i,mt in enumerate(mt_list):
#     plot_all()


# 26
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -rnd 26 -psf ~/ext/completed_mt/structural/mt12_plate.psf -nd 156 -ff results.crit_breaks/pname_framebreaks_16

# 11
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -nd 104 -psf structural/mt8nop.psf -ff results.crit_breaks/pname_framebreaks_11 -rnd 11

# 10
# cd ~/ext/completed_mt/ && ./plot_round_1314_vertlines.py -nd 104 -psf structural/mt8doz.psf -ff results.crit_breaks/pname_framebreaks_10 -rnd 10
