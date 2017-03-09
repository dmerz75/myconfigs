#!/usr/bin/env python
import sys
import os
import time

import numpy as np
import numpy.ma as ma

my_dir = os.path.abspath(os.path.dirname(__file__))


#  ---------------------------------------------------------  #
#  expand for moving_average                                  #
#  ---------------------------------------------------------  #
# mpl_moving_average


#  ---------------------------------------------------------  #
#  Start matplotlib (1/3)                                     #
#  ---------------------------------------------------------  #
import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
# import cPickle as pickle
# import scipy
# from pylab import *
# from scipy.stats import norm
# import matplotlib.mlab as mlab
# import matplotlib as mpl


# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# import matplotlib.pyplot as plt


fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'gsop' # sop | sopnucleo | gsop | namd
plot_type = 'dihed' # fe | tension | rmsd | rdf
frames = 201
residues = 28
# 201 217 6
# 201 30 6
# 201 28 6
data_name = 'seed-17_frames-%d_residues-%d-30' % (frames,residues) # seed #


def load_traj_dihed():
    # data = np.loadtxt('traj_dihed_sbd_gsop.dat')
    # data = np.loadtxt('trajectory_dihedrals_sbd_gsop_522_556_step10.dat')
    data = np.loadtxt('trajectory_dihedrals_sbd_gsop_523_555_step10.dat')
    print data.shape

    print frames,residues
    print frames * residues * 6
    my_array = data.reshape((frames,residues,6))
    print my_array.shape

    xlist = np.linspace(0,my_array.shape[0]-1,my_array.shape[0])
    ylist = np.linspace(0,my_array.shape[1]-1,my_array.shape[1])

    resid_list = []
    zlist = []
    for i in range(my_array.shape[0]):
        # print i,my_array[i,::,::].shape
        for y in range(my_array.shape[1]):
            # print i,y,my_array[i,y,::]
            # print i,y,my_array[i,y,5]
            resid = my_array[i,y,0]
            resid_list.append(resid)
            z = my_array[i,y,5]
            zlist.append(z)


    ylist = np.linspace(resid_list[0],resid_list[-1],my_array.shape[1])
    print ylist
    # sys.exit()

    z_arr = np.array(zlist)
    # print type(z_arr)


    # vmin = 18
    # vmax = 92
    # zmask1 = ma.masked_less(z_arr,vmin) # mask everything < -10
    # z_corr = zmask1.filled(10)
    # # print type(z_corr)
    # zmask2 = ma.masked_greater(z_corr,vmax)
    # z_corr = zmask2.filled(100)

    vmin = 30
    vmax = 70
    zmask1 = ma.masked_less(z_arr,vmin) # mask everything < -10
    z_corr = zmask1.filled(20)
    # print type(z_corr)
    zmask2 = ma.masked_greater(z_corr,vmax)
    z_corr = zmask2.filled(80)



    # print type(z_corr)
    # sys.exit()

    Z = z_corr.reshape(residues,frames)
    # print z_arr,z_arr.shape
    print Z,Z.shape


    # from matplotlib.colors import LinearSegmentedColormap
    # cdict1 = {'red':   ((0.0, 0.0, 0.0),
    #                     (0.5, 0.0, 0.1),
    #                     (1.0, 1.0, 1.0)                    ),

    #           'green': ((0.0, 0.0, 0.0),
    #                     (1.0, 0.0, 0.0)                    ),

    #           'blue':  ((0.0, 0.0, 1.0),
    #                     (0.5, 0.1, 0.0),
    #                     (1.0, 0.0, 0.0)                    )
    #        }

    # blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)
    # plt.register_cmap(cmap=blue_red1)
    # plt.pcolormesh(xlist, ylist, Z, cmap = plt.get_cmap('BlueRed1'),vmin=0,vmax=100)


    # Set some garish out-of-range colors and gray for bad
    # matplotlib.colors.Colormap.set_under('blue')
    # matplotlib.colors.Colormap.set_over('blue')
    # cmap.set_bad('0.5')

    # import matplotlib.colors as colors
    # # Set up a colormap:
    # palette = cm.gray
    # palette.set_over('r',vmax)
    # palette.set_under('g',vmin)
    # palette.set_bad('b',vmax)

    cmap = plt.get_cmap('summer')
    # cmap.set_bad(color = 'r', alpha = 1.)
    cmap.set_over('r',vmax)
    cmap.set_under('r',vmin)

    # 20 - 80
    plt.pcolormesh(xlist, ylist, Z, cmap = plt.get_cmap('summer'),vmin=vmin,vmax=vmax)
    plt.colorbar()
    # plt.show()
    # sys.exit()

    print 'maximum_x:',max(xlist)
    print 'maximum_y:',max(ylist)
    return min(xlist),max(xlist),min(ylist),max(ylist)


min_x,max_x,min_y,max_y = load_traj_dihed()


#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# mpl_font

# plt.title('RMSD')
plt.ylabel('Residue \#')
plt.xlabel('Frame \#')

