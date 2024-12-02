import robin_stocks.robinhood as r
import robin_stocks.robinhood.options as o
import robin_stocks.robinhood.stocks  as s
import pyotp
import time
from dotenv import dotenv_values
import json

def login():
    values = dotenv_values(".env")
    totp = pyotp.TOTP(values["TOTP"]).now()
    login = r.login(values["USERNAME"], values["PASSWORD"], mfa_code=totp)

def getOptionPositions():
    return(o.get_open_option_positions())

def getOptionsByDate(name, date):
    options = {}
    options["trdble data"] = o.find_tradable_options(name, expirationDate=date, strikePrice=None, info=None)
    options["market data"] = []
    options["return data"] = []
    for option in options["trdble data"]:
        if(option["type"] == 'call'):
            mrkt_data = o.get_option_market_data_by_id(option["id"])
            options["market data"].append(mrkt_data)
            if(mrkt_data):
                if(options["market data"][-1][0]["high_fill_rate_buy_price"]):
                    tmp = {
                        "strike_price"             : float(option["strike_price"]),
                        "exp_date"                 : option["expiration_date"],
                        "mark_price"               : float(options["market data"][-1][0]["adjusted_mark_price"]),
                        "bid_price"                : float(options["market data"][-1][0]["bid_price"]),
                        "ask_price"                : float(options["market data"][-1][0]["ask_price"]),
                        "delta"                    : float(options["market data"][-1][0]["delta"]),
                        "theta"                    : float(options["market data"][-1][0]["theta"]),
                        "high_fill_rate_buy_price" : float(options["market data"][-1][0]["high_fill_rate_buy_price"]),
                        "high_fill_rate_sell_price": float(options["market data"][-1][0]["high_fill_rate_sell_price"])
                    }
                    options["return data"].append(tmp)
    options["return data"].sort(key=lambda x: float(x["strike_price"]))
    return(options["return data"])

def orderSpread(direction, price, symbol, quantity, spread):
    return(r.orders.order_option_spread(direction, price, symbol, quantity, spread))

def getOrderByID(_id):
    return(r.orders.get_option_order_info(_id))

def trimOrder(order):
    ret_order = {
            "canceled_quantity": order["canceled_quantity"],
            "created_at": order["created_at"],
            "direction": order["direction"],
            "id": order["id"],
            "legs": [],
            "pending_quantity": order["pending_quantity"],
            "premium": order["premium"],
            "net_amount": order["net_amount"],
            "price": order["price"],
            "processed_quantity": order["processed_quantity"],
            "quantity": order["quantity"],
            "state": order["state"],
            "chain_symbol": order["chain_symbol"],
            "strategy": order["strategy"]
        }

    for leg in order["legs"]:
        ret_order["legs"].append({
                    "id": leg["id"],
                    "position_effect": leg["position_effect"],
                    "ratio_quantity": leg["ratio_quantity"],
                    "side": leg["side"],
                    "expiration_date": leg["expiration_date"],
                    "strike_price": leg["strike_price"],
                    "option_type": leg["option_type"]
                })
    return(ret_order)

def getOptionsByPrice(name, price):
    options = o.find_tradable_options(name, expirationDate=None, strikePrice=price, info=None)
    return(options)

def getHistoricals(name, interval="day", span="month"):
    historicals = s.get_stock_historicals(name, interval=interval, span=span)
    return(historicals)

def getCurrentPositions():
    holdings = r.account.build_holdings()
    positions = {}
    for key, value in holdings.items():
        positions[key] = value['equity']
    return(positions)

def get_price(name):
    price = r.stocks.get_latest_price(name)
    return(float(price[0]))

if __name__ == "__main__":
    print(dotenv_values(".env"))
    login()
    print(json.dumps(r.orders.get_option_order_info("663159a2-4d84-40e3-a830-3f01ee4c029c"), indent=4))
    print(json.dumps(o.get_open_option_positions(), indent=4))
