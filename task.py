
class Task:
    def __init__(self, idx, name, urgency=5, group=None, due=None):
        self.index = idx
        self.name = name
        self.urgency = urgency
        self.group = group
        self.due = due
    
    def __str__(self):
        s = f"[{self.index}]"
        if self.group!=None:
            s+=f"({self.group})"
        s+=f"  {self.name}"
        if self.due!=None:
            s+=f"  until {self.due}"
        s+=f" /{self.urgency}"
        return s
    
    def __repr__(self):
        return f"Task {self.index}"