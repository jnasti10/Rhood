from utils.rhoodfuncs import getOrderByID, login, orderSpread
from utils.trade_data import Trade_data
import json

if __name__ == "__main__":
    login()

    data = Trade_data(1)
    data.load()

    data.print()

    info = getOrderByID("6686aaed-2f68-455a-84e2-06a128a28baa")
    print(json.dumps(info, indent=4))

    spread = {}
    
    spread['direction'] = (info["direction"] == "credit") and "debit" or "credit" # opposite of info["direction"]
    spread['price']     =  2                      # current price
    spread['symbol']    = info["chain_symbol"]
    spread['quantity']  = info["quantity"]        # info quantity
    spread['spread']    = [
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
    ]

    new_order = orderSpread(spread["direction"], spread["price"], spread["symbol"], spread["quantity"], spread["spread"])

    data.history_db["new"] = new_order

    print("-=-=-=-=-=-=-=-=-=-=--=-==-=-=-=-=-=-====-=\n\n\n\n\n-=-=-=-=-=-=-=-=--==-=-=-==-")
    data.print()
    data.save()
