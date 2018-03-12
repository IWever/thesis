class Parent:

    def __init__(self):
        self.testList = []

class Child:

    def __init__(self, parent):
        name = "henk"
        parent.testList.append(name)

a = Parent()

print(a.testList)

b = Child(a)

print(a.testList)