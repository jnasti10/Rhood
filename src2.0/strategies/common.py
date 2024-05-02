import json, random, plotille
from datetime import datetime, timedelta

# return a function for profit by price at expiration
def get_profit_func(o0, o1, o2, o3):
    if(o0 and o1 and o2 and o3):
        price = o0["mark_price"]*1.05 - o1["mark_price"]*.95 - o2["mark_price"]*.95 + o3["mark_price"]*1.05
        func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"]) - (x > o1["strike_price"] and x - o1["strike_price"]) - (x > o2["strike_price"] and x - o2["strike_price"]) + (x > o3["strike_price"] and x - o3["strike_price"])
    elif(o0 and o1):
        price = o0["mark_price"]*1.05 - o1["mark_price"]*.95
        func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"]) - (x > o1["strike_price"] and x - o1["strike_price"])
    else:
        price = o0["mark_price"]*1.05
        func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"])
    return(func)

# returns string for expiration date and days left
def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = (two_fridays_out - curr_date).days
    if(days_left > 5):
        days_left -= 2
    
    return((days_left, str(two_fridays_out)))

# takes distribution defined by <potential_changes, weights> and simulates <days_left> days <n> times
def get_aggregate_changes(potential_changes, weights, days_left, n=100000):
    agg_changes = []
    for i in range(100000):
    #       simulate (date - current date) days
        agg_changes.append(sum(random.choices(potential_changes, weights=weights, k=days_left)))
    return(agg_changes)

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

# prints to console option strat summary
def visualize_optimal_strategy(bin_averages, optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, percentages): 
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
                elif(len(o) == 2):
                    f.write(f"{o[0]}, {o[1]} \n")
                else:    
                    f.write(f"{o[0]}, {o[1]}, {o[2]}, {o[3]}, {o[4]} \n")
  
