#!/usr/bin/env python
import sys
import os
import time
import re
import numpy as np
import numpy.ma as ma
from glob import glob

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--option",help="options: show,publish,NONE ...")
    parser.add_argument("-n","--number",help="number of subplots",type=int)
    # parser.add_argument("-s","--seed",help="seed, 84,131,280")
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
option = args['option']
number_plot = args['number']
# seed = args['seed']

# print 'seed:',seed,type(seed)
print 'option:',option,type(option),'\n','number_plot:',number_plot,type(number_plot)
# print type(number_plot),number_plot

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


gs = GridSpec(1,number_plot,wspace=0.08,hspace=0.01)
if number_plot >= 1:
    # print 'adding 1 ..'
    ax1 = plt.subplot(gs[0,0])
    ax = [ax1]
if number_plot >= 2:
    # print 'adding 2 ..'
    ax2 = plt.subplot(gs[0,1])
    ax = [ax1,ax2]
if number_plot >= 3:
    # print 'adding 3 ..'
    ax3 = plt.subplot(gs[0,2])
    ax = [ax1,ax2,ax3]
if number_plot >= 4:
    # print 'adding 4 ..'
    ax4 = plt.subplot(gs[0,3])
    ax = [ax1,ax2,ax3,ax4]
if number_plot >= 5:
    # print 'adding 5 ..'
    ax5 = plt.subplot(gs[0,4])
    ax = [ax1,ax2,ax3,ax4,ax5]
if number_plot >= 6:
    # print 'adding 6 ..'
    ax6 = plt.subplot(gs[0,5])
    ax = [ax1,ax2,ax3,ax4,ax5,ax6]


#  ---------------------------------------------------------  #
#  Import Data! (2/3)                                         #
#  ---------------------------------------------------------  #
subdir = 'unfolding2_alt3rd' # full_investigation, bigger, gump, unfolding1 (84,280 only), unfolding2 (131,84,280), +tert2tert (84)
plot_type = 'hsa_%s' % subdir # fe | tension | rmsd | rdf
# data_name = '280' # seed # 131-6,280-4,84-5 | fullinvestigation
data_name = '84' # seed # 131-5,280-6,84-5 | bigger


if data_name == '280':
    result_type = 'gsop' # sop | sopnucleo | gsop | namd
else:
    result_type = 'sopnucleo'

combined_name = '%s_%s_%s' % (result_type,plot_type + '_v4',data_name)
# save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))

def get_hsa(dirname=''):
    if data_name == '84':
        hsa_84 = 'sopnucleo/hsp70nbd_2bil*/too-large-int-*/adp-default/adp-def_*__84_*/%s/hsa*.dat' % dirname
    elif data_name == '280':
        hsa_84 = 'gsop/gsop_nbd_doubled*/nbd_*280*/%s/hsa*.dat' % dirname
    elif data_name == '131':
        hsa_84 = 'sopnucleo/hsp70nbd_unsignedint/atp/sopnuc_atp_unsigned_sopnucleo__07-01-2014__131_1098398/%s/hsa*.dat' % dirname

    lst_hsa = glob(os.path.join(my_dir,hsa_84))
    print lst_hsa
    # for h in lst_hsa:
    #     print h
    # print lst_hsa
    # sys.exit()
    # print lst_hsa,len(lst_hsa)


    dct_hsa = {}
    for i,h in enumerate(lst_hsa):
        match = re.search('_f(\d+)',h.split('/')[-1])
        resids= re.search('_r(\d+)-(\d+)',h.split('/')[-1])
        res_label = ('-').join(resids.groups())
        # print match
        if match:
            # print match.group(1),type(match.group(1))
            dct_hsa[int(match.group(1))] = {}
            dct_hsa[int(match.group(1))]['path'] = h
            dct_hsa[int(match.group(1))]['resids'] = res_label

    # for k,v in dct_hsa.iteritems():
    #     print k,v

    legend_loc = []

    for i,k in enumerate(sorted(dct_hsa.keys())):
        print i,k
        hsa = np.loadtxt(dct_hsa[k]['path'])
        # print hsa.shape
        frame = hsa[::,0]/1000
        # print frame
        sasa = hsa[::,1]
        # print area

        # identify subplot
        ax[i] = plt.subplot(gs[0,i])

        # black horizontal bar
        s = plt.axhline(0.5,color='black')
        # s = plt.axhline(0.5,color='black',label=dct_hsa[k]['resids'])

        # SASA
        # plt.plot(frame,sasa,'r-',label=dct_hsa[k]['resids'])
        below = ma.masked_greater(sasa,0.5)
        above = ma.masked_less_equal(sasa,0.5)

        print len(below)
        print len(above)

        # first: more below (RED) b/c less masked
        if ma.count_masked(below) < ma.count_masked(above):
            plt.plot(frame,below,'r-',label=dct_hsa[k]['resids'])
            plt.plot(frame,above,'b-')
            legend_loc.append((i,2))
        else:
            plt.plot(frame,below,'r-')
            plt.plot(frame,above,'b-',label=dct_hsa[k]['resids'])
            legend_loc.append((i,4))


    return dct_hsa,legend_loc

