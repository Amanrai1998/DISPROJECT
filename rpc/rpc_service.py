import subprocess


class RPCService:
    def __init__(self):
        print('RPCService Initialized')

    async def execCommand(self, command):
        cmd_arr = command.split(' ')
        if(cmd_arr[0] == 'pwd' or cmd_arr[0] == 'ls' or cmd_arr[0] == 'cat' or cmd_arr[0] == 'cp'):
            task = subprocess.Popen(
                command, shell=True,  stdout=subprocess.PIPE)
            returned_output = task.stdout.read()
            return returned_output
        else:
            return 'Not Allowed'.encode()
