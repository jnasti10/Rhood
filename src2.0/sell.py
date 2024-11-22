from utils.rhoodfuncs import getOrderByID, login, orderSpread, getOptionPositions
from utils.trade_data import Trade_data
import json

if __name__ == "__main__":
    login()

    print(json.dumps(getOrderByID("673deb6f-7d0c-4058-bc21-e09e0bce7a73"), indent=4))
    exit()
"""
    data = Trade_data(1)
    data.load()
    data.print()
    
    #print(json.dumps(getOrderByID("671118e4-d102-4165-925d-c657f9165c2d"), indent=4))
    for stock, active_positions in data.active_positions.items():
        for info in active_positions:
            order = {}

            order['direction'] = (info["direction"] == "credit") and "debit" or "credit" 
            order['symbol']    = stock
            order['quantity']  = info["quantity"]
            order['spread']    = []

            for each leg...
                {
                    "expirationDate": "2024-07-12",
                    "strike": "84.0000",
                    "optionType": "call",
                    "effect" : "close",
                    "action" : "buy"
                },
                {
                    "expirationDate": "2024-07-12",
                    "strike": "80.0000",
                    "optionType": "call",
                    "effect" : "close",
                    "action" : "sell"
                }

            
        
            order['price']  = get_price()######                       
            """
            #new_order = orderSpread(order["direction"], order["price"], order["symbol"], order["quantity"], order["spread"])
