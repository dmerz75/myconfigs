#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

import numpy as np
import numpy.ma as ma

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
# mpl_moving_average
# mpl_forcequench
# mpl_worm

#  ---------------------------------------------------------  #
#  Start matplotlib (1/4)                                     #
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
ax = [ax1]

#  ---------------------------------------------------------  #
#  Import Data! (2/4)                                         #
#  ---------------------------------------------------------  #
result_type = 'gsop' # sop | sopnucleo | gsop | namd
plot_type = 'contact_map' # fe | tension | rmsd | rdf
# data_name = '84' # seed # 153, 72, 216, 84,280,131
# save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))


#  ---------------------------------------------------------  #
#  mpl_myargs_begin                                           #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="select None,publish,show")
    parser.add_argument("-n","--number",help="select None,publish,show",type=int)
    parser.add_argument("-z","--zoom_select",help="select None,publish,show",type=int)
    # 1 (or None)
    parser.add_argument("-c","--correlation",help="select None,publish,show")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
option = args['option']
number = args['number']


#  ---------------------------------------------------------  #
#  Import Data! (3/4)                                         #
#  ---------------------------------------------------------  #

data_name = str(number)
combined_name = '%s_%s_%s' % (result_type, plot_type, data_name)

if data_name == '153':
    data = np.loadtxt(os.path.join(my_dir,'gsop/5_alpha158/sbd_a158__2khosbd__153_1635976__01-26-2015_1834/contact_maps_new/ref_contact_map.out'))
elif data_name == '72':
    data = np.loadtxt(os.path.join(my_dir,'gsop/7_equil_ibi1/equillong-ibi1-result__2khosbd__2/contact_maps_new/ref_contact_map.out'))
elif data_name == '216':
    data = np.loadtxt(os.path.join(my_dir,'gsop/6_equil/equillong__2khosbd__216_5409737__04-09-2015_1404/contact_maps_new/ref_contact_map.out'))
elif data_name == '84': # created reference
    data = np.loadtxt(os.path.join(my_dir,'sopnucleo/hsp70nbd_2bil_int/too-large-int-atpadp-defaults/adp-default/adp-def_runsopnuc__84__04-17-2014_0014__84_621235/contact_maps_new/ref_contact_map.out'))
elif data_name == '131':
    data = np.loadtxt(os.path.join(my_dir,'sopnucleo/hsp70nbd_unsignedint/atp/sopnuc_atp_unsigned_sopnucleo__07-01-2014__131_1098398/contact_maps_new/ref_contact_map.out'))
elif data_name == '280':
    data = np.loadtxt(os.path.join(my_dir,'gsop/gsop_nbd_doubled-4-11-139-169/nbd_orig2x4-11-139-169__2kho__280_7743741__09-03-2014_1021/contact_maps_new/ref_contact_map.out'))

print type(data)
print data.shape # 240, 382


#  ---------------------------------------------------------  #
#  Data Manipulation --> correlations                         #
#  ---------------------------------------------------------  #
def contact_correlation(data,start=0,stop=-1,step=1):
    if stop > data.shape[0] or stop == -1:
        print 'change stop'
        # stop = data.shape[0]
        print 'stop',stop
    print data.shape
    data = data[start:stop,::]
    print data.shape
    stop = stop - start
    start = 0
    print start,stop,step
    # sys.exit()
    matrix_corr = np.zeros((data.shape[0],data.shape[1],data.shape[1]),dtype=float)
    matrix_num_r1 = np.zeros((data.shape[1]),dtype=float)
    print 'r1',matrix_num_r1.shape,type(matrix_num_r1)
    # print matrix_num_r1
    # print matrix_corr.shape
    # print matrix_corr
    # matrix_avg = np.zeros(data.shape[0],dtype=float)
    # x = data[::,3] # 0.7, 0.775, 2.1208, 3.2875
    # print np.average(x)

    matrix_avg = np.average(data,axis=0)
    # print matrix_avg.shape # 383
    matrix_avg2 = matrix_avg ** 2
    data2 = data ** 2
    matrix_2_avg = np.average(data2,axis=0)
    # print matrix_avg # array [ 0.7 0.775 2.1208 ]
    # print matrix_avg2
    sigma = np.sqrt(matrix_2_avg - matrix_avg2)

    # numerator
    for i in range(start,stop,step):
        # print i # 0,239
        for j in range(data.shape[1]): # 0,382 ??
            for k in range(data.shape[1]): # 0,382 ??
                if k < j:
                    pass
                # print j,k # 0,0 --> 0,239 --> 1,2,3 ... 239,239
                matrix_num_r1 = (data[i,j] - matrix_avg[j]) * (data[i,k] - matrix_avg[k]) / (sigma[j] * sigma[k])
                matrix_corr[i,j,k] = matrix_num_r1

    for i in range(start,stop,step):
        print matrix_corr[i,::,::].shape
        print matrix_corr[i,::,::]
        for n in range(data.shape[1]):
            print matrix_corr[i,n,n]
        # print max(matrix_corr[i,::,::])
        print matrix_corr[i,::,::]
        # print matrix_corr[1,i,i]
    return matrix_corr