dct_hsa,legend_loc = get_hsa(plot_type) # plot_type (subdir name, hsa_bigger)


#  ---------------------------------------------------------  #
#  Make final adjustments: (3/3)                              #
#  mpl - available expansions                                 #
#  ---------------------------------------------------------  #
plt.subplots_adjust(left=0.05,right=0.980,top=0.970,bottom=0.290)
fig.set_size_inches(24.5,4.0)
plt.subplots_adjust(wspace=0.1)


# plt.ylabel('Force (pN)')
# fig.text(0.14, 0.6, "HSA Ratio", rotation="vertical", va="center")
ax1.set_ylabel("HSA Ratio")
fig.text(0.44, 0.04, "Frame # (x 1000)", va="center")
# plt.xlabel('Residue #')

# plt.title('RMSD')
# Y
# plt.ylabel("Force (pN)")
# ax1.set_ylim(-12,342)

# X
# if plot_type == 'extension':
#     plt.xlabel('Extension (nm)')
#     ax1.set_xlim(-2,82)
# elif plot_type == 'time':
#     plt.xlabel('t (ms)')
#     ax1.set_xlim(-0.5,38)
# elif plot_type == 'frame':
#     pass


# for obj in dir(ax1):
#     print obj


# from matplotlib.ticker import MaxNLocator
# my_locator = MaxNLocator(5)
# Set up axes and plot some awesome science
# ax1.yaxis.set_major_locator(my_locator)

# if data_name == '131':
#     lst_xlims = [[2000,2400],[4900,5300],[12100,12500],[14500,14900],[16300,16700],[24300,24700]]
#     lst_xticks = [[2000,2100,2200,2300,2400],\
#                   [4900,5000,5100,5200,5300],\
#                   [12100,12200,12300,12400,12500],\
#                   [14500,14600,14700,14800,14900],\
#                   [16300,16400,16500,16600,16700],\
#                   [24300,24400,24500,24600,24700]]
#     lst_xlims = [[i[0]/1000.0,i[1]/1000.0] for i in lst_xlims]
#     xt = np.array(lst_xticks) / 1000.0
#     lst_xticks = xt
#     # [[print_out(z/1000.0) for z in i] for i in lst_xticks]
# elif data_name == '84':
#     lst_xlims = [[2000,2400],[5000,5400],[6000,6400],[7800,8200],[19200,19600]]
#     lst_xticks = [[2000,2100,2200,2300,2400],\
#                   [5000,5100,5200,5300,5400],\
#                   [6000,6100,6200,6300,6400],\
#                   [7800,7900,8000,8100,8200],\
#                   [19200,19300,19400,19500,19600]]
#     lst_xlims = [[i[0]/1000.0,i[1]/1000.0] for i in lst_xlims]
#     xt = np.array(lst_xticks) / 1000.0
#     lst_xticks = xt
# elif data_name == '280':
#     lst_xlims = [[3000,3400],[7400,7800],[8900,9300],[14500,14900]]
#     lst_xticks = [[3000,3100,3200,3300,3400],\
#                   [7400,7500,7600,7700,7800],\
#                   [8900,9000,9100,9200,9300],\
#                   [14500,14600,14700,14800,14900]]
#     lst_xlims = [[i[0]/1000.0,i[1]/1000.0] for i in lst_xlims]
#     xt = np.array(lst_xticks) / 1000.0
#     lst_xticks = xt

