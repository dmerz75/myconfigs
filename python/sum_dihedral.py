#!/usr/bin/env python
import os,sys,time
from glob import *
import numpy as np

def total_forces(force_file):
    """ Calculate the total force applied!
    """
    # print data[3],data[4],data[5]
    data = np.transpose(np.loadtxt(force_file))
    sum_forces = 0.0
    for i in range(3,12):
        print i
        sum_forces += np.sum(data[i])
    print sum_forces
    # x21 = np.sum(data[3])
    # y21 = np.sum(data[4])
    # z21 = np.sum(data[5])
    # print np.sum(data[3]),np.sum(data[4]),np.sum(data[5])
    # x23 = np.sum(data[6])
    # y23 = np.sum(data[7])
    # z23 = np.sum(data[8])
    # print np.sum(data[6]),np.sum(data[7]),np.sum(data[8])
    # x34 = np.sum(data[9])
    # y34 = np.sum(data[10])
    # z34 = np.sum(data[11])
    # print np.sum(data[9]),np.sum(data[10]),np.sum(data[11])

# Start Here!
my_dir = os.path.abspath(os.path.dirname(__file__))

for path in glob(os.path.join(my_dir,'dihedral_potential_*')):
    print path
    total_forces(path)
