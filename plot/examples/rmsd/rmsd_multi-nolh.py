#!/usr/bin/env python
import os,sys,time
import numpy as np

# ./rmsd.py   (on rmsd.dat)

my_dir = os.path.abspath(os.path.dirname(__file__))

def moving_average(x, n, type='simple'):
    """ moving_average
    compute an n period moving average.
    type is 'simple' | 'exponential'
    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
    weights /= weights.sum()
    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

import matplotlib
# matplotlib.use('WxAgg') # Agg
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pylab
fig = plt.figure(0)

plt.subplots_adjust(left=0.14,right=0.96,top=0.89,bottom=0.14)
font_prop_large = matplotlib.font_manager.FontProperties(size='large')


gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])


params = {
    'figure.figsize': [7.3,4.2],
    # 'figure.dpi':900,
    # 'figure.facecolor':0.1,
    # 'figure.edgecolor':'black',

    # 'figure.subplot.left':0.18,
    # 'figure.subplot.right':0.90,
    # 'figure.subplot.top':0.88,
    # 'figure.subplot.bottom':0.19,
    # 'figure.subplot.wspace':0.2,
    # 'figure.subplot.hspace':0.2,

    'font.family':'serif',
    'font.serif':['Verdana'],
    'font.weight':'normal',
    'font.size'  : 21.0,

    'axes.labelsize': 14,
    'xtick.labelsize':8,
    'ytick.labelsize':8,
    'legend.fontsize':18,

    'lines.linewidth': 1.8,
    'legend.markerscale': 1.0,

# legend_control = {'fancybox':False,
#                   'numpoints':3,
#                   'fontsize':'small',
#                   'shadow': False,
#                   # 'frameon':True,
# figure_control = {'dpi'      :80,
#                   'facecolor':0.75,
#                   'edgecolor':'white',
#                   # 'figsize'  :(7.12,4.4),
# }
}
pylab.rcParams.update(params)

# 01-411937/
# 02-136229/
# 03-8724241/
rmsd_1 = np.loadtxt('01-411937/rmsd.dat')
rmsd_2 = np.loadtxt('02-136229/rmsd.dat')
rmsd_3 = np.loadtxt('03-8724241/rmsd.dat')


# x1 = np.linspace(0,rmsd_1.shape[0]/500.0,rmsd_1.shape[0])
x1 = np.linspace(0,rmsd_1.shape[0]/10.0,rmsd_1.shape[0])
plt.plot(x1,rmsd_1,'r-')

# x2 = np.linspace(0,rmsd_2.shape[0]/500.0,rmsd_2.shape[0])
x2 = np.linspace(0,rmsd_2.shape[0]/10.0,rmsd_2.shape[0])
plt.plot(x2,rmsd_2,'g-')

# x3 = np.linspace(0,rmsd_3.shape[0]/500.0,rmsd_3.shape[0])
x3 = np.linspace(0,rmsd_3.shape[0]/10.0,rmsd_3.shape[0])
plt.plot(x3,rmsd_3,'b-')


ax1.legend([r"411937",
            r"136229",
            r"8724241",
        ],
           loc="upper right")


###  LEGEND  # 1,2,3,4 - quadrants
## plt.legend(loc=1,prop={'size':14})
## fpropl=matplotlib.font_manager.FontProperties(size='large')

# ax1.legend([r"Protein","C-Term vs. Protein","C-Term vs. C-Term"],
#            loc=2,
#            prop={'size':18})
leg = plt.gca().get_legend()
leg.draw_frame(False)

plt.ylim([0.85,4.6])
# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])
# ax1.text(0.4,100,'region 3',bbox={'facecolor':'red','alpha':0.3,'pad':7})


plt.xlabel("Time (ns)")
plt.ylabel("Angstroms ($\AA$)")
plt.title("RMSD")

# matplotlib.rcParams['font.family'] = 'Verdana'
# matplotlib.rcParams['font.weight'] = 'normal'
# matplotlib.rcParams['font.size'] = 20.0
# matplotlib.rcParams['axes.titlesize'] = 'large'   # ??
# matplotlib.rcParams['axes.labelsize'] = 'x-small' # ??
# matplotlib.rcParams['xtick.labelsize']= 'x-small'
# matplotlib.rcParams['ytick.labelsize']= 'x-small'
# matplotlib.rcParams['legend.fontsize']= 'large'
# matplotlib.rcParams['legend.markerscale'] = 4.0
# legend_control = {'fancybox':False,
#                   'numpoints':3,
#                   'fontsize':'small',
#                   'shadow': False,
#                   # 'frameon':True,


# font_control = {'family':'Verdana', # monospace,Andale Mono,Comic Sans MS
#                 'weight':'normal',
#                 'size'  :'24',
# }
# matplotlib.rc('font',**font_control)

# axes_control = {'titlesize':'large',
#                 'labelsize':'medium',
# }
# matplotlib.rc('axes',**axes_control)

# legend_control = {'fancybox':False,
#                   'numpoints':3,
#                   'fontsize':'small',
#                   'shadow': False,
#                   # 'frameon':True,
# }
# matplotlib.rc('legend',**legend_control)

# figsubplot_control = {'left'  :0.18,
#                       'right' :0.98,
#                       'top'   :0.88,
#                       'bottom':0.13,
#                       'wspace':0.1,
#                       'hspace':0.1,
# }
# matplotlib.rc('figure.subplot',**figsubplot_control)

# figure_control = {'dpi'      :80,
#                   'facecolor':0.75,
#                   'edgecolor':'white',
#                   # 'figsize'  :(7.12,4.4),
# }
# matplotlib.rc('figure',**figure_control)


def save_pic_data(i,subdir,fname,dpi=200):
    if subdir == '':
        content_dir = my_dir
    else:
        content_dir = os.path.join('/'.join(my_dir.split('/')[0:i]),subdir)
    if not os.path.exists(content_dir): os.makedirs(content_dir)
    abs_file_name = os.path.join(content_dir,fname)
    plt.savefig('%s.png' % abs_file_name,dpi=dpi)
    plt.savefig('%s.eps' % abs_file_name,dpi=dpi)
    # plt.savefig('%s.jpg' % abs_file_name)
    os.chdir(content_dir)
    #pickle.dump(pmf_2d,open('%s.pkl' % fname,'w'))
    #np.savetxt('%s.dat' % fname,pmf_2d,fmt=['%3.4f','%3.11f'],delimiter=' ')

# save_pic_data(levels_back,subdir,name)
# example: save_pic_data(-4,'fig',name)
# example: save_pic_data(-3,'',name)
# default: save_pic_data(0,'','mypic')
# plt.show()
save_pic_data(0,'','rmsd_mult-nolh')