# for i in range(len(ax)):
#     print i
#     print ax[i].get_axes()
#     print ax[i].get_ybound()
#     print ax[i].get_ylim()[0]

#     if i == 0:
#         pass
#     else:
#         # print 'making invisible'
#         ax[i].set_yticklabels('',visible=False)

#     # ax[i].tick_params(axis='both',labelsize=14.0)
#     # ax[i].locator_params(axis='both',nbins=4)
#     # ax.locator_params(tight=True, nbins=4)

#     ax[i].set_xlim(lst_xlims[i])
#     ax[i].set_xticks(lst_xticks[i])

#     if data_name == '131':
#         ax[i].set_ylim(0.28,1.01)
#         ax[i].set_yticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
#     elif data_name == '280':
#         ax[i].set_ylim(0.18,1.02)
#         ax[i].set_yticks([0.2,0.4,0.6,0.8,1.0])
#     elif data_name == '84':
#         ax[i].set_ylim(0.18,1.02)
#         ax[i].set_yticks([0.2,0.4,0.6,0.8,1.0])



#     for label in ax[i].legend().get_lines():
#         label.set_linewidth(5.0)

#     if (data_name == '131') or (data_name == '280'):
#         handles,labels = ax[i].get_legend_handles_labels()
#         ax[i].legend(handles,labels,prop={'size':14},loc=4)
#     else:
#         handles,labels = ax[i].get_legend_handles_labels()
#         ax[i].legend(handles,labels,prop={'size':14},loc=2)



# We change the fontsize of minor ticks label
# plt.tick_params(axis='both', which='major', labelsize=10)
# plt.tick_params(axis='both', which='minor', labelsize=8)
# plt.xticks(np.linspace(0.0,32.0,17),fontsize=10)
# ax1.set_xticks(np.linspace(0,32.0,17),fontsize=10)

# ax1.xaxis.set_major_locator(np.linspace(0.0,32.0,5.0))
# ax1.xaxis.set_minor_locator(np.linspace(0,32.0,17))

# majorFormatter = FormatStrFormatter('%d')
# ax1.tick_params(which='both', width=1)
# ax1.tick_params(which='major', length=9)
# ax1.tick_params(which='minor', length=5, color='k')



for i in range(len(ax)):

    ax[i].tick_params(which='both', labelsize=20)

    if i == 0:
        pass
    else:
        # print 'making invisible'
        ax[i].set_yticklabels('',visible=False)


    ax[i].set_xlim(ax[i].get_xbound()[0]-0.03,ax[i].get_xbound()[1]+0.03)
    ax[i].set_ylim(0.18,1.04)
    # ax[i].set_yticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])

    if data_name == '131':
        if i <=1:
            minorLocator = matplotlib.ticker.MultipleLocator(0.1)
            majorLocator = matplotlib.ticker.MultipleLocator(0.2)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
        elif i == 2:
            minorLocator = matplotlib.ticker.MultipleLocator(0.1)
            majorLocator = matplotlib.ticker.MultipleLocator(0.3)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
        else:
            minorLocator = matplotlib.ticker.MultipleLocator(0.25)
            majorLocator = matplotlib.ticker.MultipleLocator(0.5)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)

    elif data_name == '280':
        if 1:
            minorLocator = matplotlib.ticker.MultipleLocator(0.1)
            majorLocator = matplotlib.ticker.MultipleLocator(0.3)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
        else:
            minorLocator = matplotlib.ticker.MultipleLocator(0.05)
            majorLocator = matplotlib.ticker.MultipleLocator(0.1)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
            ax[i].set_ylim(0.18,1.04)
            # ax[i].set_yticks([0.2,0.4,0.6,0.8,1.0])

    elif data_name == '84':
        if i == 3:
            minorLocator = matplotlib.ticker.MultipleLocator(0.25)
            majorLocator = matplotlib.ticker.MultipleLocator(1.0)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
        else:
            minorLocator = matplotlib.ticker.MultipleLocator(0.1)
            majorLocator = matplotlib.ticker.MultipleLocator(0.4)
            ax[i].xaxis.set_minor_locator(minorLocator)
            ax[i].xaxis.set_major_locator(majorLocator)
            # ax[i].set_yticks([0.2,0.4,0.6,0.8,1.0])

    # plot_number = sorted(dct_hsa.keys())[i]
    # label = dct_hsa[plot_number]['resids']
    # print label,type(label)
    # ax[i].legend(str(label),loc=2,prop={'size':18})

    handles,labels = ax[i].get_legend_handles_labels()
    # print handles
    # print labels
    ax[i].legend(handles,labels,prop={'size':26.0},loc=legend_loc[i][1])
    leg = ax[i].get_legend()
    for label in leg.get_lines():
        label.set_linewidth(3.5)


