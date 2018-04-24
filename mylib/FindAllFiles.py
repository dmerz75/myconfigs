#  ---------------------------------------------------------  #
#  findall_files:                                             #
#  ---------------------------------------------------------  #
# snippet: faf
import os
import re
import sys
# from glob import glob
import glob
import fnmatch

class FindAllFiles():
    """ File locator
        args: directory,filename/type
    """
    def __init__(self,params=None):
        self.cwd = None
        self.pattern = None
        self.dct = {}
        self.total = 0
        self.lst_files = []

        # print type(params)
        if type(params) == dict:
            for k,v in params.items():
                setattr(self,k,v)

    def print_class(self):
        keys = dir(self)
        for key in keys:
            print(key,':\t',getattr(self,key))

    def print_query(self,dct=None):
        if dct == None:
            dct = self.dct
        print(len(dct.keys()),'of',self.total)
        for k,v in dct.items():
            # print k,' type:',v['type']
            print(k,v['dirname'],v['filename'])

    def get_files(self):
        count = 0
        for dirpath,basenames,filenames in os.walk(self.cwd):
            for name in filenames:
                if fnmatch.fnmatch(name,self.pattern):
                    # curdir = os.path.basename(name)
                    # os.chdir(curdir)
                    # if len(glob.glob())
                    # if glob.glob(self.pattern):
                        # print glob.glob(self.pattern)
                    # continue
                # if not re.search(self.pattern,name) == None:

                    count += 1
                    fp = os.path.join(dirpath,name)
                    self.lst_files.append(fp)
                    self.dct[count] = {}
                    self.dct[count]['type'] = self.pattern
                    self.dct[count]['file'] = fp
                    self.dct[count]['filename'] = name
                    self.dct[count]['dirname'] = dirpath
                    self.total = count

    def merge_dct(self,lst_dct):

        # new dict
        dct = {}

        # the to be combined dct.
        for d in lst_dct:
            dct.update(d)

        # built.
        return dct

    def get_overlapping_entries(self,dctA,dctB):
        """
        Get overlapping entries (in both dct).
        """

        dct = {}

        lst_keys = []

        for k,v in dctA.iteritems():

            if k in dctB.keys():

                lst_keys.append(k)

        for k in lst_keys:
            dct[k] = dctB[k]

        return dct


    def sort_dirname(self,pos,dct=None):
        if dct == None:
            dct = self.dct

        klist = dct.keys()
        # print klist
        xlist = [dct[k]['dirname'].split('/')[pos] for k in klist]
        # print xlist
        # klist.pop(3)
        # klist.insert(3,15)
        slist = sorted(zip(xlist,klist))
        # print sorted(slist)
        count = 0
        dct_r = {}
        for s in slist:
            dct_r[count] = {}
            dct_r[count]['type'] = dct[s[1]]['type']
            dct_r[count]['file'] = dct[s[1]]['file']
            dct_r[count]['filename'] = dct[s[1]]['filename']
            dct_r[count]['dirname'] = dct[s[1]]['dirname']
            count += 1
        return dct_r

    def sort_filename(self,dct=None):
        if dct == None:
            dct = self.dct

        dlist = [k['filename'] for k in dct.values()]
        dlist2 = [int(re.findall(r'\d+',d)[0]) for d in dlist]
        slist = sorted(zip(dlist2,dct.keys()))

        count = 0
        dct_r = {}
        for s in slist:
            dct_r[count] = {}
            dct_r[count]['type'] = dct[s[1]]['type']
            dct_r[count]['file'] = dct[s[1]]['file']
            dct_r[count]['filename'] = dct[s[1]]['filename']
            dct_r[count]['dirname'] = dct[s[1]]['dirname']
            count += 1

        return dct_r

        # print sorted(dlist)
        print(dlist)
        print(dlist2)
        print(dct.keys())
        print(slist)

        return dct
        # print klist
        xlist = [dct[k]['filename'].split('/')[-1] for k in klist]
        # print xlist
        # klist.pop(3)
        # klist.insert(3,15)
        slist = sorted(zip(xlist,klist))
        # print sorted(slist)
        count = 0
        dct_r = {}
        for s in slist:
            dct_r[count] = {}
            dct_r[count]['type'] = dct[s[1]]['type']
            dct_r[count]['file'] = dct[s[1]]['file']
            dct_r[count]['filename'] = dct[s[1]]['filename']
            dct_r[count]['dirname'] = dct[s[1]]['dirname']
            count += 1
        return dct_r


    def query_file(self,searchstring,dct=None):
        if dct == None:
            dct = self.dct
        return {k:v for k,v in dct.items() if re.search(searchstring,v['file']) != None}
    def query_filename(self,searchstring,dct=None):
        if dct == None:
            dct = self.dct
        return {k:v for k,v in dct.items() if re.search(searchstring,v['filename']) != None}
    def query_dirname(self,searchstring,pos=None,dct=None):
        if dct == None:
            dct = self.dct
        if (pos == None) or (pos == -1):
            return {k:v for k,v in dct.items() if re.search(searchstring,v['dirname']) != None}
        else:
            return {k:v for k,v in dct.items() if re.search(searchstring,v['dirname'].split('/')[pos]) != None}
    def remove_file(self,searchstring,dct=None):
        if dct == None:
            dct = self.dct
        return {k:v for k,v in dct.items() if re.search(searchstring,v['file']) == None}
    def remove_filename(self,searchstring,dct=None):
        if dct == None:
            dct = self.dct
        return {k:v for k,v in dct.items() if re.search(searchstring,v['filename']) == None}
    def remove_dirname(self,searchstring,pos=None,dct=None):
        if dct == None:
            dct = self.dct
        if pos == None:
            return {k:v for k,v in dct.items() if re.search(searchstring,v['dirname']) == None}
        else:
            return {k:v for k,v in dct.items() if re.search(searchstring,v['dirname'].split('/')[pos]) == None}

    def from_dirs_get_files(self,searchstring,dct=None):
        lst_empty = []
        lst_files = []
        if dct == None:
            dct = self.dct
        dct_new = {}
        count = 0
        for k in dct.keys():
            fpall = glob.glob(os.path.join(dct[k]['dirname'],searchstring))
            if fpall:
                lst_files += fpall
            else:
                lst_empty.append(dct[k]['dirname'])
        # print lst_files
        # print lst_empty

        for i in range(len(lst_files)):
            dct_new[i] = {}
            dct_new[i]['type'] = searchstring
            dct_new[i]['file'] = lst_files[i]
            dct_new[i]['filename'] = os.path.basename(lst_files[i])
            dct_new[i]['dirname'] = os.path.dirname(lst_files[i])
        x = len(dct_new.keys())
        print('returning',len(dct_new.keys()),searchstring,'files;','empty dirs:',len(lst_empty))
        return dct_new,lst_empty

    def rename_file(self,dct=None,modstring=None):
        lst_dirs = []
        # if modstring == None:
        #     modstring = str(0).zfill(2)
        if dct == None:
            dct = self.dct

        mod_orig = modstring
        for k in dct.keys():
            os.chdir(dct[k]['dirname'])

            if mod_orig == None:
                modstring = str(0).zfill(2)
            else:
                modstring = str(int(mod_orig)).zfill(2)

            # get dirs (were "emptied")
            # list_dirs.append(dct[k]['dirname'])

            print('renaming:',dct[k]['filename'])
            newfile = dct[k]['filename'] + '.' + modstring
            # print newfile
            while os.path.exists(newfile):
                modstring = str(int(modstring) + 1).zfill(2)
                print('mod:',modstring)
                newfile = dct[k]['filename'] + '.' + modstring
            print(newfile)
            os.rename(dct[k]['filename'],newfile)

            # while os.path.exists(dct[k]['filename']):
            #     print 'current file:',dct[k]['filename']
            #     if not os.path.exists(newfile):
            #         print 'creating new file:',newfile
            #         os.rename(dct[k]['filename'],newfile)
            #     else:
            #         modstring = str(int(modstring) + 1).zfill(2)
            #         newfile = dct[k]['filename'] + '.' + modstring
            #         print 'creating new file:',newfile
            #         os.rename(dct[k]['filename'],newfile)

            # print 'file exists.'
                # print 'creating new file:',newfile
                # os.rename(dct[k]['filename'],newfile)
        # print type(lst_dirs)
        return lst_dirs

    def delete_file(self,dct=None):
        if dct == None:
            dct = self.dct
        for k in dct.keys():
            os.chdir(dct[k]['dirname'])
            print(dct[k]['filename'])
            os.remove(dct[k]['filename'])
