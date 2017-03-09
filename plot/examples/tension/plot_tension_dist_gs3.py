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

gs = GridSpec(3,1)

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
from glob import *

# for path in glob(os.path.join(my_dir,'frame_*')):
#     print path

def compute_mean_tension(start,stop):
    data_list = []
    for i in range(start,stop):
        # print i
        data_list.append(np.loadtxt('frame_dists/frame_%s_dist.dat' % str(i)))

    data = np.array(data_list)
    print data.shape
    mean_tension = data.mean(axis=0)

    np.savetxt('mean_tension_%s_%s.dat' % (str(start),str(stop)),mean_tension,fmt='%0.8f')
    return mean_tension

def pointed_tension(start,stop):
    data_list = []
    for i in range(start,stop):
        # print i
        data_list.append(np.loadtxt('frame_dists/frame_%s_dist.dat' % str(i)))

    data = np.array(data_list)
    print data.shape
    mean_tension = data.mean(axis=0)

    np.savetxt('mean_tension_%s_%s.dat' % (str(start),str(stop)),mean_tension,fmt='%0.8f')
    return mean_tension


dct_frame_loads = {'1':3001,'2':6000,'3':9000,\
                   '4':12000,'5':15000,'6':18000,'size':3000}

try:
    y_tension_1 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['1']-dct_frame_loads['size'],dct_frame_loads['1']))
    y_tension_2 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['2']-dct_frame_loads['size'],dct_frame_loads['2']))
    y_tension_3 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['3']-dct_frame_loads['size'],dct_frame_loads['3']))
    y_tension_4 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['4']-dct_frame_loads['size'],dct_frame_loads['4']))
    y_tension_5 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['5']-dct_frame_loads['size'],dct_frame_loads['5']))
    y_tension_6 = np.loadtxt('mean_tension_%s_%s.dat' % (dct_frame_loads['6']-dct_frame_loads['size'],dct_frame_loads['6']))
except:
    print 'computing tension over frames ...'
    y_tension_1 = compute_mean_tension(1,3001)
    y_tension_2 = compute_mean_tension(3000,6000)
    y_tension_3 = compute_mean_tension(6000,9000)
    y_tension_4 = compute_mean_tension(9000,12000)
    y_tension_5 = compute_mean_tension(12000,15000)
    y_tension_6 = compute_mean_tension(15000,18000)

x = np.linspace(1,y_tension_1.shape[0],y_tension_1.shape[0])

# y_tension_inspect = compute_mean_tension(1830,1880)

ax1 = plt.subplot(gs[0,:])
plt.plot(x,y_tension_1,'r-')
plt.plot(x,y_tension_2,'y-')
# plt.plot(x,y_tension_inspect,'k-',linewidth=0.5)

ax2 = plt.subplot(gs[1,:])
plt.plot(x,y_tension_3,'g-')
plt.plot(x,y_tension_4,'c-')
# plt.plot(x,y_tension_inspect,'k-',linewidth=0.5)

ax3 = plt.subplot(gs[2,:])
plt.plot(x,y_tension_5,'b-')
plt.plot(x,y_tension_6,'m-')
# plt.plot(x,y_tension_inspect,'k-',linewidth=0.5)


#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.155,right=0.96,top=0.895,bottom=0.175)
fig.set_size_inches(7.4,5.1)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')
run_control     = {'family':'sans-serif',
                   'weight':'normal',
                   'size'  :'14',
}
matplotlib.rc('font',**run_control)

# plt.title('the $\alpha$ title')
# plt.ylabel('$\lambda$ (nm)')
# plt.xlabel('$\nu$ ($s^-1$)')

xmin = 0
xmax = 383

ymin = 3.69
ymax = 3.95

ax1.set_xlim(xmin,xmax)
ax1.set_ylim(ymin,ymax)

ax2.set_xlim(xmin,xmax)
ax2.set_ylim(ymin,ymax)

ax3.set_xlim(xmin,xmax)
ax3.set_ylim(ymin,ymax)


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
save_fig(0,'','tension_prop_gs')
