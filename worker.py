from __future__ import print_function
import Pyro4
import os
import shutil

@Pyro4.expose
@Pyro4.callback
class Worker(object):

    sharing_folder = {}

    def __init__(self):
        self.sharing_folder['base'] = '/home/administrator/Documents/sister/vfs-pyro'
        self.sharing_folder['path'] = 'worker1'


    def isExistFolder(self, path):
        if(path == '/'):
            path = path+self.sharing_folder['path']

        paths = path.split('/')
        if(paths[1] != self.sharing_folder['path'] and paths[1]!='/'):
            return False
        full_path = self.sharing_folder['base']+path
        print(full_path)
        if(os.path.isdir(full_path)):
            print("Ada")
            return True
        else:
            print("Tidak")
            return False


    def getSharingFolder(self):
        return self.sharing_folder

    def checkData(self, path):
        if(path == '/'):
            path = path+self.sharing_folder['path']
        paths = path.split('/')
        if(paths[1] != self.sharing_folder['path'] and paths[1]!='/'):
            return False
        full_path = self.sharing_folder['base']+path
        print(full_path)
        if(os.path.isfile(full_path)):
            return 1, full_path
        elif(os.path.isdir(full_path)):
            return 2, full_path
        else:
            return 0, full_path

    def removeData(self, cwd, path=None):
        flag, full_path = self.checkData(path)
        print(path)
        if(flag == 1):
            print('ini file')
            os.remove(full_path)
            return None, 'Berhasil'

        elif(flag == 2):
            print('ini folder')
            shutil.rmtree(full_path)
            return None, 'Berhasil'
        else:
            print('tidak ada')
            return 'Tidak ada', ''

    def listingFolder(self, cwd, path=None):
        print (path)
        if(path == '/'):
            return None, [self.sharing_folder['path']]

        flag = self.isExistFolder(path)
        if(flag):
            list_folders = os.listdir(self.sharing_folder['base']+path)
            print(list_folders)
            return None, list_folders
        else:
            return 'Folder tidak ada', []



def main():
    Pyro4.Daemon.serveSimple(
        {
            Worker: "worker"
        },
        ns=False, host="127.0.0.1", port=9001)


if __name__ == "__main__":
    main()
