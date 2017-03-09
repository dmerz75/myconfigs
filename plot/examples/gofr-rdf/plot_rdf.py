#!/usr/bin/env python
import sys
import os
import time
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
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
# print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'namd'
plot_type = 'pmf_gofr'
data_name = 'sbd'

# -rwxrwxrwx 1 root root 9.0K 10.28.2014 15:36 gofr_protein_protein_20.dat*
# -rwxrwxrwx 1 root root 9.0K 10.28.2014 15:37 gofr_protein-resid-397-501_protein-resid-397-501_20.dat*
# -rwxrwxrwx 1 root root 9.0K 10.28.2014 15:39 gofr_protein-resid-509-603_protein-resid-509-603_20.dat*

cb = 'gofr_protein_protein_20.dat'
datb = np.loadtxt(cb)
x = datb[::,0] * 0.1
gr = datb[::,1]
# print gr[-1]
# gr = gr / 6.9
gr = gr / gr[-1]
y = -0.6 * np.log(gr)
# plt.plot(x,gr,'k-')
plt.plot(x,y,'k-')

cbr = 'gofr_protein-resid-397-501_protein-resid-397-501_20.dat'
data = np.loadtxt(cbr)
x = data[::,0] * 0.1
gr = data[::,1]
# print gr[-1]
# gr = gr / 10.79
gr = gr / gr[-1]
y = -0.6 * np.log(gr)
# plt.plot(x,gr,'r-')
plt.plot(x,y,'r-')


cbr = 'gofr_protein-resid-509-603_protein-resid-509-603_20.dat'
data = np.loadtxt(cbr)
x = data[::,0] * 0.1
gr = data[::,1]
# print gr[-1]
# gr = gr / 8.39
gr = gr / gr[-1]
y = -0.6 * np.log(gr)
# plt.plot(x,gr,'b.')
plt.plot(x,y,'g-')


# # Lennard-Jones
# r0 = 0.480
# xlj = np.linspace(0.466,2.0,200)
# V = 4 * 1.44 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
# plt.plot(xlj,V)



# V = 4 * 1.75 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
# plt.plot(xlj,V)
# V = 4 * 2.0 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
# plt.plot(xlj,V)

# lst_labels = ['PMF (namd)','PMF-10 frames-no norm','PMF-10 frames-norm','PMF-250 frames-norm','LJ(eh): 0.73','LJ(eh): 1.75','LJ(eh): 2.0']
# print V.shape,V
# # sys.exit()

lst_labels = ['PMF','PMF I','PMF II','LJ']


#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.155,right=0.96,top=0.895,bottom=0.175)
fig.set_size_inches(7.4,5.1)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')
dct_font     = {'family':'sans-serif',
                'weight':'normal',
                'size'  :'20',
}
matplotlib.rc('font',**dct_font)

# plt.title('RMSD')
plt.ylabel('Energy (kcal/mol)')
plt.xlabel('r (nm)')

ax1.set_xlim(0.38,2.02)
ax1.set_ylim(-1.6,1.55)
plt.xticks([0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0])
# plt.yticks([0,1,2,3,4,5,6])

# LEGEND
# locations: quadrants - 1,2,3,4
# lst_labels = ['sec1','sec2','sec3']
# lst_labels = ['g(r)']
# lst_labels = lst_labels
try:
    ax1.legend([lst_labels[0],
                lst_labels[1],
                lst_labels[2],
                lst_labels[3],
                # lst_labels[4],
                # lst_labels[5],
                # lst_labels[6]
            ],
               loc=1,
               prop={'size':16})
except:
    ax1.legend([lst_labels[0],
            ],
               loc=1,
               prop={'size':16})
leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(2.5)
    leg.draw_frame(False)

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
    dpi = 80
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

# print "calling save_fig ..."
# save_pic_data(levels_back,subdir,name)
# example: save_fig(-4,'fig',name)
# example: save_fig(-3,'',name)
# save_fig(0,'fig','fname_%s' % idn)
# save_fig(0,'fig','example1')
save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
