#!/usr/bin/env python
import sys
import os
import time

import numpy as np
from glob import glob

my_dir = os.path.abspath(os.path.dirname(__file__))

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# imports from my_library
from mylib.cp import *
from mylib.regex import *
# from plot.wlc import WormLikeChain
from plot.SOP import *
from mdanalysis.MoleculeUniverse import MoleculeUniverse


psf = os.path.join(my_dir,'../495917.psf')
dcd = os.path.join(my_dir,'nolh495917.dcd')

print psf,dcd

# def __init__(self,workdir,psf,dcd,destdir,idn):

# is it shifted?
# bd = MoleculeUniverse(my_dir,psf,dcd,my_dir,'495917')
# bd.get_bond_distance(10,56,264)
# bd.get_bond_distance(10,55,267)


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
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'namd' # sop | sopnucleo | gsop | namd
plot_type = 'bond' # fe | tension | rmsd | rdf
data_name = '495917' # seed #


# bond_55 = 'bond_distance_495917_55_267_step10.dat' # RED
# bond_56 = 'bond_distance_495917_56_264_step10.dat' # BLUE
# b5 = np.loadtxt(bond_55)
# b6 = np.loadtxt(bond_56)



# -rwxrwxrwx 1 root root 4.9K 11.12.2014 21:01 bond_distance_495917_56_264_step10.dat*
# -rwxrwxrwx 1 root root 5.2K 11.12.2014 21:01 bond_distance_495917_55_267_step10.dat*

lst_colors = ['r-','b-']
for i,path in enumerate(glob(os.path.join(my_dir,'*_step10.dat'))):
    print path
    data = np.loadtxt(path)
    print data.shape
    plt.plot(data[::,0]/10,data[::,1],lst_colors[i])



#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# plt.subplots_adjust(left=0.180,right=0.960,top=0.950,bottom=0.160)
# # font_prop_large = matplotlib.font_manager.FontProperties(size='large')
# # fig.set_size_inches(9.0,5.1)
plt.subplots_adjust(right=0.95)
# # for k in matplotlib.rcParams.keys():
# #     print k
# dct_font = {'family':'sans-serif',
#             'weight':'normal',
#             'size'  :'28'}
# matplotlib.rc('font',**dct_font)
# # matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rcParams['figure.dpi'] = 900
# print matplotlib.rcParams['figure.dpi']

# plt.title('RMSD')
plt.ylabel('Bond Distance ($\AA$)')
plt.xlabel('Time (ns)')

# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
plt.xticks([0,100,200,300,400])
# plt.yticks([0,1,2,3,4,5,6])
# from matplotlib.ticker import MaxNLocator
# my_locator = MaxNLocator(6)
# Set up axes and plot some awesome science
# ax1.yaxis.set_major_locator(my_locator)
# ax1.xaxis.set_major_locator(my_locator)

lst_labels = ['55 - 267','56 - 264']
# legend
ax1.legend(lst_labels,loc=2,prop={'size':18})
leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(2.5)

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
    # dpi = 300 # 300,900
    # matplotlib.rcParams['figure.dpi'] = 900
    dpi = matplotlib.rcParams['figure.dpi']
    plt.savefig('%s.png' % dir_filename,dpi=dpi)
    plt.savefig('%s.png' % fp_filename,dpi=dpi)
    plt.savefig('%s.eps' % fp_filename,dpi=dpi)
    plt.savefig('%s.svg' % fp_filename,dpi=dpi)
    plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
    plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
    plt.savefig('%s.jpg' % fp_filename,dpi=dpi)

try:
    if sys.argv[1] == 'show':
        fig.set_size_inches(5.0,4.0)
        matplotlib.rcParams['figure.dpi'] = 80
        plt.show()
        sys.exit()
    elif sys.argv[1] == 'publish':
        matplotlib.rcParams['figure.dpi'] = 1200
        data_name = data_name + '_PUB'
except IndexError:
        pass
print "calling save_fig ..."
# save_pic_data(levels_back,subdir,name)
# example: save_fig(-4,'fig',name)
# example: save_fig(-3,'',name)
# save_fig(0,'fig','fname_%s' % idn)
# save_fig(0,'fig','example1')
save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
