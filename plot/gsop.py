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
