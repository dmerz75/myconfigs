#!/usr/bin/python2
# #!/usr/bin/env python
import os
import sys
import time
import re
import numpy as np
import inspect
import MDAnalysis

# from MDAnalysis import *
from MDAnalysis.analysis.align import *
# from MDAnalysis.tests.datafiles


# calculate RDF
# from itertools import izip

# from MDAnalysis import *
# from MDAnalysis.core.distances import * ##distance_array
from MDAnalysis.lib.distances import *
# import MDAnalysis.core.units            # for bulk water density
import MDAnalysis.units

from glob import *

my_dir = os.path.abspath(os.path.dirname(__file__))


class MoleculeUniverse:
    """ Molecule's Universe for trajectory analysis
    Call with workdir,psf,dcd,destdir,idn
    """

    def __init__(self,workdir,psf,dcd,destdir,idn):
        self.workdir = workdir
        self.psf = psf
        # self.dcd = dcd
        # print MDAnalysis.coordinates
        # print MDAnalysis.coordinates.DCD
        self.dcd = MDAnalysis.coordinates.DCD.DCDReader(dcd)
        # inspect
        self.destdir = destdir
        self.idn = idn
        self.u = MDAnalysis.Universe(self.psf,dcd)



    def print_class(self):
        keys = dir(self)
        for key in keys:
            print(key,getattr(self,key))


    def gen_output(self):
        ''' Re-written as get_dihedral_angles.
        '''
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
                print(ts.frame)
                atom_ext_dihedral = []
                for i in residue_indices[:-4]:
                    print(u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),\
                        u.atoms[i:i+4].dihedral())
                    if count == 0:
                        ext_correction = u.atoms[first_last].bond()
                        print(ext_correction,'<--- Assigned')
                        count += 1
                    ext = u.atoms[first_last].bond()-ext_correction
                    print(ext,u.atoms[first_last].bond(),
                          ext_correction,
                          atom_ext_dihedral.append((u.atoms[i].resid,
                                                    u.atoms[i].pos[0],
                                                    u.atoms[i].pos[1],
                                                    u.atoms[i].pos[2],
                                                    ext,
                                                    # u.atoms[first_last].bond(),
                                                    u.atoms[i:i+4].dihedral())))
                n = np.array(atom_ext_dihedral)
                np.savetxt(fp,n,fmt=['%2d','%.8f','%.8f','%.8f','%.2f','%.2f'],\
                               header='frame %s' % ts.frame)


    def get_dihedral_angles(self,step=10,resid_first=0,resid_last=None):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        if resid_last == None:
            resid_last = len(u.atoms)
            # residue_indices = [i for i in range(0,len(u.atoms))]
        # else:
        residue_indices = [i for i in range(resid_first,resid_last)]
        print(residue_indices)
        time.sleep(2)
        first_last = [0,-1]

        # print u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),u.atoms[i:i+4].dihedral()

        all_frames_atoms_ext_dihedral = []
        ext_correction = 0.0
        count = 0
        # out_file = os.path.join(self.destdir,'traj_%s.dat' % self.idn)
        with open(os.path.join(self.destdir,'trajectory_dihedrals_%s_%d_%d_step%d.dat' % \
                               (self.idn,resid_first,resid_last,step)),'w') as fp:
            for ts in u.trajectory[::step]:
                print(ts.frame)
                atom_ext_dihedral = []
                for i,r in enumerate(residue_indices[:-4]):
                    # p: position, r: residue, i: index
                    # p = r - i
                    if resid_first != 0:
                        i = r - u.atoms[0].resid
                        # print 'correcting i:',i
                    print('resid:',u.atoms[i].resid)
                    print('\t(x,y,z):',u.atoms[i].pos)
                    print('\tbond:',u.atoms[first_last].bond())
                    print('\tdihedral:',u.atoms[i:i+4].dihedral())
                    # print u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),\
                    #     u.atoms[i:i+4].dihedral()
                    if count == 0:
                        ext_correction = u.atoms[first_last].bond()
                        print(ext_correction,'<--- Assigned')
                        count += 1
                    ext = u.atoms[first_last].bond()-ext_correction
                    # print ext,u.atoms[first_last].bond(),ext_correction
                    atom_ext_dihedral.append((u.atoms[i].resid,\
                                u.atoms[i].pos[0],u.atoms[i].pos[1],u.atoms[i].pos[2],\
                                ext,# u.atoms[first_last].bond(),\
                                              u.atoms[i:i+4].dihedral()))
                n = np.array(atom_ext_dihedral)
                np.savetxt(fp,n,fmt=['%2d','%.8f','%.8f','%.8f','%.2f','%.2f'],\
                               header='frame %s: resid x  y  z  ext  dihedral' % ts.frame)
            print('frames:',len(u.trajectory),'division',len(u.trajectory)/step)
            print('resids:',len(residue_indices))
            print('array width:',6) # see np.savetxt
            fp.write('# %d %d %d' % (len(u.trajectory)/step+1,len(residue_indices)-4,6))


    def get_bond_distance(self,step=1,resid_first=0,resid_last=None):
        # u = MDAnalysis.Universe(self.psf,self.dcd)
        if resid_last == None:
            resid_last = len(u.atoms)
            # residue_indices = [i for i in range(0,len(u.atoms))]
        # else:
        # residue_indices = [i for i in range(resid_first,resid_last)]

        # print u.atoms[i].resid,u.atoms[i].pos,u.atoms[first_last].bond(),u.atoms[i:i+4].dihedral()

        # all_frames_atoms_ext_dihedral = []
        # ext_correction = 0.0
        # count = 0
        # out_file = os.path.join(self.destdir,'traj_%s.dat' % self.idn)

        print('resid_first',resid_first,'resid_last',resid_last)
        bond_resids = [resid_first,resid_last]
        print('bond_resids:',bond_resids)

        sel_1 = 'name CA and resid %d' % resid_first
        sel_2 = 'name CA and resid %d' % resid_last
        print(sel_1)
        print(sel_2)

        # select_atoms
        atom_1 = self.u.select_atoms(sel_1)
        atom_2 = self.u.select_atoms(sel_2)

        print(atom_1)
        print(atom_2)
        print(MDAnalysis.analysis.distances.dist(atom_1,atom_2))


        with open(os.path.join(self.destdir,'bond_distance_%s_%d_%d_step%d.dat' % \
                               (self.idn,resid_first,resid_last,step)),'w') as fp:

            # fp.write('# atoms:%d traj:%d resid_first:%d resid_last:%d' % (len(u.atoms),len(u.trajectory),resid_first,resid_last))
            lst_frames = []
            lst_bonds = []
            for ts in self.u.trajectory[::step]:
                dist = MDAnalysis.analysis.distances.dist(atom_1,atom_2)
                # bond = self.u.atoms[bond_resids].bond()
                # print bond
                # bond = self.u.atoms[56,264].bond()
                # print bond
                # if ts.frame <= step:
                #     print 'resids:',self.u.atoms[resid_first].resid,self.u.atoms[resid_last].resid
                #     # print self.u.
                # print 'frame:',ts.frame,'bond:',bond
                lst_frames.append(ts.frame)
                print(dist[0],dist[1],dist[2])
                lst_bonds.append(dist[2])

            arr_bonds = np.array((lst_frames,lst_bonds),dtype=float)
            arr_bonds = np.transpose(arr_bonds)
            print(arr_bonds)
            print(arr_bonds.shape)
            np.savetxt(fp,arr_bonds,fmt=['%4d','%.4f'],\
                        header='atoms:%d traj:%d resid1:%d resid2:%d' % (len(self.u.atoms), \
                        len(self.u.trajectory),resid_first,resid_last))



    def center_of_mass(self,dct_domains,step=1):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        # residue_indices = [i for i in range(0,len(u.atoms))]
        # print len(residue_indices)
        # print u
        # print len(u.trajectory)
        lst_distances = []
        with open(os.path.join(self.destdir,'traj_%s_%s.dat' % (self.idn,dct_domains['name'])),'w') as fp:
            for ts in u.trajectory[::step]:
                # selection
                # sel_protein = u.select_atoms("protein")

                # nterm
                # if len(dct_domains['nterm']) == 2:
                # print dct_domains['nterm'][0]

                sel_nterm = u.select_atoms("protein and resid %d:%d" % (dct_domains['nterm'][0],dct_domains['nterm'][1]))
                sel_cterm = u.select_atoms("protein and resid %d:%d" % (dct_domains['cterm'][0],dct_domains['cterm'][1]))

                # print sel_nterm
                # print sel_cterm

                # try:
                #     sel_nterm1= u.select_atoms("resid %d:%d" % (dct_domains['nterm'][0][0],dct_domains['nterm'][0][1]))
                #     sel_nterm2= u.select_atoms("resid %d:%d" % (dct_domains['nterm'][1][0],dct_domains['nterm'][1][1]))
                #     sel_nterm = sel_nterm1 + sel_nterm2
                # # else:
                # except:
                #     sel_nterm = u.select_atoms("resid %d:%d" % (dct_domains['nterm'][0][0],dct_domains['nterm'][0][1]))

                # # cterm
                # # print dct_domains['cterm']
                # # print len(dct_domains['cterm'])
                # # print dct_domains['nterm']
                # # print len(dct_domains['cterm'])
                # # if len(dct_domains['cterm']) == 2:
                # try:
                #     sel_cterm1= u.select_atoms("resid %d:%d" % (dct_domains['cterm'][0][0],dct_domains['cterm'][0][1]))
                #     sel_cterm2= u.select_atoms("resid %d:%d" % (dct_domains['cterm'][1][0],dct_domains['cterm'][1][1]))
                #     sel_cterm = sel_cterm1 + sel_cterm2
                # # else:
                # except:
                # #     sel_cterm = u.select_atoms("resid %d:%d" % (dct_domains['cterm'][0][0],dct_domains['cterm'][0][1]
                #                                                ))


                # sel_nterm = u.select_atoms("resid %d:%d" % (dct_domains['nterm'][0],dct_domains['nterm'][1]))
                # sel_cterm = u.select_atoms("resid %d:%d" % (dct_domains['cterm'][0],dct_domains['cterm'][1]))
                # sel_extra = u.select_atoms("resid 187")
                # print sel_extra
                # sel_combined = sel_nterm + sel_extra
                # print sel_combined
                # sys.exit()

                # sel_cterm = u.select_atoms("resid %d:%d")
                # print sel_protein.centerOfMass(),sel_nterm.centerOfMass(),\
                #                                   sel_cterm.centerOfMass()

                # print "Selections:",sel_nterm,sel_cterm
                r = sel_nterm.centerOfMass() - sel_cterm.centerOfMass()
                d = np.linalg.norm(r)
                lst_distances.append(d)
            print("Selections:",sel_nterm,sel_cterm)
            np.savetxt(fp,np.array(lst_distances),fmt=['%.10f'])


    def compute_rmsd(self,idn,sel,psf_ref=None,pdb_ref=None,run_type=None):
        ''' Don't use this yet, just use VMD (though this is pretty much the same)
        '''

        # print idn,sel
        trj = MDAnalysis.Universe(self.psf,self.dcd)

        try:
            sel_label = sel.replace(' ','_')
        except AttributeError:
            sel_join = ('_').join(sel)
            print(sel_join,type(sel_join))
            sel_label = sel_join.replace(' ','_')
        print(sel_label)

        ref = MDAnalysis.Universe(psf_ref,pdb_ref)
        if run_type == None:
            ref_bb = ref.select_atoms(sel)
        elif run_type == 'canc':
            ref_bb = ref.select_atoms("name CA","name N","name C")
        elif run_type == 'align':
            ref_bb = ref.select_atoms("protein")
            print('aligning ...')
            alignto(trj,ref,select="protein")
        elif run_type == 'align2':
            ref_bb = ref.select_atoms("protein")
            print('aligning2 ...')
            alignto(trj,ref,select="resid 187:385")


        ref_crd = ref_bb.coordinates()
        # rmsd_select = u.select_atoms("name CA","name N","name C")

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
        #     sel = trj.select_atoms('backbone')
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
        # rmsd_select = u.select_atoms("name CA","name N","name C")
        # print rmsd_select


        # if psf_ref == None: psf_ref = self.psf
        # if pdb_ref == None:
        #     pdb_ref = rmsd_select
            # for ts in u.trajectory[0]:
            #     pdb_ref = rmsd_select

        # for ts in u.trajectory[1::]:
        #     # ref = Universe(u.select_atoms("name CA","name N","name C"))
        #     ref = Universe(u.select_atoms("name CA"))
        #     print ref

        # print rmsd(u.atoms.CA.coordinates(),ref.atoms.CA.coordinates())
        # sys.exit()
        # for ts in u.trajectory[::]:

        #     print ts
        #     print ts.frame # number of frame (i.e. 1...)
        #     print u.atoms
        #     # print u.atoms.Coord()
        #     print u.select_atoms('all')
        #     print u.select_atoms('name CA')
        #     print u.select_atoms('name N')
        #     print u.select_atoms('name C')
        #     print u.select_atoms('name CA N C')

            # pdb_ref = MDAnalysis.Writer
            # break

    def compute_aligned_rmsd(self,idn,sel,psf_ref=None,pdb_ref=None,run_type=None):
        ''' Probably doesn't work yet ...
        '''

        # print 'hello from compute aligned rmsd'
        # print idn,sel
        try:
            sel_label = sel.replace(' ','_')
        except AttributeError:
            sel_join = ('_').join(sel)
            print(sel_join,type(sel_join))
            sel_label = sel_join.replace(' ','_')
        print(sel_label)

        ref = MDAnalysis.Universe(psf_ref,pdb_ref)
        if run_type == None:
            ref_bb = ref.select_atoms(sel)
        elif run_type == 'canc':
            ref_bb = ref.select_atoms("name CA","name N","name C")
        # rmsd_select = u.select_atoms("name CA","name N","name C")

        ref_crd = ref_bb.coordinates()
        trj = MDAnalysis.Universe(self.psf,self.dcd)
        if run_type == None:
            rms_fit_trj(trj,ref,select=sel,rmsdfile='rmsdfile_%s_%s.dat' \
                        % (idn,sel_label))
        elif run_type == 'canc':
            rms_fit_trj(trj,ref,select='name CA or name N or name C', \
                        rmsdfile='rmsdfile_%s_%s.dat' % (idn,sel_label))


    def tension(self,start=0,stop=-1,step=1):
        ''' Get tension propagation. (Was working, may need small modifications,
        (remember to multiply by 70 for SOP model))
        '''
        # self.workdir = workdir
        # self.psf = psf
        # self.dcd = dcd
        # self.destdir = destdir
        # self.idn = idn
        # self.u = MDAnalysis.Universe(self.psf,self.dcd)
        u = MDAnalysis.Universe(self.psf,self.dcd)


        # frame_one_dists = u.trajectory[0]._pos
        # frame_one_coords= u.trajectory[0]
        # frame_one_atoms = u.select_atoms("resid 1:384")

        # write frame_one_dist.dat for reference
        for ts in u.trajectory[start:stop:step]:
            lst_distances = []
            # for i in range(ts.n_atoms)
            print(ts.n_atoms)
            for i in range(1,382):
                # print ts._pos[i]
                d = ts._pos[i+1] - ts._pos[i]
                # print 'd:',d
                lst_distances.append(np.linalg.norm(d))
                # print ts._pos[i+1]

            # print ts._pos[0]
            # print ts._pos[1]
            print('383:',ts._pos[382])

            arr_dist = np.array(lst_distances)
            dist_fold = os.path.join(my_dir,'Coord/frame_dists')
            if not os.path.exists(dist_fold): os.makedirs(dist_fold)
            np.savetxt('%s/frame_%s_dist.dat' % (dist_fold,ts.frame),np.array(lst_distances),fmt='%.8f')
            print(arr_dist.shape)
            print(ts._pos[382])
            print(ts._pos[0:383].shape)
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
        #         # sel_protein = u.select_atoms("protein")
        #         # print sel_protein


    def write_pdb_coords(self,start=0,stop=-1,step=1):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''
        # pdb = MDAnalysis.Writer("%s_interim.pdb" % self.id)
        u = MDAnalysis.Universe(self.psf,self.dcd)
        for ts in u.trajectory[start:stop:step]:
            print(type(ts))
            print(ts.n_atoms,'\n',ts._pos) # ts.n_atoms = len(ts._pos)
            print(ts.frame,'of',len(u.trajectory))
            print("WRITING ...")
            system = u.select_atoms("resid 1:384") # 1:384 sopnucleo-adp
            system.write("Coord/interim_%s.pdb" % str(ts.frame))

    def write_coords2(self,resid_first,resid_last,start=0,stop=-1,step=1,sel=None):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''
        # resid_first,resid_last
        # already inclusive
        # implement inclusive selections

        # print 'HEY THERE'

        # frames
        if (start != 0) or (start !=1):
            start -= 1
        # stop += 1

        if not os.path.exists(os.path.join(self.workdir,'interim_coord')):
            os.makedirs(os.path.join(self.workdir,'interim_coord'))

        print(sel)
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

        f = start
        for ts in enumerate(self.u.trajectory[start:stop:step]):

            # print ts.frame,tag,'start:',start,'stop:',stop,'i:',i
            print(ts,tag,'start:',start,'stop:',stop,'f:',f)
            # print
            # coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (str(ts.frame),tag)
            coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (f,tag)
            # system = self.u.select_atoms(selection) # 1:384 sopnucleo-adp
            # system = ts.
            print(system,len(system),selection)
            # sys.exit()
            # if re.search("70.psf",self.psf) != None:
            #     print system
            #     system = system.select_atoms("protein")
            #     print system
            #     print "using 70.psf and EXITING IMMEDIATELY"
            #     sys.exit()
            if not os.path.exists(coord_file):
                # print 'NUMATOMS:',type(ts),ts.n_atoms
                # print 'ts._pos[0,-1]:','\n',ts._pos[0],'\n',ts._pos[-1]
                # print 'writing',ts.frame,'of',len(self.u.trajectory)
                print('writing',f,'of',len(self.u.trajectory))
                system.write(coord_file)
            f += step

    def write_coords(self,resid_first,resid_last,start=0,stop=-1,step=1,sel=None):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''

        print(dir(MDAnalysis))

        # resid_first,resid_last
        # already inclusive
        # implement inclusive selections
        # print 'HEY THERE'
        # print 'start:',start
        # print 'stop:',stop
        # print 'step:',step

        # frames
        if (start != 0):
            start -= 1
        # if (start != 0) or (start !=1):
        #     start -= 1
        # stop += 1

        if not os.path.exists(os.path.join(self.workdir,'interim_coord')):
            os.makedirs(os.path.join(self.workdir,'interim_coord'))

        if sel != None:
            print('SELECTING ALL COORDS...')
            print(sel)
            selection = sel
            tag = ('-').join(re.findall('\\b\\d+\\b',sel))
            print('tag:',tag,selection)
        else:
            # selection = "resid %d:%d" % (resid_first,resid_last + 1)
            selection = "resid %d:%d" % (resid_first,resid_last)
            tag = "%d-%d" % (resid_first,resid_last)
            print('tag:',tag,selection)
        print('Start|stop|step:',start,stop,step)
        print('Selection:(in)',sel,'selection(out):',selection)
        system = self.u.select_atoms(selection)
        print('system.atoms:',system.atoms)
        # system = self.u.select_atoms("all")
        # system = self.u.select_atoms("bynum %d:%d" % (resid_first,resid_last))


        # for ts in self.dcd[start:stop:step]:
        # for ts in enumerate(self.u.trajectory[start:stop:step]):
        # for ts in system[start:stop:step]:


        # # Successfully writes dcd.
        # with MDAnalysis.Writer("mdanalysis.dcd", system.n_atoms) as W:
        #     for ts in self.u.trajectory:
        #         W.write(system)

        # for ts in self.dcd[start:stop:step]:
        for ts in self.u.trajectory[start:stop:step]:
            coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (str(ts.frame + 1),tag)
            if not os.path.exists(coord_file):
                print('writing frame',ts.frame,'of',len(self.dcd))
                print(type(ts))
                print(ts)
                print(ts.frame)
                W = MDAnalysis.Writer(coord_file,system.n_atoms)
                W.write(system)

    # End of Function.
            # ts.atoms
            # print ts.frame,tag,'start:',start,'stop:',stop,'i:',i
            # print ts
            # self.dcd[ts]
            # print len(self.dcd)
            # print ts.frame,'of',len(self.dcd)
            # print ts.frame,tag,'start:',start,'stop:',stop,'i:',i
            # print ts,tag,'start:',start,'stop:',stop,'f:',f
            # print
            # print ts._pos[0]
            # traj = MDAnalysis.coordinates.DCD.Timestep(ts)
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
            # os.remove(coord_file)
            # if 0:
                # if not os.path.exists(coord_file):
                #     # print 'NUMATOMS:',type(ts),ts.n_atoms
                #     # print 'ts._pos[0,-1]:','\n',ts._pos[0],'\n',ts._pos[-1]
                #     print 'writing frame',ts.frame,'of',len(self.dcd)
                #     # print 'writing',f,'of',len(self.u.trajectory)
                #     system.write(coord_file)
            # self.dcd.next()
            # f += tsep

    def print_resids(self,start=0,stop=-1,step=1):
        ''' Write out Coord/interim_0.pdb
        (need to make this a kwargs function)
        '''
        # if (start != 0) or (start !=1):
        #     start -= 1
        # print self.u.atoms
        # print self.u.atoms.segments
        # print self.u.atoms.resids
        # print self.u.atoms.resids()
        # print self.u.atoms.segments[0]
        # print self.u.atoms.chain
        # print self.u.atoms.chain()


        # sel = self.u.select_atoms("resid %d:%d" % (start,stop))
        # print sel.segname
        # print sel.resids
        # print sel.resid
        # print sel.resname


        print(start,stop,step)
        for i in range(start,stop+1,step):
            # print self.u.r%d % i
            print(i)
            # selection = "resid %d" % i
            # for ts in self.u.trajectory:
            #     # print type(ts),ts.n_atoms
            #     # print 'ts._pos[0,-1]:','\n',ts._pos[0],'\n',ts._pos[-1]
            #     resid = self.u.select_atoms("resid %d" % i)

            #     # segname = self.u.select_atoms("resid %d" % i).segname
            #     print "%s" % (resid)



        # print resid_first,resid_last
        # tag = "%d-%d" % (resid_first,resid_last)
        # print selection,tag
        # for ts in self.u.trajectory[start:stop:step]:
        #     # ts.n_atoms = len(ts._pos)
        #     system = self.u.select_atoms(selection) # 1:384 sopnucleo-adp
        #     coord_file = "interim_coord/interim_f%s_r-%s.pdb" % (str(ts.frame),tag)
        #     if not os.path.exists(coord_file):
        #         print type(ts),ts.n_atoms
        #         print 'ts._pos[0,-1]:','\n',ts._pos[0],'\n',ts._pos[-1]
        #         print 'writing',ts.frame,'of',len(self.u.trajectory)
        #         system.write(coord_file)


    def test(self):
        u = MDAnalysis.Universe(self.psf,self.dcd)
        # protein = u.select_atoms("protein")
        protein = u.select_atoms("protein and name CA")
        # print len(protein)
        # com = protein.centerOfMass()
        # print 'com:',com
        # protein = u.select_atoms("sphzone 8.0 (protein)")
        # print com[0],com[1],com[2]
        # sel = u.select_atoms("point %d %d %d 8.0" % (com[0],com[1],com[2]))
        # sys.exit()

        system = u.select_atoms("sphlayer 1.0 9.0 (resid 200 and name CA)")


        for ts in u.trajectory[240:250:]:
            print(ts.frame)
            system.write("frame_%s.pdb" % str(ts.frame))


    def calculate_RDF(self):
        ''' Definitely not finished.
        '''
        print('computing RDF')
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
        # solvent = universe.select_atoms("resname SOL and name OW")

        # solvent = universe.select_atoms("resname TIP3 and name OH2") # water
        solvent = universe.select_atoms("protein and name CA") # protein CA


        dmin, dmax = 0.0, 16.0
        nbins = 100

        # set up rdf
        rdf, edges = np.histogram([0], bins=nbins, range=(dmin, dmax))
        print('rdf:',rdf,rdf.shape) # rdf [1 0 0 0 0 ...] (nbins long)
        print('edges:',edges) # dmin(0.0) - dmax(16.0) like linspace
        rdf *= 0 # set all of rdf to 0 .. [0.0 0.0 0.0 ... ] (nbins long)
        print('rdf:',rdf,rdf.shape)

        # sys.exit()

        rdf = rdf.astype(np.float64)  # avoid possible problems with '/' later on

        n = solvent.numberOfAtoms() # protein: 364
        dist = np.zeros((n*(n-1)/2,), dtype=np.float64)

        print("Start: n = %d, size of dist = %d " % (n, len(dist)))

        boxvolume = 0
        # for ts in universe.trajectory[-15:-1]:
        for ts in universe.trajectory[::]:
            print("Frame %4d" % ts.frame)
            print('volume:',ts.volume)
            boxvolume += ts.volume      # correct unitcell volume
            coor = solvent.coordinates()
            print('coor.shape:',coor.shape) # (364,3))
            # periodicity is NOT handled correctly in this example because
            # distance_array() only handles orthorhombic boxes correctly

            # usually box commented, use None
            box = ts.dimensions[:3]     # fudge: only orthorhombic boxes handled correctly
            print('box:',box)
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

        print('n:',n)
        print('boxvolume:',boxvolume)
        print('vol:',vol)
        print('density:',density)
        print('norm:',norm)


        # Normalize ON | OFF (for protein)
        rdf /= norm * vol


        outfile = 'mda_rdf2.dat'
        with open(outfile,'w') as output:
            # for radius,gofr in izip(radii, rdf):
            for radius,gofr in zip(radii, rdf):
                output.write("%(radius)8.3f \t %(gofr)8.3f\n" % vars())
        print("g(r) data written to %(outfile)r" % vars())



# Available Calculations
'''
    1) eval_traj: calculate the dihedral angle
    2) get_center_of_mass: calculate the center of mass for residue slice
    3) get_rmsd to establish class, x.rmsd() to compute
'''
def get_rmsd(p):
    print('p',p)
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
    print('PSF:\t',psf)
    if idn == 'ala':
        ref_coord = os.path.join(prev_dir,'00_start_ala.pdb')
    else:
        ref_coord = os.path.join(prev_dir,'00_start_nolh.pdb')
    print('ref_coord:',ref_coord)
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
        print(domain)
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
    print(idn,my_psf,my_dcd)
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
# get_RDF()



# if __name__ == '__main__':
#     # get_RDF()
#     main()
#     # pass
