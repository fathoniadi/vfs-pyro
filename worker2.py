from __future__ import print_function
import Pyro4
import os
import shutil

@Pyro4.expose
@Pyro4.callback
class Worker(object):

    sharing_folder = {}

    def __init__(self):
        self.sharing_folder['base'] = '/home/fathoniadi/Documents/sister/vfs-pyro/worker2'


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

    def getSize(self):
        disk = os.statvfs(self.sharing_folder['base'])
        return disk.f_bfree

    def listSource(self, cwd, path=None):
        flag, full_path = self.checkData(path)
        if(flag == 1):
            print(full_path)
            
            return None, 'Berhasil'

        elif(flag == 2):
            print(full_path)
            for root, dirs, files in os.walk(full_path, topdown=True):
                for name in files:
                    print(os.path.join(root, name))
                for name in dirs:
                    print(os.path.join(root, name))

            return None, 'Berhasil'
        else:
            return 'Tidak ada', None

    def listingFolder(self, cwd, path=None):
        # if(path == '/'):
        #     return None, [self.sharing_folder['path']]
        print(path)
        flag = self.isExistFolder(path)
        if(flag):
            print(self.sharing_folder['base']+path)
            list_folders = os.listdir(self.sharing_folder['base']+path)
            return None, list_folders
        else:
            return 'Folder tidak ada', []

    def touch(self, cwd, path=None):

        # paths = path.split('/')
        # if(len(paths)==2):
        #     return 'Permission Denied: Tidak bisa membuat file di root', None

        # if(paths[1] != self.sharing_folder['path'] and paths[1]!='/'):
        #     return 'Tidak', None
        full_path = self.sharing_folder['base']+path
        if(os.path.isfile(full_path)):
            return 'Tidak bisa membuat file, file sudah ada', None
        try:
            with open(full_path, 'w'):
                os.utime(full_path, None)
                print('bisa')
                return None, 'File sudah dibuat'
        except Exception as e:
            err = str(e)
            return err.replace(self.sharing_folder['base'],''), None


def main():
    Pyro4.Daemon.serveSimple(
        {
            Worker: "worker"
        },
        ns=False, host="127.0.0.1", port=9002)


if __name__ == "__main__":
    main()
