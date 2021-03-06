import sys
from task import Task
import requests

USERNAME = "Sonex123"

requests.packages.urllib3.disable_warnings()

path = "/home/sonex/Development/python-code/to-do-Manager/tasks.csv"

if USERNAME != "LOCAL": 
    url = f"https://192.168.178.148:25565/static/{USERNAME}.csv"

    ret = requests.get(url,verify=False)
    with open(path,"wb") as f:
        f.write(ret.content)

    print(f"Logined as {USERNAME}")
else:
    print("Local User")


def read_tasks(string):
    idx, name, urgency, group, due = string.split(';')
    if urgency in ['','None']:
        urgency=5
    if group in ['','None']:
        group=None
    if due in ['','None']:
        due=None
    return Task(int(idx), name, int(urgency), group, due)

def write_tasks(tl):
    with open(path,'w') as f:
        for i in tl:
            f.write(';'.join([str(i.index), str(i.name), str(i.urgency), str(i.group), str(i.due)])+'\n')


l = open(path).read().strip().split("\n")
if len(l)!=0 and len(l[0])!=0:
    task_list = [read_tasks(i) for i in l]
else:
    task_list = []

if len(sys.argv)==1:
    for i in sorted(task_list, key=lambda i:i.urgency, reverse=True):
        print(i)

elif sys.argv[1] == "help" or sys.argv[1] == "-h":
    print(""" // Help for to-do-list \\\\
    todo done {id}
    todo add Name
            -u / --urgency 1-10 (default 5)
            -g / --group Group
            -d / --due Due
     """)

elif sys.argv[1] == "add":
    i = 2
    urgency = 5
    group = None
    due = None
    name = ""
    skip = False
    for i in range(len(sys.argv)-2):
        if skip:
            skip = False
            continue
        if sys.argv[i+2] in ['-u','--urgency']:
            urgency = int(sys.argv[i+3])
            skip = True
        elif sys.argv[i+2] in ['-g','--group']:
            group = sys.argv[i+3]
            skip = True
        elif sys.argv[i+2] in ['-d', '--due']:
            due = sys.argv[i+3]
            skip = True
        else:
            name+=sys.argv[i+2]+' '
    try:
        ind = task_list[-1].index+1
    except:
        ind = 0
    task_list.append(Task(ind,name.strip(),urgency,group,due))
    for i in sorted(task_list, key=lambda i:i.urgency, reverse=True):
        print(i)


elif sys.argv[1] == "done":
    id = int(sys.argv[2])

    task_list.pop(id)
    for i in range(len(task_list)-id):
        task_list[i+id].index -= 1
    
    for i in sorted(task_list, key=lambda i:i.urgency, reverse=True):
        print(i)

    

write_tasks(task_list)
if USERNAME != "LOCAL":
    text = open(path,"rb").read()
    url = "http://192.168.178.148:1337/gettasks"
    requests.post(url,data={"name":USERNAME, "text":text},verify=False)