if args['correlation'] == 'y' or args['correlation'] == 'yes':
    # corr = contact_correlation(data,0,17,1)
    corr = contact_correlation(data,18,36,1)
    print corr.shape,corr
    # sys.exit()
    # plt.contour(xi, yi, zi, v, linewidths=0.5, colors='k')
    # plt.contourf(xi, yi, zi, v, cmap=plt.cm.jet)
    # corr = corr[0,-1,::]

    # plt.imshow(corr[16],cmap='Spectral',aspect='auto')
    # plt.imshow(corr[17],cmap='Spectral',aspect='auto')
    plt.imshow(corr[17],cmap='Spectral',aspect='auto',vmin=-1.0,vmax=1.0)

    # plt.imshow(np.transpose(corr[0]),cmap='Spectral',aspect='auto')
    # plt.imshow(np.fliplr(corr[0]),cmap='Spectral',aspect='auto')
    # plt.imshow(np.flipud(corr[0]),cmap='Spectral',aspect='auto')
    # corr = corr[0,::-1,::]
    # plt.imshow(corr,cmap='Spectral',aspect='auto')
    x = plt.colorbar()
    ax1.set_xlim(0,382)
    ax1.set_ylim(0,382)
    plt.show()
    sys.exit()


print type(data)
vmin = 0
vmax = 12

for i,d1 in enumerate(data):
    # print max(d1.shape[0])
    # print 'frame',i,len(data[0,::])
    # for index in range(len(data[0,::])):
    #     if data[i,index] > data[0,index]:
    #         print 'alert:',i,'ref_contact:',data[0,index],index,'current:',data[i,index]

    if i % 1 == 0:
        # pass
        zmask1 = ma.masked_greater(data[i,::],vmax)
        z_corr = zmask1.filled(12)
        data[i,::] = z_corr

try:
    print max(data[5,::])
    print max(data[72,::])
except IndexError:
    pass

# zmask1 = ma.masked_less(z_arr,vmin) # mask everything < -10
# z_corr = zmask1.filled(20)
# # print type(z_corr)
# zmask2 = ma.masked_greater(z_corr,vmax)
# z_corr = zmask2.filled(80)

# plt.clim(0,16)
# cmap.set_bad(color = 'r', alpha = 1.)
# cmap.set_over('r',vmax)
# cmap.set_under('r',vmin)

cmap = plt.get_cmap('summer')
v = np.linspace(0.0, 12.0, 7)
# plt.contour(xi, yi, zi, v, linewidths=0.5, colors='k')
# plt.contourf(xi, yi, zi, v, cmap=plt.cm.jet)


# 20 - 80
# plt.pcolormesh(data, ylist, Z, cmap = plt.get_cmap('summer'),vmin=vmin,vmax=vmax)
# plt.colorbar()
plt.imshow(data,aspect='auto')
# imshow(random.rand(8, 90), interpolation='nearest', aspect='auto')
x = plt.colorbar(ticks=v)
# plt.colorbar()
# cmap.set_over('r',vmax)
# cmap.set_under('r',vmin)





#  ---------------------------------------------------------  #
#  Make final adjustments: (4/4)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
# matplotlib.rcParams[''] =

# plt.subplots_adjust(left=0.180,right=0.960,top=0.950,bottom=0.160)
# font_prop_large = matplotlib.font_manager.FontProperties(size='large')
# fig.set_size_inches(9.0,5.1)
# for k in matplotlib.rcParams.keys():
#     print k
# dct_font = {'family':'sans-serif',
#             'weight':'normal',
#             'size'  :'28'}
# matplotlib.rc('font',**dct_font)
# matplotlib.rcParams['legend.frameon'] = False
# matplotlib.rcParams['figure.dpi'] = 900
# print matplotlib.rcParams['figure.dpi']

# mpl_label
# mpl_xy: set_xlim,set_ylim,xticks,yticks
ax1.set_xlim(-0.1,382.1)
ax1.set_xticks([39,115,186,228,306])

if args['zoom_select'] == 1:
    ax1.set_xlim(170,240)
    ax1.set_ylim(72,34)
    combined_name = combined_name + '_z1'


plt.tick_params(axis='x',which='major',width=4,length=11,color='r',labelsize=16,\
                direction='out')


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

if option == 'show':
    plt.show()
    sys.exit()
elif option == 'publish':
    matplotlib.rcParams['figure.dpi'] = 1200
    data_name = data_name + '_PUB'
    print "calling save_fig ..."
    # save_pic_data(levels_back,subdir,name)
    # example: save_fig(-4,'fig',name)
    # example: save_fig(-3,'',name)
    save_fig(0,'fig',combined_name)
else:
    print 'saving image .. at dpi %d' % matplotlib.rcParams['figure.dpi']
    plt.savefig('fig/%s.png' % combined_name)
