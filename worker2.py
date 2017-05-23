from __future__ import print_function
import Pyro4
import os

@Pyro4.expose
@Pyro4.callback
class Worker(object):

    sharing_folder = {}

    def __init__(self):
        self.sharing_folder['base'] = '/home/fathoniadi/Documents/sister/vfs-pyro'
        self.sharing_folder['path'] = 'worker2'

    #def createPath(self,wcd ,path):

    def isExistFolder(self, path):
        print(path)
        if(path == '/'):
            path = path+self.sharing_folder['path']
        
        paths = path.split('/')
        if(paths[1] != self.sharing_folder['path']):
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

    def listingFolder(self, cwd, path=None):
        print (path)
        if(path == '/'):
            return None,[self.sharing_folder['path']]

        flag = self.isExistFolder(path)
        if(flag):
            print('Masuk sini')
            return None, os.listdir(self.sharing_folder['base']+path)
        else:
            return 'Folder tidak ada', []

        

def main():
    Pyro4.Daemon.serveSimple(
        {
            Worker: "worker"
        },
        ns=False, host="127.0.0.1", port=9002)


if __name__ == "__main__":
    main()