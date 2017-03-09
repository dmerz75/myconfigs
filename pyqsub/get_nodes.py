import os,sys,subprocess

my_dir    = os.path.abspath(os.path.dirname(__file__))
my_library = os.path.expanduser('~/.pylib/pyqsub')

#  ---------------------------------------------------------  #
#  subprocess                                                 #
#  ---------------------------------------------------------  #
def run_command(args):
    pipe=subprocess.Popen(args,stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = pipe.communicate()
    # print stdout
    print 'stderr >> ',stderr
    return stdout.split(' ')[1]

comp_arch = run_command(['uname','-a'])
# print comp_arch.lower()
# if (comp_arch.lower() != 'manjaro') or (comp_arch.lower() != 'm870'):
# print comp_arch.lower() == 'm870'
if (comp_arch.lower() != 'm870'):
    print "getting nodes  ..."
    text = os.system('pbsnodes > %s/temp_nodes' % my_library)   # Later 1 of 2
node_file = os.path.join(my_library,'temp_nodes')



def get_nodes():
    count = 0
    tup_nodeline_plusone = []
    # -----------------Node  file-------------------------------------
    with open(node_file,'r') as nf:
        ''' parse temp_nodes file, identify lines with available nodes
            identify lines that start with a letter and end with a digit, i.e. o9
            save line number, count and plus one, (state = free) line 
        '''
        for line in nf:
            try:
                if line[0].isalpha()==True and line[-2].isdigit()==True:
                    #print line
                    #print line[0].isalpha(),line[-2].isdigit()
                    line = line.rstrip()
                    tup_nodeline_plusone.append((count,count+1))
                else:
                    pass
            except:
                pass
            count += 1

    o = open(node_file,'r')
    text = o.readlines()
    o.close()

    available_nodes = []
    for tup_lines in tup_nodeline_plusone:
        ''' get lines identified as free nodes
            establish node, i.e. o9 or dq2
            get np, number of processors, 2 lines below node o9
            create tuple, (node,int(np)), i.e. (o3,4) node o3 with 4 procs
        '''
        node = text[tup_lines[0]].rstrip()
        np   = text[tup_lines[0]+2].split('=')[-1].strip()
        if text[tup_lines[1]].split('=')[-1].strip() == 'free':
            available_nodes.append((node,int(np)))
    if not available_nodes:
        available_nodes.append(('o2200',1))  # nprocs
    # print available_nodes[0]
    # print available_nodes
    # sys.exit()
    # os.remove(node_file)      # Later 2 of 2
    return available_nodes
