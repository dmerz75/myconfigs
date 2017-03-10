# starting from dictionaries indexed at 1

def print_out(dct,eh):
    # print json.dumps(dct,indent=1)
    for k,v in sorted(dct.items()):
        string = "{0:5d} {1:5d}     {2:1d}    {3:1.5f}    {4:1.5f}".format(k[0],k[1],1,v['dist'],eh)
        print string
    print len(dct.keys())

def print_out_gsop_format(dct):
    # from 1-indexed to 0-indexed
    shift = 1
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

def print_out_sop_format(dct):
    # from 1-indexed to 1-indexed
    shift = 0
    for k,v in sorted(dct.items()):
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
    print len(dct.keys())
