#!/usr/bin/env python
import os,sys,time
import numpy as np
import MDAnalysis

from MDAnalysis import *
from MDAnalysis.analysis.align import *
# from MDAnalysis.tests.datafiles


# calculate RDF
from itertools import izip

# from MDAnalysis import *
from MDAnalysis.core.distances import * ##distance_array
import MDAnalysis.core.units            # for bulk water density

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

    def compute_rmsd(self,idn,sel,psf_ref=None,pdb_ref=None,run_type=None):
        print 'hello from compute rmsd'
        # print idn,sel
        trj = MDAnalysis.Universe(self.psf,self.dcd)

        try:
            sel_label = sel.replace(' ','_')
        except AttributeError:
            sel_join = ('_').join(sel)
            print sel_join,type(sel_join)
            sel_label = sel_join.replace(' ','_')
        print sel_label

        ref = MDAnalysis.Universe(psf_ref,pdb_ref)
        if run_type == None:
            ref_bb = ref.selectAtoms(sel)
        elif run_type == 'canc':
            ref_bb = ref.selectAtoms("name CA","name N","name C")
        elif run_type == 'align':
            ref_bb = ref.selectAtoms("protein")
            print 'aligning ...'
            alignto(trj,ref,select="protein")
        elif run_type == 'align2':
            ref_bb = ref.selectAtoms("protein")
            print 'aligning2 ...'
            alignto(trj,ref,select="resid 187:385")


        ref_crd = ref_bb.coordinates()
        # rmsd_select = u.selectAtoms("name CA","name N","name C")

        if run_type == None:
            rms_fit_trj(trj,ref,select=sel,rmsdfile='rmsdfile_%s_%s.dat' \
                        % (idn,sel_label))
        elif run_type == 'canc':
            rms_fit_trj(trj,ref,select='name CA or name N or name C', \
                        rmsdfile='rmsdfile_%s_%s.dat' % (idn,sel_label))
        elif run_type == 'align':
            rms_fit_trj(trj,ref,select='protein',rmsdfile='rmsdfile_align_%s_%s.dat' \
                        % (idn,sel_label))
        elif run_type == 'align2':
            rms_fit_trj(trj,ref,select='resid 187:385',rmsdfile='rmsdfile_align187_%s_%s.dat' \
                        % (idn,sel_label))



        # for ts in trj.trajectory:
        #     sel = trj.selectAtoms('backbone')
        #     sel_crd = sel.coordinates()
        #     rmsdx = rmsd(ref_crd,sel_crd)
        #     print rmsdx
        #     rmsd_dat.append(rmsdx)

        # rmsd_calc = np.array(rmsd_dat)
        # np.savetxt('rmsd_mda.dat',rmsd_calc,fmt='%0.10f')

        # trj.trajectory[-1]
        # last_crd = sel_tr.coordinates()
        # print 'RMSD',rmsd(ref_crd,last_crd)

        # rms_fit_trj(trj,ref,filename='rmsfit.dcd')

        # rms_fit_trj(trj,ref,)
        # rmsd_select = u.selectAtoms("name CA","name N","name C")
        # print rmsd_select


        # if psf_ref == None: psf_ref = self.psf
        # if pdb_ref == None:
        #     pdb_ref = rmsd_select
            # for ts in u.trajectory[0]:
            #     pdb_ref = rmsd_select

        # for ts in u.trajectory[1::]:
        #     # ref = Universe(u.selectAtoms("name CA","name N","name C"))
        #     ref = Universe(u.selectAtoms("name CA"))
        #     print ref

        # print rmsd(u.atoms.CA.coordinates(),ref.atoms.CA.coordinates())
        # sys.exit()
        # for ts in u.trajectory[::]:

        #     print ts
        #     print ts.frame # number of frame (i.e. 1...)
        #     print u.atoms
        #     # print u.atoms.Coord()
        #     print u.selectAtoms('all')
        #     print u.selectAtoms('name CA')
        #     print u.selectAtoms('name N')
        #     print u.selectAtoms('name C')
        #     print u.selectAtoms('name CA N C')

            # pdb_ref = MDAnalysis.Writer
            # break

    def compute_aligned_rmsd(self,idn,sel,psf_ref=None,pdb_ref=None,run_type=None):
        print 'hello from compute aligned rmsd'
        print idn,sel
        try:
            sel_label = sel.replace(' ','_')
        except AttributeError:
            sel_join = ('_').join(sel)
            print sel_join,type(sel_join)
            sel_label = sel_join.replace(' ','_')
        print sel_label

        ref = MDAnalysis.Universe(psf_ref,pdb_ref)
        if run_type == None:
            ref_bb = ref.selectAtoms(sel)
        elif run_type == 'canc':
            ref_bb = ref.selectAtoms("name CA","name N","name C")
        # rmsd_select = u.selectAtoms("name CA","name N","name C")

        ref_crd = ref_bb.coordinates()
        trj = MDAnalysis.Universe(self.psf,self.dcd)
        if run_type == None:
            rms_fit_trj(trj,ref,select=sel,rmsdfile='rmsdfile_%s_%s.dat' \
                        % (idn,sel_label))
        elif run_type == 'canc':
            rms_fit_trj(trj,ref,select='name CA or name N or name C', \
                        rmsdfile='rmsdfile_%s_%s.dat' % (idn,sel_label))

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
            # print ts._pos[0:383][-1]

            # just xyz
            # np.savetxt('Coord/frame_one_xyz_dist.dat',ts._pos[0:383],fmt='%.8f')

            # if ts.frame >= 100:
            #     break

        # with open(os.path.join(self.destdir,'tension_%s.dat' % (self.idn)),'w') as fp:
        #     for ts in u.trajectory[::]:
        #         # for atom in u.atoms():
        #         #     print atom
        #         # sys.exit()
        #         pass

        #         # # selection
        #         # sel_protein = u.selectAtoms("protein")
        #         # print sel_protein

    def write_pdb_coords(self,start=0,stop=-1,step=1):
        # pdb = MDAnalysis.Writer("%s_interim.pdb" % self.id)
        u = MDAnalysis.Universe(self.psf,self.dcd)
        for ts in u.trajectory[start:stop:step]:
            print type(ts)
            print ts.numatoms,'\n',ts._pos # ts.numatoms = len(ts._pos)
            print ts.frame,'of',len(u.trajectory)
            print "WRITING ..."
            system = u.selectAtoms("resid 1:384") # 1:384 sopnucleo-adp
            system.write("Coord/interim_%s.pdb" % str(ts.frame))

    def test(self):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        # protein = u.selectAtoms("protein")
        protein = u.selectAtoms("protein and name CA")
        # print len(protein)
        # com = protein.centerOfMass()
        # print 'com:',com
        # protein = u.selectAtoms("sphzone 8.0 (protein)")
        # print com[0],com[1],com[2]
        # sel = u.selectAtoms("point %d %d %d 8.0" % (com[0],com[1],com[2]))
        # sys.exit()

        system = u.selectAtoms("sphlayer 1.0 9.0 (resid 200 and name CA)")


        for ts in u.trajectory[240:250:]:
            print ts.frame
            system.write("frame_%s.pdb" % str(ts.frame))


    def calculate_RDF(self):
        print 'computing RDF'
        universe = MDAnalysis.Universe(self.psf,self.dcd)

        MDAnalysis.core.flags['use_periodic_selections'] = True
        MDAnalysis.core.flags['use_KDTree_routines'] = False

        # GROMACS
        # # very short trajectory for testing; use your own!
        # # NOTE: not a good example because the trajectory uses a
        # #       dodecahedral periodic box, which MDAnalysis does NOT
        # #       handle correctly at the moment!!
        # from MDAnalysis.tests.datafiles import GRO, XTC
        # # universe = Universe(GRO, XTC)
        # universe = Universe()

        # adjust the selection, e.g. "resname TIP3 and name OH2" for CHARMM
        # solvent = universe.selectAtoms("resname SOL and name OW")

        # solvent = universe.selectAtoms("resname TIP3 and name OH2") # water
        solvent = universe.selectAtoms("protein and name CA") # protein CA


        dmin, dmax = 0.0, 16.0
        nbins = 100

        # set up rdf
        rdf, edges = np.histogram([0], bins=nbins, range=(dmin, dmax))
        print 'rdf:',rdf,rdf.shape # rdf [1 0 0 0 0 ...] (nbins long)
        print 'edges:',edges # dmin(0.0) - dmax(16.0) like linspace
        rdf *= 0 # set all of rdf to 0 .. [0.0 0.0 0.0 ... ] (nbins long)
        print 'rdf:',rdf,rdf.shape

        # sys.exit()

        rdf = rdf.astype(np.float64)  # avoid possible problems with '/' later on

        n = solvent.numberOfAtoms() # protein: 364
        dist = np.zeros((n*(n-1)/2,), dtype=np.float64)

        print "Start: n = %d, size of dist = %d " % (n, len(dist))

        boxvolume = 0
        # for ts in universe.trajectory[-15:-1]:
        for ts in universe.trajectory[::]:
            print "Frame %4d" % ts.frame
            print 'volume:',ts.volume
            boxvolume += ts.volume      # correct unitcell volume
            coor = solvent.coordinates()
            print 'coor.shape:',coor.shape # (364,3)
            # periodicity is NOT handled correctly in this example because
            # distance_array() only handles orthorhombic boxes correctly

            # usually box commented, use None
            box = ts.dimensions[:3]     # fudge: only orthorhombic boxes handled correctly
            print 'box:',box
            # sys.exit()
            # DISABLE:
            # box = None

            self_distance_array(coor, box, result=dist)  # use pre-allocated array, box not fully correct!!
            new_rdf, edges = np.histogram(dist, bins=nbins, range=(dmin, dmax))
            rdf += new_rdf
            # print

        numframes = universe.trajectory.numframes / universe.trajectory.skip
        boxvolume /= numframes    # average volume

        # Normalize RDF
        radii = 0.5*(edges[1:] + edges[:-1])
        vol = (4./3.)*np.pi*(np.power(edges[1:],3)-np.power(edges[:-1], 3))
        # normalization to the average density n/boxvolume in the simulation
        density = n / boxvolume

        # This is inaccurate when solutes take up substantial amount
        # of space. In this case you might want to use
        # import MDAnalysis.core.units
        # density = MDAnalysis.core.units.convert(1.0, 'water', 'Angstrom^{-3}')
        norm = density * (n-1)/2 * numframes

        print 'n:',n
        print 'boxvolume:',boxvolume
        print 'vol:',vol
        print 'density:',density
        print 'norm:',norm


        # Normalize ON | OFF (for protein)
        rdf /= norm * vol


        outfile = 'mda_rdf2.dat'
        with open(outfile,'w') as output:
            for radius,gofr in izip(radii, rdf):
                output.write("%(radius)8.3f \t %(gofr)8.3f\n" % vars())
        print "g(r) data written to %(outfile)r" % vars()