for i in range(len(ax)):
    print i
    print ax[i].get_axes()
    print ax[i].get_ybound()
    print ax[i].get_xbound()
    print ax[i].get_ylim()[0]
    labs = ax[i].get_xticklabels()
    for label in labs:
        label.set_rotation(60)




    # for k,v in dct_hsa.iteritems():
    #     print k,v


    # for obj in dir(ax[i].legend()):
    #     print obj
    # print dir(handles)
    # for obj in handles:
    #     print obj

# legend
# 1:
# handles,labels = ax1.get_legend_handles_labels()
# ax1.legend(handles,labels,prop={'size':10})
# 2:
# lst_labels = ['','',]
# ax1.legend(lst_labels,loc=2,prop={'size':18})
# 3:
# lst_labels = ['','',]
# leg = plt.gca().get_legend()
# for label in leg.get_lines():
#     label.set_linewidth(2.5)

    # yticklabels = ax[i].get_yticklabels()
    # setp(yticklabels, fontsize=8.0)
    # xticklabels = ax[i].get_xticklabels()
    # setp(xticklabels, fontsize=8.0)




    # plt.xlabel('Frame # (x 1000)')
    # ax1.set_xlim(-0.5,9.5)
    # plt.xticks(np.linspace(0,9.0,19),fontsize=10)
# ax3.set_xticks(np.linspace(0,32.0,17))
# # Changing the label's font-size
# ax1.tick_params(axis='x',labelsize=8)
# ax2.tick_params(axis='x',labelsize=8)
# ax3.tick_params(axis='x',labelsize=8)

# ax1.set_xlim(-0.1,4.1)
# ax1.set_ylim(-0.1,6.1)
# plt.xticks([0.0,1.0,2.0,3.0,4.0])
# plt.yticks([0,1,2,3,4,5,6])
# ax1.xaxis.set_major_locator(my_locator)

# lst_labels = ['','',]
# # legend
# from matplotlib.ticker import MaxNLocator
# my_locator = MaxNLocator(5)
# Set up axes and plot some awesome science
# ax1.yaxis.set_major_locator(my_locator)


# if re.search('hsa',plot_type):
#     for i in range(len(ax)):
#         print i
#         handles, labels = ax[i].get_legend_handles_labels()
#         ax[i].legend(handles, labels,prop={'size':10})

        # ax[i].yaxis.set_major_locator(my_locator)
        # ax[i].xaxis.set_major_locator(my_locator)
# ax1.legend(lst_labels,loc=2,prop={'size':18})
# leg = plt.gca().get_legend()
# for label in leg.get_lines():
#     label.set_linewidth(2.5)

# mpl_savefig

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
    print 'writing ',fp_filename,' at ',dpi
    plt.savefig('%s.png' % dir_filename,dpi=dpi)
    plt.savefig('%s.png' % fp_filename,dpi=dpi)
    plt.savefig('%s.eps' % fp_filename,dpi=dpi)
    plt.savefig('%s.svg' % fp_filename,dpi=dpi)
    plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
    plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
    plt.savefig('%s.jpg' % fp_filename,dpi=dpi)

print option
if option == 'show':
    plt.show()
    sys.exit()
elif option == 'publish':
    matplotlib.rcParams['figure.dpi'] = 1200
    # data_name = data_name + '_PUB'
    combined_name = combined_name  + '_PUB'
    print "calling save_fig ..."
    # save_pic_data(levels_back,subdir,name)
    # example: save_fig(-4,'fig',name)
    # example: save_fig(-3,'',name)
    # save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
    save_fig(0,'fig',combined_name)
else:
    print 'saving dpi=300 (default) image ..'
    # plt.savefig('fig/%s_%s_%s.png' % (result_type,plot_type,data_name))
    print 'writing ',combined_name,' at ',matplotlib.rcParams['figure.dpi']
    plt.savefig('fig/%s' % combined_name)
