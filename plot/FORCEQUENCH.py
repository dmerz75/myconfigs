import numpy as np

class FindForceQuench():
    """ Analyzes Worm-like chain fits, contour length.
    force_quench_initial = 3.87
    def get_force_quench():
        fq = FindForceQuench()
        fq.find_max_near(force_quench_initial,X.extension,X.force)
        print 'local_maximum:',fq.near_x,fq.near_y
    get_force_quench()
    """
    def __init__(self):
        pass

    def find_max_near(self,x,xrange,x_array,y_array):
        """
        get x, local_max => assign to self.near_x,y
        value is search point. float x = 3.84
        range is the window. float x +/- 1.00
        """
        xmin_index = np.where(x_array > x - xrange)[0][0]
        xmax_index = np.where(x_array < x + xrange)[0][-1]
        # print xmin_index,xmax_index

        the_force_quench_region_y = y_array[xmin_index:xmax_index]
        # print the_force_quench_region_y

        local_max_y = max(the_force_quench_region_y)
        # print local_max

        local_max_index = np.where(y_array==local_max_y)[0][0]
        # print local_max_index

        local_max_x = x_array[local_max_index]
        # print local_max_x

        self.near_x = local_max_x
        self.near_y = local_max_y

    def get_aaa():
        print "hello!"



class GetThis():
    '''
    '''

    print "Hey!"



