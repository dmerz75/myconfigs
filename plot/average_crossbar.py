
import sys
import os
import time

import numpy as np

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
    
# imports from my_library
# from mylib.cp import *
# from mylib.regex import *
from python.keywithmaxval import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import pprint

def compute_average_crossbar(x,min_length=10,max_length=50):

    dct_indices = {}
    array_length = x.shape[0]

    for s in range(min_length,max_length+1,4):
        # s loops from 10 to 50
        # dct_indices[s]={}
        for i in range(0,array_length-s+1,4):
            # dct_indices([s][i])={}
            # i loops from 0 to 381 - s; 371, then to 370
            # finally, at s=50, i loops up to 331
            # print i,i+s
            average = np.mean(x[i:i+s])
            # dct_indices = {(i,i+s):average}
            dct_indices[(s,i)]=average
        #     if i > 25:
        #         break
        # if s > 25:
        #     break

    # np.savetxt('array_map.dat',np.array(dct_indices))
    # pprint.pprint(dct_indices)
    # sys.exit()

    max_key = keywithmaxval(dct_indices)
    print max_key
    dct_crossbar = {'average':dct_indices[max_key],'start':max_key[1],'stop':max_key[1]+max_key[0]}

    lower_keys = lowerkeysfrommaxval(dct_indices)
    print lower_keys
    dct_lowerbars = {}
    for i,tup in enumerate(lower_keys):
        dct_lowerbars[i]={'average':dct_indices[tup],'start':tup[1],'stop':tup[1]+tup[0]}
    try:
        print dct_lowerbars
    except NameError:
        pass


    # print 'max key: ',max_key
    # print 'max key value: ',dct_indices[max_key]
    
    # dct_indices[(s,i)]=average: s is length, i is starting residue
    return dct_crossbar,dct_lowerbars


def draw_crossbar(dct_crossbar,colortype,points):
    x = np.linspace(dct_crossbar['start'],dct_crossbar['stop'],points)
    y = np.linspace(dct_crossbar['average'],dct_crossbar['average'],points)
    plt.plot(x,y,colortype)

    
