#!/usr/bin/env python
import sys
import os
import time

import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  expand for moving_average                                  #
#  ---------------------------------------------------------  #
def moving_average(x, n, type='simple'):
    """ compute an n period moving average.
    type is 'simple' | 'exponential'
    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
    weights /= weights.sum()
    a =  np.convolve(x, weights, mode='full')[:len(x)]
    # a[:n] = a[n]
    ma = a[n:]
    # print ma
    # print len(ma)
    # sys.exit()
    return ma


#  ---------------------------------------------------------  #
#  Start matplotlib (1/3)                                     #
#  ---------------------------------------------------------  #
import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('Agg')
# matplotlib.use('ps')
# matplotlib.use('TKAgg')
print matplotlib.__version__
print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax1 = plt.subplot()
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'namd' # sop | sopnucleo | gsop | namd
plot_type = 'rmsd_final' # fe | tension | rmsd | rdf
data_name = '3' # 3 | 5

def load_rmsd(filename):
    rmsd = np.loadtxt(filename,skiprows=1)
    print rmsd.shape
    x = np.linspace(0,rmsd.shape[0]/10,rmsd.shape[0])
    x = moving_average(x,50)
    y = moving_average(rmsd[::,1],50)
    return x,y

def plot_rmsd(x,y,color):
    plt.plot(x,y,color)


fn_protein = 'rmsd/trajrmsd_protein.dat'
fn_protein_3 = 'rmsd/trajrmsd_protein_397-501.dat'
fn_protein_5 = 'rmsd/trajrmsd_protein_509-603.dat'
fn_3 = 'rmsd/trajrmsd_397-501.dat'
fn_5 = 'rmsd/trajrmsd_509-603.dat'


if data_name == '3':
    lst_files = [fn_protein,fn_protein_3,fn_3]
    lst_labels = ['Protein',r"Protein vs. \textbf{$\beta$} subdomain",r"\textbf{$\beta$} subdomain"]
    # lst_labels = ['Protein',"Protein vs. beta subdomain","beta subdomain"]
else:
    lst_files = [fn_protein,fn_protein_5,fn_5]
    lst_labels = ['Protein',r'Protein vs. \textbf{$\alpha$}-helical lid',r'\textbf{$\alpha$}-helical lid']
    # lst_labels = ['Protein','Protein vs. alpha-helical lid','alpha-helical lid']

lst_colors = ['k-','r-','g-']

for i,fn in enumerate(lst_files):
    x,y = load_rmsd(fn)
    plot_rmsd(x,y,lst_colors[i])




#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# plt.subplots_adjust(left=0.140,right=0.960,top=0.940,bottom=0.200)
# fig.set_size_inches(9.0,5.1)
# font_prop_large = matplotlib.font_manager.FontProperties(size='large')
# for k in matplotlib.rcParams.keys():
#     print k
# dct_font = {'family':'sans-serif',
#             'weight':'normal',
#             'size'  :'28'}
# matplotlib.rc('font',**dct_font)
# matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rc('text',usetex=True)
# print matplotlib.rcParams['figure.dpi']


# plt.title('RMSD')
plt.ylabel(r'RMSD ($\AA$)')
plt.xlabel('Time (ns)')
# plt.xlabel('$\beta$')

ax1.set_xlim(-2,102)
ax1.set_ylim(-0.3,6.1)
plt.xticks([0,25,50,75,100])
plt.yticks([0,1,2,3,4,5,6])

# LEGEND
# locations: quadrants - 1,2,3,4

if data_name == '3':
    ax1.legend([lst_labels[0],
                lst_labels[1],
                lst_labels[2],
            ],
               loc=2,)
               # prop={'size':16})
else:
    ax1.legend([lst_labels[0],
                lst_labels[1],
                lst_labels[2],
                # lst_labels[3],
            ],
               loc=4,)
               # prop={'size':16})

leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(3.5)
#     leg.draw_frame(False)



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
save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
# save_fig(0,'fig','rmsd_%s' % idn)
