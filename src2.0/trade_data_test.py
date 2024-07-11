from utils.trade_data import Trade_data
from utils.rhoodfuncs import getOrderByID, login
import json

login()

print("loading new obj")
obj = Trade_data(1)
obj.load()
obj.print()

#obj.remove_active_positions_by_id(["6685e1fe-0bb8-45fe-9142-17a272c6a53f", "6685e5a6-b863-441d-8d01-a0461a869d94"])
#print("removed bad IDs")
obj.remove_failed_orders()
obj.print()
#obj.save()
#_id = obj.active_positions['UPRO'][0]['id']
#print(f"ID = {_id}")

#print(json.dumps(getOrderByID(_id), indent=4))

