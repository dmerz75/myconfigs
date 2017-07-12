import matplotlib
# default - Qt5Agg
# print matplotlib.rcsetup.all_backends
# matplotlib.use('GTKAgg')
# matplotlib.use('TkAgg')
# print 'backend:',matplotlib.get_backend()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# fig = plt.figure(0)

# gs = GridSpec(1,1)
# ax1 = plt.subplot(gs[0,:])
# ax2 = plt.subplot(gs[1,:-1])

import os
import sys
import time
import numpy as np
import pickle
import re
import glob
import numpy.ma as ma

# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
from mylib.moving_average import *

# def moving_average(x, n, type='simple'):
#     """ compute an n period moving average.
#     type is 'simple' | 'exponential'
#     """
#     x = np.asarray(x)
#     if type=='simple':
#         weights = np.ones(n)
#     else:
#         weights = np.exp(np.linspace(-1., 0., n))
#     weights /= weights.sum()
#     a =  np.convolve(x, weights, mode='full')[:len(x)]
#     # a[:n] = a[n]
#     ma = a[n:]
#     # print ma
#     # print len(ma)
#     # sys.exit()
#     return ma


# def Apply_Residue_Layout():
#     ''' Apply standard residue layout.
#     '''
#     alphal = 0.8
#     alphag = 0.6
#     alphah = 0.6
#     ax2.axvspan(0,170,color='orange',alpha=alphal)
#     ax2.axvspan(170,186,color='m',alpha=alphal)
#     ax2.axvspan(187,380,color='cyan',alpha=alphal)
#     # shifted -4
#     ax2.axvspan(381,393,color='m',alpha=alphal)
#     ax2.axvspan(394,415,color='lime',alpha=alphag)
#     ax2.axvspan(416,422,color=(0.0,0.9,0.5),alpha=alphag)
#     ax2.axvspan(423,456,color='lime',alpha=alphag)
#     ax2.axvspan(457,486,color=(0.0,0.9,0.5),alpha=alphag)
#     ax2.axvspan(487,496,color=(0.0,0.9,0.5),alpha=alphag)
#     ax2.axvspan(497,505,color='gray',alpha=alphah) # connecting loop
#     ax2.axvspan(506,518,color='r',alpha=alphah)
#     ax2.axvspan(519,552,color='r',alpha=alphal)
#     ax2.axvspan(553,575,color='r',alpha=alphah)
#     ax2.axvspan(576,591,color='r',alpha=alphal)
#     ax2.axvspan(592,599,color='r',alpha=alphah)
#     ax2.axvspan(600,664,color='gray',alpha=alphah)

#     tsize = 10.0
#     theight = 0.33
#     ax2.text(57,theight,"Lobe I",fontsize=tsize)
#     ax2.text(252,theight,"Lobe II",fontsize=tsize)

#     ax2.text(392,theight,"12",fontsize=tsize)
#     ax2.text(415,theight,"3",fontsize=tsize)
#     ax2.text(430,theight,"45",fontsize=tsize)
#     ax2.text(458,theight,"678",fontsize=tsize)
#     ax2.text(506,theight,"A  B   C",fontsize=tsize)
#     ax2.text(576,theight,"D",fontsize=tsize)
#     ax2.text(591,theight,"E",fontsize=tsize)


#     # Final:
#     ax1.set_ylabel('Frame #')
#     ax1.set_xlabel('Residue #')
#     plt.subplots_adjust(hspace=0.0,wspace=0.05,bottom=0.18,top=0.94,right=0.92,left=0.17)


#     # xticks = [170,385,461,510,602]
#     xticks = [170,385,496,598]
#     xlabels = ['170','385','500','602']
#     ax1.set_xticks(xticks)
#     ax1.set_xticklabels(xlabels)
#     ax1.tick_params(axis='x',which='major',width=5,length=12,color='r',labelsize=16,\
#                     direction='out',pad=0.0)
#     ax1.tick_params(axis='y',which='major',width=2,length=10,labelsize=18,\
#                     direction='out',pad=0.0)
#     ax1.xaxis.set_ticks_position('bottom')
#     ax1.yaxis.set_ticks_position('left')



