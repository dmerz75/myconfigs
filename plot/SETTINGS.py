# coding: utf-8
import os
import sys
import glob
import matplotlib
import matplotlib.pyplot as plt
import re


class SaveFig():
    '''
    Save a matplotlib figure.
    REQ:
    (1) cwd = saves here, else provide 'destdirname'
    (2) name = filename without suffix. eg. 'png' (def), 'svg'
    OPT:
    (3) destdirname: eg. 'fig/histograms'
    (4) dpi: (optional) 120 (default), 300, 600, 1200
    (5) filetypes: ['png','svg','eps','pdf']
    '''

    def __init__(self,cwd,name,**kwargs):
        '''
        Initialize Class.
        '''

        self.cwd = cwd
        self.name = name
        self.kwargs = kwargs
        self.dpi = 300
        self.filetypes = ['png']


        # begin
        # self.print_class()

        # A
        self.set_attributes()

        # B
        self.set_destdir()
        self.set_dpi()


        # C
        self.check_for_duplicates()

        # end
        # self.print_class()


        print self.__doc__

        # self.print_class()

        self.save()


    def set_attributes(self):
        '''
        Set attributes to those values provided.
        '''

        for k in self.kwargs:
            # print k,self.kwargs[k]
            setattr(self,k,self.kwargs[k])

    def print_class(self):
        '''
        Print class attributes.
        '''

        for key in dir(self):
            print key,getattr(self,key)

    def set_destdir(self):

        if 'destdirname' in self.kwargs.keys():
            self.destdir = os.path.join(self.cwd,self.kwargs['destdirname'])
        else:
            self.destdir = self.cwd

    def set_dpi(self,*args):

        # print args
        if len(args) > 0:
            self.dpi = args[0]
        # elif 'dpi' in self.kwargs.keys():
            # self.dpi = self.kwargs['dpi']

    # def set_filetypes(self):

    def check_for_duplicates(self):
        '''
        writing to destdir,
        check name in destdir.
        '''
        dct = {}

        # print 'filetypes: ',self.filetypes
        # lst = sorted(glob.glob(os.path.join(self.destdir,'%s*'
        #                                     % self.name)))
        # print lst
        # sys.exit()

        for suffix in self.filetypes:

            dct[suffix] = sorted(glob.glob(
                os.path.join(self.destdir,'%s*.%s' %
                             (self.name,
                              suffix))))

            print 'found: '
            print dct[suffix][-3:]
            # print dct.keys()

            # if len(lst) == 0:
            if len(dct[suffix]) == 0:
                # try:
                #     x = int(self.name.split('-')[-1])
                #     # return
                # except:
                self.name = self.name + '-0'
                return
            else:
                nums_found = [int(re.sub('.%s' % suffix,'',f.split('-')[-1])) for f in dct[suffix]]
                new_num = max(nums_found) + 1
                self.name = self.name + '-' + str(new_num)


    def save(self):
        '''
        Save the figure.
        '''

        if not os.path.exists(self.destdir):
            os.makedirs(self.destdir)

        fp = os.path.join(self.destdir,self.name)

        for suffix in self.filetypes:

            fps = fp + '.%s' % suffix

            if not os.path.exists(fps):
                print 'Saving: ',fps,' dpi: ',self.dpi

                # if ((suffix == 'svg') and (self.dpi < 1000)):
                #     self.dpi = 1000
                plt.savefig(fps,format=suffix,dpi=self.dpi)

            else:
                print 'File already exists! ',fps






