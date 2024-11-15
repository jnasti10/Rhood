from utils.rhoodfuncs import getOrderByID, login, orderSpread
from utils.trade_data import Trade_data
import json

if __name__ == "__main__":
    login()

    data = Trade_data(1)
    data.load()

    data.print()

    remove_these = []
    i = -1
    for pending_order in data.pending_positions["UPRO"]:
        i += 1

        if("id" not in pending_order):
            remove_these.append(i)
        else:
            info = getOrderByID(pending_order["id"])
            print(json.dumps(getOrderByID(pending_order["id"]), indent=4))
            print(json.dumps(pending_order, indent=4))
            
            if(not info["cancel_url"]):
                remove_these.append(i)
                data.active_positions[stock].append(info)

    data.save()



    #data.history_db["new"] = new_order

    print("-=-=-=-=-=-=-=-=-=-=--=-==-=-=-=-=-=-====-=\n\n\n\n\n-=-=-=-=-=-=-=-=--==-=-=-==-")
    #data.print()
    #data.save()
