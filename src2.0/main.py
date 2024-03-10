from utils.rhoodfuncs import login, get_price, getOptionsByDate, getHistoricals
import json, random, plotille
from datetime import datetime, timedelta

# return a function for profit by price at expiration
def get_profit_func(o0, o1, o2, o3):
    price = o0["mark_price"] - o1["mark_price"] - o2["mark_price"] + o3["mark_price"]
    func = lambda x: -price + (x > o0["strike_price"] and x - o0["strike_price"]) - (x > o1["strike_price"] and x - o1["strike_price"]) - (x > o2["strike_price"] and x - o2["strike_price"]) + (x > o3["strike_price"] and x - o3["strike_price"])
    return(func)

# returns string for expiration date and days left
def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = (two_fridays_out - curr_date).days
    if(days_left > 5):
        days_left -= 2
    
    return((days_left, str(two_fridays_out)))

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

if __name__ == "__main__":
    #log in to my account
    login()

    #load pickled data
    pass
    ##################

    #create price distribution for stock on certain date
    stock = "UPRO"
    days_left_to_expiration, expiration_date = get_days_left()

    #   get historical data for stock
    historicals = getHistoricals(stock)
    #   use historical data to guess a day change
    price, changes, weights = process_historicals(historicals)
    #   repeat 100000 times to get distribution for stock
    agg_changes = []
    for i in range(100000):
    #       simulate (date - current date) days
        agg_changes.append(sum(random.choices(changes, weights=weights, k=days_left_to_expiration)))
    #   update aggregate stock price dist
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
    counts = []
    for key, value in stock_change_dist.items():
        #print(key, '->', value)
        bins.append(key)
        counts.append(float(value)/1000.0)
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
        counts=counts,
        bins=bins,
        lc='blue'
    ))
    #   \print stuff

    #get options available at expiration date
    options = getOptionsByDate(stock, expiration_date)
    #loop through all four option combinations
    all_possible_combinations = [(a,b,c,d) for i0, a in enumerate(options) for i1, b in enumerate(options[i0+1:]) for i2, c in enumerate(options[i1+i0+2:]) for d in options[i2+i1+i0+3:]]
    for o0, o1, o2, o3 in all_possible_combinations:
        
        profit = get_profit_func(o0, o1, o2, o3)
    #   get profit for each price at expiration (step by inc)
    #   integrate stock price dist times profit by price to get expected value for profit
    #   keep track of maximized expected profit
