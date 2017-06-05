import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import sys

class myCDF():
    """
    Evaluate the cumulative distribution function.

    """
    def __init__(self,data):
        """
        Pass in an array.
        """
        self.data = data


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
        print 'frequency:',self.freq
        print 'bins:',self.bins
        print 'binwidth:',self.width
        print 'normalized:',self.norm
        print 'cumulative:',self.cumulative
        print 'regular-sum:',self.regsum

    def print_stats(self):
        print self.data
        self.mean = np.mean(self.data)
        self.std = np.std(self.data)

        print 'Mean:',self.mean
        print 'Stddev:',self.std


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

        if 'nbins' not in kwargs:
            nbins = 3
        else:
            nbins = kwargs['nbins']

        if 'lower_limit' in kwargs:
            setattr(self,'lower_limit',kwargs['lower_limit'])
        else:
            setattr(self,'lower_limit',min(self.data))

        if 'upper_limit' in kwargs:
            setattr(self,'upper_limit',kwargs['upper_limit'])
        else:
            setattr(self,'upper_limit',max(self.data))

        self.bins = np.linspace(self.lower_limit,self.upper_limit,nbins+1)


    def get_hist(self,**kwargs):
        '''
        Determine bins.
        '''
        print min(self.data),max(self.data)

        # for obj in kwargs:
        #     print obj
        # return

        # if not 'bins' in kwargs:
        #     # not bins:
        #     # == None:
        #     hist = np.histogram(self.data) # normed, density, still hits 10
        # else:
        #     hist = np.histogram(self.data,bins=kwargs['bins']) # normed, density, still hits 10

        hist = np.histogram(self.data,bins=self.bins)

        self.freq = hist[0]
        self.bins = hist[1]
        self.width = self.bins[1] - self.bins[0]

        # self.norm = self.freq / np.linalg.norm(self.freq)
        # print np.linalg.norm(self.freq)
        sum_tot = np.sum(self.freq)
        # print self.freq / sum_tot
        norm_arr = np.array([float(x)/sum_tot for x in self.freq])
        # print norm_arr
        # print np.sum(norm_arr)
        # print np.cumsum(norm_arr)
        self.norm = norm_arr
        # sys.exit()

        # self.norm = self.freq / np.cumsum(self.freq)
        self.cumulative = np.cumsum(self.norm)
        self.regsum = np.sum(self.norm)

        return

    def plot_bars(self,**kwargs):
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

        # CDF-1
        plt.bar(self.bins[:-1],self.norm,self.width,color=color,fill=fill,
                alpha=0.6,
                edgecolor=color)

    def plot_cdf(self,color='b'):
        '''
        Plot the CDF.
        '''
        # CDF-2
        plt.plot(self.bins[:-1],self.cumulative,color=color)


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


    def plot_hist(self,color='b'):
        ''' Manual creation of a histogram.
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
