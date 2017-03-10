# lib_contact.protein_segment

def subdomain(dct_uncut,lst_tup_first_last_resid):
    ''' Trim the provided dictionary of protein contacts by the list of
    contacts that reside on the domain provided as list of tuples of first
    and last residue numbers.
    i.e. subdomain(dct_protein,[(1,10),(15,20),(23,36)])
    '''
    dct_cut = {}
    for tup in lst_tup_first_last_resid:
        # print len(dct_cut.keys())
        dct_slice = {key: value for key,value in dct_uncut.items() if \
                     key[0] >= tup[0] and key[0] <= tup[1] }
        dct_cut.update(dct_slice)
    # print len(dct_cut.keys())
    return dct_cut

def between_2_segments(dct,series1,series2):
    ''' Called as tuple.
    between_2_segments(dct,(40,115),(1,39))
    between_2_segments(dct,[(4,11),(139,169)],domainIA)
    series: lst of tuples(first,last resid)
    series1: on this segment
    series2: in contact with this segment
    '''
    dct_inter_contacts = {}
    for tup1 in series1:
        # print 'tup1:',tup1
        for tup2 in series2:
            # print 'tup2:',tup2
            dct_slice = {key: value for key,value in dct.items() if \
                         key[0] >= tup1[0] and key[0] <= tup1[1] and \
                         key[1] >= tup2[0] and key[1] <= tup2[1]}
            dct_inter_contacts.update(dct_slice)
    return dct_inter_contacts
