#!/usr/bin/env python
import os,sys,time
import numpy as np

my_dir = os.path.abspath(os.path.dirname(__file__))

# idn = 'com_one'
# idn = 'com_I_to_II'
# idn = 'com_IB_to_IIB'
lst_idn = ['com_IA_to_IIA','com_IA_to_IB','com_IA_to_IIB',
           'com_IIA_to_IB','com_IIA_to_IIB','com_IB_to_IIB']


def plot_com(idn):
    com_data = np.loadtxt('traj_%s.dat' % idn)
    # print com_data.shape
    # sys.exit()

    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(0)

    gs = GridSpec(1,1)
    ax1 = plt.subplot(gs[0, :])
    # ax2 = plt.subplot(gs[1,:-1])
    # ax3 = plt.subplot(gs[1:, -1])
    # ax4 = plt.subplot(gs[-1,0])
    # ax5 = plt.subplot(gs[-1,-2])

    plt.subplots_adjust(left=0.15,right=0.97,top=0.87,bottom=0.18)
    fig.set_size_inches(7.12,4.4)
    font_prop_large = matplotlib.font_manager.FontProperties(size='large')
    run_control     = {'family':'sans-serif',
                       'weight':'normal',
                       'size'  :'24',
    }
    matplotlib.rc('font',**run_control)

    x = np.linspace(0,com_data.shape[0]/10.0,com_data.shape[0])
    ax1.plot(x,com_data,'k-')


    ###  LEGEND  # 1,2,3,4 - quadrants
    ## plt.legend(loc=1,prop={'size':14})
    ## fpropl=matplotlib.font_manager.FontProperties(size='large')
    ax1.legend([r"N-Term - C-Term"],
               loc=4,
               prop={'size':18})
    leg = plt.gca().get_legend()
    leg.draw_frame(False)

    # plt.ylim([7.8,16.2])
    # plt.xlim([-0.2,50.2])

    plt.ylabel('Separation ($\AA$)')
    plt.xlabel('Time (ns)')
    plt.title("Center of Mass")

    plt.draw()
    # plt.show()


    def save_pic_data(i,subdir,fname):
        if subdir == '':
            content_dir = my_dir
        else:
            content_dir = os.path.join('/'.join(my_dir.split('/')[0:i]),subdir)
        if not os.path.exists(content_dir): os.makedirs(content_dir)
        abs_file_name = os.path.join(content_dir,fname)
        plt.savefig('%s.png' % abs_file_name)
        plt.savefig('%s.eps' % abs_file_name)
        # plt.savefig('%s.jpg' % abs_file_name)
        os.chdir(content_dir)
        # pickle.dump(pmf_2d,open('%s.pkl' % fname,'w'))
        # np.savetxt('%s.dat' % fname,pmf_2d,fmt=['%3.4f','%3.11f'],delimiter=' ')
            
    # save_pic_data(levels_back,subdir,name)
    # example: save_pic_data(-4,'fig',name)
    # example: save_pic_data(-3,'',name)
    # default: save_pic_data(0,'','mypic')
    # plt.show()
    # save_pic_data(0,'','example1')
    save_pic_data(0,'fig_com_multidomains',idn)

for i in range(len(lst_idn)):
    os.chdir(my_dir)
    print i
    idn = lst_idn[i]
    plot_com(idn)
