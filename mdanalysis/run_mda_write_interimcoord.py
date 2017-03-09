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

                # nterm
                # if len(dct_domains['nterm']) == 2:
                try:
                    sel_nterm1= u.selectAtoms("resid %d:%d" % (dct_domains['nterm'][0][0],dct_domains['nterm'][0][1]))
                    sel_nterm2= u.selectAtoms("resid %d:%d" % (dct_domains['nterm'][1][0],dct_domains['nterm'][1][1]))
                    sel_nterm = sel_nterm1 + sel_nterm2
                # else:
                except:
                    sel_nterm = u.selectAtoms("resid %d:%d" % (dct_domains['nterm'][0][0],dct_domains['nterm'][0][1]))

                # cterm
                # print dct_domains['cterm']
                # print len(dct_domains['cterm'])
                # print dct_domains['nterm']
                # print len(dct_domains['cterm'])
                # if len(dct_domains['cterm']) == 2:
                try:
                    sel_cterm1= u.selectAtoms("resid %d:%d" % (dct_domains['cterm'][0][0],dct_domains['cterm'][0][1]))
                    sel_cterm2= u.selectAtoms("resid %d:%d" % (dct_domains['cterm'][1][0],dct_domains['cterm'][1][1]))
                    sel_cterm = sel_cterm1 + sel_cterm2
                # else:
                except:
                    sel_cterm = u.selectAtoms("resid %d:%d" % (dct_domains['cterm'][0][0],dct_domains['cterm'][0][1]))


                # sel_nterm = u.selectAtoms("resid %d:%d" % (dct_domains['nterm'][0],dct_domains['nterm'][1]))
                # sel_cterm = u.selectAtoms("resid %d:%d" % (dct_domains['cterm'][0],dct_domains['cterm'][1]))
                # sel_extra = u.selectAtoms("resid 187")
                # print sel_extra
                # sel_combined = sel_nterm + sel_extra
                # print sel_combined
                # sys.exit()

                # sel_cterm = u.selectAtoms("resid %d:%d")
                # print sel_protein.centerOfMass(),sel_nterm.centerOfMass(),\
                #                                   sel_cterm.centerOfMass()

                # print "Selections:",sel_nterm,sel_cterm
                r = sel_nterm.centerOfMass() - sel_cterm.centerOfMass()
                d = np.linalg.norm(r)
                lst_distances.append(d)
            print "Selections:",sel_nterm,sel_cterm
            np.savetxt(fp,np.array(lst_distances),fmt=['%.10f'])

    def rmsd(self):
        u = MDAnalysis.Universe(self.psf,self.dcd)

    def tension(self,start=0,stop=-1,step=1):
        ''' Get tension propagation.
        '''

        u = MDAnalysis.Universe(self.psf,self.dcd)

        # frame_one_dists = u.trajectory[0]._pos
        # frame_one_coords= u.trajectory[0]
        # frame_one_atoms = u.selectAtoms("resid 1:384")

        # write frame_one_dist.dat for reference
        for ts in u.trajectory[start:stop:step]:
            lst_distances = []
            # for i in range(ts.numatoms)
            print ts.numatoms
            for i in range(1,382):
                # print ts._pos[i]
                d = ts._pos[i+1] - ts._pos[i]
                # print 'd:',d
                lst_distances.append(np.linalg.norm(d))
                # print ts._pos[i+1]

            # print ts._pos[0]
            # print ts._pos[1]
            print '383:',ts._pos[382]

            arr_dist = np.array(lst_distances)
            dist_fold = os.path.join(my_dir,'Coord/frame_dists')
            if not os.path.exists(dist_fold): os.makedirs(dist_fold)
            np.savetxt('%s/frame_%s_dist.dat' % (dist_fold,ts.frame),np.array(lst_distances),fmt='%.8f')
            print arr_dist.shape
            print ts._pos[382]
            print ts._pos[0:383].shape


    def write_pdb_coords(self,start=0,stop=-1,step=1):
        # pdb = MDAnalysis.Writer("%s_interim.pdb" % self.id)
        u = MDAnalysis.Universe(self.psf,self.dcd)
        for ts in u.trajectory[start:stop:step]:
            print type(ts)
            print ts.numatoms,'\n',ts._pos # ts.numatoms = len(ts._pos)
            print ts.frame,'of',len(u.trajectory)
            print "WRITING ..."
            system = u.selectAtoms("resid 1:384") # 1:384 sopnucleo-adp
            system.write("tension_coords/interimcoord%s.pdb" % str(ts.frame))