# Available Calculations
'''
    1) eval_traj: calculate the dihedral angle
    2) get_center_of_mass: calculate the center of mass for residue slice
    3) get_rmsd to establish class, x.rmsd() to compute
'''
def get_rmsd(p):
    print 'p',p
    idn = p.split('.')[0]  # ala.dcd = ala
    idn = p.split('/')[-1].split('.')[0]
    # print 'idn',idn
    prev_dir = ('/').join(my_dir.split('/')[0:-1])
    # print prev_dir
    # psfs = glob(os.path.join(prev_dir,'*.psf'))
    # print psfs
    # sys.exit()
    # psf = filter(lambda x: idn in x,[m for m in psfs]) # w/ ala
    # print psf
    psf = os.path.join(prev_dir,idn+'.psf')
    print 'PSF:\t',psf
    if idn == 'ala':
        ref_coord = os.path.join(prev_dir,'00_start_ala.pdb')
    else:
        ref_coord = os.path.join(prev_dir,'00_start_nolh.pdb')
    print 'ref_coord:',ref_coord
    x = MoleculeUniverse(my_dir,psf,p,my_dir,idn)
    # x.compute_rmsd(idn,'backbone',psf,ref_coord) # ! great ...1
    # x.compute_rmsd(idn,'protein and backbone',psf,ref_coord) # ! great ...1
    # x.compute_rmsd(idn,psf,os.path.join(prev_dir,'00_start_ala.pdb')) # test ..
    selection = ["protein","name CA","name N","name C"]
    # x.compute_rmsd(idn,selection,psf,ref_coord,'canc') # ! great ...2
    selection = ["protein"]
    # x.compute_rmsd(idn,selection,psf,ref_coord,'align') # testing now
    x.compute_rmsd(idn,selection,psf,ref_coord,'align2')

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

