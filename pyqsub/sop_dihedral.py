#!/usr/bin/env python
import os,sys,time
import shutil,re,subprocess
import ConfigParser

my_dir = os.path.abspath(os.path.dirname(__file__))
home   = os.path.expanduser('~')
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

def copy_to_run(name_ddir):
    subdir = os.path.join(my_dir,name_ddir)
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    cp_file(my_dir,'main_pullends_dihedrals_fullGo_dcd.v2.c',subdir,\
                   'main_pullends_dihedrals_fullGo_dcd.v2.c')
    cp_file(my_dir,'Makefile',subdir,'Makefile')
    cp_file(my_dir,'pdb2mol.ent',subdir,'pdb2mol.ent')
    cp_file(my_dir,'Contact_map_intra_b_ehD1_2.0_ehD2_2.0_2mol',subdir,\
                   'Contact_map_intra_b_ehD1_2.0_ehD2_2.0_2mol')
    cp_file(my_dir,'Secondary_struct_2mol',subdir,'Secondary_struct_2mol')
    cp_file(my_dir,'def_param.h',subdir,'def_param.h')
    cp_file(my_dir,'read_protein.c',subdir,'read_protein.c')
    cp_file(my_dir,'rforce.c',subdir,'rforce.c')
    cp_file(my_dir,'force_pullends_dihedrals.c',subdir,'force_pullends_dihedrals.c')
    cp_file(my_dir,'iteration.c',subdir,'iteration.c')
    cp_file(my_dir,'update_dihedrals_dcd_fullGo.c',subdir,'update_dihedrals_dcd_fullGo.c')
    cp_file(my_dir,'ras_structure.c',subdir,'ras_structure.c')
    cp_file(my_dir,'identify.c',subdir,'identify.c')
    cp_file(my_dir,'dcdio.c',subdir,'dcdio.c')
    cp_file(my_dir,'debug.h',subdir,'debug.h')
    cp_file(my_dir,'def_const_PDB.h',subdir,'def_const_PDB.h')
    cp_file(my_dir,'def_random_seeds.h',subdir,'def_random_seeds.h')
    cp_file(my_dir,'structure.h',subdir,'structure.h')
    cp_file(my_dir,'qsub.py',subdir,'qsub.py')

def submit(name_ddir,func_argument):
    os.chdir(os.path.join(my_dir,name_ddir))
    print os.getcwd()
    pipe=subprocess.Popen(['python','qsub.py',func_argument],stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    print stdout
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
def go(tup,code,func):
    os.chdir(my_dir)
    print os.getcwd()
    label = 'l'+str(tup[0])+'h'+str(tup[1])
    print label
    lh_params= get_config(label)
    print lh_params
    dct_used = build_dct(lh_keys,lh_params)
    print dct_used
    regex_on_main(dct_used)
    # compile(func)
    copy_to_run('run_%s_%s' % (code,label))
    submit('run_%s_%s' % (code,label),'%s_final' % func)

# (l,h)
# hl = [go((l,h),'mod_cloop2','mod') for l in range(7,8) for h in range(1,5)]
# hl = [go((l,h),'lee_5','lee') for l in range(1,2) for h in range(1,3)]
# hl = [go((l,h),'gt_5','gt') for l in range(7,8) for h in range(1,3)]
hl = [go((l,h),'testing','ll') for l in range(1,4) for h in range(1,4)]

