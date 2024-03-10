import robin_stocks 
import robin_stocks.robinhood as r
import robin_stocks.robinhood.crypto as c
import pyotp
import time

def login():
    totp = pyotp.TOTP("R4TFYIX5HPKIHS7R").now()
    login = r.login("nastij150@gmail.com", "JoeyNasti18", mfa_code=totp)

def getCurrentPositions():
    holdings = r.account.build_holdings()
    positions = {}
    for key, value in holdings.items():
        positions[key] = value['equity']
    return(positions)

def get_price(name):
    price = r.stocks.get_latest_price(name)
    return(float(price[0]))

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

