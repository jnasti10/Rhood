import robin_stocks 
import robin_stocks.robinhood as r
import robin_stocks.robinhood.crypto as c
import pyotp
from cryptoData import psd
import time

def login():
    totp = pyotp.TOTP("ZQMG2DKPRNDEEV6R").now()
    login = r.login("nastij150@gmail.com", "JoeyNasti18", mfa_code=totp)

def get_all_crypto_positions():
    holdings = {}
    current_positions = r.crypto.get_crypto_positions()
    for pos in current_positions:
        ticker = pos['currency']['code']
        if(ticker != 'USD'):
            pos_in_dollars = float(r.crypto.get_crypto_quote(ticker)['mark_price']) * float(pos['quantity'])
            holdings[ticker] = pos_in_dollars
    return(holdings)
   
def get_predictions():
    db = get_all_cryptos_db("hour", "5minute")
    predictions = {}
    for key, value in db.items():
        predictions[key] = ((value[-1] - value[0]) / 12) / value[-1]
    return(predictions)

def normalize(predictions, total_value):
    next_positions = {}
    total_prediction = 0
    for name, prediction in predictions.items():
        if(prediction > 0):
            next_positions[name] = prediction
            total_prediction += prediction
        else:
            next_positions[name] = 0

    if(total_prediction != 0):
        norm_factor = total_value / total_prediction
        for name, position in next_positions.items():
            next_positions[name] = next_positions[name] * norm_factor

    return(next_positions)

def get_actions(positions, next_positions):
    actions = {}
    for name, value in positions.items():
        actions[name] = (next_positions[name] - positions[name])
    return(actions)
def get_all_cryptos_db(span, interval):
    my_cryptos = c.get_crypto_currency_pairs()
    db = build_db(my_cryptos, span, interval)
    return(db)

def get_name_from_pair(p):
    return(p["asset_currency"]["code"])

def build_db(my_crypto, _span, _interval):
    db = {}
    for c_pair in my_crypto:
        if(pair_is_tradable(c_pair)):
            name = get_name_from_pair(c_pair)
            db[name] = []
            for i in c.get_crypto_historicals(name, span=_span, interval=_interval):
                db[name].append(float(i["open_price"]))
    return(db)

def pair_is_tradable(p):
    return(p["tradability"] == "tradable")

def pChange(a,b):
    return((b-a)/a)

def is_order_complete(order_info):
    return(order_info['cancel_url'] == None)

def execute(actions):
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
            print(psd(info))
            executed_actions[name] = float(info['rounded_executed_notional'])
            if(info['side'] == 'buy'):
                executed_actions[name] = -executed_actions[name]
    return(executed_actions)

def sell_crypto_price(name, price):
    order = r.orders.order_crypto(name , "sell", price, "price")
    print(name, price, '\n', psd(order))
    order_id = order['id']
    return(order_id)

def buy_crypto_price(name, price):
    order = r.orders.order_crypto(name, "buy", price, "price")
    print(name, price, '\n', psd(order))
    order_id = order["id"]
    return(order_id)
        
def get_crypto_order_info(order_id):
    return(r.orders.get_crypto_order_info(order_id))

def cancel_crypto_order(order_id):
    r.orders.cancel_crypto_order(order_id)

