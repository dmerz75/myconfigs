#!/usr/bin/env python
import sys
import os
import time
from glob import glob
import numpy as np
from numpy import ma

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  expand for moving_average                                  #
#  ---------------------------------------------------------  #
# mpl_moving_average


#  ---------------------------------------------------------  #
#  Start matplotlib (1/3)                                     #
#  ---------------------------------------------------------  #
from pylab import *
import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
fig = plt.figure(0)

gs = GridSpec(3,1)
ax1 = plt.subplot(gs[0,:])
ax2 = plt.subplot(gs[1,:])
ax3 = plt.subplot(gs[2,:])

matplotlib.rcParams['lines.linewidth'] = 3

#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
result_type = 'sopnucleo2_multi_redblue' # sop | sopnucleo | gsop | namd
plot_type = 'tension' # fe | tension | rmsd | rdf

run_type = 'sopnucleo' # sopnucleo | gsop
nucleotide = 'atp' # None | 'adp'

seed = 84 # 280, 84, 131
if seed == 280:
    # front to front
    # lst_frames = [(1050,1250),(2600,3000),(8700,9100),(9700,10100),(11600,12000)]
    # lst_frames = [(1050,1250),(2600,3000),(8200,9200),(9700,10100),(11600,12000)]
    # modified to move 9200 over
    lst_frames = [(1050,1200),(2700,3000),(8200,8800),(9200,10000),(11700,12000)]
elif seed == 84:
    # lst_frames = [(4400,4800),(4800,5200),(18800,19200)]
    lst_frames = [(4400,4700),(4800,5100),(18800,19100)]
elif seed == 131:
    # lst_frames = [(i,i+200) for i in range(3900,4700,200)] # 3900,4100 etc ..
    lst_frames = [(3900,4900),(11150,12150),(15350,16350)]

# frames = lst_frames[0] # (1100,1250),(2700,2900),(8800,9000),(9800,10000),(11700,11900)
# frames = lst_frames[1] # (1100,1250),(2700,2900),(8800,9000),(9800,10000),(11700,11900)
frames = lst_frames[2] # (1100,1250),(2700,2900),(8800,9000),(9800,10000),(11700,11900)
# # ^-84,131,  v-280
# frames = lst_frames[3] # (1100,1250),(2700,2900),(8800,9000),(9800,10000),(11700,11900)
# frames = lst_frames[4] # (1100,1250),(2700,2900),(8800,9000),(9800,10000),(11700,11900)

# data_name = '%d-%d-%d' % (seed,frames[0],frames[1])
data_name = '%d' % (seed)


lst_colors = ['k-','r-','g-','b-','c-','m-']
# for i,path in enumerate(glob(os.path.join(my_dir,'pyten*.dat'))):
# for i,path in enumerate(glob(os.path.join(my_dir,'tensionaverage_2KHO*.dat'))):
# -rwxrwxrwx 1 root root 2.8K 10.13.2014 15:55 ten_chi/tensionaverage_2KHO_280_1100_1150.dat*
# -rwxrwxrwx 1 root root 2.7K 10.13.2014 15:58 ten_chi/tensionaverage_2KHO_280_2700_2800.dat*
# -rwxrwxrwx 1 root root 2.7K 10.13.2014 16:04 ten_chi/tensionaverage_2KHO_280_8900_9000.dat*
# -rwxrwxrwx 1 root root 2.7K 10.13.2014 16:07 ten_chi/tensionaverage_2KHO_280_9900_10000.dat*
# -rwxrwxrwx 1 root root 2.7K 10.13.2014 16:09 ten_chi/tensionaverage_2KHO_280_11700_11800.dat*
lst_ten = glob(os.path.join(my_dir,'ten_chi/tensionaverage_*.dat'))
# print lst_ten
# print len(lst_ten)
# sys.exit()


lst_multi = [os.path.join(my_dir,'ten_chi/tensionaverage_ADP_84_4400_4500.dat'),\
             os.path.join(my_dir,'ten_chi/tensionaverage_ADP_84_5100_5200.dat'),\
             os.path.join(my_dir,'ten_chi/tensionaverage_ADP_84_18900_19000.dat')]
# ten_chi/tensionaverage_ADP_84_18800_18900.dat
# ten_chi/tensionaverage_ADP_84_18900_19000.dat * 4 - 3rd
# ten_chi/tensionaverage_ADP_84_19000_19100.dat
# ten_chi/tensionaverage_ADP_84_19100_19200.dat
# ten_chi/tensionaverage_ADP_84_19200_19300.dat
# ten_chi/tensionaverage_ADP_84_4400_4500.dat * 2 - 1st
# ten_chi/tensionaverage_ADP_84_4500_4600.dat
# ten_chi/tensionaverage_ADP_84_4600_4700.dat
# ten_chi/tensionaverage_ADP_84_4700_4800.dat
# ten_chi/tensionaverage_ADP_84_4800_4900.dat
# ten_chi/tensionaverage_ADP_84_4900_5000.dat
# ten_chi/tensionaverage_ADP_84_5000_5100.dat
# ten_chi/tensionaverage_ADP_84_5100_5200.dat * 3 - 4th
# ten_chi/tensionaverage_ADP_84_5200_5300.dat


