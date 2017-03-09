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


def get_dihedrals_over_trajectory():
    my_dcd = 'dcd/2KHOsbd_D30_equil.dcd'
    my_psf = os.path.expanduser('~/ext/completed_sbd/gsop/sbd_gsop.psf')
    idn = 'sbd_gsop'
    print idn,my_psf,my_dcd
    x = MoleculeUniverse(my_dir,my_psf,my_dcd,my_dir,idn)
    # x.get_dihedral_angles(10)
    # x.get_dihedral_angles(200)
    # x.get_dihedral_angles(200,520,564) # 520 559
    x.get_dihedral_angles(10,523,555)






get_dihedrals_over_trajectory()
