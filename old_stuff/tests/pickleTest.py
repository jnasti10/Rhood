import pickle

class testObj:
    def __init__(self, string):
        self.str = string

with open("pickleTestObj", 'wb') as fp:
    obj = testObj("TEST SUCCESS!!!")
    pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)


