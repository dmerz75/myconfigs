#!/usr/bin/env python
import os,sys,time
import shutil,re,subprocess
import ConfigParser

my_dir = os.path.abspath(os.path.dirname(__file__))
home   = os.path.expanduser('~')
# py_qsub_dir = os.path.join(home,'py_qsub_dir')   # 1
py_qsub_dir = os.path.expanduser('~/.pylib/py_qsub')

main_file = 'main_sub.c'

my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

#  ---------------------------------------------------------  #
#  imports from my_library                                    #
#  ---------------------------------------------------------  #
from cp import *
from regex import *


def build_dct(keys,values):
    return dict(zip(keys,values))

def regex_on_main(dct):
    cp_file(my_dir,main_file,my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c')
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdha1_loopxx',dct['dha1_loop'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdhb_loopxx',dct['dhb_loop'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdhc2_loopxx',dct['dhc2_loop'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdha1_helixxx',dct['dha1_helix'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdha2_helixxx',dct['dha2_helix'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdhb_helixxx',dct['dhb_helix'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdhc1_helixxx',dct['dhc1_helix'])
    reg_ex(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',\
            'xxdhc2_helixxx',dct['dhc2_helix'])
# def compile(function):
#     pipe=subprocess.Popen(['make','clean'],stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     stdout,stderr = pipe.communicate()
#     print stdout
#     print 'stderr >> ',stderr
#     pipe=subprocess.Popen(['make',function],stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#     stdout,stderr = pipe.communicate()
#     print stdout
#     print 'stderr >> ',stderr

def copy_to_run(name_ddir):
    run_dir = os.path.join(my_dir,name_ddir)
    print name_ddir,'entered copy_to_run folder ....'
    print run_dir
    # sys.exit()
    if not os.path.exists(run_dir): os.makedirs(run_dir)
    cp_file(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',run_dir,\
                   'main_pullends_dihedrals_fullGo_dcd.v2.c')
    cp_file(my_dir,'Makefile',run_dir,'Makefile')
    cp_file(my_dir,'pdb2mol.ent',run_dir,'pdb2mol.ent')
    cp_file(my_dir,'Contact_map_intra_b_ehD1_2.0_ehD2_2.0_2mol',run_dir,\
                   'Contact_map_intra_b_ehD1_2.0_ehD2_2.0_2mol')
    cp_file(my_dir,'Secondary_struct_2mol',run_dir,'Secondary_struct_2mol')
    cp_file(my_dir,'def_param.h',run_dir,'def_param.h')
    cp_file(my_dir,'read_protein.c',run_dir,'read_protein.c')
    cp_file(my_dir,'rforce.c',run_dir,'rforce.c')
    cp_file(my_dir,'force_pullends_dihedrals.c',run_dir,\
                   'force_pullends_dihedrals.c')
    cp_file(my_dir,'iteration.c',run_dir,'iteration.c')
    cp_file(my_dir,'update_dihedrals_dcd_fullGo.c',run_dir,'update_dihedrals_dcd_fullGo.c')
    cp_file(my_dir,'ras_structure.c',run_dir,'ras_structure.c')
    cp_file(my_dir,'identify.c',run_dir,'identify.c')
    cp_file(my_dir,'dcdio.c',run_dir,'dcdio.c')
    cp_file(my_dir,'debug.h',run_dir,'debug.h')
    cp_file(my_dir,'def_const_PDB.h',run_dir,'def_const_PDB.h')
    cp_file(my_dir,'def_random_seeds.h',run_dir,'def_random_seeds.h')
    cp_file(my_dir,'structure.h',run_dir,'structure.h')
    cp_file(my_dir,'qsub.py',run_dir,'qsub.py')
    # sys.exit()


def submit(name_ddir,make_arg):
    os.chdir(os.path.join(my_dir,name_ddir))
    print os.getcwd()
    pipe=subprocess.Popen(['python','qsub.py','-m',make_arg],stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print 'stdout >> ',stdout
    print 'stderr >> ',stderr
    print 'waiting ...\n'
    time.sleep(2.4)

# DEFINE LIST
lh_keys = ['dha1_loop','dhb_loop','dhc2_loop','dha1_helix','dha2_helix','dhb_helix',\
            'dhc1_helix','dhc2_helix']

def get_config(id):
    config = ConfigParser.ConfigParser()
    config.read('lh.conf')
    params = config.get(id,'lh_params')
    return [p for p in params.split(',')]

# RUN
def go(tup,code,make_arg):
    os.chdir(my_dir)
    print os.getcwd()
    label = 'l'+str(tup[0])+'h'+str(tup[1])
    print label
    lh_params= get_config(label)
    print lh_params
    dct_used = build_dct(lh_keys,lh_params)
    print dct_used
    regex_on_main(dct_used)
    # sys.exit()
    # compile(make_arg)
    copy_to_run('run_%s_%s' % (code,label))
    submit('run_%s_%s' % (code,label),make_arg)

# (l,h)
def lh_submit(i):
    # hl = [go((l,h),'mod_cloop2','mod') for l in range(7,8) for h in range(1,5)]
    # hl = [go((l,h),'lee_5','lee') for l in range(1,2) for h in range(1,3)]
    # hl = [go((l,h),'gt_5','gt') for l in range(7,8) for h in range(1,3)]
    hl = [go((l,h),'rsdihed-%s' % str(i),'ll') for l in range(1,2) for h in range(1,2)]

[lh_submit(i) for i in range(1,10+1)]
