#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import Counter
import os
import shutil
# import time


def check_bad_lines(orig_file,choice='backup'):
    '''
    backup no matter what! orig_file.txt -> orig_file_bac.txt
    the choices: nothing, new, write(new to orig).

    1. backup!
    2. new.
    3. mv new to orig.

    '''

    count = 0
    lst_linew = []


    with open(orig_file) as fp:
        for i,line in enumerate(fp):

            x = len(line.split())
            lst_linew.append(x)
            if i >= 20:
                break

    print len(lst_linew)
    cc = Counter(lst_linew)
    linew = cc.most_common()
    print linew[0]
    num_per_line = linew[0][0]

    # print orig_file
    ddir = os.path.dirname(orig_file)
    bn = os.path.basename(orig_file)
    preface = os.path.splitext(bn)[0]
    ext = os.path.splitext(bn)[-1]
    print ddir
    print bn,ext

    bac_file = preface + '_bac' + ext
    bac_file = os.path.join(ddir,bac_file)
    new_file = preface + '_new' + ext
    new_file = os.path.join(ddir,new_file)

    # BACKUP COPY
    if not os.path.exists(bac_file):
        shutil.copyfile(orig_file,bac_file)
    # return


    count_nflines = 0

    # NEW FILE
    if choice == 'new':
        if not os.path.exists(new_file):
            nf = open(new_file,"w+")
            with open(bac_file) as of:
                for i,line in enumerate(of):
                    x = len(line.split())
                    if x == num_per_line:
                        nf.write(line)
                        count_nflines += 1

            print 'lines_written:',count_nflines,'of',i-1
            nf.close()

    if choice == 'write':
        shutil.move(new_file,orig_file)
    # with open()
            # if line.startswith('#'):
            #     continue
            # print x
