import sys
import os
import getpass
import re

# GET: user, address, source, dest

# def search_func(pattern,x):
#     re.search



class Connection():
    """ for RSYNC
    """
    def __init__(self,):
        self.local_user = 'default'
        self.remote_user = 'default'
        self.directory = 'default'
        self.direction = 'default'
        self.codes = ['uc','b2','biocat','lib','gpu105','gpu24',\
                      'gpu81','gpu82','gpu70']
        self.destination = 'default' # code: uc, b2 ..
        self.address = 'default'
        self.command = ['default']
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

    # def load_data(self,path):

    # def get_user(self,ucode=0,way='up',user=''):
    #     if ucode == 0:
    #         print "running get_user"
    #         user = getpass.getuser()
    #     else:
    #         if way == 'up':
    #             print 'found up'
    #             if user == 'dale':
    #                 user = 'merzdr'
    #             elif user == 'merzdr':
    #                 user = 'dmerz3'
    #             else:
    #                 user = 'dmerz3'
    #         else:
    #             print 'found down'
    #             if user == 'dale':
    #                 user = 'merzdr'
    #             elif user == 'merzdr':
    #                 user = 'dmerz3'
    #             else:
    #                 user = 'dmerz3'
    #     return user

    def get_user_local(self):
        print "running get_user_local"
        self.local_user = getpass.getuser()

    # def get_user_remote(self,address):
    def get_user_remote(self):
        print "running get_user_remote"
        print sys.argv[1:]
        destination = [x for x in self.codes if x in sys.argv[1:]]
        self.destination = destination[0]
        self.get_address()

        if re.search("ucfile",self.address) != None:
            user = 'merzdr'
        else:
            user = 'dmerz3'
        self.remote_user = user
        # return
        # elif re.search("biogate2",address) != None:
        #     user = 'dmerz3'
        # else:
        # return user

    def get_address(self):
        print "running get_address"
        print self.destination
        dct_addr = {'biocat':'10.46.1.143',
                    'lib':'10.46.1.108',
                    'gpu47':'10.43.7.47',
                    'gpu105':'10.46.1.105',
                    'gpu24':'10.46.1.24',
                    'gpu81':'10.46.1.81',
                    'gpu82':'10.46.1.82',
                    'gpu70':'10.46.1.70',
                    'uc':'ucfilespace.uc.edu',
                    'b2':'biogate2.cros.uc.edu',
                    }
        address = dct_addr.get(self.destination)
        self.address = address
        # return address

    def get_direction(self):
        result = 0
        while result == 0:
            for x in sys.argv[1:]:
                if re.search("up",x) != None:
                    self.direction = 'up'
                    result = 1
                    break
                else:
                    self.direction = 'down'
            result += 1

    def get_directory(self):
        # print os.getcwd()
        # return
        if len(sys.argv[1:]) <= 2:
            my_dir = os.path.abspath(os.path.dirname(__file__))
            print my_dir
            print os.getcwd()
            self.directory = os.path.join(os.getcwd(),'upload')
        else:
            self.directory = os.path.join(os.getcwd(),sys.argv[-1])
            pass
            # self.directory = os.path.join(os.path)

        # re.search("up",x for x in sys.argv[1:]]
        # if re.search("up",sys.argv[1:]) != None:
        #     self.direction = 'up'
        # else:
        #     self.direction = 'down'

    def build_command(self):

        if self.direction == 'up':
            dest = self.remote_user + '@' + self.address + ':' + '~'
            source = self.directory
        else:
            source = self.remote_user + '@' + self.address + ':' + self.directory # + '/*'
            dest = os.path.expanduser('~')

        command = ['rsync','-avh',source,dest]
        self.command = command

    # def run_command(self):



    def get_source_dest(self,user,way='up',address="~/highway1"):
        # address = get_address(sys.argv[2])
        if way == 'up':
            # user = get_user(1,way,user)
            user_local = get_user_local()
            user_remote = get_user_remote(address)
            dest = user_remote + '@' + address + ':' + '~'
            source = os.path.expanduser('~/upload')
        else: # DOWN
            # user = get_user(1,way,user)
            user_local = get_user_local()
            user_remote = get_user_remote(address)
            source = user_remote + '@' + address + ':' + '~/takedown'
            dest = os.path.expanduser('~')

        print "running get_source"
        return source,dest

    def load_profile(self,key=0):
        if key == 0:

            pass
        else:
            pass
