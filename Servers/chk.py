import sys
from fabric import Connection




arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
servers = []
master_first_part=[]





with open(arg1, "r") as f:
    master = f.read().split(" ")

for m in master:
    if len(m.split("="))>0:
        m=m.split("=")
        master_first_part.append(m[0])



with open(arg2, "r") as f:
    for l in f:
        servers.append(l.strip())

print(servers)



def file_checker(host,master,dir="/opt/pprbusr/java.opt"):
    new_list = []

    try:
        with Connection(host=host, user="grid", connect_kwargs={"key_filename": "id_rsa"}) as c:
            print(c)
            c.get(dir,"java.opt")
            c.r

        with open("java.opt", "r") as f:
            java = f.read().split(" ")


        result = list(set(java) - set(master))


        for i in java:
            if i in result and i != "":
                if "=" in i:
                    if i.split("=")[0] in master_first_part:

                        new_list.append(i+"!?")


                else:
                    new_list.append(i)


        with open(host+".txt","w") as f:
            f.write(" ".join(new_list))
            print(host+".txt"+" done...")

    except Exception as e:
        print(e)
        input("Some,error. Press any key")
        return None



def main():

    for host in servers:
        if len(host)>0:
            file_checker(host,master,dir=arg3)

if __name__=="__main__":
    main()
    input("Press any key")

