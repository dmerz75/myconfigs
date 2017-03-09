
import os
import sys
import numpy as np

#  ---------------------------------------------------------  #
#  WLC                                                        #
#  ---------------------------------------------------------  #
class WormLikeChain():
    """ For using a Worm-like Chain fit to determine the persistence length
        of a peptide or protein. (a characterization of the flexibility)
    """
    def __init__(self,Lc=145.0,Lp=0.5,elev=0.0):
        """ Initialization of key variables.
        Lc-Contour Length
        Lp-persistence length
        """
        self.Lc = Lc
        self.kBT = 0.6
        self.Lp = Lp
        self.elev = elev
        # z = self.zdomain(Lc)
        # print z
        # self.F = self.compute_wlc_fit(self.Lc,self.Lp,z)

    def zdomain(self,start=0.6,stop=0.965,points=5000):
        z = np.linspace(start * self.Lc,stop * self.Lc,points)
        # z_Lc = z / self.Lc
        self.z = z
        # return z

    def compute_wlc_fit(self,Lc,Lp,z=None):
        # self.Lc = Lc
        # self.kBT = 0.6
        # self.Lp = Lp
        # self.z = np.linspace(0.7*Lc,0.97*Lc,250)
        # self.z_Lc = self.z / self.Lc

        # print Lc
        # print z
        # sys.exit()
        # if z == None:
        #     z = self.zdomain(Lc)
        # print z
        # sys.exit()
        # print z[0::50]
        z_Lc = z / Lc
        first_term = 1 / (4 * ((1 - z_Lc) ** 2))
        F = self.kBT / Lp * ( first_term - 0.25 + z_Lc)

        self.F = F + self.elev
        # return z,F

    def print_class(self):
        ''' Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            # definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    def return_Force(self,max=None):
        ''' Return force.
        '''
        # print len(self.z),'\n',self.z
        # print len(self.F),'\n',self.F
        if max != None:
            condition = self.F < max
            self.F = np.extract(condition,self.F)
            # print len(self.F),'\n',self.F
            # print type(max)
            self.z = self.z[:len(self.F):]
            # print len(self.F),len(self.z)
            # sys.exit()

        return self.z,self.F

    # def return_many_Force(self):
    #     ''' Check multiple persistence lengths.
    #     '''
