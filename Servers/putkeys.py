import sys
import os
#from fabric import Connection
import subprocess


# putkeys.py id_rsa servers user#password


arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
servers = []





def read_key_file(key_file):
    key_file = os.path.expanduser(key_file)
    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')
    with open(key_file) as f:
        return f.read()

with open(arg3, "r") as f:
    for l in f:
        servers.append(l.strip())

local_key=read_key_file(arg1)

print(local_key,servers)

# ssh user@server "echo \"`cat ~/.ssh/id_rsa.pub`\" >> .ssh/authorized_keys"

#command = "ssh grid@84.201.136.227 \"echo \\`cat {}`\\\" >> .ssh/test2_keys".format(arg1)

for server in servers:
    command='ssh-copy-id -f -i {} {}@{}'.format(arg1,arg2,server)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

