from utils.rhoodfuncs import login, get_price, getOptionsByDate, getHistoricals
from utils.sendmail   import send, create_body
from utils.plot_stuff import plot_func, plot_hist
from datetime         import datetime, timedelta

import json, random, plotille

# return a function for profit by price at expiration
def get_profit_func(o0, o1, o2, o3):
    if(o2 and o3):
        price = o0["mark_price"]*1.05 - o1["mark_price"]*.95 - o2["mark_price"]*.95 + o3["mark_price"]*1.05
        func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"]) - (x > o1["strike_price"] and x - o1["strike_price"]) - (x > o2["strike_price"] and x - o2["strike_price"]) + (x > o3["strike_price"] and x - o3["strike_price"])
    else:
        price = o0["mark_price"]*1.05 - o1["mark_price"]*.95
        func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"]) - (x > o1["strike_price"] and x - o1["strike_price"])
    
    return(func)

# returns string for expiration date and days left
def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = (two_fridays_out - curr_date).days
    if(days_left > 5):
        days_left -= 2
    
    return((days_left, str(two_fridays_out)))

def get_aggregate_changes(day_changes, weights, days_left):
    agg_changes = []
    for i in range(100000):
    #       simulate (date - current date) days
        agg_changes.append(sum(random.choices(day_changes, weights=weights, k=days_left)))
    return(agg_changes)



# take historical data as input and returns price by day, changes per day, and weights for each change
def process_historicals(historicals):
    price   = []
    changes = []
    weights = []
    for i in range(len(historicals)):
        price.append(float(historicals[i]['close_price']))
        if(i != 0):
            changes.append(float(historicals[i]["close_price"]) - float(historicals[i-1]["close_price"]))
            weights.append(i)
    return((price, changes, weights))

