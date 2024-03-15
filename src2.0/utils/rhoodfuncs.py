import robin_stocks.robinhood as r
import robin_stocks.robinhood.options as o
import robin_stocks.robinhood.stocks  as s
import pyotp
import time

def login():
    totp = pyotp.TOTP("R4TFYIX5HPKIHS7R").now()
    login = r.login("jnasti101@icloud.com", "Hjkl;1234$", mfa_code=totp)

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
                tmp = {
                    "strike_price"             : float(option["strike_price"]),
                    "exp_date"                 : option["expiration_date"],
                    "mark_price"               : float(options["market data"][-1][0]["adjusted_mark_price"]),
                    "bid_price"                : float(options["market data"][-1][0]["adjusted_mark_price"]),
                    "ask_price"                : float(options["market data"][-1][0]["adjusted_mark_price"]),
                    "delta"                    : float(options["market data"][-1][0]["delta"]),
                    "theta"                    : float(options["market data"][-1][0]["theta"]),
                    "high_fill_rate_buy_price" : options["market data"][-1][0]["high_fill_rate_buy_price"],
                    "high_fill_rate_sell_price": options["market data"][-1][0]["high_fill_rate_sell_price"]
                }
                options["return data"].append(tmp)
    options["return data"].sort(key=lambda x: float(x["strike_price"]))
    return(options["return data"])

def order_spread(direction, price, symbol, quantity, spread):
    return(r.orders.order_option_spread(direction, price, symbol, quantity, spread))

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

"""def execute(actions):
    order_ids = {}
    for name, amount in actions.items():
        if(amount < -1):
            order_ids[name] = sell_crypto_price(name, -amount*.99)
    for name, amount in actions.items():
        if(amount > 1):
            order_ids[name] = buy_crypto_price(name, amount*.99)
        elif(amount <= 1 and amount >= -1):
            order_ids[name] = None
    
    time.sleep(60*3)

    executed_actions = {}
    for name, ID in order_ids.items():
        if(ID == None):
            print("No order for ", name)
            executed_actions[name] = 0.0
        else:
            info = get_crypto_order_info(ID)
            if(info['state'] == 'filled'):
                print("fully executed order for " , name)
            elif(info['cancel_url'] and float(info['rounded_executed_notional']) > 0):
                print('partially filled for ', name, "state is", info['state']) 
                cancel_crypto_order(ID)
            elif(info['cancel_url'] and float(info['rounded_executed_notional']) == 0):
                print('order not executed for ', name, "state is", info['state'], "canceling") 
                cancel_crypto_order(ID)
            else:
                print("!!ERROR!! shouldn't ever get here, state is ", info['state'], "execution is ", info["rounded_executions_notional"], "cancel_url is ", info["cancel_url"])
            executed_actions[name] = float(info['rounded_executed_notional'])
            if(info['side'] == 'buy'):
                executed_actions[name] = -executed_actions[name]
    return(executed_actions)

def sell_crypto_price(name, price):
    order = r.orders.order_crypto(name , "sell", price, "price")
    order_id = order['id']
    return(order_id)

def buy_crypto_price(name, price):
    order = r.orders.order_crypto(name, "buy", price, "price")
    order_id = order["id"]
    return(order_id)

    """