def save_fig(savedir,dir_bac,subdir,fname,option,**kwargs):
    ''' Receive savedir.
    Make subdir if necessary, dir_bac levels...
    use fname-0.type, or fname-0.type
    '''
    print "saving figure in dir...",savedir
    print 'dir_bac:(0)',dir_bac
    print "SUBDIR:",subdir
    print 'FNAME:',fname
    print 'OPTION:',option
    if dir_bac == 0:
        # print 'DIR_BAC = 0'
        content_dir = os.path.join(savedir,subdir)
    else:
        content_dir = os.path.join('/'.join(savedir.split('/')[0:dir_bac]),subdir)
    print 'savedir:',savedir
    print 'content_dir:',content_dir

    if not os.path.exists(content_dir):
        os.makedirs(content_dir)

    if option == 'publish':
        fp_filename = os.path.join(content_dir,'%s_pub' % fname,fname)
    else:
        fp_filename = os.path.join(content_dir,fname)
    print "FP:",fp_filename

    # Save in PNG,EPS,SVG,PDF,TIFF,JPG formats
    # PIL, wxpython2.8, QT5Agg may be necessary
    # Image.open('%s.png' % fp_filename).save('%s.jpg' % fp_filename,'JPEG')
    # dpi = 300 # 300,900
    # matplotlib.rcParams['figure.dpi'] = 900

    if 'dpi' in kwargs.keys():
        print 'Setting dpi:',kwargs['dpi']
        dpi = kwargs['dpi']
    else:
        dpi = matplotlib.rcParams['figure.dpi']
    # sys.exit()

    print 'searching %s ....' % fp_filename
    if option == 'show':
        print 'showing...'
        plt.show(block=True)
        # plt.show()
        # sys.wait()
        # sys.exit()
    elif option == 'publish':
        if not os.path.exists(os.path.join(content_dir,'%s_pub' % fname)):
            os.mkdir(os.path.join(content_dir,'%s_pub' % fname))
        matplotlib.rcParams['figure.dpi'] = 1200
        # EPS, SVG, PDF, TIFF
        plt.savefig('%s.eps' % fp_filename,dpi=dpi)
        plt.savefig('%s.svg' % fp_filename,dpi=dpi)
        plt.savefig('%s.png' % fp_filename,dpi=dpi)
        plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
        # plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
        # PNG
        # plt.savefig('%s.png' % fp_filename,dpi=dpi)
        matplotlib.rcParams['figure.dpi'] = 300
        fp_filename = os.path.join(content_dir,fname + '_small_PUB')
        plt.savefig('%s.png' % fp_filename,dpi=dpi)
    else:
        matplotlib.rcParams['figure.dpi'] = 120

        files = [f for f in os.listdir(content_dir) if os.path.isfile(os.path.join(content_dir,f))]
        files = [f2 for f2 in files if re.search('PUB',f2) == None]
        files = [f1 for f1 in files if re.match(fname,f1) != None]
        # print files

        # do matching
        if len(files) == 0:
            print 'no files were found. saving %s' % fp_filename
            fp_filename = fp_filename + '-0'
            plt.savefig('%s.png' % fp_filename,dpi=dpi)
        else:
            print 'fname:',fname
            print 'files:',files
            try:
                files_num_counted = [int(re.sub('.png','',f.split('-')[-1])) for f in files]
                print 'ints found:',files_num_counted
                high_num = max(files_num_counted)
                high_num += 1
                print 'new high number:',high_num
                fp_filename = fp_filename + '-' + str(high_num)
            except IndexError:
                print 'zeroeth image printed!'
                fp_filename = fp_filename + '-0'
            # except ValueError:
            #     print 'zeroeth image printed!'
            #     fp_filename = fp_filename + '-0'

                # except ValueError:
            # except ValueError:
            #     files_num_counted = [int(re.sub('.png','',f.split('-')[2])) for f in files]
            #     print 'ints found:',files_num_counted
            #     high_num = max(files_num_counted)
            #     high_num += 1
            #     print 'new high number:',high_num
            #     fp_filename = fp_filename + '-' + str(high_num)
            plt.savefig('%s.png' % fp_filename,dpi=dpi)









    # types
    # plt.savefig('fig/%s_%s_%s.png' % (result_type,plot_type,data_name))
    # plt.savefig('%s.png' % dir_filename,dpi=dpi)
    # plt.savefig('%s.png' % fp_filename,dpi=dpi)
    # plt.savefig('%s.eps' % fp_filename,dpi=dpi)
    # plt.savefig('%s.svg' % fp_filename,dpi=dpi)
    # plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
    # plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
    # plt.savefig('%s.jpg' % fp_filename,dpi=dpi)

# if option == 'show':
#     plt.show()
#     sys.exit()
# elif option == 'publish':
#     matplotlib.rcParams['figure.dpi'] = 1200
#     data_name = data_name + '_PUB'
#     print "calling save_fig ..."
#     # save_pic_data(levels_back,subdir,name)
#     # example: save_fig(-4,'fig',name)
#     # example: save_fig(-3,'',name)
#     save_fig(0,'fig','%s_%s_%s' % (result_type,plot_type,data_name))
# else:
#     print 'saving dpi=300 (default) image ..'
#     plt.savefig('fig/%s_%s_%s.png' % (result_type,plot_type,data_name))
