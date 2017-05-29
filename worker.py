from __future__ import print_function
import Pyro4
import os
import shutil

@Pyro4.expose
@Pyro4.callback
class Worker(object):

    sharing_folder = {}

    def __init__(self):
        self.sharing_folder['base'] = '/home/fathoniadi/Documents/sister/vfs-pyro/worker1'


    def isExistFolder(self, path):
        # if(path == '/'):
        #     path = path+self.sharing_folder['path']

        # paths = path.split('/')
        # if(paths[1] != self.sharing_folder['path'] and paths[1]!='/'):
        #     return False
        full_path = self.sharing_folder['base']+path
        if(os.path.isdir(full_path)):
            return True
        else:
            return False


    def getSharingFolder(self):
        return self.sharing_folder

    def checkData(self, path):
        # if(path == '/'):
        #     path = path+self.sharing_folder['path']
        # paths = path.split('/')
        # if(paths[1] != self.sharing_folder['path'] and paths[1]!='/'):
        #     return 'Tidak', None
        full_path = self.sharing_folder['base']+path
        if(os.path.isfile(full_path)):
            return 1, full_path
        elif(os.path.isdir(full_path)):
            return 2, full_path
        else:
            return 0, full_path

    def removeData(self, cwd, path=None):
        flag, full_path = self.checkData(path)
        if(flag == 1):
            os.remove(full_path)
            return None, 'Berhasil'

        elif(flag == 2):
            shutil.rmtree(full_path)
            return None, 'Berhasil'
        else:
            return 'Tidak ada', None

    def listSource(self, cwd, path=None):
        list = []
        flag, full_path = self.checkData(path)
        if(flag == 1):
            print(full_path)
            return None, 1, [{'name':path, 'type':1}]

        elif(flag == 2):
            print(full_path)
            for root, dirs, files in os.walk(full_path, topdown=True):
                for name in files:
                    list.append({'name':os.path.join(root, name).replace(full_path,''), 'type':1})
                for name in dirs:
                    list.append({'name':os.path.join(root, name).replace(full_path,''), 'type':2})

            return None, 2, list
        else:
            return 'Tidak ada', 0, None

    def listingFolder(self, cwd, path=None):
        flag = self.isExistFolder(path)
        if(flag):
            print(self.sharing_folder['base']+path)
            list_folders = os.listdir(self.sharing_folder['base']+path)
            return None, list_folders
        else:
            return 'Folder tidak ada', []

    def getSize(self):
        disk = os.statvfs(self.sharing_folder['base'])
        return disk.f_bfree

    def makeFolder(self, cwd, path):
        full_path = self.sharing_folder['base']+path
        print('Folder baru '+full_path)
        if(os.path.exists(full_path)):
            return 'Tidak bisa membuat folder, folder sudah ada', None
        try:
            os.makedirs(full_path)
            return None, 'Folder sudah dibuat'
        except Exception as e:
            err = str(e)
            err = err.replace(self.sharing_folder['base'],'')
            print(err)
            return err, None

    def makeFile(self, cwd, path, data):
        full_path = self.sharing_folder['base']+path
        if(os.path.isfile(full_path)):
            return 'Tidak bisa membuat file, file sudah ada', None
        try:
            with open(full_path, 'wb') as file:
                file.write(data)
            return None, 'File sudah dibuat'
        except Exception as e:
            err = str(e)
            return err.replace(self.sharing_folder['base'],''), None

    def readFile(self, cwd, path=None):
        flag, full_path = self.checkData(path)
        data = ''
        with open(full_path, 'rb') as file:
            data = file.read()

        return data

    def touch(self, cwd, path=None):
        full_path = self.sharing_folder['base']+path
        print(full_path)
        if(os.path.isfile(full_path)):
            return 'Tidak bisa membuat file, file sudah ada', None
        try:
            with open(full_path, 'wb'):
                os.utime(full_path, None)
                return None, 'File sudah dibuat'
        except Exception as e:
            err = str(e)
            return err.replace(self.sharing_folder['base'],''), None


def main():
    Pyro4.Daemon.serveSimple(
        {
            Worker: "worker"
        },
        ns=False, host="127.0.0.1", port=9001)


if __name__ == "__main__":
    main()
