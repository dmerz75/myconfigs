#!/usr/bin/env python
import os,sys,time
import pprint
import cPickle as pickle
import argparse
import re

my_dir = os.path.abspath(os.path.dirname(__file__))

#  ---------------------------------------------------------  #
#  Description:                                               #
#  ---------------------------------------------------------  #
''' This script submits jobs to HPC.
    It databases them using sqlite.
'''

#  ---------------------------------------------------------  #
#  Command Line options:                                      #
#  ---------------------------------------------------------  #
''' 1. ./qsub.py (1)
    2. ./qsub.py 4 o17
    Examples:
    >>> ./qsub.py -m lee
    >>> ./qsub.py -n o17 -p 16
    >>> ./qsub.py -p 1 -m ll
    >>> ./qsub.py -x 5 (times)
'''


#  ---------------------------------------------------------  #
#  Get Library                                                #
#  ---------------------------------------------------------  #
''' This library is available using:
    git clone git@github.com:dmerz75/.pylib.git
'''
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)


#  ---------------------------------------------------------  #
#  argparse                                                   #
#  ---------------------------------------------------------  #
parser = argparse.ArgumentParser()
parser.add_argument("-m","--makefile_arg",help="supply Makefile argument")
parser.add_argument("-p","--procs",help="number of processors",type=int)
parser.add_argument("-n","--node",help="type of node for computation")
parser.add_argument("-x","--xtimes",help="x times,runs,trials,duplicates",type=int)
parser.add_argument("-d","--devices",help="gpu device arguments")
args = vars(parser.parse_args())
# print args
# print args['devices']


#  ---------------------------------------------------------  #
#  Get nodes!                                                 #
#  ---------------------------------------------------------  #
''' On the cluster, one runs the command, 'pbsnodes'.
    This class parses that file searching for available nodes.
'''
from pyqsub.get_nodes import *
node_list = get_nodes()
my_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(my_dir)


#  ---------------------------------------------------------  #
#  subprocess                                                 #
#  ---------------------------------------------------------  #
def get_architecture(args):
    ''' Get Architecture with 'uname -a'
    '''
    pipe=subprocess.Popen(args,stdin=subprocess.PIPE,\
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print stdout
    print 'stderr >> ',stderr
    return stdout.split(' ')[1]

#  ---------------------------------------------------------  #
#  PBS Job characterization                                   #
#  ---------------------------------------------------------  #
''' pbs_job.pyc is a module that characterizes a job submitted by type.
    i. e. namd,namdgpu,sop,sopnucleo
'''
from pyqsub.pbs_job import *


# def job_submission(hpc='bio',jobid='testing',job_type='namd',\
#                    make_command='cluster',procs_arg=None,node_arg=None, \
#                    device_arg=None):
def job_submission(hpc='bio',jobid='testing',job_type='namd',\
                   make_command='cluster',procs_arg=None,node_arg=None, \
                   device_arg='0,1'):

    # Initialize Job as pbs_job
    Job = pbs_job(hpc,jobid,job_type,make_command,procs_arg,node_arg,device_arg)

    # --- print Job.jobid
    Job.print_class()

    # --- Render template for job.pbs
    Job.make_template()

    # Job.get_software() # Don't need, using ${HOME}/opt/$NAMD_PATH
    # Job.get_software -- Deprecated

    # --- takes dict(node_list),job_type
    # MAX_PROCS = Job.get_nodes_procs(dict(node_list),Job.job_type)
    MAX_PROCS = Job.get_nodes_procs(dict(node_list))

    # --- use a Makefile to compile
    Job.compile_with_make()

    # --- List files and directories, construct the run_dct
    run_dct = Job.build_run_dct(Job.job_type,Job.cwd,MAX_PROCS)
    # pprint.pprint(run_dct)

    # --- takes job_type,current directory, and processor count
    # Job.prepare_pbs(Job.job_type,run_dct)
    Job.prepare_pbs(run_dct)

    # --- pprint run_dct (file listings)
    pprint.pprint(run_dct)

    # --- create Job.job_dir_local
    # Job.construct_local_dir(Job.job_type,run_dct)
    Job.construct_local_dir(run_dct)

    # --- write Class info to text file.
    # Job.write_class() # will write to current directory
    Job.write_class(Job.job_path_local)

    # --- Use cPickle to write jobinfo.pkl
    pickle.dump(Job,open("%s/job-%s.pkl" % (Job.job_path_local,Job.job_dir_name),"w+"))

    # --- Submit Job
    comp_arch = get_architecture(['uname','-a'])
    # print comp_arch

    # --- Clean up
    if comp_arch == 'm870':
        # print 'submitting ...'
        # stdout,stderr = Job.submit()
        print 'no submit! just cleaning ...'
        Job.clean_with_make()
    else:
        print 'submitting ...'
        stdout,stderr = Job.submit()
        print 'cleaning ...'
        Job.clean_with_make()




#  ---------------------------------------------------------  #
#  Notes                                                      #
#  ---------------------------------------------------------  #
# remove comment on raw_input, pbs_job

#  ---------------------------------------------------------  #
#  End of notes                                               #
#  ---------------------------------------------------------  #


xtimes  = 1
if args['xtimes'] != None: xtimes = args['xtimes']

lst_args= [str(k)[0].upper()+str(v) for k,v in args.iteritems() if v is not None]
str_args= re.sub(r'[^0-9a-zA-Z]','',str(lst_args))



#  ---------------------------------------------------------  #
#  Job Identification:                                        #
#  ---------------------------------------------------------  #

# name or description
# identity = 'alpha250_60nm_lowk_%s' % str_args
# identity = 'ab180_60nm_lowk-factor-1-100_%s' % str_args
# identity = 'ab180_110110_%s' % str_args
# identity = 'ab180_nopep_%s' % str_args
# identity = 'b135_158_a180_pep_%s' % str_args
# identity = '2khosbdpep_1-1.80'
identity = '2khosbdpep_slow0000125'
# identity = '2khosbd_slow0000125'
# identity = 'b135_158_a180_pep0000625_%s' % str_args # no
# identity = '2khosbdpep_0000625_%s' % str_args # no

# lib | bio | 105(gsop-only) | ...
hpc = 'bio'

# sop | sopnucleo | namd | namdgpu | gsop
job_type = 'gsop'


for i in range(1,xtimes+1):
    if any(v is not None for v in args.values()):
        print args.values(),
        print '\t one is not none!'
        print '--->  Using Makefile argument: %s' % args['makefile_arg']
        print '--->  Using node: %s' % args['node']
        print '--->  Using processor(s): %s' % args['procs']
        print '--->  Using device(s): %s' % args['devices']
        job_submission(hpc,identity,job_type,args['makefile_arg'],args['procs'], \
                       args['node'],args['devices'])
    else:
        # Using Makefile:
        print args.values(),'\t all for none, none for all!'
        print '--->  Using default values.'
        job_submission(hpc,identity,job_type)
