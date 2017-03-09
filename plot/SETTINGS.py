import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import re

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
        # plt.savefig('%s.pdf' % fp_filename,dpi=dpi)
        plt.savefig('%s.tiff' % fp_filename,dpi=dpi)
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
