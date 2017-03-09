import numpy as np
from numpy import ma

#  ---------------------------------------------------------  #
#  functions                                                  #
#  ---------------------------------------------------------  #
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


def moving_average_array(x,n):
    ''' average_over_data: reduces the dimension of the array
    by averaging over the neighbors ...
    '''
    # x = np.asarray(x)
    new_array = np.zeros([x.shape[0]-n,x.shape[1]])
    print 'before averaging:',x.shape
    print 'after averaging:',new_array.shape

    for i in range(0,x.shape[0] - n):
        x1 = x[i:i+n:,::]
        # while not x.any():
        #     x = np.zeros()
        #     n += 1
        #     x = x[i:i+n,::]
        # if i < 5:
        #     print i,i+n
        #     print x
        # elif i == 5:
        #     print 'beyond the fifth ...'
        # else:
        #     pass
        y = np.mean(x1,axis=0)
        new_array[i] = y

    return new_array
