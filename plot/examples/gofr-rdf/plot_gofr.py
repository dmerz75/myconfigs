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
fig = plt.figure(0)

gs = GridSpec(1,1)
ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'namd' # sop | sopnucleo | gsop | namd
plot_type = 'rdf' # fe | tension | rmsd | rdf
data_name = 'sbd' # seed #

fn_prot = 'gofr/gofr_protein_and_name_CB_20_450-525.dat'
fn_3 = 'gofr/gofr_protein_and_name_CB_20_450-525_397-501.dat'
fn_5 = 'gofr/gofr_protein_and_name_CB_20_450-525_509-603.dat'


def load_gofr(fn):
    data = np.loadtxt(fn_prot)
    print data.shape
    x = data[::,0] * 0.1
    gr = data[::,1]
    gr = gr / gr[-1]

    c = ma.masked_less_equal(gr,0)
    count_zeros = ma.count(c)
    # print count_zeros
    c = ma.compressed(c)

    y = -0.6 * np.log(c)
    # plt.plot(x,gr,'r-')
    print plot_type
    if plot_type == 'gofr':
        return x,gr
    elif plot_type == 'rdf':
        # print y
        # print x.shape - count_zeros
        return x[x.shape - count_zeros::],y


def plot_gofr(x,y,color_line):
    plt.plot(x,y,color_line)


# lst_gofr = [fn_prot,fn_3,fn_5]
lst_gofr = [fn_prot] # ,fn_3,fn_5]
lst_colors = ['k-','r-','g-']

# if plot_type == 'gofr':
for i,g in enumerate(lst_gofr):
    print i,g
    x,y = load_gofr(g)
    plot_gofr(x,y,lst_colors[i])


if plot_type == 'rdf':
    # Lennard-Jones
    r0 = 0.490
    xlj = np.linspace(0.466,2.0,200)

    V = 4 * 1.35 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
    plt.plot(xlj,V,'r-')

    V = 4 * 1.20 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
    plt.plot(xlj,V,'b-')

    # V = 4 * 2.0 * ((r0 / xlj) ** 12 - (r0 / xlj) ** 6)
    # plt.plot(xlj,V)

    # lst_labels = ['PMF (namd)','PMF-10 frames-no norm','PMF-10 frames-norm','PMF-250 frames-norm','LJ(eh): 0.73','LJ(eh): 1.75','LJ(eh): 2.0']
    # print V.shape,V
    # sys.exit()
    lst_labels = ['PMF','LJ (1.35)','LJ (1.20)']



#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #


# plt.title('RMSD')
plt.ylabel('g(r)')
plt.xlabel('r($\AA$)')


if plot_type == 'gofr':
    ax1.set_xlim(-0.1,2.05)
elif plot_type == 'rdf':
    plt.subplots_adjust(left=0.180,right=0.970,top=0.930,bottom=0.210)
    ax1.set_xlim(0.2,2.05)
    plt.yticks([-1.5,-1.0,-0.5,0.0,0.5,1.0])
    ax1.set_ylim(-1.8,1.3)



# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])


# LEGEND
# locations: quadrants - 1,2,3,4
# lst_labels = ['sec1','sec2','sec3']
# lst_labels = lst_seeds
try:
    ax1.legend([lst_labels[0],
                lst_labels[1],
                lst_labels[2],
                # lst_labels[3],
            ],
               loc=4,)
    # prop={'size':16})
except:
    ax1.legend([lst_labels[0],
            ],
               loc=4,)
    # prop={'size':16})
leg = plt.gca().get_legend()
for label in leg.get_lines():
    label.set_linewidth(3.5)
    # leg.draw_frame(False)

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
