#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
import argparse

def parse_arguments():
    ''' Parse script's arguments.
    Options:
    args['makefile']
    args['procs']
    args['node'])
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--range",help="range for running")
    args = vars(parser.parse_args())
    return args
# args = parse_arguments()
