#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

import glob # uses the * asterisk/glob operator for regular expressions, finding files.
import numpy as np

# figure starts here!
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)
gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])
ax = [ax1]


# the directory of the python plotting file (this script)
my_dir = os.path.abspath(os.path.dirname(__file__))


dat_files = glob.glob(os.path.join(my_dir,'*.dat'))


# print all as one list:  ['file1.dat','file2.dat','file3.dat']
print dat_files


# do a for loop:
for i,df in enumerate(dat_files):
    print i,df


# example for loop:
for i in range(5,12): # note: won't print 12, just up to 12
    print i



# use numpy to import datafile.
data = np.loadtxt('file1.dat')
print data.shape

x = data[::,0] # if shape is 250,2  (250 rows, 2 columns), this grabs all 250 in first column
y = data[::,1] # if shape is 250,2  (250 rows, 2 columns), this grabs all 250 in second column



ax1.plot(x,y,color='b') # colors include: k-black, r-red, g-green, b-blue, m-magenta, and many more..




# figure settings:
fig.set_size_inches(8.5,5.1)
plt.subplots_adjust(left=0.22,right=0.930,top=0.900,bottom=0.22)

ax1.set_xlim(0,500)
ax1.set_ylim(-5000,20000)

ax1.set_title("Xample Plot")
ax1.set_xlabel('X')
ax1.set_ylabel('Y')


filename = 'plot_example'
plt.savefig('%s.png' % filename) # string substitution.
