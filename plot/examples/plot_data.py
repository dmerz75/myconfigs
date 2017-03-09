#!/usr/bin/env python
import os,sys,time
import numpy as np


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
data = np.loadtxt('data.out')
print data.shape

plt.plot(data[::,0],data[::,1],'g.')


#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.155,right=0.955,top=0.895,bottom=0.175)
fig.set_size_inches(7.4,5.1)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')
run_control     = {'family':'sans-serif',
                   'weight':'normal',
                   'size'  :'26',
}
matplotlib.rc('font',**run_control)

# plt.title('the $\alpha$ title')
# plt.ylabel('$\lambda$ (nm)')
# plt.xlabel('$\nu$ (s$^-1$)')


ax1.set_xlim(-0.5,100.5)
ax1.set_ylim(9,220)
plt.xticks([25,50,75])
plt.yticks([60,120,180])

# LEGEND  
# locations: quadrants - 1,2,3,4
ax1.legend(["data1",
            # "data2",
            # "data3",
        ],
           loc=2,
           prop={'size':20})
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
save_fig(0,'fig','example1')

