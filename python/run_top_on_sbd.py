#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
from glob import glob
import re

my_dir = os.path.abspath(os.path.dirname(__file__))


my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
from mylib.run_command import *
# from plot.WLC import WormLikeChain
# from plot.SOP import *
# from mdanalysis.MoleculeUniverse import MoleculeUniverse
from mylib.FindAllFiles import *





def get_files():
    """
    Get the pdb files: pdb2kho.ent
    """
    myfiles = glob.glob("*.ent")
    print myfiles
    return myfiles


def evaluate_pdbs(lst_pdbs):
    """
    1. Run/make topology.
    2.
    """
    for pdb in lst_pdbs:
        print pdb
        # command = ['run_contacts_calpha',pdb]
        command = ['run_contacts_calpha',pdb]
        # command = ['echo',pdb]
        run_command(command)

def count_residues(*args):

    dct = {}
    for i,p in enumerate(args):

        print i,p
        prefix = re.sub('.ent','',p)
        pdbcode = re.sub('pdb','',prefix)
        fp_reslimit = glob.glob("%s.*.*" % prefix)[0]
        reslim_low = int(fp_reslimit.split('.')[1])
        reslim_high = int(fp_reslimit.split('.')[2])


        print 'pdbcode:',pdbcode
        fp_contacts = "Contact_map_intra_b_%s" % pdbcode
        if not os.path.exists(fp_contacts):
            print 'file does not exist!'
            sys.exit(1)


        with open(fp_contacts) as fp:
            first_line = fp.readline()
            fp.seek(-2,2)
            while fp.read(1) != b"\n":
                fp.seek(-2,1)
            last_line = fp.readline()
            # for i,line in enumerate(fp.readlines()):
                # print line
        contact_low = int(first_line.split()[0])
        contact_high = int(last_line.split()[0])


        print prefix,fp_reslimit,reslim_low,reslim_high
        print fp_contacts
        print 'contacts:',contact_low,contact_high
        print 'contacts:',contact_low+reslim_low-1,contact_high+reslim_low-1

        corr_contact_low = contact_low+reslim_low-1
        corr_contact_high = contact_high+reslim_low-1
        if (corr_contact_high > reslim_high):
            sys.exit(1)



        dct[pdbcode] = {}

        dct[pdbcode]['high'] = reslim_high
        dct[pdbcode]['low'] = reslim_low
        dct[pdbcode]['prefix'] = prefix
        dct[pdbcode]['contactfile'] = fp_contacts
        # dct[pdbcode]['']


    return dct

        # file_bound = glob.glob("%s.\d+*" % prefix)
        # regex = re.compile(r'%s.\d+.\d+' % prefix)
        # files = os.listdir(os.getcwd())
        # break
        # [ x for x in regex.findall(files)]
        # print file_bound


def map_pdb(dct):

    for k,v in dct.iteritems():
        print k,v
        print v['contactfile']

        dct[k]['contacts'] = {}

        for i in range(dct[k]['low'],dct[k]['high']+5):
            print i
            # dct[k]['contacts'][i] = {}
            dct[k]['contacts'][i] = 0
            print dct[k]['contacts'][i]

        with open(v['contactfile']) as fp:
            for i,line in enumerate(fp.readlines()):
                print i,k
                entries = line.split()
                print entries
                dct[k]['contacts'][int(entries[0]) + dct[k]['low']] += 1
                dct[k]['contacts'][int(entries[1]) + dct[k]['low']] += 1


        # for k in range(len(dct[k]['contacts'].keys())):
            # print k
            # dct[k]['contacts'][i] = {}
            # dct[k]['contacts'][i] = 0
            # print dct[k]['contacts']
            # for k,v in dct[k]
        tally = 0
        for k1,v1 in dct[k]['contacts'].iteritems():
            print k1,v1
            # tally +=

        for r in sorted(dct[k]['contacts'].keys()):
            print r
            print '%d:' % r,dct[k]['contacts'][r]
            tally += dct[k]['contacts'][r]
        print 'tally: (%s)' % k,tally




#  ---------------------------------------------------------  #
#  Run code:                                                  #
#  ---------------------------------------------------------  #
pdbs = get_files()

if ((len(sys.argv) > 1) and (sys.argv[1] == 'run')):
    evaluate_pdbs(pdbs)
    sys.exit()
else:
    dct_allpro = count_residues(*pdbs)



if (len(sys.argv) > 1):
    if sys.argv[1] == 'map':
        dct_allpro = map_pdb(dct_allpro)


sys.exit()