dct_ten = {}
for path in lst_ten:
    # print path
    num = int(path.split('/')[-1].split('_')[3])
    dct_ten[num] = path


# sys.exit()




# for k,v in dct_ten.iteritems():
#     print k,v
# print len(dct_ten.keys())
# sys.exit()

# lst_all = lst_ten[0:2:] # 28
# lst_all = lst_ten[2:4:] # 72
# lst_all = lst_ten[4:6:] # 89
# lst_all = lst_ten

def dct_slicer(dct,low,high):
    print low,high
    # sys.exit()
    dct_slice = {key: value for key,value in dct.items() if \
                 key >= low and key <= high}
    for k,v in dct_slice.iteritems():
        print k,v
    # sys.exit()
    return dct_slice

# keep on files of interest!
dct_selected = dct_slicer(dct_ten,frames[0],frames[1])
print len(dct_selected),dct_selected.keys()
# sys.exit()

# for i,path in enumerate(lst_all):
# for i,frame in enumerate(sorted(dct_ten.keys())):
# for i,frame in enumerate(sorted(dct_selected.keys())):
for i,path in enumerate(lst_multi):
    print i,path
    # print i,frame
    # y = np.loadtxt(dct_ten[frame])
    y = np.loadtxt(path)
    print y.shape
    if nucleotide != None:
        y = y[:382:]
    y = y * 70
    # y
    y1 = ma.array(y)
    y2 = ma.masked_less(y,-10) # mask everything < -10
    y2 = y2.filled(-10) # Fill with zeroes
    y = y2
    # for i in range(len(y)):
    #     print y[i],y1[i],y2[i]

    print y.shape
    print max(y)
    x = np.linspace(1,y.shape[0],y.shape[0])
    # print x
    # plt.plot(x,y,lst_colors[i])
    if i == 0:
        ax1 = plt.subplot(gs[0,:])
        # plt.plot(x,y,'b-',alpha=0.7)
        line1 = plt.plot(x,y,'k-')
    if i == 1:
        ax2 = plt.subplot(gs[1,:],sharex=ax1,sharey=ax1)
        # plt.plot(x,y,'darkorange',alpha=0.85)
        line2 = plt.plot(x,y,'k-')
    if i == 2:
        ax3 = plt.subplot(gs[2,:],sharex=ax1,sharey=ax1)
        # plt.plot(x,y,'c-',alpha=0.7)
        line3 = plt.plot(x,y,'k-')


    # # if i == 1:
    # #     break



#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# plt.subplots_adjust(left=0.145,right=0.980,top=0.980,bottom=0.175)
# plt.subplots_adjust(left=0.155,right=0.955,top=0.895,bottom=0.175)
# font_prop_large = matplotlib.font_manager.FontProperties(size='large')
# fig.set_size_inches(11.0,6.4)
fig.set_size_inches(7.0,8.8)
# for k in matplotlib.rcParams.keys():
#     print k
# dct_font = {'family':'sans-serif',
#             'weight':'normal',
#             'size'  :'36'}
# matplotlib.rc('font',**dct_font)
# matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rcParams['font.size'] = 20.0
# print matplotlib.rcParams['figure.dpi']





fig.subplots_adjust(hspace=0)
# plt.ylabel('Force (pN)')
fig.text(0.02, 0.6, "Force (pN)", rotation="vertical", va="center")
plt.xlabel('Residue #')

ax1.set_xlim(0.0,382)
ax1.set_ylim(-24,330)
plt.yticks([0,100,200,300])

# ax1.set_xlabel('')
# print ax1.get_xticklabels()

yticklabels = ax1.get_yticklabels()
setp(yticklabels, fontsize=20.0)
yticklabels = ax2.get_yticklabels()
setp(yticklabels, fontsize=20.0)
yticklabels = ax3.get_yticklabels()
setp(yticklabels, fontsize=20.0)

xticklabels = ax1.get_xticklabels()
setp(xticklabels, visible=False)
xticklabels = ax2.get_xticklabels()
setp(xticklabels, visible=False)
xticklabels = ax3.get_xticklabels()
setp(xticklabels, fontsize=20.0)

ax3.set_xlabel('Residue #')


ax1.legend(line1,['Iholo1'],loc=2)
ax2.legend(line2,['Iholo2'],loc=2)
ax3.legend(line3,['Iholo3'],loc=3)

# if seed == 84:
#     ax1.set_ylim(-14,330)
#     plt.yticks([0,50,100,150,200,250,300])
# else:
#     ax1.set_ylim(-14,270)
#     plt.yticks([0,50,100,150,200,250])


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
