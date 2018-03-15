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



from cycler import cycler
# print matplotlib.rcParams['axes.prop_cycle']
mycolors = ['k', 'r', 'g', 'b','c','m','lime',
            'darkorange','sandybrown','hotpink',
            'mediumseagreen','crimson','slategray',
            'orange','orchid','darkgrey','indianred',
            'tan','cadetblue']
# ax1.set_prop_cycle(cycler('color',mycolors))


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
        print 'num_dimers:',num_dimers
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
        print self.dirname
        num_dimers = len(self.dimers)
        print 'num_dimers:',num_dimers
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
        print self.dirname
        num_dimers = len(self.dimers)
        print 'num_dimers:',num_dimers
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
        print data.shape
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

    def get_reverse_abscissa(self,xt):
        # print 'xt:',xt
        # print self.ext_raw[::,1][::10]

        # new_xt = self.ext_raw * -1 + xt

        new_xt = self.ext_raw + xt
        self.ext_raw = new_xt
        # pass

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
        pass
        return

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

    def truncation_by_percent(self,reversal_frame):

        print 'trunc:'
        print self.dirname


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
                   'steps']

        percent = float(reversal_frame) / self.total_frames
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
                (obj == 'externalcontacts') or (obj == 'force')):
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

        if not hasattr(self,'frameindex'):
            frameindex = int(np.where(self.frames==rev_frame)[0])
            arr_frames1 = self.frames[:frameindex]
            arr_frames2 = arr_frames[1:] + arr_frames1[-1]
            self.reversal_frame = arr_frames1[-1]
            self.frames = np.concatenate((arr_frames1,arr_frames2))
            self.frameindex = frameindex

        arr_contacts1 = getattr(self,dir_obj)[:self.frameindex]
        nesw_contacts = np.concatenate((arr_contacts1,arr_contacts[1:]))
        setattr(self,dir_obj,nesw_contacts)


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
        # frameindex =


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
        # ax1.plot(x,y)

        if ((self.direction == 'forward') and (self.truncated == 'no')):
            ax1.plot(x,y,'k-',label='Full Indent')
        elif ((self.direction == 'forward') and (self.truncated == 'yes')):
            ax1.plot(x,y,'r-',label='Partial Indent')
        else:
            ax1.plot(x,y,'g-',label='Retracting')

        if self.truncated == 'yes':
            ax1.axvline(self.reversal_ind,color='r',linestyle='-',linewidth=1.5)
        else:
            ax1.plot(x,y,label=self.name)


        ax1.set_xlim(-1,31)
        ax1.set_xticks([0,10,20,30])

        ax1.set_ylim(-.20,.905)
        ax1.set_yticks([0,.2,.4,.6,.8])
        ax1.set_ylim(-0.04,0.94)

        # ax1.set_xlabel('Indentation Depth X/nm',fontsize=16)
        # ax1.set_ylabel('Indentation Force F/nN',fontsize=16)
        ax1.set_xlabel('Indentation Depth X/nm')
        # ax1.set_ylabel('Indentation Force F/nN')
        ax1.set_ylabel('Indentation Force (nN)')
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

        ax1.set_xlabel('Indentation Depth X/nm',fontsize=24)
        ax1.set_ylabel('Indentation Force F/nN',fontsize=24)

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
        ax1.set_ylabel('Indentation Force F/nN')
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

    def plot_contacts(self,ax,dimers,shift=0,limit=None):
        '''
        Provide n the index in mt_list for plotting.
        Provide dimers, a list from "get_dimers."
        limit = 1320
        '''
        print 'plotting contacts'
        ax.set_prop_cycle(cycler('color',mycolors))

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

        # ax.set_xlabel("Frame #")
        ax.set_ylabel(r"$Q_{n}$")
        # ax.tick_params(axis='both')
        # ax.set_xlim(x1[0],x1[-1])
        ax.set_xlim(self.frames[0],self.frames[-1])
        ax.set_ylim(0.36,1.03)
        # ax.set_ylim(-0.03,1.03)

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


    def get_mtpf(self):
        """
        Plot bending angle.
        """
        print "getting mtpf."

        fp = os.path.join(self.dirname,"emol_mtpfbending_angle.dat")
        x = np.loadtxt(fp) # 858, 14
        data = np.reshape(x,(x.shape[0]/13,13,x.shape[1])) # 66, 13, 14

        # cumulative data
        pdata = data[::,::,::2] # 66, 13, 7
        cdata = data[::,::,1::2] # 66, 13, 7
        mdata = np.zeros(data.shape)


        for a in range(cdata.shape[0]):
            for b in range(cdata.shape[1]):
                # print cdata[a,b,::]
                for index,c in enumerate(cdata[a,b,::]):
                    if c > 55:
                        # print index,c
                        i2 = (index - 1) * 2 + 1
                        # print data[a,b,::]
                        mdata[a,b,0:i2] = data[a,b,0:i2]
                        break
                        # print mdata[a,b,::]

                # for c in range(data.shape[2]):
                    # print data[a,b,c]
                    # if data[a,b,c] >

        frames = np.linspace(0,self.total_frames,data.shape[1])

        # cumulative data (round 2)
        pdata = mdata[::,::,::2] # 66, 13, 7
        cdata = mdata[::,::,1::2] # 66, 13, 7

        # cumulative, transpose, remove centroids
        udata = np.cumsum(pdata,axis=2)
        ctdata = np.transpose(udata)

        self.mtpfcentroids = pdata
        self.mtpfbending = ctdata


    def plot_mtpf_global(self,ax):
        '''
        ax = list of ax1,ax2, ..
        '''
        # 7 angles in 12 dimer.
        cmap = matplotlib.cm.get_cmap("rainbow")
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

        for i,a in enumerate(ax):
            # if i == start:
            #     a.set_yticks
            if i > start:
                a.set_yticks([])


        # Plot:
        for a in range(self.mtpfbending.shape[0]):
            #                   13 :: 7
            ax[a+start].imshow(self.mtpfbending[a,::,::],aspect='auto',cmap='rainbow',vmin=0,vmax=20)


        # Colorbar:
        # plt.colorbar(ax8,ticks=[0,1])
        cb1 = matplotlib.colorbar.ColorbarBase(ax[-1],
                                               cmap=cmap)

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

        if self.num_dimers/self.num_pf == 8:
            start = 2
            # for a in ax[-3:-1]:
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
                if np.var(self.mtpfbending[i,p,::]) > 80.0:
                    # print cr
                    # print cr[p]
                    ax[i+start].plot(frames,self.mtpfbending[i,p,::],color=cmap(cr[p]))


        for a in ax:
            a.tick_params(axis='both',labelsize=12)
            a.set_yticks([-90,-45,0,45,90])
            a.set_ylim(-92,92)
            # a.set_xticks([0,200,40,600])
            a.set_xticks([0,250,500])
            a.set_xlim(frames[0],frames[-1])


        # sys.exit()

        # for i in range(len(ax)):
        #     if i != 0:
        #         ax[i].set_yticks([])

        # for a in ax:
        #     a.set_ylim(-5,100)
        cb1 = matplotlib.colorbar.ColorbarBase(ax[-1],cmap=cmap)


        # OFF unused plots.
        if self.num_dimers/self.num_pf == 8:
            for a in ax[0:2]:
                a.axis('off')




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


    def plot_contact_interface(self,ax,face='n',limits=(0,600)):
        """
        Plot Contact Interface.
        """
        ax.set_prop_cycle(cycler('color',mycolors))
        ax.tick_params(axis='both',labelsize=12)
        ax.set_ylim(-0.03,1.03)
        ax.set_xlim(self.frames[0],self.frames[-1])
        ax.text(70,0.1,face.upper())

        # Choose Face:
        if face == "n":
            icontacts = self.ncontacts
        elif face == "e":
            icontacts = self.econtacts
        elif face == "w":
            icontacts = self.wcontacts
        elif face == "s":
            icontacts = self.scontacts

        for i,d in enumerate(self.dimers):
            ax.plot(icontacts[::,d],color=mycolors[i])


    def get_break_events(self,face='n'):
        """
        Plot Contact Interface.
        # (frame, force, lat/lon/both, Qn (lon if both)
        self.break_events = []
        """

        # Choose Face:
        if face == "n":
            icontacts = self.ncontacts
        elif face == "e":
            icontacts = self.econtacts
        elif face == "w":
            icontacts = self.wcontacts
        elif face == "s":
            icontacts = self.scontacts

        def find_simple_contact_changes(arr,threshold):
            # print arr
            # print arr.shape

            for i in range(arr.shape[0]):

                if arr[i] < threshold:
                    break

            return i


        # Dictionary:
        dct_conchange = {}

        for i,d in enumerate(self.dimers):
            dct_conchange[(d,face)] = {}
            # print d
            # print min(icontacts[::,d])
            ax.plot(icontacts[::,d],color=mycolors[i])
            frame1 = find_contact_changes(icontacts[::,d],0.82) # early
            frame2 = find_contact_changes(icontacts[::,d],0.2) # late/complete
            dct_conchange[(d,face)] = sorted([frame1,frame2])


        self.dct_contact_events.update(dct_conchange)
        # self.dct_contact_events =


        # for k,v in dct_conchange.items():
        #     print k,face,v[face]


        # early lateral, late lat, early Long., late Longitudinal.
        # find_interesting_contactface_changes(dct_conchange)


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
