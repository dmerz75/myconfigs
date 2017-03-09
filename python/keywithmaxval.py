import heapq

def keywithmaxval(d):
    """ From Stackoverflow.com: 268272
        a) create a list of the dict's keys and values
        b) return the key with the max value
    """
    v = list(d.values())
    k = list(d.keys())
    # print max(v),v.index(max(v))
    return k[v.index(max(v))]
    
def lowerkeysfrommaxval(d,losers=1):
    """ Returns indices for which average is in the top 15
        but does not overlap with the previous tension propagator
    """
    lst_losers = []
    v = list(d.values())
    k = list(d.keys())
    maximum = k[v.index(max(v))]
    max_start = maximum[1]
    max_end = maximum[0]+maximum[1]
    candidates = heapq.nlargest(15,v)
    for c in candidates:
        # start: resid 150 to end: resid 190, if span was 40
        start = k[v.index(c)][1]
        end = k[v.index(c)][1]+k[v.index(c)][0]
        print 'if',start,'>',max_end,'or',end,'<',max_start
        if (start > max_end) or (end < max_start):
            print 'winner!'
            lst_losers.append(k[v.index(c)])
            # if len(lst_losers) >= losers:
            #     return lst_losers

    # list of tuples: (40,340) # 340 - 380
    return lst_losers[0:losers]
