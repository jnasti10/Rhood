from utils.trade_data import Trade_data
from utils.rhoodfuncs import getOrderByID, login
import json

login()

print("obj(1)")
obj = Trade_data(1)
obj.print()

print("loading new obj")
obj.load()
obj.print()

_id = obj.active_positions['UPRO'][0]['id']
print(f"ID = {_id}")

print(json.dumps(getOrderByID(_id), indent=4))

