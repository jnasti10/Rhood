import pickle

class testObj:
    def __init__(self, string):
        self.str = string

with open("pickleTestObj", "rb") as fp:
    obj = pickle.load(fp)

print(obj.str)
