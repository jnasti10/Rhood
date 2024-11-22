#! /usr/local/bin/python3.8
from utils.rhoodfuncs       import login, get_price, getOptionsByDate, getHistoricals, orderSpread
from utils.sendmail         import send, create_body
from utils.plot_stuff       import plot_func, plot_hist
from utils.trade_data       import Trade_data
from strategies.common      import get_profit_func, get_days_left, get_aggregate_changes, plotille_print, visualize_optimal_strategy 
from datetime               import datetime, timedelta

import strategies.first_strat as s1
import json, random, plotille, argparse
      
if __name__ == "__main__":
    #get args
    parser = argparse.ArgumentParser(description="main RHood program")
    
    parser.add_argument("--email"  , "-em"  , action="store_true", help="enables an email summary to be sent after execution")
    parser.add_argument("--execute", "-ex", action="store_true", help="enables automatic execution of optimal trades")
    parser.add_argument("--test",    "-te", action="store_true", help="disables and updates to trade data (for testing)")
    args = parser.parse_args()

    email   = args.email
    execute = args.execute
    test    = args.test

    #log in to my account
    login()

    #load pickled data
    trade_data = Trade_data(10000)
    trade_data.load()
    ##################

    # chose stock to simulate
    stocks = ["UPRO"]
    
    #### s1 main ####
    s1.main(stocks, email, execute, test, trade_data)

