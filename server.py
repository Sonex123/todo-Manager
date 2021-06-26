from flask import Flask, redirect, request
import requests
from task import Task

app = Flask(__name__)
path = "/tasks.csv"

def write_tasks(tl):
    with open(path,'w') as f:
        for i in tl:
            f.write(';'.join([str(i.index), str(i.name), str(i.urgency), str(i.group), str(i.due)])+'\n')
            
def read_tasks(string):
    idx, name, urgency, group, due = string.split(';')
    if urgency in ['','None']:
        urgency=5
    if group in ['','None']:
        group=None
    if due in ['','None']:
        due=None
    return Task(int(idx), name, int(urgency), group, due)

@app.route("/")
def main():
    l = open(path).read().strip().split("\n")
    if len(l)!=0 and len(l[0])!=0:
        task_list = [read_tasks(i) for i in l]
    else:
        task_list = []
    l = []
    for i in sorted(task_list, key=lambda i:i.urgency, reverse=True):
        l.append(f"""<tr><td>{i.name}</td><td>{i.urgency}</td><td>{i.group}</td><td>{i.due}</td> <td class="butt"><a href="/done/{i.index}">Done</a></td></tr>""")
    
    return """
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap" rel="stylesheet">
    <style>h1{text-align:center;font-size:3.5em;}body{font-family: 'Quicksand', sans-serif;background:rgb(50,50,50);color:white;}table{margin:auto;border-collapse: collapse;font-size:3em;padding:10px;background:rgb(40,40,40);border: 2px solid rgb(40,40,40); border-radius:10px;}tr{background:rgb(25,25,25)}tr:nth-child(even){background:rgb(35,35,35)}td{padding-right:20px;}a{text-decoration:none;color:white;}.butt{padding-left:5px;padding-right:10px;border-left: 15px solid rgb(50,50,50)}.butt:hover{box-shadow:5px 5px black;transition:0.2s;background:rgb(15,15,15);}</style>
</head>
<body>
    <h1>To-Do-List</h1>
    <br>
    <table>"""+"".join(l)+"""
    <td></td><td></td><td></td><td></td>
    <td class="butt">
    <a href="/add">Add</a></td></table>
</body>"""

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method == "GET":
        
        return """
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300&display=swap" rel="stylesheet">
    <style>h1{text-align:center;font-size:3.5em;}body{font-family: 'Quicksand', sans-serif;background:rgb(50,50,50);color:white;}table{margin:auto;border-collapse: collapse;font-size:3em;padding:10px;background:rgb(40,40,40);border: 2px solid rgb(40,40,40); border-radius:10px;}tr{background:rgb(25,25,25)}tr:nth-child(even){background:rgb(35,35,35)}td{padding-right:20px;}a{text-decoration:none;color:white;}.butt{padding-left:5px;padding-right:10px;border-left: 15px solid rgb(50,50,50)}.butt:hover{box-shadow:5px 5px black;transition:0.2s;background:rgb(15,15,15);}</style>
</head>
<body>
    <h1>Add</h1>
    <br>
    <form action="/add" method="POST">
        <table>
        <tr>
            <td><p>name</p></td>
            <td><input name="name"/></td>
        </tr>
        <tr>
            <td><p>urgency</p></td>
            <td><input name="urgency"/></td>
        </tr>
        <tr>
            <td><p>group</p></td>
            <td><input name="group"/></td>
        </tr>
        <tr>
            <td><p>due</p></td>
            <td><input name="due"/></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>
                <button>add</button>
            </td>
        </tr>
        </table>
    </form>
</body>"""
    else:
        l = open(path).read().strip().split("\n")
        if len(l)!=0 and len(l[0])!=0:
            task_list = [read_tasks(i) for i in l]
        else:
            task_list = []
        data = request.form
        try:
            ind = task_list[-1].index+1
        except:
            ind = 0
        
        name = data["name"]
        
        if name=="":return redirect("/add")

        try:
            urgency = int(data["urgency"])
        except:
            urgency = 5

        group = data["group"]
        print(group)
        if group==None: group=""
        
        due = data["due"]
        print(due)
        if due==None: due=""
            
        task_list.append(Task(ind, name,urgency,group,due))
        write_tasks(task_list)
        return redirect("/")


@app.route("/done/<id>", methods=["GET"])
def done(id):
    l = open(path).read().strip().split("\n")
    if len(l)!=0 and len(l[0])!=0:
        task_list = [read_tasks(i) for i in l]
    else:
        task_list = []
    task_list.pop(int(id))
    for i in range(len(task_list)-int(id)):
        task_list[i+int(id)].index -= 1
    
    write_tasks(task_list)
    
    return redirect("/")

@app.route("/gettasks", methods=["POST"])
def gettasks():
    print(request.form["text"])
    with open(path,"w") as f:
        f.write(request.form["text"])
    return request.form["text"]


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=1337)