ax1.set_xlim(min_x,max_x)
ax1.set_ylim(min_y,max_y)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])

# # LEGEND
# # locations: quadrants - 1,2,3,4
# # lst_labels = ['sec1','sec2','sec3']
# lst_labels = lst_seeds
# try:
#     ax1.legend([lst_labels[0],
#                 lst_labels[1],
#                 lst_labels[2],
#                 lst_labels[3],
#             ],
#                loc=4,)
#     # prop={'size':16})
# except:
#     ax1.legend([lst_labels[0],
#             ],
#                loc=4,)
#     # prop={'size':16})
#     leg = plt.gca().get_legend()
#     for label in leg.get_lines():
#         label.set_linewidth(3.5)
#         # leg.draw_frame(False)

def save_fig(i,subdir,fname):
    ''' Make subdir if necessary.
    '''
    if subdir == '':
        content_dir = my_dir
    else:
        content_dir = os.path.join('/'.join(my_dir.split('/')[0:i]),subdir)
    if not os.path.exists(content_dir): os.makedirs(content_dir)
    dir_filename = os.path.join(content_dir,fname)
    fp_filename = os.path.join(dir_filename,fname)
    if not os.path.exists(dir_filename): os.makedirs(dir_filename)
    # Save in PNG,EPS,SVG,PDF,TIFF,JPG formats
    # PIL, wxpython2.8, QT5Agg may be necessary
    # Image.open('%s.png' % fp_filename).save('%s.jpg' % fp_filename,'JPEG')
    # dpi = 80 or 300
    dpi = 300
    plt.savefig('%s.png' % dir_filename,dpi=dpi)
    plt.savefig('%s.png' % fp_filename,dpi=dpi)
    plt.savefig('%s.eps' % fp_filename,dpi=dpi)
    plt.savefig('%s.svg' % fp_filename,dpi=dpi)
    plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
    plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
    plt.savefig('%s.jpg' % fp_filename,dpi=dpi)

try:
    if sys.argv[1] == 'show':
        plt.show()
except IndexError:
    pass

print "calling save_fig ..."
# save_pic_data(levels_back,subdir,name)
# example: save_fig(-4,'fig',name)
# example: save_fig(-3,'',name)
# save_fig(0,'fig','fname_%s' % idn)
# save_fig(0,'fig','example1')
save_fig(-1,'fig','%s_%s_%s' % (result_type,plot_type,data_name))



# def plot_hist(data,tg):
#     ''' plot histogram
#     '''
#     bins = np.linspace(-180,180,121)
#     events, edges, patches = hist(data,bins,normed=True)
#     if tg == '1':
#         # (mu, sigma) = norm.fit(sorted(sample_angles)[500:15550])
#         (mu, sigma) = norm.fit(sorted(sample_angles))
#         y = mlab.normpdf(bins,mu,sigma)
#         l = plt.plot(bins,y,'b--',linewidth=2)
#         events, edges, patches = hist(data,bins,normed=True,facecolor='blue',\
#                                       label='$\alpha$-helix')
#     elif tg == '2':
#         # (mu, sigma) = norm.fit(sorted(sample_angles)[750:10900])
#         (mu, sigma) = norm.fit(sorted(sample_angles))
#         y = mlab.normpdf(bins,mu,sigma)
#         l = plt.plot(bins,y,'r--',linewidth=2)
#         events, edges, patches = hist(data,bins,normed=True,facecolor='red',\
#                                       label='$\beta$-sheet')
#     else:
#         (mu, sigma) = norm.fit(sorted(sample_angles))
#         y = mlab.normpdf(bins,mu,sigma)
#         events, edges, patches = hist(data,bins,normed=True,facecolor='green',\
#                                       label='Loop')
#     mu_sigma_list.append((mu,sigma))

# all_angles = []
# mu_sigma_list = []

# for i,path in enumerate(glob(os.path.join(my_dir,'angle*.dat'))):
#     print path
#     tg = path.split('.')[0].split('_')[-1]
#     sample_angles = np.loadtxt(path)
#     print sample_angles.shape
#     plot_hist(sample_angles,tg)


# l1 = plt.legend(["Helix \
#                  $\mu=%0.3f,\ \sigma=%0.3f$" \
#                  %(mu_sigma_list[0][0],mu_sigma_list[0][1]),\
#                  "Beta-sheet \
#                  $\mu=%0.3f,\ \sigma=%0.3f$" \
#                  %(mu_sigma_list[1][0],mu_sigma_list[1][1])],\
#                  # "Loop \
#                  # $\mu=%0.3f,\ \sigma=%0.3f$" \
#                  # %(mu_sigma_list[2][0],mu_sigma_list[2][1])],loc=1)
#                  loc=1)
# gca().add_artist(l1)

# plt.legend(loc='upper right')
# plt.legend(loc='lower right',prop={'size':14})
# leg = plt.gca().get_legend()
# leg.draw_frame(False)
