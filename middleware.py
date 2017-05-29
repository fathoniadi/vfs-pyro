import sys
import Pyro4
import os

list_workers = ['PYRO:worker@127.0.0.1:9001', 'PYRO:worker@127.0.0.1:9002']
workers = []


@Pyro4.expose
@Pyro4.callback
class Middleware(object):

    def __init__(self):
        self.commands = ['ls','cd','rm','mv','touch','exit']
        return

    def getCommands(self):
        return self.commands

    def generateStructureFolder(self, cwd, args, path_req=''):
        if(len(args)==1):
            return cwd
        else:
            if path_req[0] == '/':
                return path_req

            elif '../' in path_req:
                temp_args = path_req.split('../')
                empty_n = temp_args.count('')

                temp_cwds = cwd.split('/')

                if(len(temp_args)==empty_n):
                    counter = empty_n-1

                    if(empty_n>len(temp_cwds)):
                        cwd = '/'
                        return cwd

                    for i in range(len(temp_cwds)-1, 0, -1):

                        temp_cwds[i] = temp_args[counter]
                        counter-=1
                        if(counter==0):
                            cwd_fix = []
                            for temp_cwd in temp_cwds:

                                if len(temp_cwd)>0:
                                    cwd_fix.append(temp_cwd)

                            cwd_fix = '/'.join(cwd_fix)
                            if(cwd_fix=='/'):
                                cwd_fix == '/'
                            else:
                                cwd_fix = '/'+cwd_fix
                            break
                    return cwd_fix
                else:
                    temp_cwds.reverse()
                    counter=1;
                    cwd_fix = '/'
                    flag_break = 0;
                    for i in range(0, len(temp_cwds)-1):

                        temp_cwds[i] = temp_args[counter]
                        counter+=1

                        if(len(temp_args)==counter):
                            cwd_fix = []
                            temp_cwds.reverse()
                            for temp_cwd in temp_cwds:

                                if len(temp_cwd)>0:
                                    cwd_fix.append(temp_cwd)

                            cwd_fix = '/'.join(cwd_fix)
                            if(cwd_fix=='/'):
                                cwd_fix == '/'
                            else:
                                cwd_fix = '/'+cwd_fix
                            break

                    return cwd_fix
            else:
                if cwd == '/':
                    return (cwd+path_req)
                else:
                    return (cwd+'/'+path_req)
    def removeData(self, cwd, path=None):
        errors = []
        flag_exist = 0
        for worker in workers:
            error, results = worker.removeData(cwd, path)
            if(error is not None):
                errors.append(error)

        if(len(workers)==len(errors)):
            return 'Tidak ada data', ''
        return None, 'Sudah dihapus'

    def touch(self, cwd, path=None):
        errors = []
        flag_exist = 0
        for worker in workers:
            error, results = worker.touch(cwd, path)
            print('%s %s',error, results)
            if(error is not None):
                errors.append(error)

        if(len(workers)==len(errors)):
            return error, ''
        return None, results

    def listingFolder(self, cwd, path=None):

        list_folders = []
        errors = []
        flag_exist = 0
        for worker in workers:
            error, list_folder = worker.listingFolder(cwd, path)
            list_folders = list_folders+list_folder
            if(error is not None):
                errors.append(error)

        if(len(workers)==len(errors)):
            return 'Tidak ada folder', []
        return None, list_folders

    def checkDir(self, cwd):
        flag_exist = 0
        for worker in workers:
            res = worker.isExistFolder(cwd)
            if(res):
                flag_exist = 1;
                break
        if(flag_exist):
            return True
        else:
            return False

    def args(self,args,cwd):
        if args[0] == 'ls':
            if(len(args)==1):
                path = self.generateStructureFolder(cwd, args)
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            if(len(args)==1):
                error, result = self.listingFolder(cwd,path)
                return error, result, cwd
            else:
                error, result = self.listingFolder(cwd,path)
                return error, result, cwd

        elif args[0] == 'cd':
            if(len(args)==1):
                path = self.generateStructureFolder(cwd, args)
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            if(self.checkDir(path)):
                return None, cwd, path
            else:
                return 'Folder tidak ada', cwd, cwd
        elif args[0] == 'rm':
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            error, result = self.removeData(cwd, path)
            return error, result, cwd

        elif args[0] == 'touch':
            if(len(args)==1):
                return args[0]+': missing operand',None,cwd
            else:
                path = self.generateStructureFolder(cwd, args, args[1])
            print(path)
            error, result = self.touch(cwd, path)
            print('%s %s',error, result)
            return error, result, cwd

        else:
            return None, 'Perintah tidak ada', cwd



def listenToWorker():
    for list_worker in list_workers:
        worker = Pyro4.Proxy(list_worker)
        workers.append(worker)

def main():
    listenToWorker()
    Pyro4.Daemon.serveSimple(
        {
            Middleware: "middleware"
        },
        ns=False, host="127.0.0.1", port=9000)

if __name__ == "__main__":
    main()
