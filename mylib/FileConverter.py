import os
from glob import glob
import shutil
import zipfile
import gzip

class FileConverter(object):

    def __init__(self,main_path,ext1,final_path,ext2):

        self.main_path = main_path
        self.final_path = final_path
        self.temp_path = os.path.join(self.main_path,'temp_path')
        self.ext1 = ext1
        self.ext2 = ext2

        print(self.main_path)

        if not os.path.exists(self.final_path):
            os.makedirs(self.final_path)

    def MakeTempPath(self):
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)
        else:
            shutil.rmtree(self.temp_path)
            os.makedirs(self.temp_path)

    def UnzipFile(self,zipped_file,zip_to):
        zip_ref = zipfile.ZipFile(zipped_file, 'r')
        zip_ref.extractall(zip_to)
        zip_ref.close()
        self.zipfiles = glob(os.path.join(zip_to,'*'))

    def Gzip(self,gzip_src,gzip_dst):

        with open(gzip_src, 'rb') as fi, gzip.open(gzip_dst, 'ab') as fo:
            shutil.copyfileobj(fi, fo)

    def FindFiles(self):

        lst_files = glob(os.path.join(self.main_path,'*.ZIP'))
        self.files = lst_files

    def BuildCommandList(self,command):

        self.command_list.append(command)

    def ScrubData(self,raw_file):

        with open(raw_file,'rb+') as fp:
            for l in fp.readlines()[0:20]:
                print(l)

    def CopyFiles(self):

        for f in self.files:
            print(f)
            self.filename = os.path.splitext(os.path.basename(f))[0]
            print(self.filename)
            self.MakeTempPath()
            self.UnzipFile(f,self.temp_path)
            print(self.zipfiles,len(self.zipfiles))

            for z in self.zipfiles:
                # Process, sieve, ..
                self.ScrubData(z)
                file_out = os.path.join(self.final_path,self.filename + '.gz')
                self.Gzip(z,file_out)

            if os.path.exists(file_out):
                os.remove(f)
            # os.chdir(self.main_path)
            # os.remove(self.main_path)

        shutil.rmtree(self.temp_path)

