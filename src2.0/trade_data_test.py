#! /usr/local/bin/python3.8
from utils.trade_data import Trade_data
from utils.rhoodfuncs import getOrderByID, login, getOptionOrders
import json

obj = Trade_data(1)
obj.load()
login()
#print(json.dumps(getOrderByID("66a7a076-7b4a-436b-8bd9-fa748d3ede7a"), indent=2yy))

#get orders after execution/cancelation
_id = obj.active_positions["UPRO"][0]["id"]
order = getOrderByID(_id)


buy  = order
sell = { #obj.history_db["UPRO"][0]
    "id"         : None,
    "created_at" : "2024-00-00T00:00:00",
    "price"      : 4.24,
    "net_amount" : 424, 
    "quantity"   : 1, 
    "net_amount_direction" : "debit",
    }
    

out = {
    "open_id"        : buy["id"],
    "open_date"      : buy["created_at"],
    "open_price"     : buy["price"],
    "open_total"     : buy["net_amount"],
    "open_direction" : buy["net_amount_direction"],
    "close_id"       : sell["id"],
    "close_date"     : sell["created_at"],
    "close_price"    : sell["price"],
    "close_total"    : sell["net_amount"],
    "close_direction": sell["net_amount_direction"],
    "quantity"       : sell["quantity"],
    "spread"         : {
        "strikes"    : [x["strike_price"] for x in buy["legs"]],
        "expiration" : buy["legs"][0]["expiration_date"]
    }
}
if(not float(buy["canceled_quantity"])):
    obj.history_db["UPRO"].append(out)

del obj.active_positions["UPRO"][0]

print(json.dumps(obj.history_db["UPRO"], indent=2))

#obj.save()
