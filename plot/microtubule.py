# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time
import numpy as np
from glob import glob
import re

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# libraries:
# from mylib.FindAllFiles import *
from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
from mylib.moving_average import *
# from mylib.regex import reg_ex
from mylib.run_command import run_command
from plot.SETTINGS import *

import MDAnalysis
# from mdanalysis.MoleculeUniverse import MoleculeUniverse

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# from plot.cdf import *




from cycler import cycler
# print matplotlib.rcParams['axes.prop_cycle']
mycolors = ['k', 'r', 'g', 'b','c','m','lime',
            'darkorange','sandybrown','hotpink',
            'mediumseagreen','crimson','slategray',
            'orange','orchid','darkgrey','indianred',
            'tan','cadetblue']
# ax1.set_prop_cycle(cycler('color',mycolors))



def get_frame_below_threshold(arr,threshold):

    for i in range(arr.shape[0]):

        if arr[i] < threshold:
            break

    return i

def get_frame_below_avg_threshold(arr,span,threshold):

    # 5:   5,
    for i in range(arr.shape[0]-span):
        avg = np.mean(arr[i:i+span])
        if avg < threshold:
            break

    # back of span frame, Qn
    return i+span,arr[i+span]


class Microtubule():
    """
    Describing a microtubule.
    """
    def __init__(self,name):
        """
        Description:

        """
        self.name = name
        self.dimers = []
        self.truncated = 'no'
        self.num_pf = 13
        self.num_dimers = 104


        # (frame, force, lat/lon/both, Qn (lon if both)
        self.break_events = []
        self.break_events_lon = []
        self.break_events_lat = []
        self.breaking_pattern = ''
        # self.rnd = rnd


    def print_class(self):
        '''
        Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            try:
                print getattr(self,key).shape
            except:
                pass
            # definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    def set_attributes(self,dct):
        '''
        Set attributes.
        '''
        for k,v in dct.iteritems():

            if k not in dir(self):
                # print 'setting self.%s=%s' % (k,v)
                setattr(self,k,v)
            else:
                pass
                # print 'previously set self.%s=%s' % (k,v)


    def setupdirs(self):
        if not self.dirname:
            print 'return'
            return
        else:
            self.datdir = os.path.join(self.dirname,'dat')
            self.dcddir = os.path.join(self.dirname,'dcd')
            self.indentationdir = os.path.join(self.dirname,'indentation')
            self.outputdir = os.path.join(self.dirname,'output')
            self.topdir = os.path.join(self.dirname,'topologies')

    # def find_psf(self,psfdir,psf,x):
    def find_psf(self,psfdir,psf):
        os.chdir(psfdir)

        # lst = ['mt.psf','mt_noplate.psf','mt12_lev.psf',
        #        'mt12_rev.psf','mt12_plate.psf']
        # psf = lst[x]
        # self.psf = os.path.join(psfdir,psf)
        # return


        # print self.rnd
        # sys.exit()

        if psf != None:
            self.psf = os.path.join(psfdir,psf)
            return
        # if ((not re.search('nop',self.name)) and (not re.search('rev',self.name))):

        if ((self.rnd != 16) and (self.rnd != 17)):
            if re.search('nop',self.name) != None:
                lst = glob.glob('mt_noplate.psf')
            else:
                lst = glob.glob('mt.psf')
        else:
            if self.rnd == 16:
                # lst = glob('mt12_lev.psf')
                lst = glob.glob('mt12_lev.psf')
            elif self.rnd == 17:
                if re.search("rev",self.name) != None:
                    lst = glob.glob('mt12_rev.psf')
                else:
                    # lst = glob('mt12_plate.psf')
                    # lst = glob('mt12.psf')
                    # lst = glob('mt12_lev.psf')
                    lst = glob.glob('mt12_plate.psf')
                    # mt12_lev.psf
                    # mt12_plate.psf
                    # mt12.psf
                    # mt12_rev.psf
        # print lst
        # sys.exit()

        # if len(lst) == 0:
        #     lst = glob('mt12_plate.psf')[0]

        # lst = glob('*.psf')
        # print  lst
        # print self.name
        # time.sleep(5)

        if len(lst) == 1:
            psf = lst[0]
            self.psf = os.path.join(psfdir,psf)
        # elif len(lst) == 0:
        #     self.psf = os.path
        else:
            print psfdir
            print lst
            print 'multiple psf\'s found.'
            sys.exit(1)

    def find_dcd(self,dcddir=None):
        if dcddir == None:
            dcddir = self.dcddir
        if dcddir == None:
            print 'No dcddir loaded.'
            sys.exit(1)
        os.chdir(dcddir)
        lst = glob.glob('*.dcd')

        if len(lst) == 1:
            dcd = lst[0]
            self.dcd = os.path.join(self.dcddir,dcd)
        else:
            print self.dcddir
            print lst
            print 'multiple dcd\'s found.'
            sys.exit(1)

    def get_reversal_frame(self):

        # print self.dirname
        if self.direction == 'forward':
            self.reversal_frame = -1
        else:
            # print self.dirname
            self.reversal_frame = int(self.name.split('_')[-1])
            # print self.name
            # print self.reversal_frame


    def get_frame_count(self):
        os.chdir(self.dirname)

        try:
            framefile = glob('FRAME.*')[0]
        except:
            framefile = 'FRAME.-1'

        mdaframe = glob.glob('MDAframe.*')

        if len(mdaframe) == 1:
            mdaframefile = mdaframe[0]
            self.total_frames = int(mdaframefile.split('.')[-1])


        elif ((self.dcd != None) and (self.psf != None)):
            # print self.psf
            # print self.dcd

            # self.dcd = MDAnalysis.coordinates.DCD.DCDReader(dcd)
            # self.u = MDAnalysis.Universe(self.psf,self.dcd)
            try:
                self.u = MDAnalysis.Universe(self.psf,self.dcd)
            except:
                print self.psf
                print self.dcd
                print "check load value error."
                print "using default. (600)"
                run_command(['touch','MDAframe.%d' % 602])
                self.total_frames = 602
                return
                # sys.exit(1)

            # for fr in self.u.trajectory:
            #     pass
            self.total_frames = len(self.u.trajectory)
            # self.frames = np.linspace(0,self.total_frames-1,self.total_frames)

            run_command(['touch','MDAframe.%d' % self.total_frames])

                # print fr
            # print self.u.trajectory
            # print self.u.universe
            # print self.u.frames

        else:
            print 'Psf or Dcd is empty. CANNOT RUN.'
            return


        # self.frames = np.linspace(0,self.total_frames-1,self.total_frames)
        # self.frames =
        # print framefile.split('.')[1:]
        # print self.total_frames

    def get_analysis_file(self):
        os.chdir(self.dirname)
        lst = glob.glob('mt_analysis.dat')
        if len(lst) == 1:
            self.file_analysis = lst[0]
        else:
            print 'Analysis file not found.'

    def get_sop_file(self):
        # self.sopfile = os.path.join(self.dirname,'mt.sop')
        # self.sopfile = 'mt.sop'

        os.chdir(self.dirname)

        curfiles = os.listdir(os.getcwd())

        for f in curfiles:
            if re.search('.sop',f) != None:
                self.sopfile = f
                # print f
                break
        return
        # sys.exit()

        # lst = glob.glob('mt.sop')
        # if len(lst) == 1:
        #     self.sopfile = lst[0]
        #     return
        # else:
        #     lst = glob.glob('MT.sop')
        #     if len(lst) == 1:
        #         self.sopfile = lst[0]
        #         return
        #     else:
        #         try:
        #             self.sopfile = glob('*.sop')[0]
        #         except:
        #             print 'Analysis file not found.'

    def get_indentation_file(self):
        os.chdir(self.indentationdir)

        # print 'indentationdir:',self.indentationdir
        try:
            path = glob.glob('*.npy')[0]
        except IndexError:
            print 'saving npy ...'
            path = glob.glob('*_indent.dat')[0]
            npy = re.sub('.dat','.npy',path)
            print path
            x = np.loadtxt(path)
            np.save(npy,x)
            path = npy


        self.file_indent = os.path.join(self.indentationdir,path)

    def get_pdbs(self):
        os.chdir(self.dirname)
        self.ref = glob.glob('*.ref.pdb')[0]
        # self.ref = glob('mt.ref.pdb')[0]
        # if not self.ref:
        #     self.ref = glob('*.ref.pdb')[0]


        try:
            self.pdbref = glob.glob('pdbref.ent')[0]
        except IndexError:
            pass

        try:
            self.pdb = glob.glob('mt.pdb')[0]
        except IndexError:
            pass


    def get_direction_info(self):

        # print 'getting direction:'
        # print self.name
        # if ((re.search('rev',self.name) == None) and (re.search('nop',self.name) == None)):
        #     self.direction = 'forward'
        # else:
        #     self.direction = 'reverse'
        self.direction = 'forward'

        if ((re.search('_rev_',self.name) == None) and re.search('_nop_',self.name) == None):
            self.direction = 'forward'
            return

        # print self.name.split('_rev_')
        # sys.exit()

        if (re.search('_rev_',self.name)) != None:
             if int(self.name.split('_rev_')[-1]) != 0:
                 self.direction = 'reverse'
                 return
             else:
                 self.direction = 'forward'

        if (re.search('_nop_',self.name)) != None:
            print self.name
            if int(self.name.split('_nop_')[-1]) != 0:
                self.direction = 'reverse'
                return
            else:
                self.direction = 'forward'

        # sys.exit()

        # pass

    def get_plate_info(self):

        if (re.search('nop',self.name) != None):
            self.plate = 'no'
        else:
            self.plate = 'yes'

    def get_sop_info(self):
        '''
        get information from mt.sop.
        '''
        if not os.path.exists(self.sopfile):
            self.get_sop_file()

        pattern = re.compile(r"\d+\.\d*") # looking for a decimal.
        patternbead = re.compile(r"\d+")


        if self.sopfile == None:
            return
        else:
            with open(self.sopfile) as fp:
                for line in fp:
                    # print line

                    if line.startswith('indentationDeltaX'):
                        self.deltax = float(re.search(pattern,line).group())
                        # print 'deltax:',self.deltax

                    if line.startswith('fixed_beads'):
                        self.numfixedbeads = int(re.search(patternbead,line).group())
                        # print 'numfixedbeads:',self.numfixedbeads

                    if line.startswith('indentationTip'):
                        if re.search(r'\w+',line).group() == 'indentationTip':
                            line = re.sub('indentationTip','',line)
                            pos = line.split()
                            self.tipx = float(pos[0])
                            self.tipy = float(pos[1])
                            self.tipz = float(pos[2])

                    if line.startswith('numsteps'):
                        self.numsteps = int(re.search(patternbead,line).group())

                        # print 'numsteps:',self.numsteps

                    if line.startswith('dcdfreq'):
                        self.dcdfreq = int(re.search(patternbead,line).group())
                        # print 'dcdfreq:',self.dcdfreq,type(self.dcdfreq)

        self.steps = self.dcdfreq * self.total_frames
        self.total_time = 31.68 * self.steps * 0.001 * 0.001 * 0.001 # ms (milliseconds)
        # print self.total_time
        # sys.exit()

    #  ---------------------------------------------------------  #
    #  Get Data.                                                  #
    #  ---------------------------------------------------------  #
    # force-indentation.
    # external contacts.
    # contacts.
    # angles.
    # curvature.
    def get_dimers(self,threshold1=0.7,threshold2=0.9):
        '''
        Get the dimers from a Microtubule Class.
        Return a tuple.
        '''
        y = self.contacts
        frameinitial = int(y.shape[0] * 0.0)
        frametested1 = int(y.shape[0] * threshold1)
        frametested2 = int(y.shape[0] * threshold2)
        print "Frames: %d is initial 10%% of the total number of frames: %d." % (frameinitial,
                                                                                 y.shape[0])
        print "Frames: %d is 70%% of the total number of frames: %d." % (frametested1,y.shape[0])
        print "Frames: %d is 90%% of the total number of frames: %d." % (frametested2,y.shape[0])

        # tuples:
        dimers = []
        dimers70p = []

        # final lists:
        lst_dimers = []
        lst_dimers70p = []
        lst_combined = []

        # print y.shape

        for c in range(self.contacts.shape[1]):
            # diff = y[0,c] - y[-1,c]
            diff = y[frameinitial,c] - y[frametested2,c]
            dimers.append((c,diff))

        for c in range(self.contacts.shape[1]):
            # print c # 0 - 103 (104 dimers)
            # print y.shape
            # print y.shape[0] # number of frames.
            # diff = y[0,c] - y[frametested,c]
            diff = y[frameinitial,c] - y[frametested1,c]
            dimers70p.append((c,diff))

        # Sort, last 10nnnn.
        # mod_dimers = sorted(dimers, key=lambda x: x[1])[-10:]
        # print mod_dimers,len(mod_dimers)
        # self.dimers = [x[0] for x in mod_dimers]

        # List of Reversed of Sorted.
        # [(39, 0.7109375),
        #  (26, 0.7109375),
        #  (50, 0.68384879725085912),
        #  (51, 0.59649122807017552),
        sort_num = 10
        mod_dimers    = list(reversed(sorted(dimers, key=lambda x: x[1])[-sort_num:]))
        mod_dimers70p = list(reversed(sorted(dimers70p, key=lambda x: x[1])[-sort_num:]))

        print "mod_dimers/70p:"
        print mod_dimers
        print mod_dimers70p
        # sys.exit()

        # integers of dimers only
        lst_dimers = [x[0] for x in mod_dimers if x[1] > 0.32]
        print 'Selected laters, > 0.35:',len(lst_dimers),lst_dimers
        if len(lst_dimers) < 10:
            lst_dimers =  [x[0] for x in mod_dimers[0:10]]
        # elif len(lst_dimers) > 8:
        #     lst_dimers =  [x[0] for x in mod_dimers[0:8]]
        lst_dimers = lst_dimers[0:10]
        print "The Length of lst_dimers_late is: %d." % len(lst_dimers)


        lst_dimers70p = [x[0] for x in mod_dimers70p if x[1] > 0.03]
        print 'Selected earlies, > 0.051:',len(lst_dimers70p),lst_dimers70p
        if len(lst_dimers70p) < 10:
            lst_dimers70p = [x[0] for x in mod_dimers70p[0:10]]
        # elif len(lst_dimers70p) > 8:
        #     lst_dimers70p = [x[0] for x in mod_dimers70p[0:6]]
        lst_dimers70p = lst_dimers70p[0:10]
        print "The length of lst_dimers_early is: 70%% is: %d." % len(lst_dimers70p)
        # sys.exit()

        # num_of_breakingdimers = len(lst_dimers) + len(lst_dimers70p)
        # if num_of_breakingdimers <= 8:
        #     lst_dimers = [x[0] for x in mod_dimers if x[1] > 0.4]
        #     lst_dimers70p = [x[0] for x in mod_dimers70p if x[1] > 0.1]


        # print "from end evaluation:"
        # for i in range(10):
        #     print mod_dimers[i]

        # print "from 70%% evaluation:"
        # for i in range(10):
        #     print mod_dimers70p[i]

        print "length_late:",len(lst_dimers),lst_dimers
        print "length_early:",len(lst_dimers70p),lst_dimers70p

        # combining lst_dimers with lst_dimers70p
        lst_combined = lst_dimers70p
        for d in lst_dimers:
            if d not in lst_combined:
                lst_combined.append(d)
            # if len(lst_combined) >= 14:
                # break

        # if lst_combined < 14:



        # + lst_dimers70p[0:6]
        # print "Currently using most broken at 70%% frame. Frame: %d" % frametested

        print "Using the combining dimers approach: %f, %f" % (threshold1, threshold2)
        print [x*2 for x in lst_combined]
        self.dimers = lst_combined
        # sys.exit()


    def get_forceindentation(self):

        # print self.indentationdir
        # print self.file_indent

        self.data = np.load(self.file_indent)
        # print self.data.shape

        # Data:
        col1 = self.data[::,0] # 1st column
        f_raw = self.data[::,3] # from gsop147/gsop4, 4th column
        self.f_pico = f_raw * 70.0 # pico
        self.f_nano = self.f_pico * 0.001 # nano
        # self.end_to_end = self.data[::,1] * 0.1 # 2nd column A to nm
        e250 = self.data[::,10] * -0.1 + 250 # 11nd column A to nm
        eshifted = e250 - e250[0]

        simple_ma = 150
        e_ra = moving_average(eshifted,simple_ma)
        shift = np.linspace(0,0,simple_ma)
        self.end_to_end = np.concatenate((shift,e_ra))

        self.ext_raw = self.end_to_end - self.end_to_end[0] # in nanometers.
        distance = abs(self.ext_raw[-1] - self.ext_raw[0])         # total distance traveled
        ext_linear = np.linspace(0,distance,len(f_raw))


        from plot.FORCEQUENCH import FindForceQuench
        fq = FindForceQuench()
        # fq.find_max_near(force_quench_initial,X.extension,X.force)

        try:
            fq.find_max_near(25.0,5.0,self.ext_raw,self.f_nano)
            self.max_x20 = fq.near_x
            self.max_y20 = fq.near_y
        except:
            self.max_x20 = -1.0
            self.max_y20 = -1.0


        # print len(col1),len(f_raw),len(f_pico),len(f_nano),len(end_to_end),len(ext_raw),len(ext_linear)

    def get_emol_mtcontacts(self,total_num_dimers):
        '''
        '''
        # print self.file
        # print dir(self)
        # print self.indentationdir
        # print self.datdir
        print self.dirname
        num_dimers = len(self.dimers)
        print 'number of dimers breaking:',num_dimers
        # return
        # sys.exit()
        # data = np.loadtxt(os.path.join(self.)
        try:
            data = np.loadtxt(os.path.join(self.dirname,'emol_mtcontacts_by_subdomain.dat'))
        except:
            print 'No emol_mtcontacts_by_subdomain.dat file found.'
            sys.exit(1)

        print data.shape
        # sys.exit()

        print 'total_dimers:', total_num_dimers

        frames_x_dimers = data.shape[0] / 9
        print "frames_by_dimers:",frames_x_dimers

        frames = frames_x_dimers / total_num_dimers
        print 'frames:', frames

        datax = data.reshape(frames,total_num_dimers,9,10)
        print datax.shape
        # print datax[::,0,0,::]

        self.emol = datax
        return


        # frames_x_step = step * frames

        # print frames,frames_x_step
        # print frames * num_dimers * data.shape[1]
        # print frames * num_dimers


        datax = np.reshape(data,(frames,num_dimers,data.shape[1]))
        print datax.shape

        return

        num_frames9 = data.shape[0] / num_dimers
        num_frames = num_frames9 / 9
        print num_frames

        # # create frames | dimers | 9 | 9
        dataz = data.reshape(num_frames,num_dimers,9,data.shape[1])
        print dataz.shape

        # print datax[0,::,::,::] # frame 1.
        # print '-----'
        # print datax[::,0,::,::]
        # print datax[1,0:15,0:4,::]


    def get_emol_mtcontacts_3(self,fp,total_num_dimers):
        '''
        '''
        # print self.file
        # print dir(self)
        # print self.indentationdir
        # print self.datdir
        # print self.dirname
        num_dimers = len(self.dimers)
        print 'number of dimers breaking:',num_dimers
        # return
        # sys.exit()
        # data = np.loadtxt(os.path.join(self.)
        try:
            # data = np.loadtxt(os.path.join(self.dirname,'emol_mtcontacts_by_subdomain3.dat'))
            # data = np.loadtxt(os.path.join(self.dirname,fp))
            data = np.loadtxt(os.path.join(fp))
        except:
            print 'No emol_mtcontacts_by_subdomain.dat file found.'
            sys.exit(1)

        print data.shape
        # return
        # sys.exit()

        print 'total_dimers:', total_num_dimers

        frames = data.shape[0] / total_num_dimers
        datax = data.reshape(frames,total_num_dimers,data.shape[1])

        # print "..",frames_x_dimers / total_num_dimers
        # frames = frames_x_dimers / total_num_dimers
        # print 'frames:', frames

        print datax.shape
        # print datax[::,0,0,::]

        self.emol3 = datax
        return

    def get_emol_mtcontacts_3n(self,fp,total_num_dimers):
        '''
        '''
        # print self.file
        # print dir(self)
        # print self.indentationdir
        # print self.datdir
        # print self.dirname
        num_dimers = len(self.dimers)
        print 'number of dimers breaking:',num_dimers
        # return
        # sys.exit()
        # data = np.loadtxt(os.path.join(self.)
        try:
            # data = np.loadtxt(os.path.join(self.dirname,'emol_mtcontacts_by_subdomain3n.dat'))
            data = np.loadtxt(fp)
        except:
            print 'No emol_mtcontacts_by_subdomain.dat file found.'
            sys.exit(1)

        print data.shape
        # return
        # sys.exit()

        print 'total_dimers:', total_num_dimers

        frames = data.shape[0] / total_num_dimers
        datax = data.reshape(frames,total_num_dimers,data.shape[1])

        # print "..",frames_x_dimers / total_num_dimers
        # frames = frames_x_dimers / total_num_dimers
        # print 'frames:', frames

        print datax.shape
        # print datax[::,0,0,::]

        self.emol3n = datax
        return


    def get_mtanalysis(self,num_dimers=104,step=5):

        # print self.file
        data = np.loadtxt(self.file)
        # print data.shape
        frames = data.shape[0] / num_dimers
        frames_x_step = step * frames
        print frames,frames_x_step
        print frames * num_dimers * data.shape[1]
        print frames * num_dimers
        datax = np.reshape(data,(frames,num_dimers,data.shape[1]))

        # print contacts.shape

        # 0-5   alpha index findex | beta index findex
        # 6-11  SINEW: southern,internal,northern,eastern,western,external
        # 12-14 angles: alpha lateral, beta lateral, beta longitudinal
        # 15-17 RofCurva: a_lat_radius, b_lat_radius, b_lon_radius

        # frame | dimer | contacts
        self.externalcontacts = datax[::,::,11]

        # 6-11  SINEW: southern,internal,northern,eastern,western,external
        south_contacts = datax[::,::,6]
        north_contacts = datax[::,::,8]
        east_contacts = datax[::,::,9]
        west_contacts = datax[::,::,10]

        # # max over all frames  ---- no looping through frames.
        # maxc = np.linspace(-1,-1,len(self.externalcontacts[1]))
        # for d in range(self.externalcontacts.shape[1]):
        #     maxc[d] = max(self.externalcontacts[::,d])

        # self.contacts = self.externalcontacts / maxc
        self.contacts = self.externalcontacts / self.externalcontacts[0,::]


        self.scontacts_raw = datax[::,::,6]
        self.ncontacts_raw = datax[::,::,8]
        self.econtacts_raw = datax[::,::,9]
        self.wcontacts_raw = datax[::,::,10]


        self.scontacts = datax[::,::,6] / south_contacts[0,::]
        self.ncontacts = datax[::,::,8] / north_contacts[0,::]
        self.econtacts = datax[::,::,9] / east_contacts[0,::]
        self.wcontacts = datax[::,::,10] / west_contacts[0,::]

        arr_ma = 10
        self.ncontacts = moving_average_array(self.ncontacts,arr_ma)
        self.wcontacts = moving_average_array(self.wcontacts,arr_ma)
        self.econtacts = moving_average_array(self.econtacts,arr_ma)
        self.scontacts = moving_average_array(self.scontacts,arr_ma)


        # print self.contacts.shape
        # print self.contacts[::,45]
        # sys.exit()
        self.angles = datax[::,::,12:15]
        self.curvature = datax[::,::,17]


        lst_frame = [0]
        f = open(self.file,'r')
        with open(self.file) as fp:
            for line in fp:
                if line.startswith('# frame'):
                    # print line
                    numframe = int(re.search('\d+',line).group())
                    # print numframe
                    lst_frame.append(numframe)

        frame_array = np.array(lst_frame)
        self.frames = frame_array

        print 'last_frame:',frame_array[-1]
        # print len(self.contacts)
        # print frame_array,len(frame_array)
        # sys.exit()


    def get_force_by_time_series(self):
        '''
        Arrange Force vs. ITF (indentation,time,frame)
        at the length of self.f_nano.
        '''
        # force vs. indentation, time, frame
        # F vs. ITF
        # print len(self.f_nano)
        # time = self.steps * self.deltax * 0.001
        # time = self.steps * 0.001
        # time = self.steps * 0.001
        # print 'time:',time
        # print 'frame:',self.total_frames

        # fvtime = np.linspace(0,time,len(self.f_nano))
        fvtime = np.linspace(0,self.total_time,len(self.f_nano))
        fvframe = np.linspace(0,self.total_frames,len(self.f_nano))

        self.force = np.zeros((len(self.f_nano),4),dtype=float)

        # print 'f_nano:'
        # print self.f_nano
        self.force[::,0] = self.f_nano
        self.force[::,1] = self.ext_raw
        self.force[::,2] = fvtime
        self.force[::,3] = fvframe

        # print self.force
        # print self.force.shape
        # for i in range(self.force.shape[1]):
        #     print self.force[0,i],self.force[-1,i]

    # def get_reverse_abscissa(self,**kwargs):
    def get_reverse_abscissa(self,**kwargs):
        # print 'xt:',xt
        # print self.ext_raw[::,1][::10]

        # new_xt = self.ext_raw * -1 + xt

        # if "xt" in kwargs:
        #     xt = kwargs['xt']
        # else:
        #     xt = self.ext_raw[-1]

        # new_xt = self.ext_raw + xt
        # self.ext_raw = new_xt
        # # pass


        if "ext_raw" in kwargs:
            ext = kwargs['ext_raw']
        else:
            print "No array to reverse was provided."
            return


        # print self.ext_raw.shape
        # print ext.shape

        ext = ext + self.ext_raw[-1]
        self.ext_raw = np.concatenate((self.ext_raw,ext))

        # print self.ext_raw
        # print ext
        # print self.ext_raw.shape
        # print ext.shape
        # sys.exit()

    def get_analysis_by_time_series(self):
        '''
        Arrange Analysis(contacts) vs. ITF (indentation,time,frame), also angles/curvature.
        (contacts, indentation, time, frame, angles, curvature)
        at the length of self.externalcontacts.
        Currently, empty, not being used.
        '''
        # contacts or externalcontacts
        # time = self.steps * self.deltax * 0.001
        # time = self.steps * 0.001
        # avtime = np.linspace(0,time,len(self.contacts))
        # pass
        # return

        avtime = np.linspace(0,self.total_time,len(self.contacts))
        avframe = np.linspace(0,self.total_frames,len(self.contacts))
        avind = np.linspace(self.ext_raw[0],self.ext_raw[-1],len(self.contacts))
        self.analysis = np.zeros((len(self.contacts),3))
        self.analysis[::,0] = avind
        self.analysis[::,1] = avtime
        self.analysis[::,2] = avframe

        # self.analysis[::,0] = self.contacts (101,104)
        # self.analysis[::,4] = self.angles
        # self.analysis[::,5] = self.curvature
        # print dir(self)
        # self.

    # def truncation_by_percent(self,reversal_frame):
    def truncation_by_percent(self,revframe=-1):

        # print 'trunc:'
        # print self.dirname
        # print "Calling reversal"
        # self.get_reversal_frame()

        self.reversal_frame = revframe

        if self.direction == 'reverse':
            return

        if not self.reversal_frame:
            print "no reversal frame yet .."
            sys.exit()


# analysis :      [[  0.00000000e+00   0.00000000e+00   0.00000000e+00]
# angles :        [[[ 152.7  148.8  175.3]
# contacts :      [[ 1.          1.          1.         ...,  1.          1.          1.        ]
# curvature :     [[  518.3   504.3  1617.1 ...,   842.2   842.2   842.2]
# data :  [[  0.00000000e+00   4.00000000e-05   0.00000000e+00 ...,   0.00000000e+00
# dcdfreq :       1000000
# deltax :        4e-05
# end_to_end :    [  4.00000000e-06   4.00400000e-03   8.00400000e-03 ...,   3.02974610e+01
# ext_raw :       [  0.00000000e+00   4.00000000e-03   8.00000000e-03 ...,   3.02974570e+01
# externalcontacts :      [[ 182.  238.  153. ...,  203.  223.  182.]
# f_nano :        [ 0.         0.         0.        ...,  0.5583592  0.5576081  0.5387704]
# f_pico :        [   0.        0.        0.     ...,  558.3592  557.6081  538.7704]
# force : [[  0.00000000e+00   0.00000000e+00   0.00000000e+00   0.00000000e+00]
# frames :        [   0.    1.    2.    3.    4.    5.    6.    7.    8.    9.   10.   11.
# total_frames :  766
# steps : 766000000

        # data,dcdfreq,deltax,total_frames
        targets = ['analysis','angles','contacts','curvature',
                   'end_to_end','ext_raw','externalcontacts',
                   'f_nano','f_pico','force','frames','total_frames',
                   'steps','ncontacts','scontacts','econtacts','wcontacts',
                   'econtacts_raw','ncontacts_raw','scontacts_raw',
                   'wcontacts_raw']

        percent = float(self.reversal_frame) / self.total_frames
        # print self.percent

        print 'percent_for_truncating:',percent
        # sys.exit()

        for obj in targets:

            try:
                print obj,getattr(self,obj).shape
            except AttributeError:
                print '\nNo attribute:',obj
                continue
            except:
                print 'single:'
                print obj,getattr(self,obj)

            if ((obj == 'analysis') or (obj == 'contacts') or (obj == 'curvature') or
                (obj == 'externalcontacts') or (obj == 'force') or
                (obj == 'ncontacts') or (obj == 'scontacts') or
                (obj == 'econtacts') or (obj == 'wcontacts') or
                (obj == 'econtacts_raw') or (obj == 'wcontacts_raw') or
                (obj == 'scontacts_raw') or (obj == 'ncontacts_raw')):
                limit = int(getattr(self,obj).shape[0] * percent)
                arr = getattr(self,obj)[:limit,::]
                setattr(self,obj,arr)

            elif obj == 'angles':
                limit = int(getattr(self,obj).shape[0] * percent)
                arr = getattr(self,obj)[:limit,::,::]
                setattr(self,obj,arr)

            elif ((obj == 'end_to_end') or (obj == 'ext_raw') or (obj == 'f_nano') or
                (obj == 'f_pico') or (obj == 'frames')):
                limit = int(getattr(self,obj).shape[0] * percent)
                arr = getattr(self,obj)[:limit]
                setattr(self,obj,arr)
            else:
                # total_frames, steps
                limit = int(getattr(self,obj) * percent)
                setattr(self,obj,limit)

        # self.vline =
        self.truncated = 'yes'
        self.reversal_ind = self.ext_raw[-1]

        # currently, before the ext gets extended.
        self.ext_limit = self.ext_raw.shape[0]

        # self.reversal_time = self.analysis[-1,1]
        # print 'time:'
        # print self.reversal_time

        self.reversal_time = self.force[-1,2]
        print '\ntime:'
        print self.reversal_time
        # sys.exit()


        # self.force[::,0] = self.f_nano
        # self.force[::,1] = self.ext_raw
        # self.force[::,2] = fvtime
        # self.force[::,3] = fvframe

        # self.reversal_frame
        # self.analysis[::,1] = avtime
        # self.force[::,2] = fvtime

    def combine_contacts_and_frames(self,arr_contacts,arr_frames,rev_frame):

        # print self.contacts
        # print self.frames
        # print rev_frame

        # if self.truncated != 'yes':
        # print self.frames
        # print rev_frame
        try:
            frameindex = int(np.where(self.frames==rev_frame)[0])
        except:
            print np.where(self.frames==rev_frame)[0]
            frameindex = self.frames[-1]
        # sys.exit()

        self.frameindex = frameindex

        arr_contacts1 = self.contacts[:frameindex]
        arr_frames1 = self.frames[:frameindex]
        arr_frames2 = arr_frames[1:] + arr_frames1[-1]

        self.reversal_frame = arr_frames1[-1]
        self.contacts = np.concatenate((arr_contacts1,arr_contacts[1:]))
        self.frames = np.concatenate((arr_frames1,arr_frames2))


    def combine_nesw_contacts(self,obj,arr_contacts,arr_frames,rev_frame):
        '''
        obj = direction: north,south,east,west
        '''
        dir_obj = '%scontacts' % obj[0] # n, s, e, w

        # print rev_frame
        # if rev_frame < 0:
        #     sys.exit()
        # if not hasattr(self,'frames'):
        # print obj
        # if self.truncated

        # print "M1_frames:"
        # print self.frames

        # print arr_contacts.shape
        # print arr_frames.shape
        # print "Reversal_frame:",rev_frame


        # print m1_con
        # m1_contacts = getattr(self,dir_obj)[:self.frameindex]


        # for i,d in enumerate(self.dimers):
        #     print m1_contacts[-10:,d]
        #     print arr_contacts[:10,d]
        #     print '--'
        # # for i,d in enumerate(self.dimers):
        # #     ax.plot(icontacts[::,d],color=mycolors[i])

        # # for i,d in e

        # nesw_contacts = np.concatenate((m1_contacts,arr_contacts))
        # print nesw_contacts.shape
        # # print nesw_contacts

        # # sys.exit()
        # setattr(self,dir_obj,nesw_contacts)


        # return

        # previously ..

        if not hasattr(self,'frameindex'):

            frameindex = int(np.where(self.frames==rev_frame)[0])
            self.frameindex = frameindex

            arr_frames1 = self.frames[:frameindex]
            arr_frames2 = arr_frames[1:] + arr_frames1[-1]
            self.reversal_frame = arr_frames1[-1]
            self.frames = np.concatenate((arr_frames1,arr_frames2))


        m1_contacts = getattr(self,dir_obj)[:self.frameindex]


        for i,d in enumerate(self.dimers):
            print m1_contacts[-10:,d]
            print arr_contacts[:10,d]
            print '--'
        # for i,d in enumerate(self.dimers):
        #     ax.plot(icontacts[::,d],color=mycolors[i])

        # for i,d in e

        nesw_contacts = np.concatenate((m1_contacts,arr_contacts))
        print nesw_contacts.shape
        # print nesw_contacts

        # sys.exit()
        setattr(self,dir_obj,nesw_contacts)


    # def absorb(self):
    #     """
    #     Absorb.
    #     """

    def get_extNforce_at_frame(self,frame):
        '''
        Get force at a particular frame.
        '''
        # print self.f_nano
        # print self.ext_raw
        # print self.frames

        # USED
        # print self.f_nano.shape
        # print self.ext_raw.shape
        # print self.frames.shape

        percent = float(frame)/self.frames.shape[0]
        # print percent

        fsize = int(percent * self.f_nano.shape[0])
        esize = int(percent * self.ext_raw.shape[0])

        tempf = self.f_nano[:fsize]
        tempe = self.ext_raw[:esize]

        lastf = tempf[-1]
        laste = tempe[-1]

        return laste,lastf
        # sys.exit()
        # pass



    def combine_force_and_indentation(self,arr_force,arr_indentation,rev_ind):
        pass


    def combine_force(self,arr_force):

        # print self.f_nano.shape
        # print arr_force.shape
        self.f_nano = np.concatenate((self.f_nano,arr_force))
        # print self.f_nano.shape
        # sys.exit()

        # frameindex =

    def combine_ext_raw(self,ext):

        ext = ext + self.ext_raw[-1]
        self.ext_raw = np.concatenate((self.ext_raw,ext))


    def combine_contacts(self,**kwargs):
        """
        Try out this name ..
        """
        # percent = float(self.reversal_frame) / self.total_frames
        # print "percent:",percent

        for k,v in kwargs.iteritems():
            print k


            arr2 = kwargs[k]
            arr1 = getattr(self,k)

            # print arr1.shape
            # print arr2.shape

            arrc = np.concatenate((arr1,arr2))

            # print arrc.shape

            setattr(self,k,arrc)

            # print getattr(self,k).shape
        return
        #     limit = v.shape[0] * percent
        #     arr1 = getattr(self,k)[:limit,::]



        limit = int(getattr(self,obj).shape[0] * percent)
        arr = getattr(self,obj)[:limit,::]



        arr1 = getattr(self,arrname)

        print arr1.shape
        print arr2.shape


        arrc = np.concatenate((arr1,arr2))

        print arrc.shape

        setattr(self,arrname,arrc)



    def emol_topology_based_contact_files(self,dirname):
        if dirname == None:
            dirname = self.dirname
        self.emoltopfilename = "emol_mtcontacts_by_subdomain_top.dat"
        self.emoltop3filename = "emol_mtcontacts_by_subdomain3_top.dat"
        self.emoltop3nfilename = "emol_mtcontacts_by_subdomain3n_top.dat"

        self.emoltopfile = os.path.join(dirname,self.emoltopfilename)
        self.emoltop3file = os.path.join(dirname,self.emoltop3filename)
        self.emoltop3nfile = os.path.join(dirname,self.emoltop3nfilename)

    def emol_topology_contact(self,fp,num_dimers):
        '''
        '''
        data = np.loadtxt(fp)

        print data.shape
        print data.shape[0] / num_dimers


        frames = data.shape[0] / num_dimers
        datax = data.reshape(frames,num_dimers,data.shape[1])

        print 'num_dimers:',num_dimers
        print 'num_frames:',frames
        print datax.shape
        self.emol3top = datax

        return

    def plot_emol3top(self,my_dir,option,dimers=[]):
        '''
        '''
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
        plt.clf()
        fig = plt.figure(0)

        gs = GridSpec(1,1)
        ax1 = plt.subplot(gs[0,:])
        # ax2 = plt.subplot(gs[1,:-1])
        ax = [ax1]

        # fig.set_size_inches(14,6)
        # plt.subplots_adjust(left=0.14,right=0.93,top=0.950,bottom=0.15,wspace=1.0,hspace=0.8)

        # dct_font = {'family':'sans-serif',
        #             'weight':'normal',
        #             'size'  :'24'}
        # matplotlib.rc('font',**dct_font)

        # gs = GridSpec(12,9)
        # ax1 = plt.subplot(gs[1:11,0:5])

        # # SEW
        # ax2 = plt.subplot(gs[9:12,6:8])
        # ax3 = plt.subplot(gs[6:9,7:9])
        # ax4 = plt.subplot(gs[6:9,5:7])
        # # NEW
        # ax5 = plt.subplot(gs[0:3,6:8])
        # ax6 = plt.subplot(gs[3:6,7:9])
        # ax7 = plt.subplot(gs[3:6,5:7])

        # ax = [ax1,ax2,ax3,ax4,ax5,ax6,ax7]

        #  ---------------------------------------------------------  #
        #  Import Data! (2/4)                                         #
        #  ---------------------------------------------------------  #
        result_type = 'emol3top' # sop | sopnucleo | gsop | namd
        plot_type = self.name # fe | tension | rmsd | rdf
        data_name = 'initial'

        #  ---------------------------------------------------------  #
        #  Import Data! (3/4)                                         #
        #  ---------------------------------------------------------  #

        for x in range(self.emol3top.shape[1]):
            print x
            print self.emol3top[::,x,0]
            # plt.plot(self.emol3top[::,x,0])



        # return


        # for i in range(1,7):
        #     # get columns: l-first position.
        #     #              h-final position.
        #     l = (i-1)*4 + 12
        #     h = i*4 + 12
        #     print 'bounds: ',i,l,h-1

        #     # if i != 1:
        #     #     continue

        #     # Description:
        #     # REMEMBER: this h-1
        #     # 0: main
        #     #      4    4:24-27
        #     # NEW 6 5   5:28-31, 6:32-35
        #     # SEW 3 2   2:16-19, 3:20-23
        #     #      1    1:12-15
        #     #
        #     # csub = mt.emol3[::,iv[0],l:h]
        #     csub = self.emol3top[::,iv[0],l:h]
        #     x = np.arange(0,csub.shape[0])
        #     # print x
        #     # print csub.shape
        #     yt = csub[::,0]
        #     y1 = csub[::,1]
        #     y2 = csub[::,1] + csub[::,2]
        #     # y3 = csub[::,1] + csub[::,2] + csub[::,3]

        #     print 'DIMER:',iv[0]
        #     # print yt
        #     # print y1
        #     # print y2
        #     # print y3
        #     # print 'y123-t:'
        #     # print y1[0:5],'red'
        #     # print y2[0:5],'red + green'
        #     # print y3[0:5],'red + green + blue'
        #     print yt[0:5],'total'

        #     # ax[i].fill_between(x,0,y1,where=y1>0,facecolor='r',alpha=0.3,interpolate=True)
        #     # ax[i].fill_between(x,y1,y2,where=y2>y1,facecolor='g',alpha=0.3,interpolate=True)
        #     # ax[i].fill_between(x,y2,y3,where=y3>y2,facecolor='b',alpha=0.3,interpolate=True)
        #     # ax[i].fill_between(x,0,y1,where=y1>0,color='k',facecolor='r',alpha=0.6)
        #     # ax[i].fill_between(x,y1,y2,where=y2>y1,color='k',facecolor='g',alpha=0.6)
        #     # ax[i].fill_between(x,y2,y3,where=y3>y2,color='k',facecolor='b',alpha=0.6)
        #     # ax[i].fill_between(x,0,y1,where=y1>0,color='k',linewidth=0.4,facecolor='r',alpha=0.6)
        #     ax[i].fill_between(x,0,y1,where=y1>0,color='k',linewidth=0.4,facecolor='r',alpha=0.6)
        #     ax[i].fill_between(x,y1,y2,where=y2>y1,color='k',linewidth=0.4,facecolor='g',alpha=0.6)
        #     # ax[i].fill_between(x,y2,y3,where=y3>y2,color='k',linewidth=0.4,facecolor='b',alpha=0.6)
        #     ax[i].fill_between(x,y2,yt,where=yt>y2,color='k',linewidth=0.4,facecolor='b',alpha=0.6)


        # for axe in [ax2,ax3,ax4,ax5,ax6,ax7]:
        #     # axe.axis('off')
        #     axe.set_yticks([])
        #     axe.set_xticks([])
        #     axe.set_xticklabels(())
        #     axe.set_yticklabels(())

        # yticks = [0,100,200,300]
        # ax1.set_yticks(yticks)
        # ax1.set_yticklabels(yticks,fontsize=18)
        # ax1.set_y
        # for axe in ax:
        #     # axe.set_ylim(0,340)
        #     axe.set_linewidth(1.0)
        # return ax


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


        print "Need to write the new save setting."
        print __debug__,__doc__
        print __main__
        print "plot_emoltop3n"
        sys.exit()
        save_fig(my_dir,0,'fig/%s' % result_type,'%s_%s' % (plot_type,data_name),option)

        # mpl_myargs_end

    def plot_forceindentation(self,ax1):
        print 'plotting force indentation'

        x = self.ext_raw[1:]
        y = self.f_nano[1:]

        t = self.ext_limit
        # t = self.reversal_ind

        # print x.shape
        # print y.shape
        # print t
        # sys.exit()
        # ax1.plot(x,y)

        # if ((self.direction == 'forward') and (self.truncated == 'no')):
        #     ax1.plot(x,y,'k-',label='Full Indent')
        # elif ((self.direction == 'forward') and (self.truncated == 'yes')):
        #     ax1.plot(x,y,'r-',label='Partial Indent')
        # else:
        #     ax1.plot(x,y,'g-',label='Retracting')



        if self.truncated == 'yes':

            ax1.plot(x[:t],y[:t],color='k')
            ax1.plot(x[t:],y[t:],color='r')

            ax1.axvline(self.reversal_ind,color='r',linestyle='-',linewidth=1.5)
        else:
            ax1.plot(x,y,label=self.name)


        ax1.set_xlim(-1,31)
        ax1.set_xticks([0,10,20,30])

        # ax1.set_ylim(-.20,.905)
        # ax1.set_ylim(-0.04,0.94)
        # ax1.set_yticks([0,.2,.4,.6,.8])

        ax1.set_ylim(-0.04,0.96)
        ax1.set_yticks([0,0.3,0.6,0.9])

        # ax1.set_xlabel('Indentation Depth X/nm',fontsize=16)
        # ax1.set_ylabel('Indentation Force F/nN',fontsize=16)
        ax1.set_xlabel('Indentation Depth X/nm',fontsize=20)
        # ax1.set_ylabel('Indentation Force F/nN')
        ax1.set_ylabel('Force (nN)',fontsize=20)
        # ax1.title(self.name)

        # legend
        # handles,labels = ax1.get_legend_handles_labels()
        # ax1.legend(handles,labels,prop={'size':12},loc=2)

    def plot_forceindentation_color(self,ax1,color):
        print "hello color plot"

        x = self.ext_raw[1:]
        y = self.f_nano[1:]
        ax1.plot(x,y)

        ax1.set_xlim(-1,31)
        ax1.set_xticks([0,10,20,30])
        ax1.set_ylim(-.20,.905)
        ax1.set_yticks([0,.2,.4,.6,.8])
        ax1.set_ylim(-0.04,0.94)

        ax1.set_xlabel('Indentation Depth X/nm',fontsize=20)
        ax1.set_ylabel('Indentation Force F/nN',fontsize=20)

        # legend
        handles,labels = ax1.get_legend_handles_labels()
        ax1.legend(handles,labels,prop={'size':12},loc=2)

    def plot_forceframe(self,ax1):
        '''
        Class. use -fi (integer)
        '''
        x = np.linspace(self.frames[0],self.frames[-1],len(self.f_nano[1:]))
        y = self.f_nano[1:]

        ax1.plot(x,y,label=self.name)

        # ax1.set_xlim(x[0],x[-1])
        ax1.set_xlim(self.frames[0],self.frames[-1])

        # ax1.set_xticks(size=20)

        # ax1.set_ylim(-.20,.905)
        # ax1.set_yticks([0,.2,.4,.6,.8])
        # ax1.set_yticks([0,.25,.50,.75,1.0])
        ax1.set_yticks([0,0.3,0.6,0.9])
        ax1.set_ylim(-0.04,0.96)
        # ax1.set_xticks([0,200,400,600])
        # ax1.set_xlabel('Indentation Depth X/nm')
        # ax1.set_xlabel('Frame #')
        # ax1.set_ylabel('Indentation Force F/nN',fontsize=20)
        ax1.set_ylabel('Force (nN)',fontsize=20)
        ax1.set_xlabel('Frame #',fontsize=20)
        # ax1.tick_params(axis='both',labelsize=20)

        # legend
        # handles,labels = ax1.get_legend_handles_labels()
        # ax1.legend(handles,labels,prop={'size':14},loc=2)

    def get_maxforceframe(self):
        '''
        Get the frame at which the maximum force is obtained.
        Watch out for ever increasing indentation forces (such
        as when the cantilever runs into the plate.)
        '''
        print "Searching for the maxforceframe."



        # start_pos = self.break_first * 10
        # # critical_frame = int(self.f_nano.shape[0] * 0.1)


        # # use a 1% search. 10% of 10%
        # # frame10p = int(self.f_nano.shape[0] * 0.1) # frame 10%
        # # srange = int(0.4 * frame10p)
        # erange = int(0.012 * self.f_nano.shape[0]) # a 3% span on ~6000 pts. 180
        # print erange

        # for f in range(start_pos+erange,self.f_nano.shape[0]-4*erange,3*erange):
        #     # f = 18 .. 36 .. 5982 (6000-18)
        #     span1 = self.f_nano[f:f+erange]
        #     slope1 = (span1[-1] - span1[0])/span1.shape[0]
        #     span2 = self.f_nano[f+erange:f+2*erange]
        #     slope2 = (span2[-1] - span2[0])/span2.shape[0]
        #     span3 = self.f_nano[f+2*erange:f+3*erange]
        #     slope3 = (span3[-1] - span3[0])/span3.shape[0]
        #     span4 = self.f_nano[f+3*erange:f+4*erange]
        #     slope4 = (span4[-1] - span4[0])/span4.shape[0]

        #     print "frame/slopes: ",f,"  ",
        #     print "%7.5f  %7.5f  %7.5f  %7.5f" % (slope1,slope2,slope3,slope4)

        #     allslopes = [slope1,slope2,slope3,slope4]
        #     minslope = min(allslopes)
        #     minslope_index = allslopes.index(minslope)
        #     # 'big' slopes
        #     slopes = [s for s in allslopes if np.abs(s) > 0.00009] # 0.0001
        #     slopes_pos = [s for s in slopes if s > 0]
        #     slopes_neg = [s for s in slopes if s < 0]

        #     if len(slopes_neg) >= 2:
        #         critical_frame = int((f + minslope_index * erange) * 0.1)
        #         break

        #     # if ((slopes[-2] < 0) and (slopes[-1] < 0)):
        #     # print span1,span2,span3


        # print "critical_frame: ",critical_frame
        # # self.maxforceframes = lst_frames
        # self.maxforceframe = critical_frame
        # self.break_critical = critical_frame

        # sys.exit()
        # return


        def collect_frames_of_interest(initialf):
            # while condition:
            # while(initialf<self.f_nano.shape[0]):
                # print i
                # i = initial_frame
            for f in range(initialf,self.f_nano.shape[0]):

                mid_frame = initialf + srange       # ex. 200 - 260
                mid2_frame = initialf + 2 * srange
                final_frame = initialf + 3 * srange # ex. 260 - 320

                early_avg = np.mean(self.f_nano[initialf:mid_frame])
                mid1_avg = np.mean(self.f_nano[mid_frame:mid2_frame])
                late_avg = np.mean(self.f_nano[mid2_frame:final_frame])

                if ((early_avg > mid1_avg) and (early_avg > late_avg)):
                    break
                initialf += srange

            frames1 = initialf * 0.1
            frames2 = mid_frame * 0.1
            frames3 = final_frame * 0.1

            interest_frame = int(0.5 * (frames1 + frames2))

            # return (initialf*0.1,mid_frame*0.1,final_frame*)
            # return (frames1,frames2,frames3)
            return interest_frame



        # sys.exit()


        # self.f_nano
        print self.f_nano.shape
        print self.break_split_first_crit * 10
        # print "10% frame:",frame10p
        # print "frame_range:",srange

        # use a 1% search. 10% of 10%
        # frame10p = int(self.f_nano.shape[0] * 0.1) # frame 10%
        # srange = int(0.4 * frame10p)
        srange = int(0.04 * self.f_nano.shape[0])
        # erange = int(0.012 * self.f_nano.shape[0]) # a 3% span on ~6000 pts. 180
        # print erange

        lst_tups = []
        lst_tupforces = []
        lst_frames = []

        # call the collect frame of interest function
        frame = self.break_split_first_crit

        while(frame<self.f_nano.shape[0]):
            # lst_tups.append(collect_frames_of_interest(frame))
            # frame = int(lst_tups[-1][2] * 10) + srange
            lst_frames.append(collect_frames_of_interest(frame))
            frame = int(lst_frames[-1] * 10) + srange


        print "Critical Break Candidates:",lst_frames
        # sys.exit()

        # if lst_tups
        if lst_tups:
            for tup in lst_tups:
                # print tup[0],tup[1],tup[2]
                e1,f1 = self.get_extNforce_at_frame(tup[0])
                e2,f2 = self.get_extNforce_at_frame(tup[1])
                e3,f3 = self.get_extNforce_at_frame(tup[2])
                # print f1,f2,f3
                lst_tupforces.append((f1,f2,f3))

        # if lst_tups
        # if lst_tups:
        #     for i in range(len(lst_tups)):
        #         print lst_tups[i][0],lst_tups[i][1],lst_tups[i][2]
        #         print lst_tupforces[i][0],lst_tupforces[i][1],lst_tupforces[i][2]

        # print lst_frames
        self.maxforceframes = lst_frames
        self.maxforceframe = lst_frames[0]
        self.break_critical = lst_frames[0]
        # return lst_frames[0]
        # sys.exit()

    def plot_contacts(self,ax,dimers,shift=0,limit=None,**kwargs):
        '''
        Provide n the index in mt_list for plotting.
        Provide dimers, a list from "get_dimers."
        limit = 1320
        '''
        print 'plotting contacts'
        ax.set_prop_cycle(cycler('color',mycolors))

        # kwargs:
        if "loc" in kwargs:
            loc = kwargs['loc']
        else:
            loc = 2


        x1 = self.frames[1::]
        x1 = x1 + shift
        y1 = self.contacts[1::,::]

        arr_ma = 10
        x1 = moving_average(x1,arr_ma)
        y1 = moving_average_array(y1,arr_ma)

        print dimers
        for d in dimers:
            # print d
            # ax1.plot(self.frames[1::],self.contacts[1::,d])
            try:
                ax.plot(x1,y1[::,d],label=str(d*2))
            except Exception as inst:
                # x1 = x1[x1.shape - y1.shape::]
                # print Exception
                print inst
                xdiff = x1.shape[0] - (x1.shape[0] - y1.shape[0])
                # x1 = x1[xdiff::]
                x1 = x1[:xdiff]
                print x1.shape
                ax.plot(x1,y1[::,d],label=str(d*2))
                # sys.exit()

            # if ((rnd == 16) or (rnd == 17)):
            #     ax1.plot(x1,y1[::,d],label=str(d*2))
            # else:
            #     print x1.shape
            #     print y1.shape
            #     # ax1.plot(x1)
            #     print 'couldn\'t plot dimers.'
            #     sys.exit()

        # ax.set_xlabel("Frame #",fontsize=20)
        # ax.set_ylabel("Qn",fontsize=20)
        # ax.tick_params(axis='both',labelsize=20)
        # ax.set_xlim(x1[0],x1[-1])



        # ax.tick_params(axis='both')
        # ax.set_xlim(x1[0],x1[-1])
        # ax.set_ylim(-0.03,1.03)


        ax.set_xlim(self.frames[0],self.frames[-1])
        ax.set_ylim(0.36,1.03)
        ax.set_yticks([0.40,0.55,0.70,0.85,1.00])

        # if limit != None:
        #     ax1.set_xlim(x1[0],1320)
        #     ax1.set_xticks([0,200,400,600,800,1000,1200])
        # else:
        #     ax1.set_xlim(x1[0],limit)
        # legend
        # 1:
        # handles, labels = ax.get_legend_handles_labels()
        # ax.legend(bbox_to_anchor=(1.02, 1),loc=2,borderaxespad=0.0,fontsize=12)

        # ax.legend(loc=2)
        # handles, labels = ax.get_legend_handles_labels()
        # ax.legend(bbox_to_anchor=(1.02, 1),loc=2,borderaxespad=0.0,fontsize=12)

        ax.set_ylabel(r"$Q_{n}$",fontsize=20)
        ax.set_xlabel("Frame #",fontsize=20)

        if 'loc' in kwargs:
            ax.legend(loc=loc,fontsize=12)

        if hasattr(self,'reversal_frame'):
            print 'reversal_frame:',self.reversal_frame
            ax.axvline(self.reversal_frame,color='r',linestyle='-',linewidth=1.5)



    def plot_vertlines(self,ax,lstlines,**kwargs):
        '''
        '''
        print "plotting vertical lines"
        mycolors = ['black','green','magenta']

        if 'color' in kwargs:
            mycolors = [kwargs['color'] for x in range(len(lstlines))]

        if 'colors' in kwargs:
            mycolors = kwargs['colors']

        # print mycolors
        # sys.exit()

        for a,axp in enumerate(ax):

            axp.set_prop_cycle(cycler('color',mycolors))

            for i,line in enumerate(lstlines):

                # axp.axvline(line,color=mycolors[i],linestyle='-',linewidth=2.0)
                axp.axvline(line,color=mycolors[i],linestyle='--',linewidth=2.0)


    def get_mtpf_dep(self):
        """
        Plot bending angle.
        """
        print "getting mtpf."
        # ax.cla()
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
        # fig.set_size_inches(10.0,8.0)

        # gs = GridSpec(2,4)
        # ax1 = plt.subplot(gs[0,0])
        # ax2 = plt.subplot(gs[0,1])
        # ax3 = plt.subplot(gs[0,2])
        # ax4 = plt.subplot(gs[0,3])
        # ax5 = plt.subplot(gs[1,0])
        # ax6 = plt.subplot(gs[1,1])
        # ax7 = plt.subplot(gs[1,2])
        # ax8 = plt.subplot(gs[1,3])

        # ax = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]
        # ax2 = plt.subplot(gs[1,:-1])
        # ax = [ax1]
        # ax1 = plt.subplot(gs[0,:])
        # ax2 = plt.subplot(gs[1,:])
        # ax = [ax1,ax2]

        # plt.subplots_adjust(left=0.1,right=0.9,top=0.960,bottom=0.10,hspace=0.4,wspace=0.4)
        print self.dirname
        fp = os.path.join(self.dirname,"emol_mtpfbending_angle.dat")
        x = np.loadtxt(fp)
        data = np.reshape(x,(13,x.shape[0]/13,x.shape[1]))
        print x.shape
        print data.shape
        frames = np.linspace(0,self.total_frames,data.shape[1])



        for p in range(data.shape[0]):
            for i in range(data.shape[2]):
                ax[i].set_xlim(frames[0],frames[-1])
                ax[i].set_ylim(-5,185)
                ax[i].plot(frames,data[p,::,i])
        # sys.exit()


    def process_mtpf(self):
        """
        Process mtpf data.
        """
        print "Processing mtpf data."
        print self.mtpf_data.shape

        mtpf = self.mtpf_data
        # data = np.zeros(self.mtpf_data.shape)


        pdata = mtpf[::,::,::2] # 66, 13, 7  # PF angle:
        cdata = mtpf[::,::,1::2] # 66, 13, 7 # Centroid Distance:

        pfang_data = np.zeros(pdata.shape)
        cdist_data = np.zeros(cdata.shape)


        frame_at_centroid_sep = {} # pf dictionary = keys = 0-12
        for pf in range(self.mtpf_data.shape[1]):
            frame_at_centroid_sep[pf] = 9999


        for f in range(self.mtpf_data.shape[0]):
            # print f

            for pf in range(self.mtpf_data.shape[1]):
                # print pf

                # print self.mtpf_data[f,pf,::]
                # print pdata[f,pf,::]
                # print cdata[f,pf,::]
                avg_centroid_dist = np.mean(cdata[f,pf,::])
                stdev_centroid_dist = np.std(cdata[f,pf,::])
                # print avg_centroid_dist,stdev_centroid_dist
                # if avg_centroid_dist > 50.0:
                #     print "Longitudinal Break!"
                if stdev_centroid_dist > 8.0:
                    # print "Longitudinal Break!"
                    # frame_at_centroid_sep.append((f,pf))
                    if frame_at_centroid_sep[pf] > f:
                        frame_at_centroid_sep[pf] = f
                    # break
                # print ''


        # print frame_at_centroid_sep
        # print min(frame_at_centroid_sep)
        pfs_that_break = []
        for k,v in frame_at_centroid_sep.items():
            print k,v
            if v < 9999:
                pfs_that_break.append(k)



        # Assign to the Zero Arrays the data corresponding to the PF's that break,
        # but only up to the frame where the break occurs.
        for f in range(self.mtpf_data.shape[0]):
            # print f
            for pf in range(self.mtpf_data.shape[1]):

                if pf not in pfs_that_break:
                    continue

                pfang_data[f,pf,:frame_at_centroid_sep[pf]] = pdata[f,pf,:frame_at_centroid_sep[pf]]
                cdist_data[f,pf,:frame_at_centroid_sep[pf]] = cdata[f,pf,:frame_at_centroid_sep[pf]]


        print "PF-angle-shape:",pfang_data.shape
        # cumulative, transpose, remove centroids
        # udata = np.cumsum(pfang_data,axis=2)
        # utdata = np.transpose(udata)
        utdata = np.transpose(pfang_data)

        # self.mtpfcentroids = pdata
        # self.mtpfbending = ctdata

        self.mtpfbending = utdata
        self.mtpfcentroids = cdist_data


    def get_mtpf(self):
        """
        Plot bending angle.
        """
        print "getting mtpf."

        fp = os.path.join(self.dirname,"emol_mtpfbending_angle.dat")
        x = np.loadtxt(fp) # 858, 14
        data = np.reshape(x,(x.shape[0]/13,13,x.shape[1])) # 66, 13, 14
        self.mtpf_data = data
        return
        # frames = np.linspace(0,self.total_frames,data.shape[1])


        # cumulative data
        # print data.shape
        # data
        # Frame  |  PF  |  14-PFangle/Centroid-Dist.
        # (51, 13, 14)
        pdata = data[::,::,::2] # 66, 13, 7  # PF angle:
        cdata = data[::,::,1::2] # 66, 13, 7 # Centroid Distance:
        mdata = np.zeros(data.shape)

        if 0:
            for a in range(cdata.shape[0]):
                for b in range(cdata.shape[1]):
                    print 'centroid:',cdata[a,b,::]
                    print 'pfangle:',pdata[a,b,::]
                    for index,c in enumerate(cdata[a,b,::]):
                        if c > 55:
                            i2 = (index - 1) * 2 + 1
                            print index,c,i2
                            # print data[a,b,::]
                            mdata[a,b,0:i2] = data[a,b,0:i2]
                            break
                            # print mdata[a,b,::]

                    # for c in range(data.shape[2]):
                    #     print data[a,b,c]
                    #     if data[a,b,c] >


        # try to truncate the array at the big switch ..
        # if


        # cumulative data (round 2)
        pdata = mdata[::,::,::2] # 66, 13, 7
        cdata = mdata[::,::,1::2] # 66, 13, 7

        # cumulative, transpose, remove centroids
        udata = np.cumsum(pdata,axis=2)
        ctdata = np.transpose(udata)


        self.mtpfcentroids = pdata
        self.mtpfbending = ctdata

        sys.exit()


    def plot_mtpf_global(self,ax):
        '''
        ax = list of ax1,ax2, ..
        '''
        # 7 angles in 12 dimer.
        cmap = matplotlib.cm.get_cmap("jet")
        print self.mtpfbending.shape

        for a in ax:
            a.tick_params(axis='both',labelsize=12)
             # a.set_yticklabels([str(x) for x in np.arange(1,14,2)])
            # a.set_yticks(np.linspace(0,13,2),np.arange(1,14,2))
            # a.set_yticks(np.linspace(0,13,2))
            # a.set_ylabel(np.arange(1,14,2))


        # print self.num_dimers/self.num_pf
        if self.num_dimers/self.num_pf == 8:
            start = 2
            # for a in ax[-3:-1]:
            for a in ax[0:2]:
                a.axis('off')
        else:
            start = 0


        # Y-Ticks:
        ax[0+start].set_yticks(np.linspace(0,12,4))
        ax[0+start].set_yticklabels(np.arange(1,14,4))


        # frames = np.linspace(0,self.total_frames,self.mtpfbending.shape[2])

        for i,a in enumerate(ax):
            # if i == start:
            #     a.set_yticks
            if i > start:
                a.set_yticks([])


        for i,a in enumerate(ax[:-1]):
            pass
            # a.set_xticks()
            # a.set_xticklabels(np.arange(100,self.total_frames,3))


        # Plot:
        for a in range(self.mtpfbending.shape[0]): # use the 7
            #                   13 :: 7
            # print self.mtpfbending[a,::,::]
            # print min(self.mtpfbending[a,0,::])
            # print max(self.mtpfbending[a,0,::])

            im = ax[a+start].imshow(self.mtpfbending[a,::,::],
                                    aspect='auto',cmap=cmap,vmin=-50,vmax=50)

            if a == int(self.mtpfbending.shape[0] * 0.5) + 1:
                plt.colorbar(im,cax=ax[-1],use_gridspec=True)
                # ax[a].colorbar(this_ax,cax=[ax[-1]])


        # max_ax = int(self.mtpfbending.shape[0] * 0.5) + 1
        # cb1 = matplotlib.colorbar.ColorbarBase(ax[-1],cmap=cmap)
        # plt.colorbar(ax=this_ax,cmap=cmap,cax=ax[-1])


        # Colorbar:
        # plt.colorbar(ax8,ticks=[0,1])
        # plt.colorbar(ax[-1],cax=axes)


        # cbar = plt.colorbar(cax=ax[-1])
        # plt.colorbar
        # ax[-1]
        # for i in range(len(ax)):
        #     if i != 0+start:
        #         ax[i+start].set_yticks([])
        # for a in ax:
            # a.set_xlim(-5,100)


    def plot_mtpf_local(self,ax):
        """
        Plot pf bending angle, local.
        """
        cmap = matplotlib.cm.get_cmap("rainbow")
        cr = np.linspace(1,0,self.mtpfbending.shape[1])


        print self.mtpfbending.shape

        for a in ax:
            a.tick_params(axis='both',labelsize=12)
            # a.locator_params(axis='x',nticks=4)
        # # OFF unused plots.
        # if self.num_dimers/self.num_pf == 8:
        #     for a in ax[0:2]:
        #         a.axis('off')

        if self.num_dimers/self.num_pf == 8:
            start = 2
            for a in ax[0:2]:
                a.axis('off')
        else:
            start = 0

        frames = np.linspace(0,self.total_frames,self.mtpfbending.shape[2])


        for i in range(self.mtpfbending.shape[0]):
            # 7
            i2 = i*2 + 1

            for p in range(self.mtpfbending.shape[1]):
                # 13
                # print np.var(self.mtpfbending[i,p,::])
                if np.var(self.mtpfbending[i,p,::]) > 20.0:
                    # print cr
                    # print cr[p]
                    ax[i+start].plot(frames,self.mtpfbending[i,p,::],color=cmap(cr[p]))


        for i,a in enumerate(ax):
            if i >= start:
                a.tick_params(axis='both',labelsize=12)
                a.set_yticks([-60,-30,0,30,60])
                a.set_ylim(-72,72)

                # To specify the number of ticks on both or any single axes
                # a.locator_params(axis='y', nticks=6)


            if i > start:
                a.set_yticks([])
                a.set_xlim(frames[0],frames[-1])
                # a.set_xticks([0,250,500])


        cb1 = matplotlib.colorbar.ColorbarBase(ax[-1],cmap=cmap)



    def remove_early_contact_losses(self,face='n'):
        '''
        Remove the early contact losses.
        '''
        early_frame = 75 # in first 75 frames
        decrease = 0.89 # 11% drop
        icontacts = self.contacts
        if face == "n":
            icontacts = self.ncontacts
        elif face == "e":
            icontacts = self.econtacts
        elif face == "w":
            icontacts = self.wcontacts
        elif face == "s":
            icontacts = self.scontacts

        lst_frames_dimers = []
        for i,d in enumerate(self.dimers):
            # print d
            # print min(icontacts[::,d])
            # if i > 18:
            #     break
            # ax.plot(icontacts[::,d],color=mycolors[i])

            for f in range(icontacts.shape[0]):

                if f == icontacts.shape[0] - 1:
                    lst_frames_dimers.append((f,d))

                if icontacts[f,d] < decrease:
                    lst_frames_dimers.append((f,d))
                    break


        new_dimers = []
        for f in lst_frames_dimers:
            # print f[0],f[1]
            if f[0] > early_frame:
                new_dimers.append(f[1])

        self.dimers = new_dimers

        # print min_f
        # min_f = min(lst_frames_dimers,key=lambda f: f[0])
        # sys.exit()

        # print 'Min_f:',min_f
        # self.plot_vertlines(ax,[min_f])
        # sys.exit()

        # ax.set_xlim(limits)
        # ax.set_ylim(-0.03,1.03)
        # ax.set_xlim(self.frames[0],self.frames[-1])
        # ax.text(70,0.1,face.upper())
        # return min_f


    # def plot_contact_interface(self,ax,face='n',limits=(0,600)):
    def plot_contact_interface(self,ax,**kwargs):
        """
        Plot Contact Interface.
        """
        if "limits" in kwargs:
            limits = kwargs['limits']
        else:
            limits = (0,600)


        for k,v in kwargs.iteritems():

            print k

            if re.search('contacts',k) == None:
                continue

            icontacts = getattr(self,k)
            break


        # else:
        #     print "need a contact array."
        #     return

        # # Choose Face:
        # if face == "n":
        #     icontacts = self.ncontacts
        # elif face == "e":
        #     icontacts = self.econtacts
        # elif face == "w":
        #     icontacts = self.wcontacts
        # elif face == "s":
        #     icontacts = self.scontacts


        print len(mycolors)
        print len(self.dimers)

        ax.set_prop_cycle(cycler('color',mycolors))
        ax.tick_params(axis='both',labelsize=12)
        ax.set_ylim(-0.03,1.03)
        ax.set_xlim(self.frames[0],self.frames[-1])


        ax.set_xlabel("Frame #",fontsize=16)
        ax.set_ylabel(r"$Q_{n}$",fontsize=16)


        # ax.text(70,0.1,face.upper())
        ax.text(70,0.1,k[0].upper())


        for i,d in enumerate(self.dimers):
            ax.plot(icontacts[::,d],color=mycolors[i])


    def manual_override_first_crit_break_frames(self,fp_name):
        """
        Manually Read the Config file again.
        """

        # print fp_name
        # print self.name

        # print dir(self)
        # print self.file
        # print self.filename
        ffile = os.path.join(self.my_dir,fp_name)
        print ffile
        print fp_name
        print self.name

        # pattern = "round_%s*%s" % (self.rnd,self.name)
        # print pattern

        # return

        with open(ffile) as fp:

            for line in fp:

                if line.startswith('#'):
                    continue

                if((re.search(self.name,line) != None) and
                   (re.search('round_%s' % self.rnd,line) != None)):

                    print 'match:'
                    print line
                    numbers = [int(x) for x in line.split('.dat')[-1].split()]
                    print numbers

                    if numbers:
                        self.break_first = numbers[0]
                        self.break_critical = numbers[1]
                    # break

        # print numbers
        # sys.exit()




    # def set_breaking_pattern(self):
    #     """
    #     Set the breaking pattern, a final check.
    #     """
        # if self.

        # if((Lat1 < Lat2) and (Lat1 < Lon)):

        #     if((Lon < Lat2 + 5) and (Lon > Lat2 - 5)):
        #         self.breaking_pattern = "LatLatLonsame"

        #     if(Lat2 < Lon):
        #         self.breaking_pattern = "LatLat"

        #     elif(Lon < Lat2):
        #         self.breaking_pattern = "LatLon"

        # else:
        #     # self.breaking_pattern = "Other"
        #     self.breaking_pattern = "LonFirst"

        # # sys.exit()



    def get_crit_break_events(self):
        """
        Focus on just the first few.
        """
        if not hasattr(self,'break_events'):
            self.break_events = []
        if not hasattr(self,'break_first_dimers'):
            self.break_first_dimers = []

        # # Choose Face:
        # if face == "n":
        #     icontacts = self.ncontacts
        # elif face == "e":
        #     icontacts = self.econtacts
        # elif face == "w":
        #     icontacts = self.wcontacts
        # elif face == "s":
        #     icontacts = self.scontacts



        first_complete_break_dimers_lat = []
        first_complete_break_dimers_lon = []

        for i,d in enumerate(self.dimers):

            frame = get_frame_below_threshold(self.ncontacts[::,d],0.3)
            # if (d,frame) not in first_complete_break_dimers_lon:
            first_complete_break_dimers_lon.append((d,frame))

            frame = get_frame_below_threshold(self.scontacts[::,d],0.3)
            # if (d,frame) not in first_complete_break_dimers_lon:
            first_complete_break_dimers_lon.append((d,frame))

            # if len(first_complete_break_dimers_lon) >= 4:
            #     break

        # for i,d in enumerate(self.dimers):
        #     frame = get_frame_below_threshold(self.wcontacts[::,d],0.3)
        #     if (d,frame) not in first_complete_break_dimers_lat:
        #         first_complete_break_dimers_lat.append((d,frame))
        #     frame = get_frame_below_threshold(self.econtacts[::,d],0.3)
        #     if (d,frame) not in first_complete_break_dimers_lat:
        #         first_complete_break_dimers_lat.append((d,frame))

        #     if len(first_complete_break_dimers_lat) >= 4:
        #         break


        # Dictionary:
        first_complete_break_dimers_lon = sorted(first_complete_break_dimers_lon,
                                                 key=lambda tup: tup[1])[0:3]
        # first_complete_break_dimers_lat = sorted(first_complete_break_dimers_lat,
        #                                          key=lambda tup: tup[1])

        print first_complete_break_dimers_lon
        # sys.exit()
        # print first_complete_break_dimers_lat

        # for i in range(1,len(first_complete_break_dimers_lon)-1):

        #     df1 = first_complete_break_dimers_lon[i-1]
        #     df2 = first_complete_break_dimers_lon[i]

        #     if df2[1] - df1[1] < 10:
        #         self.break_first_dimers.append(df1[0])
        #         self.break_first_dimers.append(df2[0])
        #         break

        # for i in range(1,len(first_complete_break_dimers_lat)-1):

        #     df1 = first_complete_break_dimers_lat[i-1]
        #     df2 = first_complete_break_dimers_lat[i]

        #     if df2[1] - df1[1] < 10:
        #         self.break_first_dimers.append(df1[0])
        #         self.break_first_dimers.append(df2[0])
        #         # self.break_first_dimers_lat = [df1[0],df2[0]]
        #         break


        first_complete_break_results = []

        # for i,con in enumerate([self.ncontacts,self.scontacts,self.wcontacts,self.econtacts]):
        for i,con in enumerate([self.ncontacts,self.scontacts]):
            for b in first_complete_break_dimers_lon:

                d = b[0] # dimer
                frame,qn = get_frame_below_avg_threshold(con[::,d],4,0.01)
                e,f = self.get_extNforce_at_frame(frame)

                # first_complete_break_results.append()
                if((f > 0.2) and (f < 1.0) and (frame < 500)):
                    first_complete_break_results.append((frame,'lon',qn,e,f))



        # Remove Duplicate Break Events. (First)
        first_breaks = sorted(first_complete_break_results,key=lambda t: t[4])
        # first_breaks = sorted(first_complete_break_results)
        # for f in first_breaks:
        #     print f
        # print '--'
        # first_breaks = sorted(list(set(first_breaks)))
        # first_breaks = sorted(first_complete_break_results,key=lambda t: t[4])

        for f in first_breaks:
            print f
        # sys.exit()

        # limit
        # break_critical_frame = int(np.mean([t[0] for t in first_breaks]))

        if((self.rnd == '11') or
           (self.rnd == '16') or
           (self.rnd == '26')):
            break_critical_frame = first_breaks[-1][0] + 50
        else:
            break_critical_frame = first_breaks[-1][0]

        print "critical_frame:",break_critical_frame
        self.break_critical,self.force_critical = self.get_maxforce_uptoframe(break_critical_frame)
        print self.break_critical,self.force_critical
        # print self.break_critical,crit_force

        # self.break_critical = first_breaks[-1][0]
        # self.break_critical = int(break_criticals)

        # sys.exit()

    def get_maxforce_uptoframe(self,frame):
        """
        Get the Maximum force up to the corresponding frame limit.
        """
        # print self.f_nano.shape[0]

        # percent = (float(frame)*10)/self.frames.shape[0]
        percent = (float(frame)*10)/self.f_nano.shape[0]
        # print 'percent:',percent

        fsize = int(percent * self.f_nano.shape[0])
        esize = int(percent * self.ext_raw.shape[0])

        tempf = self.f_nano[:fsize]
        tempe = self.ext_raw[:esize]


        frame = list(tempf).index(max(tempf))
        frame = int(float(frame) / 10.0)


        # print max(tempf)
        return frame,max(tempf)

        # lastf = tempf[-1]
        # laste = tempe[-1]
        # return laste,lastf




    # def get_first_break_events(self,face='n'):
    def get_first_break_events(self):
        """
        Focus on just the first few.
        """
        if not hasattr(self,'break_events'):
            self.break_events = []
        if not hasattr(self,'break_first_dimers'):
            self.break_first_dimers = []

        # # Choose Face:
        # if face == "n":
        #     icontacts = self.ncontacts
        # elif face == "e":
        #     icontacts = self.econtacts
        # elif face == "w":
        #     icontacts = self.wcontacts
        # elif face == "s":
        #     icontacts = self.scontacts



        first_complete_break_dimers_lat = []
        first_complete_break_dimers_lon = []

        for i,d in enumerate(self.dimers):

            frame = get_frame_below_threshold(self.ncontacts[::,d],0.3)
            if (d,frame) not in first_complete_break_dimers_lon:
                first_complete_break_dimers_lon.append((d,frame))
            frame = get_frame_below_threshold(self.scontacts[::,d],0.3)
            if (d,frame) not in first_complete_break_dimers_lon:
                first_complete_break_dimers_lon.append((d,frame))

        for i,d in enumerate(self.dimers):
            frame = get_frame_below_threshold(self.wcontacts[::,d],0.3)
            if (d,frame) not in first_complete_break_dimers_lat:
                first_complete_break_dimers_lat.append((d,frame))
            frame = get_frame_below_threshold(self.econtacts[::,d],0.3)
            if (d,frame) not in first_complete_break_dimers_lat:
                first_complete_break_dimers_lat.append((d,frame))



        # Dictionary:
        dct_conchange = {}
        break_events = []

        first_complete_break_dimers_lon = sorted(first_complete_break_dimers_lon,
                                                 key=lambda tup: tup[1])
        first_complete_break_dimers_lat = sorted(first_complete_break_dimers_lat,
                                                 key=lambda tup: tup[1])


        # print first_complete_break_dimers_lon
        # print first_complete_break_dimers_lat

        for i in range(1,len(first_complete_break_dimers_lon)-1):

            df1 = first_complete_break_dimers_lon[i-1]
            df2 = first_complete_break_dimers_lon[i]

            if df2[1] - df1[1] < 10:
                self.break_first_dimers.append(df1[0])
                self.break_first_dimers.append(df2[0])
                break

        for i in range(1,len(first_complete_break_dimers_lat)-1):

            df1 = first_complete_break_dimers_lat[i-1]
            df2 = first_complete_break_dimers_lat[i]

            if df2[1] - df1[1] < 10:
                self.break_first_dimers.append(df1[0])
                self.break_first_dimers.append(df2[0])
                # self.break_first_dimers_lat = [df1[0],df2[0]]
                break


        first_complete_break_results = []

        for i,con in enumerate([self.ncontacts,self.scontacts,self.wcontacts,self.econtacts]):

            for d in self.break_first_dimers:

                frame,qn = get_frame_below_avg_threshold(con[::,d],5,0.9)
                e,f = self.get_extNforce_at_frame(frame)
                # print d,frame,qn,e,f

                # frame, face, Qn, force, extension, description.
                if i <= 1:
                    first_complete_break_results.append((frame,'lat',qn,e,f))
                else:
                    first_complete_break_results.append((frame,'lon',qn,e,f))


        # Remove Duplicate Break Events. (First)
        first_breaks = sorted(first_complete_break_results)
        # for f in first_breaks:
        #     print f
        first_breaks = sorted(list(set(first_breaks)))

        # print 'removed duplicates.'
        # for f in first_breaks:
        #     print f


        Lat1 = -1
        Lon  = -1
        count = 0

        while((Lat1 == -1) or (Lon == -1)):
            if((first_breaks[count][1] == 'lat') and (Lat1 == -1)):
                Lat1 = first_breaks[count][0]
                self.breaking_pattern = self.breaking_pattern + 'lat'

            if((first_breaks[count][1] == 'lon') and (Lon == -1)):
                Lon = first_breaks[count][0]
                self.breaking_pattern = self.breaking_pattern + 'lon'

            count += 1

            if count >= len(first_breaks):
                break

        self.Lat1 = Lat1
        self.Lon = Lon
        self.break_first = min([Lat1,Lon])
        # print dir(self)
        # self.fir
        # for f in first_breaks:
        #     if f[1] == 'lat':
        #         Lat1 = f[0]



        # if first_breaks[0] == 'lat':
        #     Lat1 = first_breaks[0][0]
        #     for f in first_breaks:
        #         if f[1] != 'lat':
        #             Lon = f[0]
        #             break
        # else:
        #     Lon = first_breaks[0][0]
        #     for f in first_breaks:
        #         if f[1] != 'lon':
        #             Lat1 = f[0]
        #             break

        # for f in first_breaks:
        #     first_breaks[0]

        return

        # # Determine Breaking Pattern:
        # # Get Lat-Lon-Lat; or Lat-Lat-Lon
        Lat1 = sorted(lst_early_lat)[0][0]
        Lat2 = sorted(lst_late_lat)[0][0]
        Lon = sorted(lst_early_lon)[0][0]
        Lon2= sorted(lst_early_lon)[0][1]

        if((Lat1 < Lat2) and (Lat1 < Lon)):

            if((Lon < Lat2 + 5) and (Lon > Lat2 - 5)):
                self.breaking_pattern = "LatLatLonsame"

            if(Lat2 < Lon):
                self.breaking_pattern = "LatLat"

            elif(Lon < Lat2):
                self.breaking_pattern = "LatLon"

        else:
            # self.breaking_pattern = "Other"
            self.breaking_pattern = "LonFirst"

        # sys.exit()


    def get_break_events(self,face='n'):
        """
        Plot Contact Interface.
        # (frame, force, lat/lon/both, Qn (lon if both)
        self.break_events = []
        """
        # criteria = {}
        # criteria['n'] =

        if not hasattr(self,'break_events'):
            self.break_events = []

        # Choose Face:
        if face == "n":
            icontacts = self.ncontacts
        elif face == "e":
            icontacts = self.econtacts
        elif face == "w":
            icontacts = self.wcontacts
        elif face == "s":
            icontacts = self.scontacts



            # if sigFrames:
            #     # break_events.extend(sigFrames)

            #     self.break_events.extend(sigFrames)

            #     if((face == 'n') or (face == 's')):
            #         self.break_events_lon.extend(sigFrames)
            #     else:
            #         self.break_events_lat.extend(sigFrames)



        def find_contact_changes(d,arr):
            """
            Find all significant contact changes.
            Dimer,contact array
            """
            # print d,arr
            # if not arr:



            # frames
            sigI = []
            # restart = 0

            for fr in range(arr.shape[0]):
                # if restart == 0:

                if arr[fr] > 0.90:
                    continue
                else:

                    # print fr
                    try:
                        e,f = self.get_extNforce_at_frame(fr)
                    except IndexError:
                        break


                    # have fr, face, arr[fr] (Qn), f,e
                    if len(sigI) < 1:
                        sigI.append((fr,face,arr[fr],f,e,'early')) # early
                        continue

                    # most recent entry
                    prev_frame = sigI[-1][0] # frame
                    prev_force = sigI[-1][3] # f (force)
                    prev_q     = sigI[-1][2] # previous Qn
                    prev_ind   = sigI[-1][4] # previous Ind.

                    if arr[fr] < 0.2:
                        sigI.append((fr,face,arr[fr],f,e,'late'))
                        break

                    # # if force changed since last entry
                    # if np.abs(prev_force - f) > 0.1:
                    #     sigI.append((fr,face,arr[fr],f,e,'mid'))
                    #     continue

                    # # if frame changed since last entry
                    # if np.abs(prev_frame - fr) > 5:
                    #     sigI.append((fr,face,arr[fr],f,e,'mid')) # late
                    #     continue

                    # # if Qn changed since last entry
                    # if np.abs(prev_q - arr[fr]) > 0.1:
                    #     sigI.append((fr,face,arr[fr],f,e,'mid'))
                    #     continue


                    # if force changed since last entry
                    if ((np.abs(prev_force - f) > 0.1) and
                        (np.abs(prev_frame - fr) > 5) and
                        (np.abs(prev_q - arr[fr]) > 0.1)):
                        sigI.append((fr,face,arr[fr],f,e,'mid'))
                        continue


            # frame, face, Qn, force, extension, description.
            return sigI


                # i1 = arr[fr]
                # i2 = arr[fr+2]
                # i3 = arr[fr+4]
                # i4 = arr[fr+6]
                # diff2 = i2 - i1
                # diff3 = i3 - i1
                # diff4 = i4 - i1
                # # print i1,i2,i3,i4," ",diff2,diff3,diff4
                # print diff2,diff3,diff4

                # negdiffs = [d for d in [diff2,diff3,diff4] if d < 0]

                # try:
                #     diff = max([np.abs(d) for d in negdiffs])
                # except:
                #     diff = 0

                # if diff > 0.1:
                #     print "Got one!"
                #     sigI.append(fr)

            # print "Significant Indices of the contact array."
            # print d,sigI

            # if not sigI:
                # print d,arr
                # self.dimers.remove(d)

            # sys.exit()



        def find_simple_contact_changes(arr,threshold):
            # print arr
            # print arr.shape

            for i in range(arr.shape[0]):

                if arr[i] < threshold:
                    break

            return i


        # Dictionary:
        dct_conchange = {}
        break_events = []

        for i,d in enumerate(self.dimers):
            dct_conchange[(d,face)] = {}
            # print d
            # print min(icontacts[::,d])
            # ax.plot(icontacts[::,d],color=mycolors[i])
            # frame1 = find_contact_changes(icontacts[::,d],0.82) # early
            # frame2 = find_contact_changes(icontacts[::,d],0.2) # late/complete
            # dct_conchange[(d,face)] = sorted([frame1,frame2])
            sigFrames = find_contact_changes(d,icontacts[::,d])
            # print d,sigFrames
            if sigFrames:
                # break_events.extend(sigFrames)

                self.break_events.extend(sigFrames)

                if((face == 'n') or (face == 's')):
                    self.break_events_lon.extend(sigFrames)
                else:
                    self.break_events_lat.extend(sigFrames)


    def process_break_events(self):
        '''
        Process break events.
        '''

        def print_list_of_tuples(tup):

            for t in tup:
                print t[0],t[1],t[2],t[3],t[4],t[5]


        def get_breaktype(ltup,face1,face2,eventtime):

            breaks = sorted([b for b in ltup if (
                ((b[1] == face1) or (b[1] == face2))
                and (b[5] == eventtime))],
                                     key=lambda x: x[0])

            # list of tuples: 0-5: frame, face, force, Qn, Ext, Early/Late
            return breaks


        print "Processing break events."
        # print self.break_events
        # break_lat_early = sorted([b for b in self.break_events if (
        #     ((b[1] == 'e') or (b[1] == 'w'))
        #     and (b[5] == 'early'))],
        #                          key=lambda x: x[0])
        # break_lon_early = sorted([b for b in self.break_events if (
        #     ((b[1] == 'n') or (b[1] == 's'))
        #     and (b[5] == 'early'))],
        #                          key=lambda x: x[0])

        # Breaks:
        lst_early_lat = get_breaktype(self.break_events,'e','w','early')
        lst_early_lon = get_breaktype(self.break_events,'n','s','early')
        lst_late_lat = get_breaktype(self.break_events,'e','w','late')
        lst_late_lon = get_breaktype(self.break_events,'n','s','late')

        # Consider removing duplicates.

        print len(lst_early_lat)
        print_list_of_tuples(lst_early_lat)

        print len(lst_early_lon)
        print_list_of_tuples(lst_early_lon)

        print len(lst_late_lat)
        print_list_of_tuples(lst_late_lat)

        print len(lst_late_lon)
        print_list_of_tuples(lst_late_lon)


        # Histograms:
        # cdf = myCDF(data)
        # # cdf.print_class()
        # # cdf.determine_bins(lower_limit=0.3,upper_limit=0.6,nbins=3) # set
        # # cdf.determine_bins_limits(lower_limit=0.3,upper_limit=0.6,nbins=)
        # cdf.determine_bins_limits(lower_limit=lower_limit,
        #                           upper_limit=upper_limit,
        #                           nbins=nbins) # set

        # # print cdf.bins
        # # print alpha
        # # sys.exit()

        # # cdf.get_hist(bins=cdbins)
        # cdf.get_hist()
        # cdf.print_values()




        # print "all_lat:"
        # print_list_of_tuples(self.break_events_lat)
        # print "all_lon:"
        # print_list_of_tuples(self.break_events_lon)


        # Sorted by force.
        force_early_lat = sorted(lst_early_lat, key=lambda tup: tup[3])
        force_early_lon = sorted(lst_early_lon, key=lambda tup: tup[3])
        force_late_lat = sorted(lst_late_lat, key=lambda tup: tup[3])
        force_late_lon = sorted(lst_late_lon, key=lambda tup: tup[3])

        critforces = force_early_lat[-5:] + \
                     force_early_lon[-5:] + \
                     force_late_lat[-5:] + \
                     force_late_lon[-5:]

        critforce_targets = sorted([t for t in critforces if t[2] < 0.4])
        nc = int(len(critforce_targets) * 0.4)

        if len(critforce_targets) > 10:
            critforce_targets = critforce_targets[3:-3]
        elif len(critforce_targets) > 8:
            critforce_targets = critforce_targets[2:-2]
        else:
            critforce_targets = critforce_targets[1:-1]

        self.break_critical = np.mean([t[0] for t in critforce_targets])
        print 'Critical_break:',self.break_critical

        sys.exit()

        # for c in critforce_targets:
        #     print c

        # for c in range(nc,len(critforce_targets)):
        #     print critforce_targets[c]



        # print critforce_early_lat[-5:]
        # print critforce_early_lon[-5:]
        # print


        # sys.exit()

        # top_crit_targets = []
        # top_crit_targets.extend(critforce_early_lat[-5:])
        # top_crit_targets.extend(critforce_early_lon[0:5])
        # top_crit_targets.extend(critforce_late_lat[-4])
        # top_crit_targets.extend(critforce_late_lon[-4])

        # top_crit_targets = sorted(top_crit_targets)
        # print top_crit_targets
        # # print_list_of_tuples(top_crit_targets)
        # sys.exit()


        # Need:
        # Both the first frame force. - All frames near that force level??
        # Determine Lat,Lon,Lat etc.
        # Write it into Lat,Lon.
        # early_lat_frames = np.array(sorted([t[0] for t in lst_lat_early]))
        # print early_lat_frames.shape
        # print early_lat_frames
        # early_lat = [t[0] for t in lst_lat_early if(float(t[0])/float(lst_lat_early[0][0]) > 0.98)]
        # print early_lat


        # # Determine Breaking Pattern:
        # # Get Lat-Lon-Lat; or Lat-Lat-Lon
        Lat1 = sorted(lst_early_lat)[0][0]
        Lat2 = sorted(lst_late_lat)[0][0]
        Lon = sorted(lst_early_lon)[0][0]
        Lon2= sorted(lst_early_lon)[0][1]

        if((Lat1 < Lat2) and (Lat1 < Lon)):

            if((Lon < Lat2 + 5) and (Lon > Lat2 - 5)):
                self.breaking_pattern = "LatLatLonsame"

            if(Lat2 < Lon):
                self.breaking_pattern = "LatLat"

            elif(Lon < Lat2):
                self.breaking_pattern = "LatLon"

        else:
            # self.breaking_pattern = "Other"
            self.breaking_pattern = "LonFirst"

        # print "Lat1,Lat2,Lon:",Lat1,Lat2,Lon
        # Lat1 197
        # Lon  186
        # Lat2 250
        # Lon2 304
        breakfirst_candidates = sorted([Lat1,Lat2,Lon,Lon2])

        self.break_first = sorted([Lat1,Lat2,Lon,Lon2])[1]
        self.break_split_first_crit = max([Lat1,Lat2,Lon])

        # print break_lat_early
        # for t in break_lat_early:
            # print t[0],t[1],t[2],t[3],t[4],t[5]

        # early_lat_frames = [f[0] for f in break_lat_early if f[]]
        # sys.exit()



    def determine_early_late_contact_changes(self):
        """
        Determine Early and Late Lateral and Longitudinal contact changes.
        Early = < 82% remains
        Late = < 20% remains
        "The Breaking Pattern:
           Lat-Lon-Lat
           or
           Lat-Lat-Lon
        """

        def find_repeated_frames(lst):

            f1 = lst[0]

            # for i in range(5,2,-1):
            #     print i
            #     avg = np.mean(lst[0:i])
            #     if f1 / avg > 0.98:
            #         break

            for i in range(len(lst)):

                if float(f1) / lst[i] < 0.9:
                    break

            late_frame = lst[i]
            return f1,late_frame
            # for i,f in enumerate(lst):
            #     print i,f


        lst_early_lat = []
        lst_early_lon = []

        lst_late_lat = []
        lst_late_lon = []

        for k,v in self.dct_contact_events.items():
            print k,v

            if((k[1] == 'e') or (k[1] == 'w')):
                lst_early_lat.append(v[0])

            if((k[1] == 'e') or (k[1] == 'w')):
                lst_late_lat.append(v[1])

            if((k[1] == 'n') or (k[1] == 's')):
                lst_early_lon.append(v[0])

            if((k[1] == 'n') or (k[1] == 's')):
                lst_late_lon.append(v[1])


        # print "\nSorted Early lat/lon:"
        # print sorted(lst_early_lat)
        # print sorted(lst_early_lon)

        # print "\nSorted Late/Complete lat/lon:"
        # print sorted(lst_late_lat)
        # print sorted(lst_late_lon)


        # el1, ll1 = find_repeated_frames(sorted(lst_early_lat))
        # el2, ll2 = find_repeated_frames(sorted(lst_late_lat))
        # eL1, lL1 = find_repeated_frames(sorted(lst_early_lon))
        # eL2, lL2 = find_repeated_frames(sorted(lst_late_lon))

        # print "\nResults. early lat 1,2;  late lat 1,2;  early Lon 1,2;  late Lon 1,2"
        # print el1,el2
        # print ll1,ll2

        # print eL1,eL2
        # print lL1,lL2

        # Determine Breaking Pattern:
        # Get Lat-Lon-Lat; or Lat-Lat-Lon
        Lat1 = sorted(lst_early_lat)[0]
        Lat2 = sorted(lst_late_lat)[0]
        Lon = sorted(lst_early_lon)[0]

        if((Lat1 < Lat2) and (Lat1 < Lon)):

            if((Lon < Lat2 + 5) and (Lon > Lat2 - 5)):
                self.breaking_pattern = "LatLatLonsame"

            if(Lat2 < Lon):
                self.breaking_pattern = "LatLat"

            elif(Lon < Lat2):
                self.breaking_pattern = "LatLon"

        else:
            # self.breaking_pattern = "Other"
            self.breaking_pattern = "LonFirst"

        # print "Lat1,Lat2,Lon:",Lat1,Lat2,Lon

        self.break_first = sorted([Lat1,Lat2,Lon])[1]
        self.break_split_first_crit = max([Lat1,Lat2,Lon])


        # sys.exit()
        # self.plot_vertlines()



    def plot_contact_interface2(self,ax,face='n',limits=(0,600)):
        """
        """

        def search_contact_array(start_f):
            # searching contact array
            lst_frames_dimers = []
            for i,d in enumerate(self.dimers):
                # print d
                # print min(icontacts[::,d])
                # ax.plot(icontacts[::,d],color=mycolors[i])
                if i >= 18:
                    break

                # print icontacts.shape[0]
                start_f = lst_frames_dimers[-1][0]

                for f in range(start_f,icontacts.shape[0]): # 586 frames..
                    print 'f:',f,'of',icontacts.shape[0]
                    # print icontacts

                    # to get last frame, only if necessary.
                    if f == icontacts.shape[0] - 1:
                        lst_frames_dimers.append((f,d))
                        break

                    slope1 = icontacts[f-15,d] - icontacts[f,d]
                    slope2 = icontacts[f-10,d] - icontacts[f,d]
                    slope3 = icontacts[f-5,d] - icontacts[f,d]
                    slope = max([slope1,slope2,slope3])

                    if len(lst_frames_dimers) < 1:
                        if np.abs(slope) > slope_criterion:
                            # print slope
                            lst_frames_dimers.append((f,d))
                            break
                    else:
                        if np.abs(slope) > slope_final:
                            lst_frames_dimers.append((f,d))
                            break


                    # if icontacts[f,d] < decrease:
                    #     lst_frames_dimers.append((f,d))
                    #     break


        #  ---------------------------------------------------------  #
        #  Import Data! (2/4)                                         #
        #  ---------------------------------------------------------  #
        print "hello isolate Contacts!  ",face
        # print ax
        print self.contacts.shape # only goes dimers.
        print self.dimers # need to be doubled.

        ax.set_prop_cycle(cycler('color',mycolors))
        ax.tick_params(axis='both',labelsize=12)
        # ax.legend(loc=3,fontsize=6)

        if face == "n":
            icontacts = self.ncontacts
        elif face == "e":
            icontacts = self.econtacts
        elif face == "w":
            icontacts = self.wcontacts
        elif face == "s":
            icontacts = self.scontacts

        if((face == "n") or (face == "s")):
            # n,s: north, south
            decrease = 0.20
            slope_criterion = 0.3
        else:
            # w,e: west, east
            decrease = 0.85
            slope_criterion = 0.1

        slope_final = 0.5

        # print icontacts.shape
        # for i in range(icontacts.shape[1]):
        # sys.exit()

        min_f = self.frames[-1] # the last frame.
        start_f = 95 # start beyond frame 95

        for i,d in enumerate(self.dimers):
            # print d
            # print min(icontacts[::,d])
            ax.plot(icontacts[::,d],color=mycolors[i])


        while(found_frame < self.frames[-1]):

            found_frame = search_contact_array(0)


        sys.exit()




        for f in lst_frames_dimers:
            print f[0],f[1]
            if f[0] > start_f:
                if f[0] < min_f:
                    min_f = f[0]



        print min_f
        min_f = min(lst_dimers_frames,key=lambda f: f[0])
        sys.exit()

        # print 'Min_f:',min_f
        # self.plot_vertlines(ax,[min_f])
        # sys.exit()

        # ax.set_xlim(limits)
        ax.set_ylim(-0.03,1.03)
        ax.set_xlim(self.frames[0],self.frames[-1])
        ax.text(70,0.1,face.upper())

        # print "Early frame: ",min_f
        # sys.exit()
        return min_f


    def get_cendist(self):
        """
        Get the centroid distance file.
        File: emol_mtpfdist_centroid.dat
        """

        # print dir(self)
        # print self.dirname
        # print self.num_pf
        # print self.num_dimers

        dimer_length = self.num_dimers / self.num_pf
        # print dimer_length


        fp_cendist = os.path.join(self.dirname,"emol_mtpfdist_centroid.dat")
        data_cendist = np.loadtxt(fp_cendist)
        # print data_cendist.shape

        arrsize_1 = data_cendist.shape[0] / self.num_pf
        # print arrsize_1
        frames = arrsize_1 / (dimer_length-1)

        # print (frames,dimer_length-1)
        # print frames * (dimer_length-1) * self.num_pf

        data_angles = np.reshape(data_cendist,(frames,self.num_pf,
                                               dimer_length-1,data_cendist.shape[1]))

        self.data_cendist = data_angles
        # print data_angles.shape
        # for pf in range(self.num_pf):
        #     print pf
        #     print data_angles[0,pf,::,::]
        # sys.exit()

    def plot_cendist(self,ax):
        """
        Plot the data_cendist
        """
        print self.data_cendist.shape
        cdata = self.data_cendist


        for f in range(cdata.shape[0]):
            print f
            print cdata[f,0,::,::]

            # break

            # ax.plot()



        sys.exit()


    def get_beta_angle(self):
        """
        Get beta angle.
        File:
        """

        # print dir(self)
        # print self.dirname
        # print self.num_pf
        # print self.num_dimers

        dimer_length = self.num_dimers / self.num_pf
        # print dimer_length


        fp_beta = os.path.join(self.dirname,"emol_mtpf_beta_angle.dat")
        data_beta = np.loadtxt(fp_beta)
        # print "Beta Angles: ",data_beta.shape

        frames = data_beta.shape[0] / self.num_pf
        # print frames
        # frames = arrsize_1 / (dimer_length-1)

        # print (frames,dimer_length-1)
        # print frames * (dimer_length-1) * self.num_pf

        # data = np.reshape(data_beta,(frames,self.num_pf,
                                     # dimer_length-1,data_beta.shape[1]))

        data = np.reshape(data_beta,(frames,data_beta.shape[0]/frames,data_beta.shape[1]))
        # print data.shape
        # self.data_cendist = data_angles
        # print data_angles.shape
        # for pf in range(self.num_pf):
        #     print pf
        #     print data_angles[0,pf,::,::]
        # sys.exit()


        break_points = {}

        for i in range(self.num_pf):
            break_points[i] = 9999


        for f in range(data.shape[0]):
            # print data[f]

            for pf in range(data.shape[1]):

                # print data[f,pf,::]
                pfline = data[f,pf,::]
                pfcdist = data[f,pf,::2]
                pfang = data[f,pf,1::2]
                # print pfcdist
                # print pfang

                if max(pfcdist) > 50.0:

                    if f < break_points[pf]:
                        break_points[pf] = f


        for k,v in break_points.items():
            print k,v

            # first_half = data[:v,k,::]
            second_half = data[v+1:,k,::]
            second_half.fill(0)
            data[v+1:,k,::] = second_half




        for f in range(data.shape[0]):
            for pf in range(data.shape[1]):

                print data[f,pf,::]
                pfline = data[f,pf,::]
                pfcdist = data[f,pf,::2]
                pfang = data[f,pf,1::2]
                print pfcdist
                print pfang
                print '-------'



            print '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||'


        first_pf_to_break = -1

        frames_break_pf = break_points.values()
        first_frame_break = min(frames_break_pf)


        for k,v in break_points.items():
            print k,v

            if v == first_frame_break:
                self.first_pf_to_break = k
                break


        print self.first_pf_to_break
        self.frame_of_first_pf_to_break = break_points[self.first_pf_to_break]

        self.data_beta_angle = data

        # sys.exit()

    def plot_beta_angle(self,axes):
        """
        Plot beta angles.
        """
        print "Hello."



        pfdata = self.data_beta_angle[::,self.first_pf_to_break,:self.frame_of_first_pf_to_break]

        cen_all = pfdata[::,::2]
        ang_all = pfdata[::,1::2]


        print pfdata.shape

        for f in range(pfdata.shape[0]):

            # print pfdata[f,::]

            cen = pfdata[f,::2]
            ang = pfdata[f,1::2]

            print cen
            print ang



        # for ax in axes:


    def get_point4ab(self):
        """
        Get Point4ab.
        File:
        """

        # print dir(self)
        # print self.dirname
        # print self.num_pf
        # print self.num_dimers

        dimer_length = self.num_dimers / self.num_pf
        # print dimer_length


        fp_point4ab = os.path.join(self.dirname,"emol_mtpf_point4AB.dat")
        data_point4ab = np.loadtxt(fp_point4ab)
        # print "Beta Angles: ",data_point4ab.shape

        frames = data_point4ab.shape[0] / self.num_pf
        print "Frames: ",frames
        # frames = arrsize_1 / (dimer_length-1)
        # print (frames,dimer_length-1)
        # print frames * (dimer_length-1) * self.num_pf

        data = np.reshape(data_point4ab,(frames,data_point4ab.shape[0]/frames,data_point4ab.shape[1]))
        print data.shape
        # self.data_cendist = data_angles
        # print data_angles.shape
        # for pf in range(self.num_pf):
        #     print pf
        #     print data_angles[0,pf,::,::]
        # sys.exit()

        data_cdist = data[::,::,::2]
        data_angle = data[::,::,1::2]

        break_points = {}

        for i in range(self.num_pf):
            break_points[i] = 9999


        for f in range(data.shape[0]):

            for pf in range(data.shape[1]):

                # print data[f,pf,::]
                # print data_cdist[f,pf,::]
                # print data_angle[f,pf,::]

                if max(data_cdist[f,pf,::]) > 72.0:

                    if f < break_points[pf]:
                        break_points[pf] = f + 1


        # Zero out the beyond the break points.
        for k,v in break_points.items():
            print k,v

            # first_half = data[:v,k,::]
            second_half = data[v+1:,k,::]
            second_half.fill(0)
            data[v+1:,k,::] = second_half


        data_angle = data[::,::,1::2]

        self.data_point4ab = data_angle
        self.point4ab_breakframes = break_points

        # sys.exit()
        return

    def plot_point4ab(self,axes):
        """
        Plot point4ab.
        """
        data = self.data_point4ab
        print data.shape

        # print "Hello."
        cmap = matplotlib.cm.get_cmap("jet")
        # "jet": blue is 0,1,2
        #      : maroon, red is 12, 11, 10 ..

        # color = {0:'purple',1:'r',2:'m',
        #          3:'hotpink',4:'',5:'m',
        #          6:''}
        # mycolors = ['k', 'r', 'g', 'b','c','m','lime',
        #     'darkorange','sandybrown','hotpink',
        #     'mediumseagreen','crimson','slategray',
        #     'orange','orchid','darkgrey','indianred',
        #     'tan','cadetblue']

        cr = np.linspace(0,1,data.shape[1])

        # ax[i+start].plot(frames,self.mtpfbending[i,p,::],color=cmap(cr[p]))


        x = np.linspace(0,data.shape[0]*10,data.shape[0])

        for i in range(data.shape[2]):
            print i

            for p in range(data.shape[1]):
                print p

                if self.point4ab_breakframes[p] == 9999:
                    continue

                # axes[i].plot(x,data[::,p,i],color=mycolors[p])
                # print cmap(cr[p])
                # sys.exit()
                # if p > 5:
                    # continue
                axes[i].plot(x,data[::,p,i],color=cmap(cr[p]))

        # axes[-1].colorbar
        cb1 = matplotlib.colorbar.ColorbarBase(axes[-1],cmap=cmap)


        for ax in axes[:-1]:
            ax.set_ylim((-1,67))

    def get_entire_PF_ang(self):
        """
        """
        # print dir(self)
        # print self.dirname
        # print self.num_pf
        # print self.num_dimers

        dimer_length = self.num_dimers / self.num_pf

        fp_pfang = os.path.join(self.dirname,"emol_mtpf_entire_PFang.dat")

        data_pfang = np.loadtxt(fp_pfang)
        # print "Beta Angles: ",data_pfang.shape

        frames = data_pfang.shape[0] / self.num_pf
        print "Frames: ",frames
        # frames = arrsize_1 / (dimer_length-1)
        # print (frames,dimer_length-1)
        # print frames * (dimer_length-1) * self.num_pf

        # data = np.reshape(data_pfang,(data_pfang.shape[0]/frames,frames,data_pfang.shape[1]))
        data = np.reshape(data_pfang,(frames,data_pfang.shape[0]/frames,data_pfang.shape[1]))

        self.data_entire_pfang = data
        print data.shape

        # for i in range(data.shape[0]):
            # print data[i,::,::]

        # print data[::,0,0]
        # sys.exit()

    def get_angle_at_frame(self,frame):
        """
        Get the angle by the frame provided.
        Determine the angle array for histogramming.
        """
        print "Getting angle at %d." % frame

        data = self.data_entire_pfang

        percent = float(frame)/self.frames.shape[0]
        percent_extra = percent + 0.1
        # print percent

        asize = int(percent * data.shape[0])
        asize_extra = int(percent_extra * data.shape[0])
        # fsize = int(percent * self.f_nano.shape[0])
        # esize = int(percent * self.ext_raw.shape[0])
        # tempf = self.f_nano[:fsize]
        # tempe = self.ext_raw[:esize]
        # lastf = tempf[-1]
        # laste = tempe[-1]

        tempa = data[:asize,::,::]
        lastangles = tempa[-1,::,::]

        # print lastangles
        # print lastangles.shape
        angle = max(lastangles[::,5])

        index = list(lastangles[::,5]).index(angle)

        self.max_angle_array = data[:asize,index,5]
        # self.max_angle_array = data[:asize_extra,index,5]
        # sys.exit()

        return angle

    def write_max_angle_upto_frame(self,frame):
        """
        Get the angle by the frame provided.
        """

        print self.dirname

        fname = 'max_angle_criticalbreak_array.dat'
        full_path = os.path.join(self.dirname,fname)

        np.savetxt(full_path,self.max_angle_array,fmt='%7.3f')

        # with open(full_path,'w+') as fp:
            # fp.write(self.max_angle_array)
            # np.savetxt()



    def plot_entire_PF_ang(self,axes):
        """
        Plot the entire PF.
        """
        # (13, 4, 121)

        # mycolors = ['k', 'r', 'g', 'b','c','m','lime',
        #             'darkorange','sandybrown','hotpink',
        #             'mediumseagreen','crimson','slategray',
        #             'orange','orchid','darkgrey','indianred',
        #             'tan','cadetblue']
        mycolors = ['firebrick','r','darkorange','khaki','springgreen',
                    'lime','limegreen',
                    'green','cyan','dodgerblue','cadetblue','blue','navy']


        data = self.data_entire_pfang
        x = np.linspace(0,data.shape[0]*5,data.shape[0])

        for p in range(data.shape[1]):
            axes.plot(x,data[::,p,5],color=mycolors[p],label=str(p+1))



        # legend
        handles,labels = axes.get_legend_handles_labels()
        axes.legend(handles,labels,prop={'size':12},loc=2)


        axes.set_ylim((-2,112))
        axes.set_ylabel(r"Angle$^\circ$",fontsize=20)
        axes.set_xlabel("Frame #",fontsize=20)

        # for p in range(data.shape[0]):
            # print np.std(data[p,::,3])
            # print data[p,::,3]
            # if np.var(data[p,::,3]) > 50:
            #     axes.plot(x,data[p,::,3])
            #     axes.plot(x,data[p,::,2])
        # for p in range(data)
        # sys.exit()

    def get_work(self):
        """
        Get the Indentation Work.
        """

        def dx(x,y):
            # print x - y
            return y - x

        print self.ext_limit
        print self.f_nano.size
        print self.ext_raw.shape
        t = self.ext_limit
        dist = self.ext_raw[t]

        print dist
        dist_in = self.ext_raw[:t]
        dist_out = self.ext_raw[t:]

        print "in:",np.abs(dist_in[-1] - dist_in[0])
        print "out:",np.abs(dist_out[-1] - dist_out[0])
        print self.ext_raw


        # dx_in = np.array([dx(dist_in[i-1] - dist_in[i])  for i in range(1,dist_in.shape+1)])
        dx_in = np.array([dx(dist_in[i-1],dist_in[i]) for i in range(1,dist_in.shape[0])])
        # dx_in = np.array([float(dist_in[i-1] - dist_in[i]) for i in range(1,dist_in.shape[0]+1)])


        dx_out = np.array([dx(dist_out[i],dist_out[i-1]) for i in range(1,dist_out.shape[0])])

        # print dx_in
        # print dx_in.shape
        # print dx_out
        # print dx_out.shape

        dx_tot = np.concatenate([dx_in,dx_out])


        # now use the self.f_nano[1:] * dx_in  as integral(f*dx)
        work_indentation = np.cumsum(self.f_nano[1:t] * dx_in)
        # print work_indentation[-1]

        # just the cumulative force
        # work_indentation = np.cumsum(self.f_nano[:t])
        # print work_indentation[-1]
        # sys.exit()

        # work_total = np.cumsum(self.f_nano)
        # print self.f_nano.shape
        # print dx_tot.shape

        work_total = np.cumsum(self.f_nano[2:] * dx_tot)

        convf = (1/4.184) * 6.02 * 100
        self.work_indentation = work_indentation[-1] * convf
        self.work_total = work_total[-1] * convf
        self.work_retraction = self.work_total - self.work_indentation


        # print work,work[-1]
        # sys.exit()
        # return self.work

    def get_energy_beginend(self):
        """
        Get the work, at the beginning and the end of the log file.
        Thermodynamics.
        Getting the Enthalpy, H.
        Will compute the Entropy.
        del G = del H - T del S
        """
        # print self.my_dir
        # print self.dirname  # ***
        # print self.indentation_dir
        # print self.outputdir
        # print dir(self)
        # print "frame:",self.frameindex
        # print self.frameindex * 1000000
        stepmax = self.frameindex * 1000000
        # print self.frame_of_first_pf_to_break

        lst_logfile = glob.glob(os.path.join(self.dirname,'mt*.log'))
        try:
            logfile = lst_logfile[0]
        except:
            lst_logfile = glob.glob(os.path.join(self.dirname,'MT*.log'))
            logfile = lst_logfile[0]
        print logfile

        fo = open(logfile,"r+")
        filelines = fo.readlines()
        num_lines = len(filelines)
        # filelines = logfile.readlines()

        for i,line in enumerate(filelines):

            if line.startswith("Writing output at step 0"):
                print "Current line:",i
                i = i + 2
                # print line
                line = filelines[i]
                potentE0 = float(line.split()[2])
                break

        # print "Next line-1, line, and next 2 lines:"
        # print filelines[i-1]
        # print filelines[i]
        # print filelines[i+1]
        # print filelines[i+2]

        # print "Next 10 lines:"

        for j,k in enumerate(range(i,num_lines)):

            line = filelines[k]

            if line.startswith("Writing output at step 100000"):
                print "Current line:",k
                k = k + 2

                line = filelines[k]
                potentE1 = float(line.split()[2])
                break

            # print j,k,filelines[k]
            # if j > 10:
            #     break


        count = 0


        for m,n in enumerate(range(k,num_lines)):

            line = filelines[n]

            if line.startswith("Writing output"):


                step = int(re.search(r'\d+',line).group())
                # print line,step
                # print line.index("step ")
                # break
                if step > stepmax:
                    count += 1

                    print "Current line:",n
                    line = filelines[n+2]
                    potentE2 = float(line.split()[2])
                    break

        # LAST

        if count == 0:
            for m,n in enumerate(range(num_lines-1,num_lines-100,-1)):

                print "n:",n
                print m,n,num_lines
                line = filelines[n]

                if line.startswith("Writing output"):
                    count += 1

                    if count > 1:

                        print "Current line:",n
                        n = n + 2

                        line = filelines[n]
                        potentE2 = float(line.split()[2])
                        break


        print "Potential Energies:"
        print potentE0,potentE1,potentE2

        self.potentE0 = potentE0
        self.potentE1 = potentE1
        self.potentE2 = potentE2
        # sys.exit()

            # print fp[i]
            # print fp[i+1]


        # with open(logfile,"r+") as fp:
        #     for i,line in enumerate(fp):
        #         if line.startswith("Writing output at step 0"):
        #             print "Current line:"
        #             print line
        #             # break
        #         print fp[i-1]
        #         print fp[i]
        #         print fp[i+1]




    def get_min_lateral_contacts(self):
        """
        Dimers,

        need to check frame limit
        """


        # print dir(self)
        # print "Reversal: index, time, frame."
        # print self.reversal_ind
        # print self.reversal_time
        # print self.reversal_frame
        # print self.ext_limit
        # print self.wcontacts_raw.shape

        # print "East,West"
        # print self.econtacts_raw
        # print self.wcontacts_raw

        lst_con = []
        # curr_diff = 0
        lst_econtactslost = []
        # lst_eqn = []
        lst_wcontactslost = []

        bool_recovers = True


        for d in self.dimers:
            # lst_con.append(self.econtacts_raw[::,d])
            # min_d = min(self.econtacts_raw[::,d])
            # min_d = self.econtacts_raw[0,d]
            # max_d = max(self.econtacts_raw[::,d])
            # last_d = self.econtacts_raw[-1,d] # truncated already!

            # print self.econtacts_raw.shape
            # print self.frameindex


            # does it recover..
            c1 = self.econtacts_raw[0,d]
            c2 = min(self.econtacts_raw[:self.frameindex,d])
            c3 = self.econtacts_raw[-1,d]
            diff = c1 - c2
            initial_final_ratio = float(c3) / c1

            print c1,float(c2)/c1,c2,"recover:",c3

            if initial_final_ratio < 0.9:
                bool_recovers = False




            if float(c2)/c1 < 0.70:
                lst_econtactslost.append(diff)
            else:
                lst_econtactslost.append(0.0)

            # diff = max_d - min_d
            # diff = last_d - min_d
            # lst_con.append(diff)
            # print max_d,min_d,diff
            # if diff > curr_diff:
                # curr_diff = diff
                # lst_con.append(diff)

            # min_d = self.wcontacts_raw[0,d]
            # last_d = self.wcontacts_raw[-1,d] # truncated already!
            # diff = last_d - min_d
            # lst_con.append((c1,c2,c3,diff))
            # lst_econtactslost.append(diff)


        for d in self.dimers:
            c1 = self.wcontacts_raw[0,d]
            c2 = min(self.wcontacts_raw[:self.frameindex,d])
            c3 = self.wcontacts_raw[-1,d]
            diff = c1 - c2
            initial_final_ratio = float(c3) / c1

            print c1,float(c2)/c1,c2,"recover:",c3

            if initial_final_ratio < 0.9:
                bool_recovers = False


            if float(c2)/c1 < 0.70:
                lst_wcontactslost.append(diff)
            else:
                lst_wcontactslost.append(0.0)

            # lst_wcontactslost.append(diff)


        # print lst_con
        print 'east'
        print lst_econtactslost
        print 'west'
        print lst_wcontactslost
        print "The lattice recovers? %s" % bool_recovers

        mine = np.sum(np.array(lst_econtactslost))
        minw = np.sum(np.array(lst_wcontactslost))

        print "work_in:",self.work_indentation
        print "contacts:(e,w):",mine,minw
        avgwE = self.work_indentation / mine
        avgwW = self.work_indentation / minw
        print "east,west work:",avgwE,avgwW


        self.bool_recovers = bool_recovers



        # if float(min([mine,minw]))/max([mine,minw]) > 0.7:
        #     max_diff_con = max([mine,minw])
        # else:
        #     print 'east,west total contacts lost'
        #     print mine,minw
        #     print "Difference is too large."
        #     # sys.exit()

        return min([mine,minw])
