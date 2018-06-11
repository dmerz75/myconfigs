# coding: utf-8

import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import sys
import re
from decimal import Decimal

from scipy import stats

class KSTest():
    """
    Perform the Kolmogorov-Smirnov-Test for distribution comparison.

    The two sample K-S test.
    https://en.wikipedia.org/wiki/Kolmogorov_Smirnov_test
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
    Result: Reject or Accept, null hypothesis: the distributions are the same.
    """

    # def __init__(self,d1,d2,**kwargs):
    def __init__(self,d1,d2):


        # \alpha  : 0.10  0.05   0.025   0.01   0.005   0.001
        # C(alpha): 1.22  1.36   1.48    1.63   1.73    1.95
        self.alpha = np.array([0.10,0.05,0.025,0.01,0.005,0.001])
        self.calpha = np.array([1.22,1.36,1.48,1.63,1.73,1.95])

        self.d1 = d1
        self.d2 = d2


        self.d1size = d1.shape[0]
        self.d2size = d2.shape[0]


        self.criterion = "p"

        self.null_hypothesis = True


        # self.compute_KS_and_p_value()


    def print_description(self):
        '''
        # d,p = Kolmogorov_Smirnov_Test(lst_cdf[i].data,lst_cdf[f].data)
        '''
        print """ The null hypothesis is that the distributions of the two
        samples are the same.
        If the K-S value is small: reject the null hypothesis.
        If the p-value is high: reject the null hypothesis. """

        print "Sizes:"
        print self.d1size,self.d2size


    def print_result(self):


        print "K-S value: (critical)",self.d
        print "two-tailed p-value:",self.p
        # print "Result:",self.Result

        print "Criterion: ",self.criterion


        if self.criterion == 'p':
            print self.Results[-1][0]
            print self.Results[-1][1]

        else:
            for i,res in enumerate(self.Results[0:-1]):
                print res[0]
                print self.alpha[i],res[1]



        # return d,p,Result

        # if p < 0.01:
        #     print "We reject the null hypothesis. (a different distribution)"
        #     print "Reject."
        #     Result = 'Reject. diff dist.'
        # elif p > 0.1:
        #     print "We cannot reject the null hypothesis. (more/less the same dist.)"
        #     print "Do Not Reject."
        #     Result = 'Do Not Reject. (same dist.)'
        # else:
        #     print p,"It is uncertain whether we can reject the null hypothesis. Reject. ?"

    # print data1.shape
    # print data2.shape

    def compute_radicands(self,**kwargs):

        if (('size1' in kwargs) and ('size2' in kwargs)):

            size1 = kwargs['size1']
            size2 = kwargs['size2']

        else:
            size1 = self.d1size
            size2 = self.d2size


        radicand = float(size1 + size2) / float((size1 * size2))
        self.rad = np.sqrt(radicand)


    def compute_KS_and_p_value(self,**kwargs):

        # sqrt ( (n+m)  /  n*m )  ==> rad
        # rad * c(alpha)

        # else:
            # radicand = float(self.d1size + self.d2size) / float((self.d1size * self.d2size))
            # self.rad = np.sqrt(radicand)

        # if "binsize" in kwargs:
            # self.d1size

        # print "radicand:",radicand
        # print "sqrt:",self.rad

        if "size1" in kwargs:
            size1 = kwargs['size1']
        else:
            size1 = self.d1size

        if "size2" in kwargs:
            size2 = kwargs['size2']
        else:
            size2 = self.d2size


        self.compute_radicands(size1=size1,size2=size2)


        # list of critical values:
        lst_cv = []

        for i in range(len(self.alpha)):

            critical_value = self.calpha[i] * self.rad
            # print i,alpha[i],calpha[i],critical_value
            lst_cv.append(critical_value)

        self.critical_values = np.array(lst_cv)

        self.d,self.p = stats.ks_2samp(self.d1,self.d2)



    def reject_null(self,**kwargs):
        '''
        cv: critical_value
        '''
        # self.Result = "Reject the null hypothesis. The distributions are different."

        if 'p' in kwargs:

            if self.criterion == 'KS':
                # res_label = "%13.10f < %13.10f (<-d)" \
                #     % (kwargs['critical'],kwargs['d'])
                # res_label = "%13.10f" % self.p
                res_label = "%0.3E" % self.p
            else:
                res_label = "%f %f" % (self.pthreshold,kwargs['p'])

        else:
            res_label = "%9.6f < %9.6f (<-d)" % (kwargs['critical'],kwargs['d'])

        Result = "Reject the null hypothesis. The distributions are different."
        self.null_hypothesis = False

        # lst_Results.append((self.Result,res_label))
        return Result,res_label



    def accept_null(self,**kwargs):
        # self.Result = "Accept the null hypothesis. The distributions are the same."

        if 'p' in kwargs:

            # res_label = "%f %f" % (self.pthreshold,kwargs['p'])
            if self.criterion == 'KS':
                # res_label = "%13.10f" % self.p
                # res_label = "%13.10f %13.10f" % (self.pthreshold,kwargs['p'])
                res_label = "%0.3E" % self.p
            else:
                res_label = "%f %f" % (self.pthreshold,kwargs['p'])

        else:
            res_label = "%9.6f > %9.6f (<-d)" % \
                (kwargs['critical'],kwargs['d'])

        Result = "Accept the null hypothesis. The distributions are the same."
        self.null_hypothesis = True

        # lst_Results.append((self.Result,res_label))
        return Result,res_label


    def evaluate_hypothesis(self,pthreshold=0.05):
        """
        # if p < 0.05:
        #     print "We reject the null hypothesis. (a different distribution)"
        #     Result = 'Reject. (diff dist.)'
        # else:
        #     print "We cannot reject the null hypothesis. (more/less the same dist.)"
        #     Result = 'Do Not Reject. (same dist.)'

        """
        self.criterion = "KS" # or p

        if((self.d1size > 50) and (self.d2size > 50)):
            self.criterion = "KS"
        else:
            self.criterion = "p"


        self.pthreshold = pthreshold
        lst_Results = []


        # First alternative for determining large data set similarity.
        # if self.criterion == "KS":
        #     # D, or KS-value comparison:
        #     # If the K-S value is small: reject the null hypothesis.
        #     for i,crit in enumerate(self.critical_values):
        #         if self.d < crit:
        #             R,L = self.accept_null(d=self.d,critical=crit)
        #             lst_Results.append((R,L))
        #         else:
        #             R,L = self.reject_null(d=self.d,critical=crit)
        #             lst_Results.append((R,L))

        if self.criterion == "KS":

            if self.p > 0.000000001:
                # p value low
                R,L = self.accept_null(p=self.p)
                lst_Results.append((R,L))
            else:
                # p value high
                R,L = self.reject_null(p=self.p)
                lst_Results.append((R,L))



        else:
            # If the p-value is high: reject the null hypothesis.

            # pthreshold = 0.05 (default)
            if self.p > pthreshold:
                # p value low
                R,L = self.accept_null(p=self.p)
                lst_Results.append((R,L))
            else:
                # p value high
                R,L = self.reject_null(p=self.p)
                lst_Results.append((R,L))


        self.Results = lst_Results



    def plot_KS_result(self,ax,**kwargs):
        """
        Plot the KS result.
        Are the distributions the same or different?
        """

        # Must be null hypothesis Reject/False.
        # -- that the distributions are different
        if self.null_hypothesis == True:
            return


        # print kwargs.items()
        # print kwargs['pos']

        if 'pos' in kwargs:
            x = kwargs['pos'][0]
            y = kwargs['pos'][1]
        else:
            print "did not find pos."
            x = 0.5
            y = 0.5
            print "x:",x,"y:",y

        # if KS.criterion == 'p':
        #     lst_KStups.append((lst_cdf[i].name,lst_cdf[f].name,KS.d,KS.p,KS.Results[-1]))
        #     # print KS.Results[-1]
        #     # sys.exit()
        #     print KS.Results[-1][0]

        #     # Search for Do Not Reject the null hypothesis, same dist.
        #     if re.search('Accept',KS.Results[-1][0]) != None:
        #         print "Same, Found it!"
        #         # sys.exit()
        #     else:
        #         print "Different"
        #         KS.plot_KS_result(ax,color='r')
        #         # sys.exit()
        # else:
        #     lst_KStups.append((lst_cdf[i].name,lst_cdf[f].name,KS.d,KS.p,KS.Results[:-1]))


        # if
        # print self.Results
        # print dir(self)

        for i,res in enumerate(self.Results):

            if re.search('Reject the null',res[0]) != None:

                print res[0],res[1],self.alpha[i]

                ax.text(x,y,"Reject",color='r',
                        style='oblique',size=22,rotation=15)

                break


        # sys.exit()





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
        if self.data.shape[0] < 100:
            print self.data,self.data.shape
        else:
            print self.data.shape,self.data[0:8]
        print 'Mean:',self.mean
        print 'StdDev:',self.std
        print 'binwidth:',self.width
        print 'bins:'
        if self.bins.shape[0] > 20:
            print self.bins[0:5]
            print self.bins[-4:]
        else:
            print self.bins

        print 'frequency:',self.freq
        print 'normalized:'
        if self.norm.shape[0] > 20:
            print self.norm[0:5]
            print self.norm[-4:]
        else:
            print self.norm

        print 'cumulative:'
        if self.cumulative.shape[0] > 20:
            print self.cumulative[0:5]
            print self.cumulative[-4:]
        else:
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
        # patterns = ('-','\\')
        # for bar, pattern in zip(bars, patterns):
            # bar.set_hatch(pattern)
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

        ax.legend(loc=2,fontsize=16)

        # ax.set_xlim([])

        # print min(self.norm)
        # print max(self.norm)
        # print dir(self)
        # print self.data
        # print min(self.bins)
        # print max(self.bins)
        # print self.bins[0]
        # print self.bins[-1]

        minx = self.bins[0] - self.width
        maxx = self.bins[-1] + 0.5 * self.width
        # print self.width
        # sys.exit()

        # ax.set_xlim([self.bins[0],self.bins[-1]])
        ax.set_xlim([minx,maxx])
        # sys.exit()



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