def get_pdbs(p):
    coord_dir = os.path.dirname(p)
    dcd_file = os.path.basename(p)
    molecule_id = os.path.basename(p).split('.')[0]
    psf_name = molecule_id + '.psf'
    # x = MoleculeUniverse(my_dir,psf,p,my_dir,'com')
    x = MoleculeUniverse(my_dir,os.path.join(my_dir,'Coord/%s' % psf_name),p,\
                    my_dir,molecule_id)
    x.print_class()
    x.write_pdb_coords(start=0,stop=150)
    # x.tension()

def get_RDF():
    # 08_prod_01.dcd
    # 08_prod_01.coor
    # 08_prod_01.psf
    my_dcd = '08_prod_01.dcd'
    my_psf = '08_prod_01.psf'
    idn = '08_prod_01'
    print idn,my_psf,my_dcd
    x = MoleculeUniverse(my_dir,my_psf,my_dcd,my_dir,idn)
    # x.print_class()
    # x.test()
    x.calculate_RDF()
    # x.write_pdb_coords(-11,-1)


# for path in glob(os.path.join(my_dir,'sop_dev__2013-09-12__run_4/Coord/pdb2mol.ent')):
# for path in glob(os.path.join(my_dir,'Coord/ADP4B9Q.dcd')):
    # print path
    # eval_traj(path)
    # get_tension(path) # - not complete! (my way)
    # get_pdbs(path)

# list_dcds = glob(os.path.join(my_dir,'*.dcd'))
# # print list_dcds
# # sys.exit()
# list_dcds = ['102377.dcd','495917.dcd','864904.dcd','ala.dcd']
# # 102377.dcd
# # 495917.dcd
# # 864904.dcd
# # ala.dcd

# # for path in glob(os.path.join(my_dir,'ala.dcd')):
# for dcd in list_dcds:
#     print dcd
#     get_rmsd(dcd)
#     break
#     # get_center_of_mass(path)


# get RDF
get_RDF()
