#!/usr/bin/env python
import os,sys,time
import numpy as np
from glob import *

my_dir = os.path.abspath(os.path.dirname(__file__))


#  ---------------------------------------------------------  #
#  expand for moving_average                                  #
#  ---------------------------------------------------------  #
# mpl_moving_average


#  ---------------------------------------------------------  #
#  Start matplotlib (1/3)                                     #
#  ---------------------------------------------------------  #
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0, :])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
# rmsd_102377.dat
# rmsd_495917.dat
# rmsd_864904.dat
# rmsd_ala.dat

# for path in glob(os.path.join(my_dir,rmsd_*.dat)):
y1 = np.loadtxt('rmsd_102377.dat')
y4 = np.loadtxt('rmsd_495917.dat')
y8 = np.loadtxt('rmsd_864904.dat')
ala= np.loadtxt('rmsd_ala.dat')

print ala.shape[0] # = 749
x = np.linspace(0,75,ala.shape[0])

plt.plot(x,y1,'r-')
plt.plot(x,y4,'g-')
plt.plot(x,y8,'b-')
plt.plot(x,ala,'k-')

# sys.exit()    



#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.155,right=0.96,top=0.895,bottom=0.175)
fig.set_size_inches(7.4,5.1)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')
run_control     = {'family':'sans-serif',
                   'weight':'normal',
                   'size'  :'26',
}
matplotlib.rc('font',**run_control)

plt.title('RMSD')
plt.ylabel('RMSD $(\AA)$')
plt.xlabel('Time (ns)')

ax1.set_xlim(-0.1,75.1)
ax1.set_ylim(-0.1,6.1)
plt.xticks([5,25,50,70])
plt.yticks([1,2,3,4,5])

# LEGEND  
# locations: quadrants - 1,2,3,4
ax1.legend(["102377",
            "495917",
            "864904",
            "ala",
        ],
           loc=2,
           prop={'size':16})
leg = plt.gca().get_legend()
leg.draw_frame(False)

def save_fig(i,subdir,fname):
    ''' Make subdir if necessary.
    '''
    if subdir == '':
        content_dir = my_dir
    else:
        content_dir = os.path.join('/'.join(my_dir.split('/')[0:i]),subdir)
    if not os.path.exists(content_dir): os.makedirs(content_dir)
    # Save in PNG and EPS formats
    abs_file_name = os.path.join(content_dir,fname)
    plt.savefig('%s.png' % abs_file_name)
    plt.savefig('%s.eps' % abs_file_name)
    # plt.savefig('%s.jpg' % abs_file_name)
    os.chdir(content_dir)
        
print "calling save_fig ..."
# save_pic_data(levels_back,subdir,name)
# example: save_fig(-4,'fig',name)
# example: save_fig(-3,'',name)
# plt.show()
save_fig(0,'fig','rmsd75')


