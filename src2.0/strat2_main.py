import json
import time
from datetime import datetime, timedelta
import logging
from utils.rhoodfuncs import login, getOptionsByDate, orderSpread, getOrderByID, getHistoricals
from utils.trade_data import Trade_data
from utils.sendmail import send
from utils.summarymailtemplate import SummaryMailTemplate
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotille
from scipy.stats import norm

# Load configuration
def load_config(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f)

# Send summary email
def send_summary_email(pending_positions, active_positions):
    recipient = config["email_recipient"]
    sender = config["email_sender"]
    subject = "Trading Strategy Summary"
    
    # Generate email body
    body_template = SummaryMailTemplate()
    body = body_template.create_summary_email(pending_positions, active_positions)
    
    send(to=recipient, frm=sender, subject=subject, body=body)

# Find the option that minimizes the loss function
def find_best_option(options, loss_function_strategy, projection_pdf, mean, std_dev, current_profit_function):
    if not options:
        return None
    if(loss_function_strategy == "maximize_profit"):
        optimal_o = None
        optimal_action = None
        optimal_E_profit = get_E_value(current_profit_function, projection_pdf, mean, std_dev)
        logging.info(f"Starting E_profit = {optimal_E_profit}")
        total_iterations = len(options)
        current_iteration = 0.0
        for o in options:
            print(round(current_iteration/total_iterations * 100, 2), end='%%\r')
            current_iteration += 1.0
            for action in ['buy', 'sell']:
                if(o['type'] == 'call' and action == 'buy'):
                    new_profit_function = lambda x : current_profit_function(x) - o['high_fill_rate_buy_price']  + (x - o['strike_price'] if x > o['strike_price'] else 0)
                elif(o['type'] == 'call' and action == 'sell'):
                    new_profit_function = lambda x : current_profit_function(x) + o['high_fill_rate_sell_price'] - (x - o['strike_price'] if x > o['strike_price'] else 0)
                if(o['type'] == 'put' and action == 'buy'):
                    new_profit_function = lambda x : current_profit_function(x) - o['high_fill_rate_buy_price']  + (o['strike_price'] - x if x < o['strike_price'] else 0)
                elif(o['type'] == 'put' and action == 'sell'):
                    new_profit_function = lambda x : current_profit_function(x) + o['high_fill_rate_sell_price'] - (o['strike_price'] - x if x < o['strike_price'] else 0)
                
                # continue on situations where we have more sells than buys
                if(new_profit_function(-1) < new_profit_function(0)):
                    continue
                if(new_profit_function(99999999) < new_profit_function(99999998)):
                    continue

                # find expected value of profit
                E_profit = get_E_value(new_profit_function, projection_pdf, mean, std_dev)
                """if(o["strike_price"] == 97.5 and action == "buy"):
                    start = mean - 3*std_dev
                    stop  = mean + 3*std_dev
                    step  = .01 * std_dev
                    X = [start + i * step for i in range(int((stop - start) / step))]
                    logging.info(f"printing debug info for option {o} Expected profit = {E_profit} mean stdDev = {(mean, std_dev)}\n{plotille.plot(X, [projection_pdf(x) for x in X])}\n{plotille.plot(X, [new_profit_function(x) for x in X])}")
                """
                if(E_profit > optimal_E_profit):
                    optimal_o        = o
                    optimal_E_profit = E_profit
                    optimal_action   = action
        if(True):
            logging.info(f"Found option that maximizes profit: \n{optimal_o}\naction   = {optimal_action}\nE_profit = {optimal_E_profit}")
        return((optimal_E_profit, optimal_action))
                
    return((None, None))

def get_E_value(func, pdf, mean, std_dev):
    step  = .001 * std_dev
    start = mean - 3*std_dev
    stop  = mean + 3*std_dev

    E_value = 0.0
    i = start  # Initialize `i` to the starting value
    while i <= stop:  # Condition: continue while `i` is less than or equal to `stop`
        E_value += func(i) * pdf(i) * step  # Update the E_value
        i += step  # Increment `i` by the step size

    return(E_value)

def get_next_friday(weeks_per):
    """Calculate the next Friday based on the current date and weeks_per."""
    today = datetime.now().date()
    days_until_friday = (4 - today.weekday()) % 7  # 4 represents Friday (0=Monday, 6=Sunday)
    # Add the days to get to the next Friday and account for weeks_per
    next_friday = today + timedelta(days=days_until_friday + (7 * (weeks_per - 1)))
    return next_friday

def get_projection_pdf(historicals, strat, days_left):
    if(strat == "linear"): 
        # get linear model
        prices = np.array([float(h['close_price']) for h in historicals])
        days   = np.array(range(len(prices))).reshape(-1,1)
        model = LinearRegression()
        model.fit(days, prices)
        y = model.predict(days)
        m = y[1] - y[0]
        b = y[0] 
        func = lambda x : x*m + b

        # get mean and std dev
        mean = func(len(historicals) - 1 + days_left)
        variance = 0
        for day, price in enumerate([float(h['close_price']) for h in historicals]):
              variance += (price - func(day))**2
        variance = variance * days_left / len(historicals)
        sd = (variance) ** (.5)
        
        pdf = lambda x : norm.pdf(x, loc=mean, scale=sd)
        return((pdf, mean, sd))

# Main strategy execution
def execute_strategy(config):
    # Step 1: Log in to Robinhood
    login()
    logging.info("Logged into Robinhood.")

    # Step 2: Load trade data
    trade_data = Trade_data(10000, "strat2_data.obj")
    
    # Step 3: Check expiration date
    today = datetime.now().date()
    expiration_date = trade_data.expiration_date if hasattr(trade_data, "expiration_date") else None

    # Set expiration date 
    if not expiration_date or expiration_date <= today:
        new_date = get_next_friday(config["weeks_per"])
        trade_data.expiration_date = new_date
        logging.info(f"Set new expiration date: {new_date}")
    days_left = (trade_data.expiration_date - datetime.now().date()).days
    days_left = days_left - (days_left // 7) * 2
    logging.info(f"Trade days till expiration: {days_left}")

    # Step 5: Fetch available options
    stock = config["stock"]
    expiration_date = trade_data.expiration_date.strftime("%Y-%m-%d")
    options = getOptionsByDate(stock, expiration_date) + getOptionsByDate(stock, expiration_date, "put")
    logging.info(f"Got all calls and puts for {stock} with expiration date {expiration_date}")

    # Step 6: Find optimal option using loss function
    projection_pdf, mean, std_dev = get_projection_pdf(getHistoricals(config["stock"]), config["projection_strategy"], days_left)
    start = mean - 3*std_dev
    stop  = mean + 3*std_dev
    step  = .01 * std_dev
    X = [start + i * step for i in range(int((stop - start) / step))]
    pdf_plot = plotille.plot(X, [projection_pdf(x) for x in X]) 
    logging.info(f"Printing stock projection pdf \n{pdf_plot}")
    best_option = find_best_option(options, config["loss_function"], projection_pdf, mean, std_dev, lambda x : 0)

    if not best_option:
        logging.warning("No suitable options found.")
        return

    # Step 7: Execute the trade if cash threshold is met
    if False:
        order = orderSpread("credit", best_option["price"], stock, 1, best_option["spread"])
        trade_data.cash -= best_option["price"]
        trade_data.pending_positions[stock].append(order)
        logging.info(f"Executed trade: {order}")

    # Step 8: Send email summary
    send_summary_email(
        trade_data.pending_positions,
        trade_data.active_positions,
    )
    trade_data.save()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    # Load configuration
    config = load_config()

    # Schedule execution every hour
    execute_strategy(config)

