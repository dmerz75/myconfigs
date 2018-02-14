#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MDTraj3
# #!/usr/bin/python2
import sys
import os
import time
import re
import glob

import numpy as np
# import mdtraj as md
# import

import MDAnalysis
from MDAnalysis.analysis.align import *
from MDAnalysis.lib.distances import *
import MDAnalysis.units


# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# libraries:
# from mylib.FindAllFiles import *
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
from mylib.run_command import run_command


# my_dir = os.path.abspath(os.path.dirname(__file__))

class MDAnalysisHSA():
    ''' The new MDTraj3 class.
    '''
    def __init__(self,pdb,dcd,psf,workdir):
        self.pdb = pdb
        self.dcd = dcd
        self.workdir = workdir
        self.coord_dir = os.path.join(workdir,'interim_coord')

        # self.traj = md.load(dcd,top=pdb) # MDTraj
        # self.top = self.traj.topology # MDTraj

        self.dcd = MDAnalysis.coordinates.DCD.DCDReader(dcd)
        self.u = MDAnalysis.Universe(psf,dcd) # universe


    def print_class(self):
        keys = dir(self)
        for key in keys:
            print(key,getattr(self,key))

    def write_pdb(self,start=0,stop=100000,step=1,sel=None):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''

        try:
            print(self.sel)
            print('start:',start,'stop:',stop,'step:',step)
        except AttributeError:
            print("No selection made, cannot write pdb's.")
            return

        self.coord_dir = os.path.join(self.workdir,'interim_coord')

        if not os.path.exists(self.coord_dir):
            os.makedirs(self.coord_dir)

        selection = self.sel

        print("selection:")
        print(selection)

        digits = [int(i) for i in re.findall('\\b\\d+\\b',self.sel)]
        tag = ('-').join(re.findall('\\b\\d+\\b',self.sel))


        if selection != 'all':
            resid1 = digits[0]
            resid2 = digits[1]
            self.resid1 = resid1
            self.resid2 = resid2

        print('resid1:',self.resid1)
        print('resid2:',self.resid2)
        # sys.exit()


        print(digits)
        print(tag)

        # selection = "resid %d:%d" % (resid_first,resid_last)
        # tag = "%d-%d" % (resid_first,resid_last)

        print('tag:',tag,selection)
        print('Start|stop|step:',start,stop,step)
        print('Selection:(in)',sel,'selection(out):',selection)
        system = self.u.select_atoms(selection)
        print('system.atoms:',system.atoms)
        # system = self.u.select_atoms("all")
        # system = self.u.select_atoms("bynum %d:%d" % (resid_first,resid_last))


        # # Successfully writes dcd.
        # with MDAnalysis.Writer("mdanalysis.dcd", system.n_atoms) as W:
        #     for ts in self.u.trajectory:
        #         W.write(system)

        # for ts in self.dcd[start:stop:step]:

        arr_frames = []
        for ts in self.u.trajectory[start:stop:step]:

            num_frame = ts.frame
            # num_frame = ts.frame + 1
            str_frame = str(num_frame)
            coord_file = "interim_coord/interim_f%s.pdb" % str_frame

            arr_frames.append(num_frame)

            if not os.path.exists(coord_file):
                print('writing frame',ts.frame,'of',len(self.dcd))
                print(type(ts))
                print(ts)
                print(ts.frame)
                W = MDAnalysis.Writer(coord_file,system.n_atoms)
                W.write(system)

        self.frames = np.array(arr_frames)


    def write_pdb_dep(self,start=0,stop=100000,step=1):
        ''' Deprecated, from MDTraj
        '''

        try:
            print(self.sel)
            print('start:',start,'stop:',stop,'step:',step)
        except AttributeError:
            print("No selection made, cannot write pdb's.")
            return

        self.coord_dir = os.path.join(self.workdir,'interim_coord')

        if not os.path.exists(self.coord_dir):
            os.makedirs(self.coord_dir)

        selection = self.sel

        print("selection:")
        print(selection)

        digits = [int(i) for i in re.findall('\\b\\d+\\b',self.sel)]
        tag = ('-').join(re.findall('\\b\\d+\\b',self.sel))

        print(digits)
        print(tag)

        # sub_sel = re.sub('resid','',self.sel)
        # sub_sel2= re.sub('to ','',sub_sel)
        # print(sub_sel)
        # print(sub_sel2)
        # sys.exit()
        # split_sel = sub_sel2.split()
        # resid1 = int(split_sel[0])
        # resid2 = int(split_sel[1])
        # print('resid1:',resid1,'resid2:',resid2)

        resid1 = digits[0]
        resid2 = digits[1]

        self.resid1 = resid1
        self.resid2 = resid2

        print('resid1:',resid1)
        print('resid2:',resid2)
        # sys.exit()


        # From MDTraj.
        # print(len(self.traj))
        # print('frames:',self.traj.n_frames)
        # print('n_atoms:',self.traj.n_atoms)
        # print('n_residues:',self.traj.n_residues)



        # def write(self, positions, topology, modelIndex=None, unitcell_lengths=None,
        #           unitcell_angles=None, bfactors=None):
        lst_frames = []
        for i,f in enumerate(self.traj[start:stop:step]):
            # print i,start + i*step,f
            frame = start + i*step
            lst_frames.append(frame)
            # coord_file = "interim_coord/interim_f%d_r-%d-%d.pdb" % (frame,resid1,resid2)
            coord_file = "interim_coord/interim_f%d.pdb" % frame

            fp_coord = os.path.join(self.workdir,coord_file)
            # print(fp_coord)

            if os.path.exists(fp_coord):
                # print(fp_coord,"exists.")
                # print(coord_file,"exists.")
                continue

            X = md.formats.PDBTrajectoryFile(coord_file,mode='w',
                                             force_overwrite=True)
            X.write(self.traj.xyz[frame],self.top)
            # X.write(selection,self.top)
            # X.write(self.traj.xyz[frame],selection) # fails ..
            # X.write(self.traj.xyz[frame],self.sel) # fails

        self.frames = np.array(lst_frames)



    def remove_interim_coords(self,pdbtype='rebuilt'):
        ''' Remove PDBs. .rebuilt.pdb from pulchra
        or the interim_coord_f500.pdb from MDTraj
        '''

        coord_dir = os.path.join(self.workdir,'interim_coord')
        if os.path.exists(coord_dir):
            self.coord_dir = coord_dir
        else:
            print('Coord_dir does not exist.',coord_dir)
            return

        os.chdir(self.coord_dir)
        fp_coords = glob.glob('interim_f*.pdb')
        fp_rebuilts = [f for f in fp_coords if re.search('rebuilt',f)]

        # print("fp_coords")
        # print(fp_coords)

        # print("rebuilts")
        # print(fp_rebuilts)

        if pdbtype == 'rebuilt':
            [os.remove(f) for f in fp_rebuilts]

        if pdbtype == 'all':
            [os.remove(f) for f in fp_coords]


    def remove_hsa_files(self):

        coord_dir = os.path.join(self.workdir,'interim_coord')
        if os.path.exists(coord_dir):
            self.coord_dir = coord_dir
        else:
            print('Coord_dir does not exist.',coord_dir)
            return

        os.chdir(self.coord_dir)
        fp_targets1 = glob.glob('Ratio_aa.*')
        fp_targets2 = glob.glob('Area_atom.*')
        fp_targets3 = glob.glob('Area_aa.*')
        fp_targets = fp_targets1 + fp_targets2 + fp_targets3

        # print(fp_targets)
        [os.remove(f) for f in fp_targets]



    def print_interim_coord_files(self):

        coord_dir = os.path.join(self.workdir,'interim_coord')
        if os.path.exists(coord_dir):
            self.coord_dir = coord_dir
        else:
            print('Coord_dir does not exist.',coord_dir)
            return

        os.chdir(self.coord_dir)
        fp_coords = glob.glob('interim_*.pdb')

        for f in fp_coords:
            print(f)


    def run_pulchra(self):

        try:
            print(self.coord_dir)
            if not os.path.exists(self.coord_dir):
                print("Could not locate: ",self.coord_dir)
                print("No coordinate directory.")
                return
        except AttributeError:
            print("No self.coord_dir")
            return

        os.chdir(self.coord_dir)
        # fp_coords = glob.glob(os.path.join(self.coord_dir,'interim_f*.pdb'))
        fp_coords = glob.glob('interim_f*.pdb')
        fp_interims = [f for f in fp_coords if not re.search('rebuilt',f)]
        fp_rebuilts = [re.sub('.pdb','.rebuilt.pdb',f) for f in fp_interims]

        fp_tups = list(zip(fp_interims,fp_rebuilts))
        # print(fp_tups)

        # for i in range(len(fp_interims)):
        #     print(fp_interims[i])
        #     print(fp_rebuilts[i])
        #     print(fp_tups[i])

        # sys.exit()
        # print(fp_coords)
        # return

        for i in range(len(fp_tups)):
            if not os.path.exists(fp_tups[i][1]):
                run_command(['pulchra',fp_tups[i][0]])
            else:
                print('not running pulchra on:',fp_tups[i][0])
            # if i > 10:
            #     break

    def run_hsa(self):

        os.chdir(self.coord_dir)

        fp_coords = glob.glob('interim_f*.rebuilt.pdb')

        # fp_ratios = []
        # for fp in fp_coords:
        #     print(fp)

        fp_ratios = ['Ratio_aa.%d.%d.%s' % (self.resid1,
                                            self.resid2,
                                            fp) for fp in fp_coords]

        fp_targets = list(zip(fp_coords,fp_ratios))


        for fp in fp_targets:
            print(fp[0],fp[1])
            if not os.path.exists(fp[1]):
                print('run_area:')
                run_command(['run_area',fp[0],str(self.resid1),str(self.resid2)])
            else:
                print('%s:' % fp[1],'exists, HSA complete.')
        # sys.exit()

        # fp_ratios = ['Ratio_aa.%d.%d.interim_f%d.rebuilt.pdb'
        #              % (self.resid1,self.resid2,i) for i in self.frames]

        # for i in range(len(fp_ratios)):
        #     if not os.path.exists(fp_ratios[i]):
        #         run_command(['run_area',fp_coords[i],str(self.resid1),str(self.resid2)])
        #     else:
        #         print('not running HSA on:', fp_ratios[i])

        # for i,fp in enumerate(fp_coords):
        #     run_command(['run_area',fp,str(self.resid1),str(self.resid2)])

            # if i > 10:
            #     break


    def get_hsa(self):

        print("Getting HSA. (requires .write_pdb())")
        os.chdir(self.coord_dir)
        fp_ratios = ['Ratio_aa.%d.%d.interim_f%d.rebuilt.pdb'
                     % (self.resid1,self.resid2,i) for i in self.frames]

        # print(fp_ratios)
        # for f in fp_ratios:
        #     print(f)

        lst_hydro = []
        lst_frames= []
        lst_zipped = []

        for f in fp_ratios:
            print(f)
            try:
                o = open(f,'r+')
                final_line = o.readlines()[-1]
                hydrophobes_exposed = final_line.split()[-1]
                print(final_line,hydrophobes_exposed)
                o.close()
                frame = int(re.search('_f(\d+)',f).groups(1)[0])
                lst_frames.append(frame)
                lst_hydro.append(float(hydrophobes_exposed))
            except IOError:
                print('No Ratio_aa file.')
                pass


        lst_zipped = zip(lst_frames,lst_hydro)
        hsa_data = np.array(sorted(lst_zipped))
        script_args = (' ').join(sys.argv)

        os.chdir(self.workdir)
        if not os.path.exists('hsa_current'):
            os.makedirs('hsa_current')

        # print(hsa_data.shape)
        # print(hsa_data)
        # hsa_data = np.array([15,1.0])
        # print(hsa_data.shape)
        # print(hsa_data)
        # print(hsa_data.size)
        # sys.exit()
        if hsa_data.size > 0:
            fn_hsa = 'hsa_current/hsa_r%d-%d_f%d-%d.dat' % (self.resid1,
                                                            self.resid2,
                                                            self.frames[0],
                                                            self.frames[-1])
            print("Writing:",fn_hsa,self.workdir)
            np.savetxt(fn_hsa,hsa_data,fmt='%5d %5.3f',header=script_args)






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
            print(key,getattr(self,key))

    def write_traj(self,start=None,stop=None,step=None):
        print(self.traj[1:10])
        print(self.top)
        print(self.top.select(self.sel))
        selection = self.top.select(self.sel)
        resid1 = selection[0]
        resid2 = selection[-1]

        traj_sel = self.traj

        if not os.path.exists(os.path.join(self.workdir,'interim_coord')):
            os.makedirs(os.path.join(self.workdir,'interim_coord'))

        # os.ch

        # print coord_file

        print(len(self.traj))
        print(self.traj.n_frames,self.traj.n_atoms,self.traj.n_residues)


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
            print('SELECTING ALL COORDS...')
            print(sel)
            selection = sel
            tag = ('-').join(re.findall('\\b\\d+\\b',sel))
            print('tag:',tag)
            # sys.exit()
            # tag = re.sub(^\d+,'',sel)
        else:
            # selection = "resid %d:%d" % (resid_first,resid_last + 1)
            selection = "resid %d:%d" % (resid_first,resid_last)
            tag = "%d-%d" % (resid_first,resid_last)
            print(selection,tag)
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
        print(start,stop,step)
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
                print('writing frame',ts.frame,'of',len(self.dcd))
                # print 'writing',f,'of',len(self.u.trajectory)
                system.write(coord_file)
            self.dcd.next()
            # f += tsep
