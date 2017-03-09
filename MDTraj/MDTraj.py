#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time


import numpy as np
my_dir = os.path.abspath(os.path.dirname(__file__))

import mdtraj as md


class MDTraj():
    """ The MDTraj class.
    """
    def __init__(self,workdir,destdir,dcd,pdb,sel):

        self.workdir = workdir
        self.destdir = destdir
        self.pdb = pdb
        self.dcd = dcd
        self.traj = md.load(dcd,top=pdb)
        self.top = self.traj.topology
        self.sel = sel

    def print_class(self):
        keys = dir(self)
        for key in keys:
            print key,getattr(self,key)

    def write_traj(self,start=None,stop=None,step=None):
        print self.traj[1:10]
        print self.top
        print self.top.select(self.sel)
        selection = self.top.select(self.sel)
        resid1 = selection[0]
        resid2 = selection[-1]

        traj_sel = self.traj

        if not os.path.exists(os.path.join(self.workdir,'interim_coord')):
            os.makedirs(os.path.join(self.workdir,'interim_coord'))

        # os.ch

        # print coord_file

        print len(self.traj)
        print self.traj.n_frames,self.traj.n_atoms,self.traj.n_residues


        if start == None:
            start = 0
        if stop == None:
            stop = len(self.traj)
        if step == None:
            step = 1

        # topo = self.top

        for i,f in enumerate(self.traj[start:stop:step]):
            # print i,start + i*step,f
            frame = start + i*step
            coord_file = "interim_coord/interim_f%d_r-%d-%d.pdb" % (frame,resid1,resid2)
            # print coord_file
            X = md.formats.PDBTrajectoryFile(coord_file,mode='w')
            X.write(self.traj.xyz[frame],self.top)
            # X.write(self.traj.xyz[frame],selection)

        for i,f in enumerate(self.traj[start:stop:step]):
            # print i,start + i*step,f
            frame = start + i*step
            coord_file = "interim_coord/interim_f%d_r-%d-%d.pdb" % (frame,resid1,resid2)
            # print coord_file
            X = md.formats.PDBTrajectoryFile(coord_file,mode='w')
            X.write(self.traj.xyz[frame],self.top)
            # X.write(self.traj.xyz[frame],selection)

            # print type(self.traj[frame].xyz) # <type 'numpy.ndarray'>
            # print len(self.traj.xyz[frame]) # 221


        # for



    def write_coords(self,resid_first,resid_last,start=0,stop=-1,step=1,sel=None):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''
        if (start != 0) or (start !=1):
            start -= 1
        # print sel
        # time.sleep(5)
        if sel != None:
            print 'SELECTING ALL COORDS...'
            print sel
            selection = sel
            tag = ('-').join(re.findall('\\b\\d+\\b',sel))
            print 'tag:',tag
            # sys.exit()
            # tag = re.sub(^\d+,'',sel)
        else:
            # selection = "resid %d:%d" % (resid_first,resid_last + 1)
            selection = "resid %d:%d" % (resid_first,resid_last)
            tag = "%d-%d" % (resid_first,resid_last)
            print selection,tag
            # sys.exit()
        system = self.u.select_atoms(selection)

        # system = self.u.select_atoms(selection)
        # print system
        # system = self.u.select_atoms("all")
        # print system
        # system = self.u.select_atoms("bynum %d:%d" % (resid_first,resid_last))
        # print system
        # sys.exit()

        # f = start

        # dcd = MDAnalysis.coordinates.DCD(self.dcd)
        # for ts in self.u.trajectory[start:stop:step]:
            # print ts
            # continue

        # sys.exit()
        print start,stop,step
        for ts in self.dcd[start:stop:step]:

        # for ts in enumerate(self.u.trajectory[start:stop:step]):


            # print ts.frame,tag,'start:',start,'stop:',stop,'i:',i
            # print ts
            # self.dcd[ts]
            # print len(self.dcd)
            # print ts.frame,'of',len(self.dcd)
            # print ts.frame,tag,'start:',start,'stop:',stop,'i:',i
            # print ts,tag,'start:',start,'stop:',stop,'f:',f
            # print


            # print ts._pos[0]
            # coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (str(ts.frame + 1),tag)
            traj = MDAnalysis.coordinates.DCD.Timestep(ts)


            # coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (f,tag)

            # system = self.u.select_atoms(selection) # 1:384 sopnucleo-adp
            # system = self.dcd.select_atoms(selection) # 1:384 sopnucleo-adp
            # system = ts.
            # print system,len(system),selection
            # sys.exit()
            # if re.search("70.psf",self.psf) != None:
            #     print system
            #     system = system.select_atoms("protein")
            #     print system
            #     print "using 70.psf and EXITING IMMEDIATELY"
            #     sys.exit()
            os.remove(coord_file)
            if not os.path.exists(coord_file):
                # print 'NUMATOMS:',type(ts),ts.n_atoms
                # print 'ts._pos[0,-1]:','\n',ts._pos[0],'\n',ts._pos[-1]
                print 'writing frame',ts.frame,'of',len(self.dcd)
                # print 'writing',f,'of',len(self.u.trajectory)
                system.write(coord_file)
            self.dcd.next()
            # f += tsep
