import os,sys,time
import random,subprocess,pprint
from glob import *
import ConfigParser

#  ---------------------------------------------------------  #
#  Description:                                               #
#  ---------------------------------------------------------  #
''' This script is a module employed by qsub.py.
    It classifies jobs by type: namd,namdgpu,sop,sopnucleo.
'''

#  ---------------------------------------------------------  #
#  Get Library                                                #
#  ---------------------------------------------------------  #
''' This library is available using:
    git clone git@github.com:dmerz75/.pylib.git
    It has cp.pyc and regex.pyc.
'''
my_library = os.path.expanduser('~/.pylib')
sys.path.append(my_library)

# import my library
from mylib.cp import *
from mylib.regex import *


class pbs_job():
    def __init__(self,hpc,jobid,job_type,make_command='lee',\
                 procs_arg=0,node_arg=0):
        ''' pbs_job characterization
        '''
        # print 'hpc','jobid','job_type','make_command','procs_arg','node_arg'
        # print hpc,jobid,job_type,make_command,procs_arg,node_arg
        # print job_type
        # sys.exit()
        if (job_type == 'namd') or (job_type=='namdgpu') or (job_type=='sop') \
           or (job_type == 'sopnucleo') or (job_type == 'gsop'):
            self.hpc      = hpc
            self.jobid    = jobid
            self.job_type = job_type
            self.cwd      = os.getcwd()
            self.procs_arg= procs_arg
            self.node_arg = node_arg
            self.user     = os.path.basename(os.path.expanduser('~'))
            self.seed300  = random.randint(1,300)

            # get Langevin seed from .namd or .conf file
            try:
                with open(glob(os.path.join(self.cwd,'*.namd'))[0]) as fopen:
                    print type(fopen)
                    for line in fopen:
                        if line[0:4]=='seed':
                            print line
                            self.seed10_7 = re.findall(r'\d+',line)[0]
            except:
                self.seed10_7 = random.randint(10000,10000000)

            if (procs_arg == 0) or (procs_arg == None):
                self.nprocs = 1
            else:
                self.nprocs = int(procs_arg)

            self.dir_path = os.path.dirname(self.cwd)
            self.dir_name = os.path.basename(self.cwd)
            self.proj_name= self.cwd.split('/')[-2]
            # print "The default project name is: ",self.proj_name
            # x = raw_input("Type a new name (hit [enter] to keep default: %s) >> " % self.proj_name)
            # if not x == '': self.proj_name = x
            # desc = raw_input("Enter a project description now. >> ")
            # if not desc == '': self.description = desc

            self.description = "lorem ipsum"
            self.sub_time = time.strftime("%H%M")
            self.sub_date = time.strftime("%m-%d-%Y")

            self.job_dir_name  = self.jobid+'_'+self.dir_name+ \
                            '__'+self.sub_date+'_'+self.sub_time + \
                            '__'+str(self.seed300)+'_'+str(self.seed10_7)

            self.pyqsubdir = os.path.join(my_library,'pyqsub')

            if self.hpc == 'lib':
                self.template = os.path.join(self.pyqsubdir,'template_lib%s.pbs' \
                                             % self.job_type)
            else:
                self.template = os.path.join(self.pyqsubdir,'template_%s.pbs' \
                                             % self.job_type)


            self.job_path_run   = '/scratch/%s/%s' % (self.user,self.job_dir_name)
            self.job_path_local = os.path.join(self.cwd,self.job_dir_name)
            self.pbs_script = os.path.join(self.cwd,'job.pbs')
            self.job_path_local_pbs_script = os.path.join(self.job_path_local,'job.pbs')
            self.completed_dir = os.path.expanduser('~/completed/%s' \
                                                    % self.job_dir_name)
            self.make_command = make_command
            self.fn_main_sub = 'main_sub.c'
            self.fp_main_sub = os.path.join(self.cwd,self.fn_main_sub)
            self.fn_main_sop = 'main_pullends_dihedrals_fullGo_dcd.v2.c'
            self.fp_main_sop = os.path.join(self.cwd,self.fn_main_sop)

        # Other Job Types:
        elif job_type == 'generic':
            pass

    def print_class(self):
        ''' Print class and its attributes.
        '''
        keys = dir(self)
        for key in keys:
            print key,':\t',getattr(self,key)
            definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            # o.write(definition)

    def make_template(self):
        ''' Copies 'template_sop.pbs' to job.pbs or other template
        '''
        if (self.job_type == 'namd') or (self.job_type == 'namdgpu') or \
           (self.job_type == 'sop') or (self.job_type == 'sopnucleo') or \
           (self.job_type == 'gsop'):
            cp_file(self.pyqsubdir,self.template,self.cwd,'job.pbs')

        # elif (self.job_type == 'gsop'):
        #     cp_file(self.pyqsubdir,self.template,self.job_path_local,'meta.sh')
        
        reg_ex(self.cwd,self.pbs_script,'xx_jobname_xx',self.jobid)
        reg_ex(self.cwd,self.pbs_script,'xxuserxx',self.user)
        reg_ex(self.cwd,self.pbs_script,'xxmy_dirxx',self.cwd)
        reg_ex(self.cwd,self.pbs_script,'xxjob_dir_namexx',self.job_dir_name)
        reg_ex(self.cwd,self.pbs_script,'xxjob_path_localxx',self.job_path_local)
        reg_ex(self.cwd,self.pbs_script,'xxjob_path_runxx',self.job_path_run)
        reg_ex(self.cwd,self.pbs_script,'xxcompleted_dirxx',self.completed_dir)
        reg_ex(self.cwd,self.pbs_script,'xxsubnamexx',self.job_type)



        # elif (self.job_type == 'gsop'):
        #     cp_file(self.pyqsubdir,self.template,self.cwd,'job.pbs')

    # def get_software(self): -- DEPRECATED
    #     if self.job_type == 'namd':
    #         cp_file(os.path.expanduser('~/opt/NAMD_2.9_Linux-x86_64-multicore'),\
    #                 'namd2',self.cwd,'namd2')
    #     elif self.job_type == 'namdgpu':
    #         cp_file(os.path.expanduser('~/opt/NAMD_2.9_Linux-x86_64-multicore-CUDA'), \
    #                 'namd2',self.cwd,'namd2')
    #     else:
    #         pass

    def get_nodes_procs(self,node_dct,type='sop'):
        ''' perform regular expressions specific to processor and node needs by 
            jobtype
        '''
        if self.procs_arg != None:
            reg_ex(self.cwd,'job.pbs','xxprocsxx',str(self.procs_arg))
        if self.node_arg != None:
            reg_ex(self.cwd,'job.pbs','xxnodexx',self.node_arg)

        node_list_dq = filter(lambda x: 'dq' in x,[n for n in node_dct.keys()])
        node_list_opteron = filter(lambda x: 'o' in x,[n for n in node_dct.keys()])
        node_list_qc = filter(lambda x: 'qc' in x,[n for n in node_dct.keys()])
        node_list_node = filter(lambda x: 'node' in x,[n for n in node_dct.keys()])
        node_list_gpu = filter(lambda x: 'gpu' in x,[n for n in node_dct.keys()])

        if type=='namdgpu':
            # define node_list: per section; node: per subsection;
            node_list = node_list_gpu
            if self.hpc == 'lib':
                node  = min(node_list)
                max_number_procs = node_dct[node]
                reg_ex(self.cwd,'job.pbs','xxprocsxx',str(max_number_procs))
                reg_ex(self.cwd,'job.pbs','xxnodexx','gpu')
            elif self.hpc == 'bio':
                try:
                    node_list.remove('gpu1')
                except:
                    pass
                try:
                    node_list.remove('gpu2')
                except:
                    pass
                node  = min(node_list)
                max_number_procs = node_dct[node]
                reg_ex(self.cwd,'job.pbs','xxprocsxx',str(max_number_procs))
                reg_ex(self.cwd,'job.pbs','xxnodexx',min(node_list))
        
        elif type=='namd':
            # define node_list: per section; node: per subsection;
            node_list = node_list_qc + node_list_dq + node_list_opteron + node_list_node
            node  = min(node_list)
            # print node_list,node
            max_number_procs = node_dct[node]
            # print max_number_procs,self.pbs_script # (if o-node-> 4, dq-node-> 8)
            reg_ex(self.cwd,'job.pbs','xxnodexx',min(node_list))
            # print 'self.nprocs',self.nprocs,int(self.nprocs)
            # print 'max_number_procs',max_number_procs,int(max_number_procs)
            if int(self.nprocs) <= int(max_number_procs):
                reg_ex(self.cwd,'job.pbs','xxprocsxx',str(self.nprocs))
            else:
                print "%s must be less than %s" % (self.nprocs,max_number_procs)
                print "Using maximum of processors allowed, %s" % max_number_procs
                time.sleep(1.4)
                reg_ex(self.cwd,'job.pbs','xxprocsxx',str(max_number_procs))

        elif type=='sop':
            # define node_list: per section; node: per subsection;
            node_list = node_list_opteron + node_list_node
            node  = min(node_list)
            max_number_procs = node_dct[node]
            reg_ex(self.cwd,'job.pbs','xxnodexx',node)
            
        elif type=='sopnucleo':
            # define node_list: per section; node: per subsection;
            node_list = node_list_node + node_list_qc + node_list_dq
            node  = min(node_list)
            max_number_procs = node_dct[node]
            reg_ex(self.cwd,'job.pbs','xxnodexx',node)

        elif type=='gsop':
            max_number_procs = 1

        # print node,node_list
        return max_number_procs

    def compile_with_make(self):
        ''' sop: issue make command
        '''
        if self.job_type=='namdgpu':
            pass
            
        elif self.job_type=='namd':
            pass

        elif self.job_type=='gsop':
            pass

        elif self.job_type=='sop':

            def build_dct(keys,values):
                return dict(zip(keys,values))

            def regex_on_main(dct):
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdha1_loopxx',dct['dha1_loop'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdhb_loopxx',dct['dhb_loop'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdhc2_loopxx',dct['dhc2_loop'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdha1_helixxx',dct['dha1_helix'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdha2_helixxx',dct['dha2_helix'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdhb_helixxx',dct['dhb_helix'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdhc1_helixxx',dct['dhc1_helix'])
                reg_ex(self.cwd,self.fn_main_sop,\
                       'xxdhc2_helixxx',dct['dhc2_helix'])

            def get_config(id):
                config = ConfigParser.ConfigParser()
                config.read('lh.conf')
                params = config.get(id,'lh_params')
                return [p for p in params.split(',')]

            # clean
            pipe=subprocess.Popen(['make','clean'],stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = pipe.communicate()
            print 'stdout >> ',stdout
            print 'stderr >> ',stderr

            # Start Regular Expressions on main_pullends.c
            cp_file(self.cwd,self.fn_main_sub,self.cwd,\
                    self.fn_main_sop)

            # substituted params
            lh_keys = ['dha1_loop','dhb_loop','dhc2_loop','dha1_helix',
                       'dha2_helix','dhb_helix',\
                       'dhc1_helix','dhc2_helix']
            lh_params = get_config('DEFAULT')
            print lh_params
            dct_used = build_dct(lh_keys,lh_params)
            print dct_used
            regex_on_main(dct_used)

            # End Regular Expressions on main_pullends.c
            print 'reqular expressions on main_sub.c COMPLETE'

            # make command
            pipe=subprocess.Popen(['make',self.make_command],stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = pipe.communicate()
            print 'stdout >> ',stdout
            print 'stderr >> ',stderr
            return stdout,stderr
            
        elif self.job_type=='sopnucleo':
            # clean
            pipe=subprocess.Popen(['make','clean'],stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = pipe.communicate()
            print 'stdout >> ',stdout
            print 'stderr >> ',stderr
            # return stdout,stderr # EXITS - must comment
            # make_command: make lee
            pipe=subprocess.Popen(['make',self.make_command],stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = pipe.communicate()
            print 'stdout >> ',stdout
            print 'stderr >> ',stderr
            return stdout,stderr

    def build_run_dct(self,type='sop',dir_loc=os.getcwd(),ppn=1):
        ''' returns dictionary of files in os.listdir
            with key equivalent to 3 letter code
            use: run_dct = build_run_dct(specific_directory)
        '''
        file_list = os.listdir(dir_loc)
        # file_list.remove('submit.py')
        dct = {}
        dct['procs']=ppn
        if (type=='sop') or (type=='sopnucleo'):
            code3 = []
            for f in file_list:
                s = f.lower().strip()[0:3]   # 345
                code3.append(s)
                dct[s]=f
            # print code3
            return dct
        elif (type=='namd') or (type=='namdgpu') or (type=='gsop'):
            codes = []
            for f in file_list:
                s = f.lower().strip().split('.')[-1]
                codes.append(s)
                dct[s]=f
            return dct
        else:
            print 'no job type, exiting script from build_run_dct()'
            sys.exit()

    # def prepare_pbs(self,type='sop',command_dct={}):
    def prepare_pbs(self,command_dct={}):
        ''' perform regular expressions regarding running the job specific to job type
            i.e. namd,namdgpu,sop,sopnucleo
        '''
        # print self.job_type
        # sys.exit()
        # if (type=='sop') or (type=='sopnucleo'):
        print "JOB TYPE selected: %s" % self.job_type

        if (self.job_type=='sop') or (self.job_type=='sopnucleo'):
            # print "found JOB TYPE: %s" % self.job_type
            try:
                reg_ex(self.cwd,'job.pbs','xxstructxx',command_dct['sec'])
            except:
                pass
            reg_ex(self.cwd,'job.pbs','xxpdbxx',command_dct['pdb'])
            reg_ex(self.cwd,'job.pbs','xxcontactxx',command_dct['con'])
            reg_ex(self.cwd,'job.pbs','xxseedxx',str(self.seed300))
            reg_ex(self.cwd,'job.pbs','xxrunxx',command_dct['run'])
            reg_ex(self.cwd,'job.pbs','xxargv_onexx',self.make_command)
            
        elif (self.job_type=='gsop'):
            pass

# {'.gi': '.git',
#  '1aj': '1AJ3.pdb',
#  'bio': 'biopython',
#  'con': 'Contact_map_intra_b_ehD1_2.0_ehD2_2.0_2mol',
#  'dcd': 'dcdio.c',
#  'deb': 'debug.h',
#  'def': 'def_param_debug.h',
#  'for': 'force_pullends_dihedrals.c',
#  'ide': 'identify.c',
#  'ite': 'iteration.c',
#  'job': 'job-testing_sop_dev__02-19-2014_1850__193_4285991.txt',
#  'mai': 'main_sub.c',
#  'mak': 'Makefile',
#  'pdb': 'pdb2dhl.ent',
#  'plo': 'plot_sop.py',
#  'procs': 4,
#  'qsu': 'qsub.py',
#  'ras': 'ras_structure.c',
#  'rea': 'README.md',
#  'rfo': 'rforce.c',
#  'run': 'run_protein_ll',
#  'sec': 'Secondary_struct_2dhl',
#  'sop': 'sopnucleo',
#  'str': 'structure.h',
#  'sum': 'sum_dihedral.py',
#  'syn': 'sync_up.sh',
#  'tag': 'TAGS',
#  'tem': 'template_sop.pbs',
#  'upd': 'update_dihedrals_dcd_fullGo.c'}
            # ./xxrunxx xxpdbxx xxcontactxx xxstructxx xxseedxx
            # ./run_protein xxpdbxx xxcontactxx xxstructxx xxseedxx
            # make xxargv_onexx
            #PBS -l nodes=1:ppn=1:xxnodexx

        elif (self.job_type=='namd') or (self.job_type=='namdgpu'):
            print "JOBTYPE: %s" % self.job_type
            reg_ex(self.cwd,'job.pbs','xxnamdconfigxx',command_dct['namd'])
            # if (len(sys.argv)==2) or (len(sys.argv)==3):
            #     print 'command line argument, # of processors: %s' % command_dct['procs']
            #     reg_ex(self.cwd,'job.pbs','xxprocsxx',command_dct['procs'])
            # elif type=='namdgpu':
            #     reg_ex(self.cwd,'job.pbs','xxprocsxx',str(command_dct['procs']))
            # else:
            #     print 'Used 1 processor'
            #     reg_ex(self.cwd,'job.pbs','xxprocsxx','1')

        else:
            print 'NO job type FOUND, exiting script'
            sys.exit()

    # def construct_local_dir(self,type='sop',command_dct={}):
    def construct_local_dir(self,command_dct={}):
        ''' Make and copy necessary files into local_dir, based on job type.
            i.e. namd,namdgpu,sop,sopnucleo
        '''
        # make directory
        print "constructing job's local directory: %s" % self.job_path_local
        if not os.path.exists(self.job_path_local): os.makedirs(self.job_path_local)
        
        # develop
        # print self.job_type
        # import pprint
        # pprint.pprint(command_dct)
        # sys.exit()

        if (self.job_type=='namd') or (self.job_type=='namdgpu'):
            cp_file(self.cwd,command_dct['namd'],self.job_path_local,command_dct['namd'])
            cp_file(self.cwd,command_dct['pdb'],self.job_path_local,command_dct['pdb'])
            cp_file(self.cwd,command_dct['prm'],self.job_path_local,command_dct['prm'])
            cp_file(self.cwd,command_dct['psf'],self.job_path_local,command_dct['psf'])
            cp_file(self.cwd,command_dct['tcl'],self.job_path_local,command_dct['tcl'])
            cp_file(self.cwd,command_dct['pbs'],self.job_path_local,command_dct['pbs'])

            ref_files = glob('*.ref')
            [cp_file(self.cwd,ref,self.job_path_local,ref) for ref in ref_files]
            # cp_file(self.cwd,'hold_ca.ref',self.job_path_local,'hold_ca.ref')
            psf_files = glob('*.psf')
            [cp_file(self.cwd,psf,self.job_path_local,psf) for psf in psf_files]

            vel_files = glob('*.vel')
            [cp_file(self.cwd,vel,self.job_path_local,vel) for vel in vel_files]

            coor_files = glob('*.coor')
            [cp_file(self.cwd,coor,self.job_path_local,coor) for coor in coor_files]

            xsc_files = glob('*.xsc')
            [cp_file(self.cwd,xsc,self.job_path_local,xsc) for xsc in xsc_files]

            # JOBTYPE: namd
            # {'config': 'config',
            #  'dat': 'center_minmax_00_start.dat',
            # *** #  'namd': '01_min.namd',
            #  'pbs': 'job.pbs',
            # *** #  'pdb': '00_start.pdb',
            # *** #  'prm': 'par_all27_prot_lipid.prm',
            #  'procs': 8,
            # *** #  'psf': '00_start.psf',
            #  'py': 'submit.py',
            #  'ref': 'hold.ref',
            # *** # hold_ca.ref
            # *** #  'tcl': 'minmax_density.tcl'}

        elif self.job_type=='sop':
            pass

        elif self.job_type=='sopnucleo':
            cp_file(self.cwd,command_dct['mak'],self.job_path_local,command_dct['mak'])
            cp_file(self.cwd,command_dct['run'],self.job_path_local,command_dct['run'])
            cp_file(self.cwd,command_dct['job'],self.job_path_local,command_dct['job'])
            cp_file(self.cwd,command_dct['con'],self.job_path_local,command_dct['con'])
            cp_file(self.cwd,command_dct['pdb'],self.job_path_local,command_dct['pdb'])
            cp_file(self.cwd,command_dct['qsu'],self.job_path_local,command_dct['qsu'])
            cp_file(self.cwd,'def_param.h',self.job_path_local,'def_param.h')

            # Directories are currently made in Bash template scripts
            # dir_path_Struct_data = os.path.join(self.job_path_local,'Struct_data')
            # if not os.path.exists(dir_path_Struct_data): os.makedirs(dir_path_Struct_data)
            # dir_path_Coord = os.path.join(self.job_path_local,'Coord')
            # if not os.path.exists(dir_path_Coord): os.makedirs(dir_path_Coord)
        # return max_number_procs
        
        elif self.job_type=='gsop':
            dir_temp = os.path.join(self.cwd,'templates')
            # if not os.path.exists(self.job_path_local): os.makedirs(self.job_path_local)
            seed_equilibrate = random.randint(10000,10000000)
            cp_file(dir_temp,'run_equil_template.sop',self.job_path_local,'run_equil.sop')
            reg_ex(self.job_path_local,'run_equil.sop','xxseedxx',str(seed_equilibrate))
            cp_file(dir_temp,'run_pull_template.sop',self.job_path_local,'run_pull.sop')
            reg_ex(self.job_path_local,'run_pull.sop','xxseedxx',str(self.seed10_7))

            cp_tree(self.cwd,'structures',self.job_path_local,'structures')
            cp_tree(self.cwd,'topologies',self.job_path_local,'topologies')
            
            # template_gsop.pbs => job.pbs => meta.sh
            cp_file(self.cwd,'job.pbs',self.job_path_local,'meta.sh')


    def write_class(self,location=None):
        ''' Write class and its attributes.
        '''
        # print location
        if location == None:
            o = open('job-%s.txt' % self.job_dir_name,'w+')
        else:
            o = open('%s/job-%s.txt' % (self.job_path_local,self.job_dir_name),'w+')
        keys = dir(self)
        for key in keys:
            # print key,':\t',getattr(self,key)
            definition = key + ':\t' + str(getattr(self,key)) + '\n'
            # print type(definition)
            o.write(definition)
        o.close()

    def submit(self):
        ''' Change to job_path_local, submit job_path_local_pbs_script.
        '''
        if self.job_type == 'gsop':
            print 'returning with no job submission'
            return 'stdout N/A','stderr N/A'
        # job_path_local :        /home/dale/sop_dev/sopnucleo/runsopnuc/testing_runsopnuc__05-17-2014_2114__207_8116469
        # job_path_local_pbs_script :     /home/dale/sop_dev/sopnucleo/runsopnuc/testing_runsopnuc__05-17-2014_2114__207_8116469/job.pbs
        os.chdir(self.job_path_local)
        pipe=subprocess.Popen(['qsub',self.job_path_local_pbs_script],stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = pipe.communicate()
        print 'stdout >> ',stdout
        print 'stderr >> ',stderr

        # -*- GET jobid -*-
        # # print os.path.dirname(path)
        # new_file = os.path.join(os.path.dirname(path),'sync1.sh')
        job_id_number = stdout.split('.')[0]

        try:
            print 'writing stdout to cwd'
            job_id_fname = job_id_number + '.OUT'
            # job_id_fpath = os.path.join(self.cwd,job_id_fname)
            job_id_fpath = os.path.join(self.job_path_local,job_id_fname)

            # write stdout to cwd
            with open(job_id_fpath,'w+') as fp:
                fp.write(job_id_number)

        except:
            print 'failed to write stdout to cwd'
            # pass

        # write stdout to job_rundir
        # try:
        #     print 'writing stdout to job_rundir'
        #     job_rundir_name = 'qsub_r.' + job_id_number + '.OUT'
        #     job_rundir_file = os.path.join(self.job_path_run,job_rundir_name)

        #     with open(job_rundir_file,'w+') as fp:
        #         fp.write(job_id_number)

        # except:
        #     print 'failed to write stdout to job_rundir'
        #     # pass
        
        # -*- Change back to self.cwd -*-
        os.chdir(self.cwd)
        return stdout,stderr

    def clean_with_make(self):
        import subprocess

        def run_command(invocation):
            pipe=subprocess.Popen(invocation,stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = pipe.communicate()
            print 'stdout >> ',stdout
            print 'stderr >> ',stderr

        if self.job_type == 'sopnucleo':
            print 'cleaning up %s' % self.job_type
            run_command(['make','pure'])
        
        if self.job_type == 'gsop':
            print 'cleaning up %s' % self.job_type
            os.remove('job.pbs')
            # os.remove(os.path.join(self.cwd,'job.pbs'))
            # run_command(['make','pure'])
        
    def db_mysql(self):
        # import MySQLdb
        # db = MySQLdb.connect(host="localhost",
        #                      user=self.user,
        #                      passwd='75',
        #                      db='~/thearchives.db')
        # cur = db.cursor()
        import sqlite3
