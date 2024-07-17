from utils.trade_data import Trade_data
from utils.rhoodfuncs import getOrderByID, login
import json

obj = Trade_data(1)
obj.load()
del obj.history_db['new']

buy  = obj.active_positions["UPRO"][0]
sell = obj.history_db["UPRO"][0]

out = {
    "open_id"        : buy["id"],
    "open_date"      : buy["created_at"],
    "open_price"     : buy["price"],
    "open_total"     : buy["estimated_total_net_amount"],
    "open_direction" : buy["net_amount_direction"],
    "close_id"       : sell["id"],
    "close_date"     : sell["created_at"],
    "close_price"    : sell["price"],
    "close_total"    : sell["estimated_total_net_amount"],
    "close_direction": sell["net_amount_direction"],
    "quantity"       : sell["quantity"],
    "spread"         : {
        "strikes"    : (sell["legs"][0]["strike_price"], sell["legs"][1]["strike_price"]),
        "expiration" : sell["legs"][0]["expiration_date"]
    }
}

obj.history_db["UPRO"][0] = out

del obj.active_positions["UPRO"][0]
obj.print()
