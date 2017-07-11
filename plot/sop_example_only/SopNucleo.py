
import sys
import os
import time
from glob import *
import numpy as np





class SopNucleo():
    def __init__(self,main_dir):
        ''' For Plotting SopNucleo force-extension curves!
        '''
        self.main_dir = main_dir
        # self.subdir = subdir
        # self.fp_subdir = os.path.join(main_dir,subdir)
        # self.subdirs = os.listdir(main_dir)

    def get_trajectories(self):
        ''' Find target trajectories.
        Return dictionary of seed:full path

        '''
        dct_traj = {}
        for path in glob(os.path.join(self.fp_subdir,'*/out*80.dat')):
            # print path
            seeds = path.split('__')[-1]
            small_seed = seeds.split('_')[0]
            dct_traj[small_seed] = path

        self.trajectories = dct_traj
        return dct_traj

    def print_class(self):
        ''' Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            # definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    def get_xy(self,target_seed):
        ''' Acquire force, extension for each trajectory.
        '''
        # print self.trajectories[target_seed]
        data = np.loadtxt(self.trajectories[target_seed])
        print data.shape
