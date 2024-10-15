from strategies.common import * 
from utils.rhoodfuncs  import login, get_price, getOptionsByDate, getHistoricals, orderSpread
from utils.sendmail    import send, create_body
from utils.plot_stuff  import plot_func, plot_hist
from utils.trade_data  import Trade_data
from strategies.common import get_profit_func, get_days_left, get_aggregate_changes, plotille_print, visualize_optimal_strategy 
from datetime          import datetime, timedelta
import json
import plotille

class leg:
    def __init__(self, action, expirationDate, strike, optionType, effect):
        self.action = action
        self.expirationDate = expirationDate
        self.strike = strike
        self.optionType = optionType
        self.effect = effect
        self.info = (action, expirationDate, strike, optionType, effect)

    def print(self):
        s = ""
        s += f"-------------- LEG --------------\n"
        s += f"| action:     {self.action}\n"
        s += f"| expiration: {self.expirationDate}\n"
        s += f"| strike:     {self.strike}\n"
        s += f"| type:       {self.optionType}\n"
        s += f"| effect:     {self.effect}\n"
        s += f"|________________________________\n"
        print(s)

class strategy:
    def __init__(self):
        self.legs = []

    def create_spread(self):
        actions = ["buy", "sell", "sell", "buy"]
        price = 0
        spread = []
        for i in range(len(strat)):
            if(strat[i]):
                price += (actions[i] == "buy" and strat[i]['high_fill_rate_buy_price']) or (actions[i] == "sell" and -strat[i]['high_fill_rate_sell_price']) 
                tmp = {
                    "expirationDate": strat[i]["exp_date"],
                    "strike"         : strat[i]["strike_price"],
                    "optionType"     : "call",
                    "effect"         : "open", 
                    "action"         : actions[i]
                }
                spread.append(tmp)
        
        if(price >= 0):
            direction = "debit"
        else:
            direction = "credit"
        
        if(price < 0):
            price = -price

        price = round(price, 2)
        if(price == 0):
            price = .01
            direction = "debit"

        return({
            "direction" : direction,
            "price"     : price,
            "symbol"    : stock, 
            "quantity"  : 1,
            "spread"    : spread
        })


