from strategies.common import * 

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

# returns optimal strategy given list of all possible option sets
def get_optimal_strategy(all_possible_combinations, stock_change_dist, percentages, current_price):
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

        if(o0 and o1 and o2 and o3):
            exp_profit_per_strategy.append((o0['strike_price'], o1['strike_price'], o2['strike_price'], o3['strike_price'], exp_profit))
        elif(o0 and o1):
            exp_profit_per_strategy.append((o0['strike_price'], o1['strike_price'], exp_profit))
        else:
            exp_profit_per_strategy.append((o0['strike_price'], exp_profit))

        #if(o0["strike_price"] == 63.0 and o1["strike_price"] == 66.0 and o2["strike_price"] == 68.0 and o3["strike_price"] == 70.0):
        #    print(o0["strike_price"],o1["strike_price"],o2["strike_price"],o3["strike_price"])

        if(exp_profit > optimal_exp_profit):
        #    if(o0["strike_price"] == 55.0 and o1["strike_price"] == 58.5 and o2["strike_price"] == 59.0 and o3["strike_price"] == 60.0):
        #        print(o0["strike_price"],o1["strike_price"],o2["strike_price"],o3["strike_price"])

            optimal_exp_profit = exp_profit
            optimal_strategy = (o0, o1, o2 ,o3)
            optimal_profit_func = profit

    return((optimal_strategy, optimal_exp_profit, optimal_profit_func, exp_profit_per_strategy, bin_averages))

def create_spread(strat):
    actions = ["buy", "sell", "sell", "buy"]
    price = 0
    spread = []
    for i in range(len(strat)):
        if(strat[i]):
            price += (actions[i] == "buy" and strat[i]['mark_price'] * 1.05) or (actions[i] == "sell" and strat[i]['mark_price'] * -.95) 
            tmp = {
                "expirationDate": strat[i]["exp_date"],
                "strike"         : strat[i]["strike_price"],
                "optionType"     : "call",
                "effect"         : "open", 
                "action"         : actions[i]
            }
            spread.append(tmp)
    
    if(price > 0):
        direction = "debit"
    else:
        direction = "credit"
    
    if(price < 0):
        price = -price

    return({
        "direction" : direction,
        "price"     : round(price, 2),
        "symbol"    : "UPRO", 
        "quantity"  : 1,
        "spread"    : spread
    })

