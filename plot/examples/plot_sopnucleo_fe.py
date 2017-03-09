#!/usr/bin/env python
import sys
import os
import time

my_dir = os.path.abspath(os.path.dirname(__file__))

import numpy as np

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
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #

from glob import *

for path in glob(os.path.join(my_dir,'out*80.dat')):
    print path
    data = np.loadtxt(path)
    print data.shape
    x = 0.1 * data[::,10]
    y = 70.0 * data[::,3]
    plt.plot(x,y)


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

# plt.title('the $\alpha$ title')
# plt.ylabel('$\lambda$ (nm)')
# plt.xlabel('$\nu$ ($s^-1$)')

# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])

# LEGEND
# locations: quadrants - 1,2,3,4
# ax1.legend(["data1",
#             # "data2",
#             # "data3",
#         ],
#            loc=1,
#            prop={'size':16})
# leg = plt.gca().get_legend()
# for label in leg.get_lines():
#     label.set_linewidth(2.5)
#     leg.draw_frame(False)

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
save_fig(0,'','fe')
