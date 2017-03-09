#!/usr/bin/env python
import sys
import os
import time

import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
# from plot.wlc import WormLikeChain
# from plot.SOP import *
from mdanalysis.MoleculeUniverse import MoleculeUniverse

from glob import glob

def get_center_of_mass():
    dcd = os.path.join(my_dir,'nolh495917.dcd')
    psf = glob(os.path.join(my_dir,'../495917.psf'))
    print psf
    psf = os.path.normpath(psf[0])
    print psf,dcd
    # sys.exit()

    x = MoleculeUniverse(my_dir,psf,dcd,my_dir,'com')
    # sys.exit()
    # center_of_mass(self,dict((domain) I,(domain) II)):

    # Domain Definitions
    IA = ((4,39),(116,188))
    IIA= ((189,228),(307,385))
    IB = ((40,115),())
    IIB= ((229,306),())
    # -------------------
    # original  = {'name':'orig','nterm':(4,186),'cterm':(187,367)}
    I_to_II   = {'name':'I_to_II','nterm':(4,187),'cterm':(189,367)}
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
    # lst_domains = [IA_to_IIA,IA_to_IB,IA_to_IIB,IIA_to_IB,
    #                IIA_to_IIB,IB_to_IIB]
    lst_domains = [I_to_II]

    for domain in lst_domains:
        print domain
        x.center_of_mass(domain,25)
    # x.center_of_mass(original)
    # x.center_of_mass(I_to_II)
    # x.center_of_mass()
    # x.print_class()

get_center_of_mass()
