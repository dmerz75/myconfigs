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

    # def __init__(self,job_type,plot_type,data_name,point_start=0,point_stop=310000,ma_value=100):
    def __init__(self,job_type,point_start=0,point_stop=310000,ma_value=100,step=1,\
                 ts=18.67,nav=10000,\
                 dcdfreq=200000,outputtiming=100000,
                 seam='down'):
        """ Initialization of key parameters.
        job_type: sopnucleo,gsop4,gsop147,gsop
        point_start: 0 or 1001 (check for minimization/heating)
        point_stop: if the chain is overstretched ...
        ma_value: moving average
        step: splicing out a segment
        ts: 18.67
        nav: actually the nav1 value.
        """
        # job_type: sop, gsop, sopnucleo
        self.job_type = job_type

        # plot_type: (force) - frame, ext
        # self.plot_type = plot_type

        # description
        # self.data_name = data_name

        # total number of acceptable data points
        self.point_start = point_start
        self.point_stop = point_stop
        self.step = step
        self.ts = ts

        # moving average value
        self.ma_value = ma_value
        # nav
        self.nav = nav
        # seam up / seam down
        self.seam = seam

        # new
        self.dcdfreq = dcdfreq
        self.outputtiming = outputtiming
        self.total_time_ms = float(point_stop) * float(ts) / 1000.0 / float(nav)
        self.time_start = float(point_start)/float(point_stop) * self.total_time_ms
        self.time_finish = self.total_time_ms
        # time = np.linspace((point_start/point_stop)*self.total_time_ms,\
        #                    self.total_time_ms,int(float(point_stop)/step)+1)
        # self.time_array_ms = moving_average(time,self.ma_value)
        # self.time_array_ms = time

        # num_frames = int(float(point_stop) / float(dcdfreq) * nav)
        print point_start,point_stop,dcdfreq,nav,1000
        start = float(point_start)
        stop = float(point_stop)
        dcdf = float(dcdfreq)
        navf = float(nav)
        print start,stop,dcdf,navf,1000.0
        num_frames = stop / dcdf * 1000.0
        # print num_framesnum_frames
        # num_frames = int((float(point_stop) / float(dcdfreq) * float(nav)) / 1000.0)
        print "num_frames",num_frames
        # self.frame_first = float(point_start) / float(point_stop) * float(num_frames)
        self.frame_first = start / stop * num_frames
        if self.frame_first == 0:
            print "is it zero?",self.frame_first
            self.frame_last = self.frame_first + num_frames

        # initial_frame = int(point_start / point_stop * num_frames)
        # print "inital_frame:",point_start / point_stop * num_frames
        # print "final_frame:",num_frames + initial_frame
        # frame = np.linspace((point_start/point_stop)* num_frames,\
        #                     num_frames,int(float(point_stop)/step)+1)
        # self.frame = moving_average(frame,self.ma_value)
        # self.frame = frame


        self.print_class()
        print "<<<<<<<<<<<<<<<<<<  end of class  >>>>>>>>>>>>>>>>>>>\n"
        # sys.exit()


    def print_class(self):
        ''' Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    # def load_data(self,path):


    def load_data(self,path):

        # # pickle!
        # # testing speed of the pkl vs. npy ...
        # # print dir(self)
        # bn = os.path.basename(path)
        # fp = os.path.dirname(path)
        # pkl = re.sub('.dat','.pkl',bn)
        # fp_pkl = re.sub('.dat','.pkl',path)
        # # print fp
        # # print path
        # # print bn
        # # print pkl
        # # print fp_pkl

        # # keys = dir(self)
        # # print type(keys)
        # # for key in keys:
        # #     print key,type(key)


        # # print pickle.HIGHEST_PROTOCOL
        # if os.path.exists(fp_pkl):
        #     check_keys = ['job_type','point_start','point_stop','step','ts','ma_value']
        #     print 'loading pickle ..'
        #     pkl_loaded = pickle.load(open(fp_pkl,'r+'))


        #     if any(getattr(self,key) != getattr(pkl_loaded,key) for key in check_keys):
        #         # stay in load_data function! build up self.__init__ from new declarations.
        #         os.remove(fp_pkl)
        #         print 'ONE or more DOES NOT MATCH!'
        #         for key in check_keys:
        #             print 'self_vs_pkl_loaded:',key,getattr(self,key),'|',getattr(pkl_loaded,key)
        #     else:
        #         print 'These all match.'
        #         for key in check_keys:
        #             print 'self_vs_pkl_loaded:',key,getattr(self,key),'|',getattr(pkl_loaded,key)
        #         for key in dir(pkl_loaded):
        #             # print key,getattr(pkl_loaded,key)
        #             setattr(self,key,getattr(pkl_loaded,key))
        #         return



        # print 'loading data for:',path
        print os.path.relpath(os.path.dirname(path))
        print ('/').join(path.split('/')[-2:])

        # print os.path.basename(path)
        # return


        # # pickle2-name
        # bn = os.path.basename(path)
        # fp = os.path.dirname(path)
        # pkl = re.sub('.dat','v2.pkl',bn)
        # fp_pkl = re.sub('.dat','v2.pkl',path)

        # # pickle2-load
        # if os.path.exists(fp_pkl):
        #     print 'loading pickle2 ..'
        #     data = pickle.load(open(fp_pkl,'r+'))
        #     print data.shape
        # else:
        #     print 'loading data (not yet pickled)'
        #     data = np.loadtxt(path)
        #     print data.shape
        #     pickle.dump(data,open(fp_pkl,'w+'),protocol=pickle.HIGHEST_PROTOCOL)

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




        if self.job_type == 'sop':
            print 'deprecated plot.SOP sop'
            sys.exit()


            print "exiting, fix frames,time,ext ..."
            sys.exit()


            force = data[101::,3]*70 # (1,000,000 min) - print out 10000
            end_to_end = data[101::,2]
            # print data[100,::],'\n',data[101,::],'\n',data[102,::] # --> check!
            # print data[101,::] # --> check!
            # ext = data[101::,12] # 0.1,0.2
            extension = end_to_end[-1] - end_to_end[0]
            print 'extension',extension,'forces:',force.shape,'!!!wrong!!!'
            extension_array = np.linspace(0.0,extension,force.shape[0])
            self.force = force
            self.extension = extension_array
            # plt.plot(extension_array,force)

        elif self.job_type == 'gsop-new':
            ''' self. force vs. indentation,frame,time_array_ms (IFT)
            not actually correct ... because of the extension being linearly spaced.
            '''
            print "BRAND NEW: 2016 testing: gsop-new in plot.SOP"


            # File grab: force,end_to_end,frames
            f_raw = data[self.point_start:self.point_stop:self.step,3] # from gsop147/gsop4, 4th column
            end_to_end = data[self.point_start:self.point_stop:self.step,1] * 0.1 # 2nd column A to nm

            col1 = data[::,0] # 1st column
            # col1 = data[self.point_start:self.point_stop:self.step,0] # 1st column

            # size of array after moving average
            size_arr = len(end_to_end) - self.ma_value

            # Force manipulations:
            # f_raw = data[self.point_start:self.point_stop:self.step,4] # 5th column
            f70 = f_raw * 70.0
            f_ma = moving_average(f_raw,self.ma_value)  # moving_average
            f_pico = f_ma * 70.0                        # pico Newtons
            f_nano = f_ma * 0.7                         # nano Newtons !check??

            # Extension manipulations:
            ext_raw = end_to_end - end_to_end[0]
            # total distance traveled
            ext = moving_average(ext_raw,self.ma_value)
            distance = abs(max(ext) - min(ext))
            ext_linear = np.linspace(0,distance,size_arr)

            if (len(f_pico) != len(f_nano)) or (len(f_pico) != size_arr):
                print 'WARNING: fpico != fnano != size_arr. exiting'
                sys.exit()


            # time | steps
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
            time_array = np.linspace(0,timems,size_arr)

            # frames:
            frame_last = total_steps / self.dcdfreq
            # frame_last = float(self.point_stop - self.point_start) / self.nav
            frame = np.linspace(1,frame_last,size_arr)

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
            self.f70 = f70
            self.end_to_end = end_to_end
            self.ext_raw = ext_raw
            self.force = f_pico # or nano if using mt
            self.ext = ext
            self.extension = ext
            self.ext_linear = ext_linear
            self.time = time_array
            self.time_array_ms = time_array
            self.frame = frame

            print '---force vs. extension/time/frame---'
            print 'force_len:',self.force[-1],len(self.force)
            print 'extension_len:',self.extension[-1],len(self.extension)
            print 'ext_linear_len:',self.ext_linear[-1],len(self.ext_linear)
            print 'time:',self.time[-1],len(self.time)
            print 'frame:',self.frame[-1],len(self.frame)


        elif self.job_type == 'sopnucleo':
            print 'deprecated sopnucleo'
            sys.exit()


            print "exiting, fix frames,time,ext ..."
            sys.exit()

            the_one = data[self.point_start-1:self.point_start:,12]
            the_zero = data[self.point_start:self.point_start+1:,12]
            # print the_one[0],the_zero[0]
            # sys.exit()
            # print data[self.point_start-1:self.point_start:,::]
            # print data[self.point_start:self.point_start+1:,::]
            # print data[self.point_start+1:self.point_start+2:,::]

            if (int(the_one[0]) != 1 or int(the_zero[0]) != 0):
                print 'Warning!'
                print 'change the point_start'
                print 'try %s' % str(int(self.point_start) + 1)
                sys.exit()
            else:
                print 'the_one:',the_one,'the_zero',the_zero,'checks out!'

            f = data[self.point_start:self.point_stop:self.step,3]*70
            print f.shape,'maximum force:',max(f)
            force = moving_average(f,self.ma_value)


            # Column 2 (3rd): end_to_end      # USE THIS!
            end_to_end = data[self.point_start:self.point_stop:self.step,2] * 0.1
            print 'end_to_end:',end_to_end[0],end_to_end[-1]
            extension = moving_average(end_to_end-end_to_end[0],self.ma_value)
            print 'extension from end_to_end',extension[0],extension[-1]
            # extension = np.linspace(0.0,end_to_end[-1],force.shape[0])

            # Column 10 (11th): extension of tension
            ext = data[::,10]*0.1
            print 'extension of tension:',ext.shape,ext[0],ext[-1]
            # # ext = moving_average(ext,75)
            # extension = np.linspace(0,ext[-1],force.shape[0])

            # Column 1 (0th): frame * 10^-5
            # frame = data[:point_tally:,0]*0.00001 # 5000
            # frame = data[self.point_start:self.point_stop:self.step,0]*0.00000001 # x 1000
            frame = moving_average(self.frame,self.ma_value)

            self.force = force
            self.extension = extension
            self.frame = frame

            # total time
            # nav1 = 10000
            print 'if nav1 is equal to %d' % self.nav
            # self.total_time_ms = self.point_stop * self.ts * nav1 * 0.000000001
            self.total_time_ms = self.point_stop * self.ts * self.nav * 0.000000001
            self.time_array_ms = np.linspace(0,self.total_time_ms,len(self.force))


        elif self.job_type == 'gsop' or self.job_type == 'gsop147' or self.job_type == 'gsop4':
            print 'deprecated plot.SOP gsop'
            sys.exit()

            print 'self.job_type:',self.job_type,'from plot.SOP'
            # print data.shape # (3500001, 7)
            end_to_end = data[self.point_start:self.point_stop:self.step,1] * 0.1 # Angstroms to nm
            self.end_to_end = end_to_end
            print 'end_to_end:',end_to_end[0],end_to_end[-1]

            # get extension: 13.05 A to start, to 147.73 at end => 147.73 - 13.05 = 0.0 - 144.68
            self.ext = end_to_end - end_to_end[0]
            print 'ext:',self.ext[0],self.ext[-1]

            # get simple moving_average: (extension) 0.0 - 80.2285 => 0.0799026 - 80.250663
            extension = moving_average(self.ext,self.ma_value)
            print 'extension:',extension[0],extension[-1]

            # get frames
            # if self.job_type == 'gsop' or self.job_type == 'gsop147' or self.job_type == 'gsop4':
                # pass
                # force: 0 column
            f = data[self.point_start:self.point_stop:self.step,0]
            f2 = f / 200000000
            self.f = f2

            print 'self.f:',self.f

            # get forces: 3rd column for gsop147
            if self.job_type == 'gsop147' or self.job_type == 'gsop4':
                forces_raw = data[self.point_start:self.point_stop:self.step,2] * 70
            else:
                forces_raw = data[self.point_start:self.point_stop:self.step,3] * 70

            # get simple moving average: (forces)
            self.f = forces_raw
            force = moving_average(forces_raw,self.ma_value)

            # CHECK: size of forces and extension
            if force.shape[0] != extension.shape[0]:
                print force.shape[0]
                print extension.shape[0]
                print 'must be equal!'
                sys.exit(1)

            print 'maximum_force:',max(force)

            # self. force | extension | frame
            self.force = force
            self.extension = extension
            # self.frame = frame

            # self. total_time_ms | time_array_ms
            # nav1 = 10000
            # print 'if nav1 is equal to %d' % nav1
            # print 'if nav1 is equal to %d' % self.nav
            # self.total_time_ms = self.point_stop * self.ts * nav1 * 0.0000000001


            # if self.job_type == 'gsop':
            #     self.total_time_ms = self.point_stop * self.ts * self.nav * 0.0000000001
            #     #                                                             123456789
            # elif self.job_type != 'gsop': # gsop4,gsop147
            #     print 'get outputtiming, continue use only if it is 200000 ..'
            #     time.sleep(1)
            #     print self.point_stop
            #     print self.ts
            #     print 'outputtiming:',200000
            #     print 200000 * self.ts * self.point_stop
            #     self.total_time_ms = self.point_stop * self.ts * 200000  * 0.000000001

            # print 'the total time was: %f ' % self.total_time_ms,'in milliseconds'
            # self.time_array_ms = np.linspace(0,self.total_time_ms,len(self.force))


            # NEW
            # self.dcdfreq = dcdfreq
            # self.total_time_ms = float(point_stop) * ts / 1000.0 / float(nav)

            # time = np.linspace((point_start/point_stop)*self.total_time_ms,\
            #                    self.total_time_ms,int(float(point_stop)/step)+1)
            # self.time_array_ms = moving_average(time,self.ma_value)
            # self.time_array_ms = time

            # num_frames = int(float(point_stop) / float(dcdfreq) * nav)
            # num_frames = int((float(point_stop) / float(dcdfreq) * nav) / 1000)
            # initial_frame = int(point_start / point_stop * num_frames)
            # print "inital_frame:",point_start / point_stop * num_frames
            # print "final_frame:",num_frames + initial_frame
            # frame = np.linspace((point_start/point_stop)* num_frames,\
                #                     num_frames,int(float(point_stop)/step)+1)
            # self.frame = moving_average(frame,self.ma_value)
            # self.frame = frame

            self.time = np.linspace(self.time_start,self.time_finish,len(self.extension))
            self.time_array_ms = self.time
            self.frame = np.linspace(self.frame_first,self.frame_last,len(self.extension))


            print 'next 4 -- first -- last -- length.'
            print 'force:',self.force[0],self.force[-1],len(self.force)
            print 'extension:',self.extension[0],self.extension[-1],len(self.extension)
            print 'time:',self.time[0],self.time[-1],len(self.time)
            print 'frame:',self.frame[0],self.frame[-1],len(self.frame)
            # sys.exit()



        elif self.job_type == 'mt':
            ''' self. force vs. indentation,frame,time_array_ms (IFT)
            '''
            print 'deprecated plot.SOP mt'
            sys.exit()

            if self.seam == 'down':
                # 1/10
                z_coordinate = 0.1 * data[self.point_start:self.point_stop:self.step,10] # 11th column
                indentation_length = z_coordinate[0] - z_coordinate[-1]
                extension = (z_coordinate * -1) + z_coordinate[0]
            elif self.seam == 'up':
                z_coordinate = data[self.point_start:self.point_stop:self.step,10][::-1] # 11th column
                # z_coordinate = data[self.point_start:self.point_stop:self.step,10] # 11th column - goes CRAZY
                # 1/10
                z_coordinate = z_coordinate * -1 * 0.1
                indentation_length = z_coordinate[-1] - z_coordinate[0]
                extension = (z_coordinate) + (-1 * z_coordinate[-1])


                # sys.exit()
            print 'seam:',self.seam
            print 'z_coordinate:',z_coordinate
            print 'indentation_length:',indentation_length
            print 'extension:',extension


            # # seam up / seam down
            # if self.seam == 'down':

            # elif self.seam == 'up':
            #     extension = ((z_coordinate) - z_coordinate[-1])[::-1]

            extension = moving_average(extension,self.ma_value)
            print 'initial and final indenation:',extension[0],extension[-1]

            # force: 0 column

            if self.seam == 'down':
                f = data[self.point_start:self.point_stop:self.step,4] # 4th column
            elif self.seam == 'up':
                f = (data[self.point_start:self.point_stop:self.step,4])[::-1] # 4th column

            # forces_raw = f * 70 # pico
            forces_raw = f * .07 # nano
            # self.f = forces_raw

            # get simple moving average: (forces)
            force = moving_average(forces_raw,self.ma_value)


            # frames: convert the 1st column (timestep) into frames
            zeroeth_column = data[self.point_start:self.point_stop:self.step,0] # 0th column
            zeroeth_column_step = zeroeth_column[1]
            print zeroeth_column,zeroeth_column_step
            frame = 0.1 * zeroeth_column / zeroeth_column_step
            frame = moving_average(frame,self.ma_value)
            print 'frame:',frame[-1]
            # sys.exit()


            # CHECK: size of forces and extension
            if force.shape[0] != extension.shape[0]:
                print force.shape[0]
                print extension.shape[0]
                print 'must be equal!'
                sys.exit(1)
            elif force.shape[0] != frame.shape[0]:
                print force.shape[0]
                print frame.shape[0]
                print 'must be equal!'
                sys.exit(1)

            print 'maximum_force:',max(force)


            # self. force | indentation | frame | time
            self.force = force
            self.extension = extension
            self.frame = frame

            # self. total_time_ms | time_array_ms
            # nav1 = 10000
            # print 'if nav1 is equal to %d' % nav1
            print 'if nav1 is equal to %d' % self.nav
            # self.total_time_ms = self.point_stop * self.ts * nav1 * 0.0000000001


            self.total_time_ms = self.point_stop * self.ts * self.nav * 0.0000000001
            self.time_array_ms = np.linspace(0,self.total_time_ms,len(self.force))


            # print self.ma_value
            # print len(self.force)
            if len(self.force) > 100000 and self.step < 2:
                print 'try step size:',len(self.force) / 10000

            print 'deprecated'
            sys.exit()

        elif self.job_type == 'MT':
            ''' self. force vs. indentation,frame,time_array_ms (IFT)
            not actually correct ... because of the extension being linearly spaced.
            '''
            # extension / force computed:
            end_to_end = 0.1 * data[self.point_start:self.point_stop:self.step,1] # 2nd column A to nm
            size_arr = len(end_to_end) - self.ma_value
            ext = end_to_end - end_to_end[0]
            z_coordinate = 0.1 * data[self.point_start:self.point_stop:self.step,10] # 11th column
            distance = abs(max(z_coordinate) - min(z_coordinate))
            extension = np.linspace(0,distance,size_arr)
            f = data[self.point_start:self.point_stop:self.step,4] # 5th column
            f = moving_average(f,self.ma_value)
            fpico = f * 70 # pico Newtons
            fnano = f * 0.07 # nano Newtons
            col1 = data[self.point_start:self.point_stop:self.step,0] # 1st column

            # extension / force printed:
            print 'extension/force:'
            print ' end_to_end:',end_to_end[0],end_to_end[-1]
            print ' ext:',ext[0],ext[-1]
            print ' z_coordinate:',z_coordinate[0],z_coordinate[-1],min(z_coordinate)
            print ' distance:',distance
            print ' extension:',extension[0],extension[-1]
            print ' force:',len(f),'points of which the max is:',max(f)
            print ' force(pico):',max(fpico),'force(nano):',max(fnano)

            # time | steps
            total_steps = self.outputtiming * len(end_to_end)
            timestep = 200
            timeps = total_steps * timestep
            timens = timeps * 0.001
            timeus = timens * 0.001
            timems = timeus * 0.001
            time_array = np.linspace(0,timems,size_arr)
            # outputtiming 100000
            # dcdfreq 1000000

            frame_last = total_steps / self.dcdfreq
            frame = np.linspace(1,frame_last,size_arr)

            # frames
            print 'frames:'
            print ' dcdfreq:',self.dcdfreq
            print ' outputtiming:',self.outputtiming
            print ' data_points:',len(end_to_end)
            print ' column1:',col1[0],col1[-1]
            print ' total steps:',total_steps
            print ' frames_last:',frame_last
            print ' frames:',frame[0:5],'..',frame[-5:]

            # time
            print 'time:'
            print ' total steps:',total_steps
            print ' assuming timestep(200):',timestep
            # print ' time(ps):',timeps
            # print ' time(ns):',timens
            print ' time(ms):',timems
            print ' time_array:',time_array

            # plotted: force vs. extension, time, frame
            self.force = fnano
            self.extension = extension
            self.time = time_array
            self.time_array_ms = time_array
            self.frame = frame
            print '<<<  force vs. extension/time/frame  >>>'
            print self.force[-1],len(self.force)
            print self.extension[-1],len(self.extension)
            print self.time[-1],len(self.time)
            print self.frame[-1],len(self.frame)
            # sys.exit()

        # elif self.job_type == 'proto':
        #     ''' self. force vs. indentation,frame,time_array_ms (IFT)
        #     not actually correct ... because of the extension being linearly spaced.
        #     '''
        #     # extension / force computed:
        #     end_to_end = 0.1 * data[self.point_start:self.point_stop:self.step,1] # 2nd column A to nm
        #     size_arr = len(end_to_end) - self.ma_value
        #     ext = end_to_end - end_to_end[0]
        #     z_coordinate = 0.1 * data[self.point_start:self.point_stop:self.step,10] # 11th column
        #     distance = abs(max(z_coordinate) - min(z_coordinate))
        #     extension = np.linspace(0,distance,size_arr)
        #     f = data[self.point_start:self.point_stop:self.step,4] # 5th column
        #     f = moving_average(f,self.ma_value)
        #     fpico = f * 70 # pico Newtons
        #     fnano = f * 0.07 # nano Newtons
        #     col1 = data[self.point_start:self.point_stop:self.step,0] # 1st column

        #     # extension / force printed:
        #     print 'extension/force:'
        #     print ' end_to_end:',end_to_end[0],end_to_end[-1]
        #     print ' ext:',ext[0],ext[-1]
        #     print ' z_coordinate:',z_coordinate[0],z_coordinate[-1],min(z_coordinate)
        #     print ' distance:',distance
        #     print ' extension:',extension[0],extension[-1]
        #     print ' force:',len(f),'points of which the max is:',max(f)
        #     print ' force(pico):',max(fpico),'force(nano):',max(fnano)

        #     # time | steps
        #     total_steps = self.outputtiming * len(end_to_end)
        #     timestep = 200
        #     timeps = total_steps * timestep
        #     timens = timeps * 0.001
        #     timeus = timens * 0.001
        #     timems = timeus * 0.001
        #     time_array = np.linspace(0,timems,size_arr)
        #     # outputtiming 100000
        #     # dcdfreq 1000000

        #     frame_last = total_steps / self.dcdfreq
        #     frame = np.linspace(1,frame_last,size_arr)

        #     # frames
        #     print 'frames:'
        #     print ' dcdfreq:',self.dcdfreq
        #     print ' outputtiming:',self.outputtiming
        #     print ' data_points:',len(end_to_end)
        #     print ' column1:',col1[0],col1[-1]
        #     print ' total steps:',total_steps
        #     print ' frames_last:',frame_last
        #     print ' frames:',frame[0:5],'..',frame[-5:]

        #     # time
        #     print 'time:'
        #     print ' total steps:',total_steps
        #     print ' assuming timestep(200):',timestep
        #     # print ' time(ps):',timeps
        #     # print ' time(ns):',timens
        #     print ' time(ms):',timems
        #     print ' time_array:',time_array

        #     # plotted: force vs. extension, time, frame
        #     self.force = fnano
        #     self.extension = extension
        #     self.time = time_array
        #     self.time_array_ms = time_array
        #     self.frame = frame
        #     print '<<<  force vs. extension/time/frame  >>>'
        #     print self.force[-1],len(self.force)
        #     print self.extension[-1],len(self.extension)
        #     print self.time[-1],len(self.time)
        #     print self.frame[-1],len(self.frame)
        #     # sys.exit()

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
            print 'Extension:',len(self.extension),self.extension[0],self.extension[-1]
            print 'Force_len:',len(self.force),'force_max:',max(self.force),'force_final:',self.force[-1]
            print 'Time points:',len(self.time_array_ms),'Total time:',self.time_array_ms[-1]
            print 'LAST_FRAME:',self.frame[-1]

            total_length = len(self.force)
            interval = total_length / 1000.0


            print 'Extension,frame,time comparison ... skipped for now'

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
            print p_ext
            p_time = self.time_array_ms[-1] * percentage
            print p_time
            p_frame = self.frame[-1] * percentage
            print p_frame

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

    def plot(self,plot_type='ext',**kwargs):
        # if self.job_type == 'mt':
        #     if (plot_type == 'ext') or (plot_type == 'extension'):


        if (plot_type == 'ext') or (plot_type == 'extension'):
            # lineObject = plt.plot(self.extension,self.force)
            plt.plot(self.extension,self.force)
        elif plot_type == 'frame':
            # lineObject = plt.plot(self.frame,self.force)
            plt.plot(self.frame,self.force)
        elif plot_type == 'time':
            # lineObject = plt.plot(self.time_array_ms,self.force)
            plt.plot(self.time_array_ms,self.force)
        elif plot_type == 'indentation':
            plt.plot(self.extension,self.force)

    def plot3ax(self,plot_type):
        # ax1 = plt.subplot(gs[0,:])
        # ax = [ax1]
        # ax =[ax1,ax2,ax3]
        # ax2 = ax1.twiny()
        # ax3 = ax1.twiny()
        if (plot_type == 'ext') or (plot_type == 'extension'):
            plt.plot(self.extension,self.force,'k-')
        elif plot_type == 'time':
            plt.plot(self.time,self.force,'b-')
        elif plot_type == 'frame':
            plt.plot(self.frame,self.force,'m-')


        # return lineObject
        # print args
        #     if (plot_type == 'ext') or (plot_type == 'extension'):
        #         plt.plot(self.extension,self.force,kwargs['linec'],label=kwargs['label'])
        #     elif plot_type == 'frame':
        #         plt.plot(self.frame,self.force,kwargs['linec'],label=kwargs['label'])
        # else:
        #     if (plot_type == 'ext') or (plot_type == 'extension'):
        #         plt.plot(self.extension,self.force)
        #     elif plot_type == 'frame':
        #         plt.plot(self.frame,self.force)

    # def plot3ax(self,plot_type):
    #     if (plot_type == 'ext') or (plot_type == 'extension'):
    #         plt.plot(self.extension,self.force,'k-')
    #     elif plot_type == 'time':
    #         plt.plot(self.time,self.force,'b-')
    #     elif plot_type == 'frame':
    #         plt.plot(self.frame,self.force,'m-')


    def plot_label(self,plot_type,label):
        if (plot_type == 'ext') or (plot_type == 'extension'):
            plt.plot(self.extension,self.force,label=label)
        elif plot_type == 'frame':
            plt.plot(self.frame,self.force,label=label)
        elif plot_type == 'time':
            plt.plot(self.time_array_ms,self.force,label=label)

    def plot_colorline(self,plot_type,lc):
        if (plot_type == 'ext') or (plot_type == 'extension'):
            print 'ext length:',len(self.extension),'force length:',len(self.force)
            plt.plot(self.extension,self.force,lc)
        elif plot_type == 'frame':
            print 'frame length:',len(self.frame),'force length:',len(self.force)
            plt.plot(self.frame,self.force,lc)
        elif plot_type == 'time':
            plt.plot(self.time_array_ms,self.force,lc)

    def plot_colorline_label(self,plot_type,lc,label):
        if (plot_type == 'ext') or (plot_type == 'extension'):
            plt.plot(self.extension,self.force,lc,label=label)
        elif plot_type == 'frame':
            plt.plot(self.frame,self.force,lc,label=label)
        elif plot_type == 'time':
            plt.plot(self.time_array_ms,self.force,lc,label=label)