class PlotSop():
    """ The plotting class for SOP,GSOP,and SOPNucleo trajectories.
    """
    def __init__(self,**kwargs):
    # def __init__(self,job_type,point_start=0,point_stop=310000,ma_value=100,step=1,\
    #              ts=18.67,nav=10000,\
    #              dcdfreq=200000,outputtiming=100000,
    #              seam='down'):
        """ Initialization of key parameters.

        function: gsop
        --> nav
        --> start
        --> stop
        --> step (..to skip data points ..)
        --> ma
        --> ts
        --> dcdfreq
        --> outputtiming

        my_library = os.path.expanduser('~/.pylib')
        sys.path.append(my_library)
        from plot.gsop import PlotSop

        plotsop = PlotSop(job_type='gsop',nav=1000,start=0,stop=1000000,
        ma=50,ts=20.0,dcdfreq=200000,outputtiming=200000)
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        # defaults:
        if 'step' not in kwargs:
            setattr(self,'step',1)
            # self.step = 1


    def print_class(self):
        ''' Print class and its attributes.
        '''
        for key in dir(self):
            print key,getattr(self,key)

    def load_data(self,path):

        # print 'loading data for:',path
        print os.path.relpath(os.path.dirname(path))
        print ('/').join(path.split('/')[-2:])

        # npy-name
        bn = os.path.basename(path)
        fp = os.path.dirname(path)
        npy = re.sub('.dat','.npy',bn)
        fp_npy = re.sub('.dat','.npy',path)

        print "DAT: time last modified: %s" % time.ctime(os.path.getmtime(fp))

        try:
            print "NPY: time last modified: %s" % time.ctime(os.path.getmtime(fp_npy))
            if (os.path.getmtime(fp) <= os.path.getmtime(fp_npy)) == True:
                print "DATFILE: is older than npy. proceed."
            else:
                print "DATFILE: is newer than npy. remaking now!!!"
                os.remove(fp_npy)
        except OSError:
            pass

        # npy-load
        if os.path.exists(fp_npy):
            print 'loading npy ..'
            data = np.load(fp_npy)
            print data.shape
        else:
            print 'loading data (not yet npy)'
            data = np.loadtxt(path)
            print data.shape
            np.save(fp_npy,data)
        self.data = data


    def process_data(self,percent=1.0):
        if self.job_type == 'gsop':
            ''' self. force vs. indentation,frame,time_array_ms (IFT)
            not actually correct ... because of the extension being linearly spaced.
            '''
            print "Develop: June 7, 2016. in testing. 'gsop'"

            # Data:
            col1 = self.data[::,0] # 1st column
            print 'col1 length:',len(col1),col1[-1]
            navdatagap = col1[-1] / (len(col1) - 1)
            print  'navdatagap:',col1[-1] / (len(col1) - 1),'nav:',self.nav

            portion = self.stop - self.start
            print 'start-stop:',self.start,self.stop
            print 'portion_arr:',portion
            # print
            # sys.exit()

            # Force manipulations:
            # f_raw = data[self.point_start:self.point_stop:self.step,4] # 5th column
            f_raw = self.data[self.start:self.stop:self.step,3] # from gsop147/gsop4, 4th column
            size_arr = len(f_raw) - self.ma        # SIZE_ARR

            frame_fraction = float(size_arr * self.step) / len(col1)
            # sys.exit()

            ma_step = int(float(size_arr)/self.ma)
            f_ma = moving_average(f_raw,self.ma)  # moving_average
            f70 = f_raw * 70.0
            f70 = np.delete(f70,np.arange(0,size_arr,ma_step))
            # f_raw_ma2 = moving_average(f_raw,)
            f_pico = f_ma * 70.0                        # pico Newtons
            f_nano = f_ma * 0.07                         # nano Newtons !check?? 0.7?

            if (len(f_pico) != len(f_nano)) or (len(f_pico) != size_arr):
                print 'WARNING: fpico != fnano != size_arr. exiting'
                sys.exit()

            # Extension manipulations:
            end_to_end = self.data[self.start:self.stop:self.step,1] * 0.1 # 2nd column A to nm
            # size_arr = len(end_to_end) - self.ma        # SIZE_ARR
            ext_raw = end_to_end - end_to_end[0]        # in nanometers.
            # ext_step = float(self.ma)/float(size_arr) + 1

            # ext_step_arr = ext_raw[::ext_step]
            # print 'ext_step:',ext_step
            # sys.exit()
            ext = moving_average(ext_raw,self.ma)       # no longer averaging ext_raw
            # print 'ext_short size:',len(ext_raw)
            ext_short = np.delete(ext_raw,np.arange(0,size_arr,ma_step))
            # print 'ext_short size(l):',len(ext_short)
            # ext_smooth = moving_average(ext_raw,s)
            # print ext_raw.shape
            # print size_arr
            # print ext_raw
            # print result
            # print result.shape
            # sys.exit()
            distance = abs(ext[-1] - ext[0])         # total distance traveled
            # distance = abs(max(ext) - min(ext))         # total distance traveled
            ext_linear = np.linspace(0,distance,size_arr)


            # Time/Steps:
            # total_steps = self.outputtiming * len(end_to_end)
            # total_steps = self.nav * len(end_to_end)
            # total_steps = float(self.point_stop - self.point_start) * self.nav
            # total_steps = col1[-1] * self.nav
            numlines = len(col1)
            total_steps = numlines * self.nav - self.nav
            print 'total_steps:',total_steps
            # sys.exit()
            timeps = self.ts * total_steps
            # timeps = total_steps * timestep
            # timeps = self.ts * self.steps
            timens = timeps * 0.001
            timeus = timens * 0.001
            timems = timeus * 0.001
            # time_array = np.linspace(0,timems,size_arr)
            # time_array = time_array[self.start:self.stop]
            time_last = frame_fraction * timems
            time_array = np.linspace(0,time_last,size_arr)

            # Frames:
            frame_maxlast = total_steps / self.dcdfreq
            frame_last = frame_fraction * frame_maxlast
            frame = np.linspace(0,frame_last,size_arr)


            # --------- Printing ------------------
            # extension / force printed:
            print 'extension/force:'
            print ' end_to_end:',end_to_end[0],end_to_end[-1]
            print ' ext:',ext[0],ext[-1]
            # print ' z_coordinate:',z_coordinate[0],z_coordinate[-1],min(z_coordinate)
            print ' distance:',distance
            print ' ext_linear:',ext_linear[0],ext_linear[-1]
            print ' force:',len(f_raw),'points of which the max is:',max(f_raw)
            print ' force(pico):',max(f_pico),'force(nano):',max(f_nano)

            # frames
            print 'frames:'
            print ' dcdfreq:',self.dcdfreq
            print ' outputtiming:',self.outputtiming
            print ' data_points:',len(end_to_end)
            print ' column1:',col1[0],col1[-1]
            print ' total steps:',total_steps
            print ' frames_last:',frame_last
            print ' frame:',frame[0:5],'..',frame[-5:],len(frame)

            # time
            print 'time:'
            print ' total steps:',total_steps
            # print ' assuming timestep(200):',timestep
            # print ' time(ps):',timeps
            # print ' time(ns):',timens
            print ' time(ms):',timems
            print ' time_array:',time_array,len(time_array)

            # plotted: force vs. extension, time, frame
            print 'array size:',size_arr
            self.f_raw = f_raw
            self.f_pico = f_pico
            self.f70 = f70
            self.end_to_end = end_to_end
            self.ext_raw = ext_raw
            self.force = f_pico # or nano if using mt
            self.ext_short = ext_short
            self.ext = ext
            self.extension = ext
            self.ext_linear = ext_linear
            self.time = time_array
            self.time_array_ms = time_array
            self.frame = frame

            print '---force vs. extension/time/frame---'
            print 'force_len:(%d)' % len(self.force),self.force[-1]
            print 'extension_len:(%d)' % len(self.extension),self.extension[-1]
            print 'ext_linear_len:(%d)' % len(self.ext_linear),self.ext_linear[-1]
            print 'time:(%d)' % len(self.time),self.time[-1]
            print 'frame:(%d)' % len(self.frame),self.frame[-1]


            # Get Barrier:
            total_length = len(self.force)
            interval = total_length / 1000.0

            # idx = (np.abs(self.time_array_ms - 10.0)).argmin()
            # print 'idx:',idx
            # idx_step = idx / 6.1
            # print 'idx_step:',idx_step
            # print self.extension[0:idx:idx/idx_step]
            # print self.frame[0:idx:idx/idx_step]
            # print self.time_array_ms[0:idx:idx/idx_step]

            percentage = float(percent) * 0.01
            p_ext = self.extension[-1] * percentage
            # print p_ext
            p_time = self.time_array_ms[-1] * percentage
            # print p_time
            p_frame = self.frame[-1] * percentage
            print 'ext/time/frame:',p_ext,p_time,p_frame

            dct_barrier = {}
            dct_barrier['ext'] = {}
            dct_barrier['time'] = {}
            dct_barrier['frame'] = {}
            dct_barrier['interval'] = interval

            dct_barrier['ext']['start'] = self.extension[0] - p_ext
            dct_barrier['ext']['stop'] = self.extension[-1] + p_ext

            dct_barrier['time']['start'] = self.time_array_ms[0] - p_time
            dct_barrier['time']['stop'] = self.time_array_ms[-1] + p_time

            dct_barrier['frame']['start'] = self.frame[0] - p_frame
            dct_barrier['frame']['stop'] = self.frame[-1] + p_frame

            self.barrier = dct_barrier


    def describe_data(self,percent=1.0):
        ''' self. extension,force,frame,time_array_ms
        '''
        if self.job_type == 'mt':
            print 'data points ..'
            print 'Indentation:',len(self.extension),self.extension[0],self.extension[-1]
            print 'Force:',len(self.force),'force_max:',max(self.force),'force_final:',self.force[-1]
            print 'Time_total:',len(self.time_array_ms),self.time_array_ms[-1]
            print 'FRAMES:',self.frame[-1]

            # total_length = len(self.force)
            # interval = total_length / 1000.0

            # print 'Extension,frame,time comparison ...'
            # idx = (np.abs(self.time_array_ms - 10.0)).argmin()
            # print 'idx:',idx
            # idx_step = idx / 6.1
            # print 'idx_step:',idx_step
            # print self.extension[0:idx:idx/idx_step]
            # print self.frame[0:idx:idx/idx_step]
            # print self.time_array_ms[0:idx:idx/idx_step]

            # percentage = float(percent) * 0.01
            # p_ext = self.extension[-1] * percentage
            # print p_ext
            # p_time = self.time_array_ms[-1] * percentage
            # print p_time
            # p_frame = self.frame[-1] * percentage
            # print p_frame

        else:
            # print 'Extension:',len(self.extension),self.extension[0],self.extension[-1]
            # print 'Force_len:',len(self.force),'force_max:',max(self.force),'force_final:',self.force[-1]
            # print 'Time points:',len(self.time_array_ms),'Total time:',self.time_array_ms[-1]
            # print 'LAST_FRAME:',self.frame[-1]

            total_length = len(self.force)
            interval = total_length / 1000.0


            # print 'Extension,frame,time comparison ... skipped for now'
            # return

            idx = (np.abs(self.time_array_ms - 10.0)).argmin()
            print 'idx:',idx
            idx_step = idx / 6.1
            print 'idx_step:',idx_step
            # print self.extension[0:idx:idx/idx_step]
            # print self.frame[0:idx:idx/idx_step]
            # print self.time_array_ms[0:idx:idx/idx_step]

            percentage = float(percent) * 0.01
            p_ext = self.extension[-1] * percentage
            # print p_ext
            p_time = self.time_array_ms[-1] * percentage
            # print p_time
            p_frame = self.frame[-1] * percentage
            print 'ext/time/frame:',p_ext,p_time,p_frame

            dct_barrier = {}
            dct_barrier['ext'] = {}
            dct_barrier['time'] = {}
            dct_barrier['frame'] = {}
            dct_barrier['interval'] = interval

            dct_barrier['ext']['start'] = self.extension[0] - p_ext
            dct_barrier['ext']['stop'] = self.extension[-1] + p_ext

            dct_barrier['time']['start'] = self.time_array_ms[0] - p_time
            dct_barrier['time']['stop'] = self.time_array_ms[-1] + p_time

            dct_barrier['frame']['start'] = self.frame[0] - p_frame
            dct_barrier['frame']['stop'] = self.frame[-1] + p_frame
            self.barrier = dct_barrier

    def get_analysis(self,dirname,atype):
        '''
        Get analysis. Tension/CosTheta, Contacts, Chi.
        '''

        if atype == 'tension':
            self.fp_tension =  glob.glob(os.path.join(dirname,'tension_*.dat'))[0]
            self.data_tension = np.loadtxt(self.fp_tension)
        if atype == 'costheta':
            self.fp_costheta = glob.glob(os.path.join(dirname,'costheta_*.dat'))[0]
            self.data_costheta = np.loadtxt(self.fp_costheta)
        if atype == 'chi':
            self.fp_chi = glob.glob(os.path.join(dirname,'chi_*.dat'))[0]
            self.data_chi = np.loadtxt(self.fp_chi)
        if atype == 'contacts':
            self.fp_contacts_intra = glob.glob(os.path.join(dirname,'contacts_intra*.dat'))[0]
            self.fp_contacts_residue = glob.glob(os.path.join(dirname,'contacts_by_residue*.dat'))[0]
            self.data_contacts_intra = np.loadtxt(self.fp_contacts_intra)
            self.data_contacts_residue = np.loadtxt(self.fp_contacts_residue)

            # reshaping:
            num_res = self.data_contacts_intra.shape[1] # 664
            size_arr = self.data_contacts_residue.shape[0] # 1376472 / 664 = 2073
            num_frames = self.data_contacts_residue.shape[0] / self.data_contacts_intra.shape[1] # 2073
            last_dim = self.data_contacts_residue.shape[1] # 25

            self.data_contacts_residue = self.data_contacts_residue.reshape(
                num_frames,num_res,last_dim)

            print 'reshaped:',self.data_contacts_residue.shape

        # print dir(self)
        # print F.data_chi.shape
        # print F.data_tension.shape
        # print F.data_costheta.shape
        # print self.data_contacts_intra.shape
        # print F.data_contacts_residue.shape
        # (2073, 664)
        # (2073, 663)
        # (2073, 663)
        # (2073, 664)
        # (1376472, 25)



    def Plot_Fext(self,plot_type,color='k'):
        '''
        Plot FE.
        '''
        print "plotting FE."

        if (plot_type == 'ext') or (plot_type == 'extension'):
            plt.plot(self.extension,self.force,color=color)
        elif plot_type == 'frame':
            plt.plot(self.frame,self.force,color=color)
        elif plot_type == 'time':
            plt.plot(self.time_array_ms,self.force,color=color)
        elif plot_type == 'indentation':
            plt.plot(self.extension,self.force,color=color)

    def Plot_Multi(self):
        '''
        Plot Multiple: FE, frame, time.
        '''
        fig = plt.figure(0)
        fig.set_size_inches(8,7)
        gs = GridSpec(1,1)
        plt.subplots_adjust(left=0.210,right=0.930,top=0.940,bottom=0.32)

        ax1 = plt.subplot(gs[0,:])
        ax2 = ax1.twiny()
        ax3 = ax1.twiny()

        gline = ax1.plot(self.ext_short,self.f70,'g-',linewidth=0.4)
        eline = ax1.plot(self.ext_linear,self.force,'k-',linewidth=2.0)
        tline = ax2.plot(self.time,self.force,'b')
        fline = ax3.plot(self.frame,self.force,'m')

        ax1.set_ylabel('Force (pN)',size=24,labelpad=8.0)
        fig.text(0.01,0.26,'Ext. (nm)',color='g',size=18)
        fig.text(0.01,0.18,'Time (ms)',color='b',size=18)
        fig.text(0.01,0.095,'Frame #',color='m',size=18)

        ax2.spines['bottom'].set_color('b')
        ax2.spines['bottom'].set_position(('outward',65.0))
        ax2.xaxis.set_ticks_position('bottom')
        for tick in ax2.xaxis.get_major_ticks():
            tick.label.set_fontsize(16)


        ax3.spines['bottom'].set_color('m')
        ax3.spines['bottom'].set_position(('outward',110.0))
        ax3.xaxis.set_ticks_position('bottom')
        for tick in ax3.xaxis.get_major_ticks():
            tick.label.set_fontsize(16)

        # print '--- --- --- --- --- ---'
        # print self.barrier['ext']['start']
        # print self.barrier['ext']['stop']
        # print self.barrier['time']['start']
        # print self.barrier['time']['stop']
        # print self.barrier['frame']['start']
        # print self.barrier['frame']['stop']

        ax1.set_xlim(self.barrier['ext']['start'],self.barrier['ext']['stop'])
        ax2.set_xlim(self.barrier['time']['start'],self.barrier['time']['stop'])
        ax3.set_xlim(self.barrier['frame']['start'],self.barrier['frame']['stop'])

    def Plot_Tension(self):
        '''
        Plot Multiple: FE, frame, time.
        '''
        data = self.data_tension
        print data.shape

        fig = plt.figure(0)
        fig.set_size_inches(8,5)
        gs = GridSpec(2,2,width_ratios=[11,1],height_ratios=[1,11])
        ax1 = plt.subplot(gs[1,0]) # main
        ax2 = plt.subplot(gs[0,0]) # res_layout
        ax3 = plt.subplot(gs[0,1])
        ax4 = plt.subplot(gs[1,1]) # colorbar
        ax = [ax1,ax2,ax3,ax4]

        cmap = plt.get_cmap('YlOrRd') # seismic, bwr, summer, bwr_r
        vmin = 0.0
        vmax = 320.0

        dm = ma.masked_less(data,vmin)
        dn = dm.filled(vmin)
        do = ma.masked_greater(dn,vmax)
        dp = do.filled(vmax)
        data = dp

        # NEW: .pylib.mylib.moving_average_array
        pdata = moving_average_array(data,5)

        iplot = ax1.imshow(pdata,cmap=cmap,aspect='auto',\
                           extent=[0,
                                   data.shape[1],
                                   data.shape[0],
                                   0],\
                           clim=(vmin,vmax),\
                           interpolation='nearest')
        v = np.linspace(vmin,vmax,6)

        cbar = plt.colorbar(iplot,ticks=v,cax=ax4)
        cbar.ax.tick_params(labelsize=16)
        ax3.axis('off')
        xlim = ax1.get_xlim()
        ax2.set_xlim(xlim[0],xlim[1])
        ax2.axis('off')
        self.Apply_Residue_Layout(ax)

        # x = plt.colorbar(ticks=v)
        # if args['fline'] != None:
        #     flines = args['fline'].split(',')
        #     fcolors = ['k','r','g','b']
        #     for f,fl in enumerate(flines):
        #         ax1.axhline(int(flines[f]),color=fcolors[f])

        # plt.tick_params(axis='x',which='major',width=6,length=14,color='r',labelsize=22,\
        #                 direction='out')
        # plt.tick_params(axis='y',which='major',width=4,length=12,color='m',labelsize=20,\
        #                 direction='out')


        # xlim2 = ax1.get_xlim()[1]
        # xticks = [x for x in [397,427,461,491,523] if (x < xlim2)]
        # ax1.set_xticks(xticks)
        # ax1.set_xticks([397,430,461,491,523])
        # ax1.set_ylabel('Frame #')
        # ax1.set_xlabel('Residue #')


    def Plot_Chi(self):
        '''
        Plot Multiple: FE, frame, time.
        '''
        data = self.data_chi
        print data.shape

        fig = plt.figure(0)
        fig.set_size_inches(8,5)
        gs = GridSpec(2,2,width_ratios=[11,1],height_ratios=[1,11])
        ax1 = plt.subplot(gs[1,0]) # main
        ax2 = plt.subplot(gs[0,0]) # res_layout
        ax3 = plt.subplot(gs[0,1])
        ax4 = plt.subplot(gs[1,1]) # colorbar
        ax = [ax1,ax2,ax3,ax4]

        cmap = plt.get_cmap('bwr') # seismic, bwr, summer, bwr_r
        vmin = 0.5
        vmax = 1.0

        print 'ylimit:',data.shape[0]*2
        iplot = ax1.imshow(data,cmap=cmap,aspect='auto',\
                           extent=[0,
                                   data.shape[1],
                                   data.shape[0],
                                   0],\
                           clim=(vmin,vmax),\
                           interpolation='nearest')
        v = np.linspace(vmin,vmax,6)
        # x = plt.colorbar(ticks=v)

        cbar = plt.colorbar(iplot,ticks=v,cax=ax4)
        cbar.ax.tick_params(labelsize=16)
        ax3.axis('off')
        xlim = ax1.get_xlim()
        ax2.set_xlim(xlim[0],xlim[1])
        ax2.axis('off')
        self.Apply_Residue_Layout(ax)

        # plt.tick_params(axis='x',which='major',width=6,length=14,color='r',labelsize=22,\
        #                 direction='out')
        # plt.tick_params(axis='y',which='major',width=4,length=12,color='m',labelsize=20,\
        #                 direction='out')
        # ax1.set_xticks([397,430,461,491,523])
        # xlim2 = data.shape[1] + 382
        # xticks = [x for x in [397,427,461,491,523] if (x < xlim2)]
        # ax1.set_xticks(xticks)
        # ax1.set_ylabel('Frame #')
        # ax1.set_xlabel('Residue #')

    def Plot_Costheta(self):
        '''
        Plot Multiple: FE, frame, time.
        '''
        data = self.data_costheta
        print data.shape


        fig = plt.figure(0)
        fig.set_size_inches(8,5)
        gs = GridSpec(2,2,width_ratios=[11,1],height_ratios=[1,11])
        ax1 = plt.subplot(gs[1,0]) # main
        ax2 = plt.subplot(gs[0,0]) # res_layout
        ax3 = plt.subplot(gs[0,1])
        ax4 = plt.subplot(gs[1,1]) # colorbar
        ax = [ax1,ax2,ax3,ax4]


        cmap = plt.get_cmap('jet')
        vmin = -1
        vmax = 1
        v = np.linspace(-1.0,1.0,5)

        for i,d in enumerate(data):
            zmask1 = ma.masked_greater(data[i,::],vmax)
            z_corr = zmask1.filled(12)
            data[i,::] = z_corr

        iplot = ax1.imshow(data,cmap=cmap,aspect='auto',extent=[0,data.shape[1],data.shape[0],0],vmin=-1.0,vmax=1.0)

        cbar = plt.colorbar(iplot,ticks=v,cax=ax4)
        cbar.ax.tick_params(labelsize=16)
        ax3.axis('off')
        xlim = ax1.get_xlim()
        ax2.set_xlim(xlim[0],xlim[1])
        ax2.axis('off')
        self.Apply_Residue_Layout(ax)

        # zmask1 = ma.masked_less(z_arr,vmin) # mask everything < -10
        # z_corr = zmask1.filled(20)
        # # print type(z_corr)
        # zmask2 = ma.masked_greater(z_corr,vmax)
        # z_corr = zmask2.filled(80)


    def Plot_Contacts(self):
        '''
        Plot Multiple: FE, frame, time.
        '''
        data = self.data_contacts_residue
        print data.shape

        fig = plt.figure(0)
        fig.set_size_inches(8,5)
        gs = GridSpec(2,2,width_ratios=[11,1],height_ratios=[1,11])
        ax1 = plt.subplot(gs[1,0]) # main
        ax2 = plt.subplot(gs[0,0]) # res_layout
        ax3 = plt.subplot(gs[0,1])
        ax4 = plt.subplot(gs[1,1]) # colorbar
        ax = [ax1,ax2,ax3,ax4]

        new_stack = np.zeros((data.shape[0],data.shape[1]))
        initial_contact_arr = np.zeros(data.shape[1])

        for r in range(data.shape[1]):
            concount0 = len([con for con in data[0,r,1::] if con != -1])
            initial_contact_arr[r] = concount0
            # print r,concount0

        for f in range(data.shape[0]):
            for r in range(data.shape[1]):
                # print data9[f,r,::]

                for con in data[f,r,1::]:
                    if con != -1:
                        # print f,r,con
                        new_stack[f,r] += 1
                        # new_stack[f,int(con-diff_resid-1)] +=1
                        new_stack[f,int(con)] +=1

        # range:
        cmap = plt.get_cmap('jet') # red, yellow, green, blue
        vmin = 0.0
        vmax = 8.0

        # plot:
        iplot = ax1.imshow(new_stack,aspect='auto',
                           extent=[0,
                                   data.shape[1],
                                   data.shape[0],
                                   0],
                           clim=(vmin,vmax),
                           cmap=cmap)
        # ticks:
        v = np.linspace(vmin,vmax,(vmax * 0.5 + 1))

        cbar = plt.colorbar(iplot,ticks=v,cax=ax4)
        cbar.ax.tick_params(labelsize=16)
        ax3.axis('off')
        xlim = ax1.get_xlim()
        ax2.set_xlim(xlim[0],xlim[1])
        ax2.axis('off')
        self.Apply_Residue_Layout(ax)


    def Apply_Residue_Layout(self,ax):
        ''' Apply standard residue layout.
        '''
        alphal = 0.8
        alphag = 0.6
        alphah = 0.6
        ax[1].axvspan(0,170,color='orange',alpha=alphal)
        ax[1].axvspan(170,186,color='m',alpha=alphal)
        ax[1].axvspan(187,380,color='cyan',alpha=alphal)
        # shifted -4
        ax[1].axvspan(381,393,color='m',alpha=alphal)
        ax[1].axvspan(394,415,color='lime',alpha=alphag)
        ax[1].axvspan(416,422,color=(0.0,0.9,0.5),alpha=alphag)
        ax[1].axvspan(423,456,color='lime',alpha=alphag)
        ax[1].axvspan(457,486,color=(0.0,0.9,0.5),alpha=alphag)
        ax[1].axvspan(487,496,color=(0.0,0.9,0.5),alpha=alphag)
        ax[1].axvspan(497,505,color='gray',alpha=alphah) # connecting loop
        ax[1].axvspan(506,518,color='r',alpha=alphah)
        ax[1].axvspan(519,552,color='r',alpha=alphal)
        ax[1].axvspan(553,575,color='r',alpha=alphah)
        ax[1].axvspan(576,591,color='r',alpha=alphal)
        ax[1].axvspan(592,599,color='r',alpha=alphah)
        ax[1].axvspan(600,664,color='gray',alpha=alphah)

        tsize = 10.0
        theight = 0.33
        ax[1].text(57,theight,"Lobe I",fontsize=tsize)
        ax[1].text(252,theight,"Lobe II",fontsize=tsize)

        ax[1].text(392,theight,"12",fontsize=tsize)
        ax[1].text(415,theight,"3",fontsize=tsize)
        ax[1].text(430,theight,"45",fontsize=tsize)
        ax[1].text(458,theight,"678",fontsize=tsize)
        ax[1].text(506,theight,"A  B   C",fontsize=tsize)
        ax[1].text(576,theight,"D",fontsize=tsize)
        ax[1].text(591,theight,"E",fontsize=tsize)


        # Final:
        ax[0].set_ylabel('Frame #')
        ax[0].set_xlabel('Residue #')
        plt.subplots_adjust(hspace=0.0,wspace=0.05,bottom=0.18,top=0.94,right=0.90,left=0.17)


        # xticks = [170,385,461,510,602]
        xticks = [170,385,496,598]
        xlabels = ['170','385','500','602']
        ax[0].set_xticks(xticks)
        ax[0].set_xticklabels(xlabels)
        ax[0].tick_params(axis='x',which='major',width=5,length=12,color='r',labelsize=16,\
                        direction='out',pad=0.0)
        ax[0].tick_params(axis='y',which='major',width=2,length=10,labelsize=18,\
                        direction='out',pad=0.0)
        ax[0].xaxis.set_ticks_position('bottom')
        ax[0].yaxis.set_ticks_position('left')