#def create_stock_change_dist(agg_change):
def plotille_print(agg_changes):
    mx = max(agg_changes)
    mn = min(agg_changes)
    inc = .5
    bucket = mn//inc * inc
    stock_change_dist = {}
    num_buckets = 0
    while(bucket <= mx):
        stock_change_dist[bucket] = 0
        bucket += inc
        num_buckets += 1
    for c in agg_changes:
        b = c//inc * inc
        stock_change_dist[b] += 1

    #   print stuff
    bins = []
    percentages = []
    for key, value in stock_change_dist.items():
        #print(key, '->', value)
        bins.append(key)
        percentages.append(float(value)/1000.0)
    bins.append(mx//inc * inc + inc)

    print(plotille.histogram(
        agg_changes,
        bins=num_buckets,
        X_label="Price Change",
        Y_label="%",
        x_min=(mn//inc * inc),
        x_max=(mx//inc * inc + inc),
        lc="blue"
    ))

    print(plotille.hist_aggregated(
        counts=percentages,
        bins=bins,
        lc='blue'
    ))

    return(stock_change_dist, percentages)

# returns optimal strategy given list of all possible option sets
def get_optimal_strategy(all_possible_combinations, stock_change_dist, percentages):
    optimal_strategy    = None
    optimal_exp_profit  = 0
    optimal_profit_func = None
    exp_profit_per_strategy = []
    for o0, o1, o2, o3 in all_possible_combinations:
        #if(o0["strike_price"] < current_price * .9 or o3["strike_price"] > current_price * 1.1):
        #    continue

        profit = get_profit_func(o0, o1, o2, o3)

        exp_profit = 0
        bin_averages = [current_price + key + .25 for key, val in stock_change_dist.items()]
        for i in range(len(bin_averages)):
            exp_profit += percentages[i] * .01 * profit(bin_averages[i])

        # 5% chance we end up at worst case 
        # exp_profit = exp_profit * .9 + .05 * profit(o0["strike_price"]) + .05 * profit(o3["strike_price"])

        if(o2 and o3):
            exp_profit_per_strategy.append((o0['strike_price'], o1['strike_price'], o2['strike_price'], o3['strike_price'], exp_profit))
        else:
            exp_profit_per_strategy.append((o0['strike_price'], o1['strike_price'], exp_profit))

        #if(o0["strike_price"] == 63.0 and o1["strike_price"] == 66.0 and o2["strike_price"] == 68.0 and o3["strike_price"] == 70.0):
        #    print(o0["strike_price"],o1["strike_price"],o2["strike_price"],o3["strike_price"])

        if(exp_profit > optimal_exp_profit):
        #    if(o0["strike_price"] == 55.0 and o1["strike_price"] == 58.5 and o2["strike_price"] == 59.0 and o3["strike_price"] == 60.0):
        #        print(o0["strike_price"],o1["strike_price"],o2["strike_price"],o3["strike_price"])

            optimal_exp_profit = exp_profit
            optimal_strategy = (o0, o1, o2 ,o3)
            optimal_profit_func = profit

    return((optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, bin_averages))

# prints to console option strat summary
def visualize_optimal_strategy(optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, percentages): 
    if(optimal_strategy):
        for o in optimal_strategy:
            print(json.dumps(o, indent=4))
        print(plotille.plot(bin_averages, [optimal_profit_func(p) for p in bin_averages]))
        print(plotille.plot(bin_averages, percentages))
        print("expected profit: ", optimal_exp_profit)
        with open("out.txt", "w") as f:
            for o in exp_profit_per_strategy:
                if(len(o) == 3):
                    f.write(f"{o[0]}, {o[1]}, {o[2]} \n")
                else:    
                    f.write(f"{o[0]}, {o[1]}, {o[2]}, {o[3]}, {o[4]} \n")
        

if __name__ == "__main__":
    #log in to my account
    login()

    #load pickled data
    pass
    ##################

    # chose stock to simulate
    stock = "UPRO"
    days_left_to_expiration, expiration_date = get_days_left()

    #get historical data for stock
    historicals = getHistoricals(stock)

    #use historical data to guess a day change
    price, changes, weights = process_historicals(historicals)

    #use changes per day to simulate days_left_to_expiration days
    agg_changes = get_aggregate_changes(changes, weights, days_left_to_expiration)

    #create probabilty distribution from aggregate changes
    stock_change_dist, percentages = plotille_print(agg_changes)

    #get options available at expiration date
    options = getOptionsByDate(stock, expiration_date)
    current_price = get_price(stock)
    options = [o for o in options if o["strike_price"] - current_price < max(agg_changes) and o["strike_price"] - current_price > min(agg_changes)]

    #loop through all four option combinations, optimize profit
    all_possible_4_combinations = [(a,b,   c,   d) for i0, a in enumerate(options) for i1, b in enumerate(options[i0+1:]) for i2, c in enumerate(options[i1+i0+2:]) for d in options[i2+i1+i0+3:]]
    all_possible_2_combinations = [(a,b,None,None) for i0, a in enumerate(options) for b     in           options[i0+1:]]
    all_possible_2_combinations_flipped = [(b, a, None, None) for a, b, _, __ in all_possible_2_combinations]
    all_possible_combinations = all_possible_2_combinations + all_possible_4_combinations + all_possible_2_combinations_flipped
    optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, bin_averages = get_optimal_strategy(all_possible_combinations, stock_change_dist, percentages)

    #visualize optimal option strategy
    visualize_optimal_strategy(optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, percentages) 

    # generate plot images
    plot_func(optimal_profit_func, int(current_price + min(agg_changes)), int(current_price + max(agg_changes)), "/var/www/html/jn/profit_func.png")
    plot_hist([current_price + o for o in agg_changes], "/var/www/html/jn/stock_price_pdf.png", bins=100) 
    pdf_func = lambda x: stock_change_dist[(x - current_price)//.5 * .5]
    plot_func(lambda x: optimal_profit_func(x) * pdf_func(x), int(min(list(stock_change_dist.keys())) + current_price + 1), int(max(list(stock_change_dist.keys())) + current_price), "/var/www/html/jn/profit_by_pdf.png", title="Profit X PDF", ylabel=None)

    # send the email summary
    body = create_body(optimal_strategy, 
                        [
                            {
                                "name" : "profit_func.png",
                                "description": "PROFIT!!!!!"
                            },
                            {
                                "name" : "stock_price_pdf.png",
                                "description": "PRICE PROBABILITY DISTRIBUTION FUNC!!!!!"
                            },
                            {
                                "name" : "profit_by_pdf.png",
                                "description": "PROFIT TIMES PROBABILITY DISTRIBUTION FUNC!!!!!"
                            }
                        ])

    print(body)
    #send("jnasti101@icloud.com", "jo@joeynasti.com", "Option Strat Summary", body)                                
    
    #   get profit for each price at expiration (step by inc)
    #   integrate stock price dist times profit by price to get expected value for profit
    #   keep track of maximized expected profit
