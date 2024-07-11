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

    args = parser.parse_args()

    #log in to my account
    login()

    #load pickled data
    trade_data = Trade_data(10000)
    trade_data.load()
    ##################

    # chose stock to simulate
    stock = "UPRO"
    if(stock not in trade_data.active_positions):
        trade_data.active_positions[stock] = []
    days_left_to_expiration, expiration_date = get_days_left()

    #get historical data for stock
    historicals = getHistoricals(stock)

    #use historical data to guess a day change
    price, changes, weights = s1.process_historicals(historicals)

    #use changes per day to simulate days_left_to_expiration days
    agg_changes = get_aggregate_changes(changes, weights, days_left_to_expiration)

    #create probabilty distribution from aggregate changes
    stock_change_dist, percentages = plotille_print(agg_changes)

    #get options available at expiration date
    print("getting options by date: ", stock, expiration_date)
    options = getOptionsByDate(stock, expiration_date)
    current_price = get_price(stock)
    print(options[0])
    exit
    #options = [o for o in options if o["strike_price"] - current_price < max(agg_changes) and o["strike_price"] - current_price > min(agg_changes)]

    #loop through all four option combinations, optimize profit
    all_possible_4_combinations         = [(a,b,     c,    d) for i0, a in enumerate(options) for i1, b in enumerate(options[i0+1:]) for i2, c in enumerate(options[i1+i0+2:]) for d in options[i2+i1+i0+3:]]
    all_possible_2_combinations         = [(a,b,  None, None) for i0, a in enumerate(options) for b     in           options[i0+1:]]
    all_possible_2_combinations_flipped = [(b, a, None, None) for a, b, _, __ in all_possible_2_combinations]
    all_singles                         = [(a,None,None,None) for a in options]
    all_possible_combinations = all_possible_2_combinations + all_possible_4_combinations + all_possible_2_combinations_flipped + all_singles
    optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, bin_averages = s1.get_optimal_strategy(all_possible_combinations, stock_change_dist, percentages, current_price)

    #visualize optimal option strategy
    visualize_optimal_strategy(bin_averages, optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, percentages) 

    # generate plot images
    images = [f"profit_func_{days_left_to_expiration}_.png", f"stock_price_pdf_{days_left_to_expiration}_.png", f"profit_by_pdf_{days_left_to_expiration}_.png"]
    plot_func(optimal_profit_func, int(current_price + min(agg_changes)), int(current_price + max(agg_changes)), "/var/www/html/jn/" + images[0])
    plot_hist([current_price + o for o in agg_changes], "/var/www/html/jn/" + images[1], bins=100) 
    pdf_func = lambda x: stock_change_dist[(x - current_price)//.5 * .5]
    plot_func(lambda x: optimal_profit_func(x) * pdf_func(x), int(min(list(stock_change_dist.keys())) + current_price + 1), int(max(list(stock_change_dist.keys())) + current_price), "/var/www/html/jn/" + images[2], title="Profit X PDF", ylabel=None)

    # execute trades
    if(args.execute):
        spread = s1.create_spread(optimal_strategy)
        print(json.dumps(spread, indent=4))
        trade_data.active_positions[stock].append(orderSpread(spread["direction"], spread["price"], spread["symbol"], spread["quantity"], spread["spread"]))
    # send the email summary
    body = create_body(optimal_strategy, images, optimal_exp_profit)

    #print(body)
    if(args.email):
        send("jnasti101@icloud.com", "jo@joeynasti.com", "Daily Summary", body)                                
    

    # save data and exit
    trade_data.save()
    print("Success!") 
    #   get profit for each price at expiration (step by inc)
    #   integrate stock price dist times profit by price to get expected value for profit
    #   keep track of maximized expected profit