# Available Calculations
'''
    1) eval_traj: calculate the dihedral angle
    2) get_center_of_mass: calculate the center of mass for residue slice
    3) get_rmsd to establish class, x.rmsd() to compute
'''
def get_rmsd(p):
    idn = p.split('.')[0]  # ala.dcd = ala
    psfs = glob(os.path.join(my_dir,'*.psf'))
    psf = filter(lambda x: idn in x,[m for m in psfs]) # w/ ala
    x = MoleculeUniverse(my_dir,psf,p,my_dir,idn)

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

    # Domain Definitions
    IA = ((4,39),(116,188))
    IIA= ((189,228),(307,385))
    IB = ((40,115),())
    IIB= ((229,306),())
    # -------------------
    # original  = {'name':'orig','nterm':(4,186),'cterm':(187,367)}
    # I_to_II   = {'name':'I_to_II','nterm':(4,187),'cterm':(189,367)}
    # IB_to_IIB = {'name':'IB_to_IIB','nterm':(40,115),'cterm':(229,306)}

    IA_to_IIA  = {'name':'IA_to_IIA','nterm':IA,'cterm':IIA}
    IA_to_IB   = {'name':'IA_to_IB','nterm':IA,'cterm':IB}
    IA_to_IIB  = {'name':'IA_to_IIB','nterm':IA,'cterm':IIB}

    IIA_to_IA  = {'name':'IIA_to_IA','nterm':IIA,'cterm':IA}
    IIA_to_IB  = {'name':'IIA_to_IB','nterm':IIA,'cterm':IB}
    IIA_to_IIB = {'name':'IIA_to_IIB','nterm':IIA,'cterm':IIB}

    IB_to_IA   = {'name':'IB_to_IA','nterm':IB,'cterm':IA}
    IB_to_IIA  = {'name':'IB_to_IIA','nterm':IB,'cterm':IIA}
    IB_to_IIB  = {'name':'IB_to_IIB','nterm':IB,'cterm':IIB}

    IIB_to_IA   = {'name':'IIB_to_IA','nterm':IIB,'cterm':IA}
    IIB_to_IIA  = {'name':'IIB_to_IIA','nterm':IIB,'cterm':IIA}
    IIB_to_IB   = {'name':'IIB_to_IB','nterm':IIB,'cterm':IB}

    # lst_domains = [IA_to_IIA,IA_to_IB,IA_to_IIB,IIA_to_IA,
    #                IIA_to_IB,IIA_to_IIB,IB_to_IA,IB_to_IIA,
    #                IB_to_IIB,IIB_to_IA,IIB_to_IIA,IIB_to_IB]
    lst_domains = [IA_to_IIA,IA_to_IB,IA_to_IIB,IIA_to_IB,
                   IIA_to_IIB,IB_to_IIB]

    for domain in lst_domains:
        print domain
        x.center_of_mass(domain)
    # x.center_of_mass(original)
    # x.center_of_mass(I_to_II)
    # x.center_of_mass(IB_to_IIB)

    # x.center_of_mass()
    # x.print_class()

def get_tension(p):
    coord_dir = os.path.dirname(p)
    dcd_file = os.path.basename(p)
    molecule_id = os.path.basename(p).split('.')[0]
    psf_name = molecule_id + '.psf'
    # x = MoleculeUniverse(my_dir,psf,p,my_dir,'com')
    x = MoleculeUniverse(my_dir,os.path.join(my_dir,'Coord/%s' % psf_name),p,\
                    my_dir,molecule_id)
    x.print_class()
    x.tension()

def get_pdbs(p,start,stop):
    coord_dir = os.path.dirname(p)
    dcd_file = os.path.basename(p)
    molecule_id = os.path.basename(p).split('.')[0]
    psf_name = molecule_id + '.psf'
    # x = MoleculeUniverse(my_dir,psf,p,my_dir,'com')
    x = MoleculeUniverse(my_dir,os.path.join(my_dir,'Coord/%s' % psf_name),p,\
                    my_dir,molecule_id)
    x.print_class()
    x.write_pdb_coords(start,stop)
    # x.tension()


# for path in glob(os.path.join(my_dir,'sop_dev__2013-09-12__run_4/Coord/pdb2mol.ent')):
# for path in glob(os.path.join(my_dir,'Coord/ADP4B9Q.dcd')):
#     # print path
#     get_pdbs(path,1600,2099)

# pdbADP4B9Q.pdb
# def
