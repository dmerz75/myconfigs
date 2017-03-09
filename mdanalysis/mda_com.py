#!/usr/bin/env python
import os,sys,time
import numpy as np
import MDAnalysis
from glob import *

my_dir = os.path.abspath(os.path.dirname(__file__))


class MoleculeUniverse:
    """ Molecule's Universe for trajectory analysis
    """
    def __init__(self,workdir,psf,dcd,destdir,idn):
        self.workdir = workdir
        self.psf = psf
        self.dcd = dcd
        self.destdir = destdir
        self.idn = idn
    def print_vals(self):
        print self.workdir
        print self.psf
        print self.dcd
        print self.destdir
        print self.idn
    def print_class(self):
        keys = dir(self)
        for key in keys:
            print key,getattr(self,key)
    def gen_output(self):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        residue_indices = [i for i in range(0,len(u.atoms))]
        first_last = [0,-1]
        
        # print u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),u.atoms[i:i+4].dihedral()

        all_frames_atoms_ext_dihedral = []
        ext_correction = 0.0
        count = 0
        # out_file = os.path.join(self.destdir,'traj_%s.dat' % self.idn)
        with open(os.path.join(self.destdir,'traj_%s.dat' % self.idn),'w') as fp:
            for ts in u.trajectory[101::10]:
                print ts.frame
                atom_ext_dihedral = []
                for i in residue_indices[:-4]:
                    print u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),\
                        u.atoms[i:i+4].dihedral()
                    if count == 0:
                        ext_correction = u.atoms[first_last].bond()
                        print ext_correction,'<--- Assigned'
                        count += 1
                    ext = u.atoms[first_last].bond()-ext_correction
                    print ext,u.atoms[first_last].bond(),ext_correction
                    atom_ext_dihedral.append((u.atoms[i].resid,\
                                u.atoms[i].pos[0],u.atoms[i].pos[1],u.atoms[i].pos[2],\
                                ext,# u.atoms[first_last].bond(),\
                                              u.atoms[i:i+4].dihedral()))
                n = np.array(atom_ext_dihedral)
                np.savetxt(fp,n,fmt=['%2d','%.8f','%.8f','%.8f','%.2f','%.2f'],\
                               header='frame %s' % ts.frame)
    def center_of_mass(self,dct_domains):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        # residue_indices = [i for i in range(0,len(u.atoms))]
        # print len(residue_indices)
        # print u
        # print len(u.trajectory)
        lst_distances = []
        with open(os.path.join(self.destdir,'traj_%s_%s.dat' % (self.idn,dct_domains['name'])),'w') as fp:
            for ts in u.trajectory[::]:
                # selection
                # sel_protein = u.selectAtoms("protein")
                sel_nterm = u.selectAtoms("resid %d:%d" % (dct_domains['nterm'][0],dct_domains['nterm'][1]))
                sel_cterm = u.selectAtoms("resid %d:%d" % (dct_domains['cterm'][0],dct_domains['cterm'][1]))
                # sel_cterm = u.selectAtoms("resid %d:%d")
                # print sel_protein.centerOfMass(),sel_nterm.centerOfMass(),\
                #                                   sel_cterm.centerOfMass()
                r = sel_nterm.centerOfMass() - sel_cterm.centerOfMass()
                d = np.linalg.norm(r)
                lst_distances.append(d)
            np.savetxt(fp,np.array(lst_distances),fmt=['%.10f'])


# Available Calculations
'''
    1) eval_traj: calculate the dihedral angle
    2) get_center_of_mass: calculate the center of mass for residue slice

'''
def eval_traj(p):
    traj_id = p.split('/')[-3].split('__')[-2].split('_')[-1]
    x = MoleculeUniverse(my_dir,os.path.join(my_dir,'2mol.psf'),p,\
                         os.path.expanduser('~/analysis/sop_dev__2013-09-12__run_4'),\
                         traj_id)
    x.print_vals()
    x.gen_output()
def get_center_of_mass(p):
    # print os.path.dirname(p)
    # print os.path.basename(p)
    psf = os.path.join(('/').join(p.split('/')[0:-2]),'00_start_nolh135.psf')
    # def __init__(self,workdir,psf,dcd,destdir,idn):
    x = MoleculeUniverse(my_dir,psf,p,my_dir,'com')
    # center_of_mass(self,dict((domain) I,(domain) II)):
    original  = {'name':'orig','nterm':(4,186),'cterm':(187,367)}
    I_to_II   = {'name':'I_to_II','nterm':(4,187),'cterm':(189,367)}
    IB_to_IIB = {'name':'IB_to_IIB','nterm':(40,115),'cterm':(229,306)}

    # 1A: 4 - 39, 116 - 118
    # 1B: 40- 115,
    # 2A: 189-228, 307 - 385
    # 2B: 229-306,

    x.center_of_mass(original)
    x.center_of_mass(I_to_II)
    x.center_of_mass(IB_to_IIB)

    # x.center_of_mass()
    # x.print_class()


# for path in glob(os.path.join(my_dir,'sop_dev__2013-09-12*__run_lee*4*/Coord/2mol.dcd')):
#     print path
#     eval_traj(path)
for path in glob(os.path.join(my_dir,'all.dcd')):
    print path
    get_center_of_mass(path)

