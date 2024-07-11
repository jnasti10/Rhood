import pickle
import os
import json

class Trade_data():
    def __init__(self, principle, data_obj_name="trade_data.obj"):
        self.pickle_file      = data_obj_name
        self.principle        = principle
        self.total_value      = principle
        self.cash             = principle
        self.active_positions = {}
        self.history_db       = {}

    def save(self):
        with open('/home/ec2-user/Misc/RHood/src2.0/utils/' + self.pickle_file, "wb") as fp:
            pickle.dump(self, fp, pickle.HIGHEST_PROTOCOL)

    def load(self):
        path = '/home/ec2-user/Misc/RHood/src2.0/utils/' + self.pickle_file
        if(os.path.exists(path)):
            with open(path, "rb") as fp: 
                obj = pickle.load(fp)
                self.copy(obj)
        else:
            print("No trade_data.obj, nothing to do")

    def copy(self, obj):
        self.pickle_file      = obj.pickle_file
        self.principle        = obj.principle
        self.total_value      = obj.total_value
        self.cash             = obj.cash
        self.active_positions = obj.active_positions
        self.history_db       = obj.history_db
        
    def print(self):
        s  = "========== TRADE DATA ==========\n"
        s += " pickle_file = " + self.pickle_file + "\n"
        s += " princple    = " + str(self.principle) + "\n"
        s += " total_value = " + str(self.total_value) + "\n"
        s += " cash        = " + str(self.cash) + "\n"
        s += "========== active pos ==========\n" + json.dumps(self.active_positions, indent=4) + "\n"
        s += " history_db  = " + str(self.history_db) + "\n"
        print(s)

if(__name__ == "__main__"):
    print("obj(1)")
    obj = Trade_data(1)
    obj.print()

    print("loading new obj")
    obj.load()
    obj.print()
