#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time

my_dir = os.path.abspath(os.path.dirname(__file__))


# mylib/faf
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# libraries:
# from mylib.FindAllFiles import *
# from mylib.moving_average import *
# from mylib.cp import *
# from mylib.FindAllFiles import *
# from mylib.highway_check import *
# from mylib.moving_average import *
# from mylib.regex import reg_ex
# from mylib.run_command import run_command
from contacts.Contacts import Contacts


#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    '''
    parser = argparse.ArgumentParser()
    # parser.add_argument("-m","--makefile_arg",help="supply Makefile argument")
    # parser.add_argument("-p","--procs",help="number of processors",type=int)
    parser.add_argument("-f","--file",help="contact file.")
    parser.add_argument("-p","--pos",
                        help="# positions in a contact line. i.e. typically 4 or 5",
                        type=int)
    args = vars(parser.parse_args())
    return args

args = parse_arguments()
''' Options:
args['makefile']
args['procs']
args['node'])
'''
print args


cn = Contacts(args['file'])
cn.get_contacts(pos=args['pos'],shift=0)


# print 'regular ......'
# cn.print_out()

# print 'for gsop ........'
# cn.print_out_gsop_format()


# print 'get a subdomain'
# dct_sub = cn.subdomain([(0,64)])
# print 'see a subdomain'
# cn.print_out(dct_sub)

# print 'get bridging contacts'
# dct_btn = cn.between_segments([(10,40)],[(75,85)])
# print 'see bridging contacts'
# cn.print_out(dct_btn)

# print 'changing eh for some contacts'
# dct_btn = cn.set_eh(1.35,dct_btn)
# cn.dct.update(dct_btn)

# print 'new eh dict'
# cn.print_out()


#  ---------------------------------------------------------  #
#  Examples Above. Start below.                               #
#  ---------------------------------------------------------  #

# change eh to 1.35
print 'changing eh to 1.35'
dct_all = cn.set_eh(1.35)
cn.print_out_gsop_format(dct_all)
