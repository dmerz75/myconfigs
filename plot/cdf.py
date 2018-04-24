# coding: utf-8

import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import sys

from scipy import stats


def Kolmogorov_Smirnov_Test(data1,data2):
    """
    The two sample K-S test.
    https://en.wikipedia.org/wiki/Kolmogorov-Smirnov_test
    Two-sample Kolmogorov–Smirnov test

    //
    scipy.

    scipy.stats.ks_2samp(data1, data2)[source]
    Computes the Kolmogorov-Smirnov statistic on 2 samples.
    This is a two-sided test for the null hypothesis that 2 independent
    samples are drawn from the same continuous distribution.

    Parameters:
    a, b : sequence of 1-D ndarrays
    two arrays of sample observations assumed to be drawn from a
    continuous distribution, sample sizes can be different

    Returns:
    D : (float) KS statistic
    p-value : (float) two-tailed p-value
    """

    d,p = stats.ks_2samp(data1,data2)

    return d,p


class myCDF():
    """
    Evaluate the cumulative distribution function.

    """
    def __init__(self,data,**kwargs):
        """
        Pass in an array.

        Default values:
        minimum # of bins: 4
        alpha:             0.5 (full)
        """
        self.name = "default"
        self.data = data

        if 'lower_limit' in kwargs:
            self.lower_limit = kwargs['lower_limit']
        else:
            self.lower_limit = min(data)

        if 'upper_limit' in kwargs:
            self.upper_limit = kwargs['upper_limit']
        else:
            self.upper_limit = max(data)


        if 'nbins' in kwargs:
            self.nbins = kwargs['nbins']
        else:
            self.nbins = 4

        if 'alpha' in kwargs:
            self.alpha = kwargs['alpha']
        else:
            self.alpha = 0.5

        if 'pattern' in kwargs:
            self.pattern = kwargs['pattern']
        else:
            self.pattern = None

        # print 'nbins:',nbins
        # sys.exit()
        # cdf = myCDF(data)
        # cdf.print_class()
        # cdf.determine_bins(lower_limit=0.3,upper_limit=0.6,nbins=3) # set
        # cdf.determine_bins_limits(lower_limit=0.3,upper_limit=0.6,nbins=)
        # cdf.determine_bins_limits(lower_limit=lower_limit,
        #                           upper_limit=upper_limit,
        #                           nbins=nbins) # set



    def print_class(self):
        '''
        Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            try:
                print key,':\t',getattr(self,key).shape
            except:
                pass
            # definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    def print_values(self):
        print 'Data:'
        print self.data
        print 'Mean:',self.mean
        print 'StdDev:',self.std
        print 'binwidth:',self.width
        print 'bins:',self.bins
        print 'frequency:',self.freq
        print 'normalized:'
        print self.norm
        print 'cumulative:'
        print self.cumulative
        print 'regular-sum:',self.regsum

    def get_meanstdev(self):
        # print self.data
        self.mean = np.mean(self.data)
        self.std = np.std(self.data)
        # print 'Mean:',self.mean
        # print 'Stddev:',self.std

    def determine_bins_limits(self,**kwargs):
        '''
        Determine bins.
        '''
        # print 'getting bins.'
        # print 'first-last:'
        # print self.data[0],self.data[-1]

        # print 'min-max:'
        # print min(self.data),max(self.data)

        # for k,v in kwargs.iteritems():
        #     print k,v

        # self.lower_limit = min(self.data)
        # self.upper_limit = max(self.data)


        if 'nbins' in kwargs:
            # self.nbins = 3
            setattr(self,'nbins',kwargs['nbins'])
        else:
            setattr(self,'nbins',3)
            # self.nbins = kwargs['nbins']

        # print self.nbins


        if 'lower_limit' in kwargs:
            setattr(self,'lower_limit',kwargs['lower_limit'])
        else:
            setattr(self,'lower_limit',min(self.data))

        if 'upper_limit' in kwargs:
            setattr(self,'upper_limit',kwargs['upper_limit'])
        else:
            setattr(self,'upper_limit',max(self.data))


        # print dir(self)
        # print self.data
        # print type(self.lower_limit),type(self.upper_limit),type(self.nbins)
        self.bins = np.linspace(self.lower_limit,self.upper_limit,self.nbins+1)


    def get_hist(self,**kwargs):
        '''
        Determine bins.
        '''
        # print min(self.data),max(self.data)

        # for obj in kwargs:
        #     print obj
        # return

        # if not 'bins' in kwargs:
        #     # not bins:
        #     # == None:
        #     hist = np.histogram(self.data) # normed, density, still hits 10
        # else:
        #     hist = np.histogram(self.data,bins=kwargs['bins']) # normed, density, still hits 10

        # print self.data


        hist = np.histogram(self.data,bins=self.bins)

        self.freq = hist[0]
        self.bins = hist[1]
        self.width = self.bins[1] - self.bins[0]

        # print self.freq
        # print self.bins
        # print self.width

        # self.norm = self.freq / np.linalg.norm(self.freq)
        # print np.linalg.norm(self.freq)
        sum_tot = np.sum(self.freq)
        # print sum_tot
        # sys.exit()


        # print self.freq / sum_tot
        norm_arr = np.array([float(x)/float(sum_tot) for x in self.freq])
        # print norm_arr
        # sys.exit()
        # print np.sum(norm_arr)
        # print np.cumsum(norm_arr)
        self.norm = norm_arr
        # sys.exit()

        # self.norm = self.freq / np.cumsum(self.freq)
        self.cumulative = np.cumsum(self.norm)
        self.regsum = np.sum(self.norm)

        return


    def plot_cdf(self,ax,color='b',multiplier=1):
        '''
        Plot the CDF.
        '''
        # CDF-2
        cumulative = self.cumulative * multiplier
        ax.plot(self.bins[:-1],cumulative,color=color)


    def empty(self):
        # ax[0].set_xlim(bins[0],bins[-1])

        # CDF-3
        if 1:
            # with:
            ax[0].set_ylim(-0.05,2.8)
            ax[0].set_xlim(0.22,1.30)
        else:
            # without:
            ax[0].set_ylim(-0.05,1.12)
            ax[0].set_xlim(0.30,1.30)

        ax[0].set_xlabel('Forces',fontsize=24)
        # ax[0].set_ylabel('Frequency',fontsize=24)
        ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
        return bins

    def plot_bars(self,ax,**kwargs):
        '''
        Plot a histogram (bar graph).
        '''

        if 'color' in kwargs:
            color = kwargs['color']
        else:
            color = 'b'

        if 'fill' in kwargs:
            fill = kwargs['fill']
        else:
            fill = True

        if 'alpha' in kwargs:
            alpha = kwargs['alpha']
        else:
            alpha = 1.0

        if 'pattern' in kwargs:
            pattern = kwargs['pattern']
        else:
            pattern = None

        if 'label' in kwargs:
            label = kwargs['label']
        else:
            label = None

        # print alpha
        # print pattern
        # sys.exit()

        # patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
        # for bar, pattern in zip(bars, patterns):
        #     bar.set_hatch(pattern)
        # CDF-1
        # print self.bins
        # print self.norm
        # print self.width
        # print color
        # print fill
        # print alpha
        # print color
        # print pattern
        # print label

        # alpha

        ax.bar(self.bins[:-1],self.norm,self.width,color=color,fill=fill,
               alpha=alpha,edgecolor=color,
               hatch=pattern,label=label)

        ax.legend(loc=2)



    def plot_hist(self,color='b'):
        ''' Manual creation of a histogram.

        Possibly Deprecated.
        '''
        print min(data),max(data)

        bins = np.linspace(0.30,0.65,7)
        width = bins[1] - bins[0]
        hist = np.histogram(data,bins=bins) # normed, density, still hits 10
        norm = hist[0] / np.linalg.norm(hist[0])

        print 'width:',width
        print 'hist:'
        print hist
        print hist[0],len(hist[0])
        print hist[1],len(hist[1])
        print 'norm:'
        print norm

        # ax[0].bar(bins[:-1],hist[0],width,color=color,alpha=0.6)
        ax[0].bar(bins[:-1],norm,width,color=color,alpha=0.6)

        ax[0].set_xlim(bins[0],bins[-1])
        ax[0].set_xlabel('Forces',fontsize=24)
        ax[0].set_ylabel('Frequency',fontsize=24)
        return bins

    def plot_hist4(self,bins,color='b'):
        '''
        Manual creation of a histogram. Normalized.
        '''
        print min(data),max(data)
        # binmax = 5
        # bins = np.linspace(min(data),max(data),binmax)
        width = bins[1] - bins[0]
        # while width > 0.05:
        #     binmax += 1
        #     bins = np.linspace(min(data),max(data),binmax)
        #     width = bins[1] - bins[0]
        # print 'binmax:',binmax

        hist = np.histogram(data,bins=bins) # normed, density, still hits 10
        norm = hist[0] / np.linalg.norm(hist[0])

        print 'width:',width
        print 'hist:'
        print hist
        print hist[0],len(hist[0])
        print hist[1],len(hist[1])
        print 'norm:'
        print norm

        # CDF-1
        cumulative = np.cumsum(norm)

        ax[0].bar(bins[:-1],norm,width,color=color,alpha=0.6)

        # CDF-2
        plt.plot(bins[:-1],cumulative,color=color)

        # ax[0].set_xlim(bins[0],bins[-1])

        # CDF-3
        if 1:
            # with:
            ax[0].set_ylim(-0.05,2.8)
            ax[0].set_xlim(0.22,1.30)
        else:
            # without:
            ax[0].set_ylim(-0.05,1.12)
            ax[0].set_xlim(0.30,1.30)

        ax[0].set_xlabel('Forces',fontsize=24)
        # ax[0].set_ylabel('Frequency',fontsize=24)
        ax[0].set_ylabel('Norm. Freq. & CDF',fontsize=24)
        return bins

    # def plot_cdf(data,color='b'):
    #     '''
    #     With the cumulative distribution function, CDF.
    #     '''
    #     # values,base = np.histogram(data,bins=len(bins))
    #     # cumulative = np.cumsum(values)
    #     # plt.plot(base[:-1],self.cumulative,color=color)
    #     # plt.plot()
