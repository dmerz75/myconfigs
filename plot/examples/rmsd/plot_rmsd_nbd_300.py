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
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #

def load_rmsd(filename):
    rmsd = np.loadtxt(filename,skiprows=1)
    print rmsd.shape
    x = np.linspace(0,rmsd.shape[0]/10,rmsd.shape[0])
    x = moving_average(x,50)
    y = moving_average(rmsd[::,1],50)
    return x,y

def plot_rmsd(x,y,color):
    plt.plot(x,y,color)


idn = 'align' # back, pr, align, domain

lst_labels = ['Ala','102377','495917','864904']
bb_102 = 'protein_backbone_align-start_rmsd_102377.dat'
bb_495 = 'protein_backbone_align-start_rmsd_495917.dat'
bb_864 = 'protein_backbone_align-start_rmsd_864904.dat'
bb_ala = 'protein_backbone_align-start_rmsd_ala.dat'
pr_102 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_102377.dat'
pr_495 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_495917.dat'
pr_864 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_864904.dat'
pr_ala = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_ala.dat'
al_102 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_align_102377.dat'
al_495 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_align_495917.dat'
al_864 = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_align_864904.dat'
al_ala = 'protein_backbone_align-start_rmsd_resid187-385_rmsd_align_ala.dat'

lst_labels = ['Protein','C-Term vs. Protein','C-Term vs. C-Term']
# rmsd_by_domain = [bb_ala,pr_ala,al_ala]
# rmsd_by_domain = [bb_102,pr_102,al_102]
# rmsd_by_domain = [bb_495,pr_495,al_495]
rmsd_by_domain = [bb_864,pr_864,al_864]
idn = 'domain_864'

if idn == 'back':
    x,y = load_rmsd(bb_ala)
    plot_rmsd(x,y,'k-')
    x,y = load_rmsd(bb_102)
    plot_rmsd(x,y,'r-')
    x,y = load_rmsd(bb_495)
    plot_rmsd(x,y,'g-')
    x,y = load_rmsd(bb_864)
    plot_rmsd(x,y,'b-')
elif idn == 'pr':
    x,y = load_rmsd(pr_ala)
    plot_rmsd(x,y,'k-')
    x,y = load_rmsd(pr_102)
    plot_rmsd(x,y,'r-')
    x,y = load_rmsd(pr_495)
    plot_rmsd(x,y,'g-')
    x,y = load_rmsd(pr_864)
    plot_rmsd(x,y,'b-')
elif idn == 'align':
    lst_files = [al_ala,al_102,al_495,al_864]
    lst_colors = ['k-','r-','g-','b-']
    for i,f in enumerate(lst_files):
        x,y = load_rmsd(f)
        plot_rmsd(x,y,lst_colors[i])
elif idn.startswith('domain'):
    lst_colors = ['k-','r-','g-','b-']
    for i,f in enumerate(rmsd_by_domain):
        x,y = load_rmsd(f)
        plot_rmsd(x,y,lst_colors[i])



#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.155,right=0.96,top=0.895,bottom=0.175)
fig.set_size_inches(7.4,5.1)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')
run_control     = {'family':'sans-serif',
                   'weight':'normal',
                   'size'  :'24',
}
matplotlib.rc('font',**run_control)

plt.title('RMSD')
plt.ylabel('RMSD ($\AA$)')
plt.xlabel('Time (ns)')

ax1.set_xlim(-5,305)
ax1.set_ylim(-0.4,5.5)
plt.xticks([0,50,100,150,200,250,300])
plt.yticks([0,1,2,3,4,5,6])

# LEGEND  
# locations: quadrants - 1,2,3,4

ax1.legend([lst_labels[0],
            lst_labels[1],
            lst_labels[2],
            # lst_labels[3],
        ],
           loc=4,
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
save_fig(0,'fig','rmsd_%s' % idn)

