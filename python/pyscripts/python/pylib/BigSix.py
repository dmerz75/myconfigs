# BigSix
import random
import sys

class BigSix(object):
    """
    """

    def __init__(self,):
        """
        The Big Six wheel!
        """
        dct = {}
        n = 0

        nlist = [[i,j,k] for i in range(1,7) for j in range(1,7) for k in range(1,7)]
        # print 'nlist:\n',nlist
        # print 'len_nlist:',len(nlist)

        for obj in nlist:
            sorted_key = sorted(obj)
            str_key = ''.join(str(x) for x in sorted_key)
            dct[str_key] = {}
            dct[str_key][0] = sorted_key[0]
            dct[str_key][1] = sorted_key[1]
            dct[str_key][2] = sorted_key[2]

        # print 'unique_keys:',len(dct.keys())
        # for k,v in dct.iteritems():
        #     print k,v

        self.cash = 0.0
        self.wager = {}
        for i in range(1,7):
            self.wager[i] = 0.0

        self.wheel = dct
        self.nspins = 0
        self.outcomes = {}
        for i in range(1,7):
            self.outcomes[i] = 0

    def spin(self,n=1):
        """
        The spin.
        """
        # lst = list(self.wheel.keys())
        self.nspins += n
        # print(lst)

        for i in range(0,n):
            spin = random.choice(list(self.wheel.keys()))
            self.results(self.wheel[spin])

            print(spin,self.wheel[spin])



            break
            # self.nspins += 1





    def results(self,spin):
        """
        print results
        """
        # print "result recorded.",spin
        self.outcomes[spin[0]] += 1
        self.outcomes[spin[1]] += 1
        self.outcomes[spin[2]] += 1
        # print

    def print_results(self,):
        """
        Print results.
        """
        tally = 0
        for k,v in self.outcomes.items():
            print(k,v)
            tally += v
        print("total:",tally)
        print('total:',self.nspins,'x3:',self.nspins * 3)

    def show_wager(self,):
        print("----------")
        for k,v in self.wager.items():
            if v != 0.0:
                print(k,'| ',v)
        print("----------")

    def set_wager(self,n,f):
        self.wager[n] = f

    def bet(self,wager):
        """
        All bets down!
        """
        for k,v in wager.items():
            print(k,v)
