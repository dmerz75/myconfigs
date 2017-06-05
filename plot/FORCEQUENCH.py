import numpy as np
import sys

class FindForceQuench():
    """ Analyzes Worm-like chain fits, contour length.
    force_quench_initial = 3.87
    def get_force_quench():
        fq = FindForceQuench()
        fq.find_max_near(force_quench_initial,X.extension,X.force)
        print 'local_maximum:',fq.near_x,fq.near_y
    get_force_quench()
    """
    def __init__(self,**kwargs):
        # pass
        # self.backpercent = 0.05
        for k in kwargs:
            print k,kwargs[k]
            setattr(self,k,kwargs[k])

            # print key,':\t',getattr(self,key)
            # try:
                # print getattr(self,key).shape
            # except:
                # pass
            # definition = key + ':\t' + str(getattr(self,key)) + '\n'
        # sys.exit()


    def find_max_near(self,x,x_range,x_array,y_array):
        """
        get x, local_max => assign to self.near_x,y
        value is search point. float x = 3.84
        range is the window. float x +/- 1.00
        """
        self.x = x
        self.x_range = x_range
        self.x_array = x_array
        self.y_array = y_array

        # print x_array.shape
        # print y_array.shape
        # print x - x_range
        try:
            xmin_index = np.where(x_array > x - x_range)[0][0]
        except IndexError:
            xmin_index = 0

        xmax_index = np.where(x_array < x + x_range)[0][-1]
        # print xmin_index,xmax_index

        the_force_quench_region_y = y_array[xmin_index:xmax_index]
        # print the_force_quench_region_y

        local_max_y = max(the_force_quench_region_y)
        # print local_max

        local_max_index = np.where(y_array==local_max_y)[0][0]


        # percent1 = int(local_max_index * 0.01)
        percent1 = int(local_max_index * self.backpercent)
        if percent1 < 10:
            percent1 = 10
            # print "Array slice is too small. See plot/FORCEQUENCH"
            # print "local_max_index: "
            # print x_array[::100]
            # print y_array[::100]
            # print x_array.shape, y_array.shape
            # print local_max_index
            # sys.sleep(2)
            # sys.exit(1)
            # self.backendperce
            # percent1 =

        # Array is sliced from local_pre_max_index --> local_max_index
        local_pre_max_index = local_max_index - percent1

        local_max_x = x_array[local_max_index]
        # print local_max_x

        self.near_x = local_max_x
        self.near_y = local_max_y
        self.avg_y = np.mean(y_array[local_pre_max_index:local_max_index])

    def get_aaa():
        print "hello!"



class GetThis():
    '''
    '''

    print "Hey!"
