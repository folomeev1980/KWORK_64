from fabric import Connection

with Connection(host="84.201.136.227", user="grid",connect_kwargs={"password": ""}) as c:
    #c.run("cd")
    c.get("/home/grid/servers")
    #print(c)