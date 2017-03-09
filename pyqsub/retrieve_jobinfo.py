#!/usr/bin/env python
import os,sys,time
import cPickle as pickle

my_dir = os.path.abspath(os.path.dirname(__file__))

from glob import *
# print my_dir
pickle_list = glob(os.path.join(my_dir,'job-*.pkl'))
print pickle_list
if len(pickle_list) == 1:
    pickled_job = pickle_list[0]
else:
    sys.exit()

#  ---------------------------------------------------------  #
#  Description:                                               #
#  ---------------------------------------------------------  #
''' This script submits jobs to HPC, from the stored pickle.
'''

#  ---------------------------------------------------------  #
#  Command Line options:                                      #
#  ---------------------------------------------------------  #
''' 1. ./retrieve_jobinfo.py
    2. ./retrieve_jobinfo.py 
'''
# from optparse import OptionParser
# parser = OptionParser()
# parser.add_option("-d","--dir",dest=)


#  ---------------------------------------------------------  #
#  Get Library                                                #
#  ---------------------------------------------------------  #
''' This library is available using:
    git clone git@github.com:dmerz75/.pylib.git
    It has cp.pyc and regex.pyc.
'''
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)
# sys.path.append(os.path.join(my_library,'py_qsub'))
from cp import *
from regex import *

#  ---------------------------------------------------------  #
#  Get nodes!                                                 #
#  ---------------------------------------------------------  #
''' On the cluster, one runs the command, 'pbsnodes'.
    This class parses that file searching for available nodes.
'''
from py_qsub.get_nodes import *
node_list = get_nodes()

#  ---------------------------------------------------------  #
#  PBS Job characterization                                   #
#  ---------------------------------------------------------  #
''' pbs_job.pyc is a module that characterizes a job submitted by type.
    i. e. namd,namdgpu,sop,sopnucleo
'''
from py_qsub.pbs_job import *


# Create Job from Pickle
# Job = pbs_job(jobid='crazy',job_type='namd')
Job = pickle.load(open(pickled_job,'r'))

if len(sys.argv) > 1:
    Job.completed_dir = Job.completed_dir + sys.argv[1]
    Job.job_dir       = Job.job_dir + sys.argv[1]
    Job.job_sub       = Job.job_sub + sys.argv[1]
# completed_dir:	/home/dale/completed/crazy_dale__pylibtest__02-18-2014_2340__200_9219541
# job_dir:	/scratch/dale/crazy_dale__pylibtest__02-18-2014_2340__200_9219541
# job_sub:	crazy_dale__pylibtest__02-18-2014_2340__200_9219541

Job.print_class()
Job.make_template()
Job.get_software()
    # print Job.jobid
MAX_PROCS = Job.get_nodes_procs(dict(node_list),Job.job_type)
# MAX_PROCS = Job.nprocs
    # takes dict(node_list),job_type
    # print MAX_PROCS
run_dct = Job.build_run_dct(Job.job_type,Job.cwd,MAX_PROCS)
# run_dct = Job.build_run_dct(Job.job_type,Job.cwd,Job.nprocs)
    # pprint.pprint(run_dct)
    # takes job_type,current directory, and processor count
Job.prepare_pbs(Job.job_type,run_dct)

# --- Use cPickle to write jobinfo.pkl
# import cPickle as pickle
# pickle.dump(Job,open("jobinfo.pkl","w+"))

# --- Submit Job
stdout,stderr = Job.submit()
