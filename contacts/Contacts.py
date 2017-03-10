# coding: utf-8
# import sys
# print __file__

class Contacts(object):
    """
    """
    def __init__(self,fp):
        """
        [yas] elisp error: Symbol’s value as variable is void: text
        [yas] elisp error: Symbol’s value as variable is void: text
        """
        self.fp = fp
        self.dct = {}
        # self.dct['zindex'] = {} # zero-index
        # self.dct['findex'] = {} # file-index


    def get_contacts(self,**kwargs):
        '''
        shift: 1 default (b/c gsop starts on 1 instead of zero)
        '''

        # for k,v in kwargs.iteritems():
        #     print k,v
        #     setattr(k,v)

        print kwargs.keys()
        if not 'shift' in kwargs.keys():
            # print 'shift not found'
            shift = 0
        else:
            shift = kwargs['shift']

        if not 'pos' in kwargs.keys():
            # print 'pos not found'
            pos = 5
        else:
            pos = kwargs['pos']

            # print 'found shift'
        # return
        # print shift

        with open(self.fp) as fp:
            for line in fp.readlines():
                # if line.startswith(';'):
                #     print line
                #     continue
                # else:
                lst = line.split()
                if len(lst) == pos:
                    # if int()
                    # print line
                    try:
                        lst = line.split()
                        resid = int(lst[0]) - shift
                        cresid = int(lst[1]) - shift
                        dist = float(lst[3])
                        if pos > 4:
                            eh = float(lst[4])
                        else:
                            eh = 1.00

                        self.dct[(resid,cresid)] = {}
                        self.dct[(resid,cresid)]['dist'] = dist
                        self.dct[(resid,cresid)]['eh'] = eh
                    except ValueError:
                        continue
                        # pass


    def print_out(self,dct=None):
        '''
        Starting from dictionaries indexed at 1 or 0? (0-default).
        '''
        if dct == None:
            dct = self.dct

        for k,v in sorted(dct.items()):
            string = "{0:5d} {1:5d}     {2:1d}    {3:1.5f}    {4:1.5f}".format(k[0],k[1],1,v['dist'],v['eh'])
            print string
        print len(dct.keys())


    def print_out_gsop_format(self,dct=None,shift=0):
        '''
        '''
        if dct == None:
            dct = self.dct

        # from 1-indexed to 0-indexed
        # shift = 1
        for k,v in sorted(dct.items()):
            # print v['dist']
            # {3:10.5f} 10 > 5
            # string = "{0:5d} {1:5d}     {2:1d} {3:10.5f}    {4:1.5f}".format(k[0]-4,k[1]-4,1,\
            #                                                                   v['dist'],\
            #                                                                   v['eh'])
            string = "{0:5d} {1:5d}     {2:1d} {3:10.5f}    {4:1.5f}".format(k[0]-shift,k[1]-shift,1,\
                                                                              v['dist'],\
                                                                              v['eh'])
            print string
        print len(dct.keys())

    def print_out_sop_format(self,dct=None):
        '''
        '''
        if dct == None:
            dct = self.dct

        # from 1-indexed to 1-indexed
        shift = 0
        for k,v in sorted(self.dct.items()):
            # print v['dist']
            # {3:10.5f} 10 > 5
            # string = "{0:5d} {1:5d}     {2:1d} {3:10.5f}    {4:1.5f}".format(k[0]-3,k[1]-3,1,\
            #                                                                   v['dist'],\
            #                                                                   v['eh'])
            # string = "{0:5d} {1:5d}     {2:1d} {3:10.5f}    {4:1.5f}".format(k[0],k[1],1,\
            #                                                                   v['dist'],\
            #                                                                   v['eh'])
            string = "{0:5d} {1:5d}   {2:1.3f}  {3:1.2f}".format(k[0],k[1],\
                                                                 v['dist'],\
                                                                 v['eh'])
            print string
        print len(self.dct.keys())

    def print_bond_section(self,dct=None):
        '''
        '''
        if dct == None:
            dct = self.dct


        string = "{0:5d} {1:5d}     {2:1d} {3:10.5f}    {4:1.5f}".format(k[0],k[1],1,\
                                                                         v['dist'],\
                                                                         v['eh'])





    def subdomain(self,lst_tup_slice,dct=None):
        ''' Trim the provided dictionary of protein contacts by the list of
        contacts that reside on the domain provided as list of tuples of first
        and last residue numbers.
        i.e. subdomain(dct_protein,[(1,10),(15,20),(23,36)])
        '''
        if dct == None:
            dct = self.dct

        dct_cut = {}
        for tup in lst_tup_slice:
            # print len(dct_cut.keys())
            dct_slice = {key: value for key,value in dct.items() if \
                         key[0] >= tup[0] and key[0] <= tup[1] }
            dct_cut.update(dct_slice)
        # print len(dct_cut.keys())
        return dct_cut

    def between_segments(self,tuple1,tuple2,dct=None):
        ''' Called as tuple.
        between_2_segments((40,115),(1,39)) (defaults to self.dct)
        between_2_segments((40,115),(1,39),dct)

        series: lst of tuples(first,last resid)
        series1: on this segment
        series2: in contact with this segment

        '''
        if dct == None:
            dct = self.dct

        # print dct.keys()
        # print tuple1
        # print tuple2

        dct_inter_contacts = {}

        for tup1 in tuple1:
            # print 'tup1:',tup1
            for tup2 in tuple2:
                # print 'tup2:',tup2
                dct_slice = {key: value for key,value in dct.iteritems() if \
                             key[0] >= tup1[0] and key[0] <= tup1[1] and \
                             key[1] >= tup2[0] and key[1] <= tup2[1]}
                dct_inter_contacts.update(dct_slice)
        return dct_inter_contacts


    def set_eh(self,eh,dct=None):
        '''

        '''
        if dct == None:
            dct = self.dct

        for k in dct.keys():
            # print k
            # print dct[k]
            dct[k]['eh'] = eh

        return dct
