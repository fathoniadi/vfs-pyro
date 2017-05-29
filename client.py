import sys
import Pyro4

def main():
    uri = 'PYRO:middleware@127.0.0.1:9000'
    middleware = Pyro4.Proxy(uri)
    commands = middleware.getCommands()
    cwd = '/'
    while True:
        args = []
        print('Client > '+cwd+' % '),
        arg = raw_input()
        args.extend(arg.split(' '))

        if args[0] in commands:
            if args[0] == 'exit':
                break

            if args[0] == 'cd':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)
            if args[0] == 'ls':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)
                else:
                    if(isinstance(results, list)):
                        for result in results:
                            print(result)
                    else:
                        print(results)
            if args[0] == 'rm' or args[0] == 'touch' or args[0] == 'cp':
                errors, results, cwd = middleware.args(args, cwd)
                if(errors is not None):
                    print('Server: '+errors)
                else:
                    print('Server: '+results)

        elif args[0] == '':
            continue
        else:
            print('server: command not found: '+args[0])



if __name__ == "__main__":
    main()
