# Robinhood Trading Bot

This repository contains a Python-based trading bot that interacts with the Robinhood API via the unofficial `robin_stocks` library. It automates trading strategies, monitors pending orders, and sends email updates using AWS SES.

```plaintext
.
├── last_run.log            # Log file for tracking the latest bot run
├── main.py                 # Main script for executing the bot
├── monitor_pending.py      # Script to monitor pending orders and update status
├── out.txt                 # Output file for logging bot actions or results
├── rhoodtest.py            # Script for testing Robinhood API interactions
├── sell.py                 # Script for handling sell orders
├── strategies              # Directory containing trading strategy implementations
│   ├── common.py           # Common functions used across strategies
│   ├── first_strat.py      # First trading strategy implementation
│   ├── first_strat_v2.py   # Updated version of the first trading strategy
│   └── __pycache__         # Compiled Python files for faster execution
├── tests                   # Directory for test scripts
├── trade_data_test.py      # Test script for trade data management
└── utils                   # Utility functions and classes
    ├── cpy0815.obj         # Object file used in the project (possibly for caching data)
    ├── mailtemplate.py     # HTML template for email summaries
    ├── plot_stuff.py       # Functions for generating plots
    ├── __pycache__         # Compiled Python files for faster execution
    ├── rhoodfuncs.py       # Core functions to interact with Robinhood API
    ├── sendmail.py         # Email sending functions using AWS SES
    ├── trade_data.obj      # Pickle file for persisting trade data
    └── trade_data.py       # Class for managing trade data and positions
```
## Setup

1. **Install Dependencies**
   ```bash
   pip install robin-stocks boto3 matplotlib numpy python-dotenv pyotp pillow
2. **Environment Variables**
    Create a .env file with the following content to store sensitive information:
```
USERNAME=<your_robinhood_username>
PASSWORD=<your_robinhood_password>
TOTP=<your_totp_secret>
```
3. **Amazon SES Setup**

* Configure Amazon Simple Email Service (SES) in your AWS account for sending emails.
* Ensure your email addresses (sender and receiver) are verified in SES, especially if in a sandbox environment.

## Usage
1. Main Bot Execution

* Run main.py to execute the bot’s core functions, including checking orders, placing trades, and generating email summaries.
2. Monitor Pending Orders

* Use monitor_pending.py to track the status of pending orders, updating them as they are executed or canceled.
3. Sell Orders

* Run sell.py to handle any sell orders, especially for positions that need to be closed.
4. Testing

* Run tests in the tests directory to verify the functionality of different components.
* trade_data_test.py specifically tests the functionality in trade_data.py.
5. Strategies

* The strategies directory contains the trading strategies. first_strat.py and first_strat_v2.py represent different implementations.
* common.py holds utility functions shared across strategies.
6. Email Summaries

* The utils/mailtemplate.py file defines an HTML email template that summarizes trading activities.
* Use sendmail.py to send the generated email summaries via AWS SES.
7. Plotting and Visualization

* The utils/plot_stuff.py script provides functions for generating line and histogram plots.
* Plots can be saved as images for use in email reports.
## Example Code
**Sending an Email Summary**

```python 
from utils.mailtemplate import MailTemplate
from utils.sendmail import send, create_body

# Example data
strategy = [
    {"mark_price": 7.0, "strike_price": 60.0},
    {"mark_price": 4.0, "strike_price": 64.0},
    {"mark_price": 3.0, "strike_price": 66.0},
    {"mark_price": 1.0, "strike_price": 72.5}
]
images = ["profit_func.png", "stock_price_pdf.png", "profit_by_pdf.png"]
expected_profit = 1.56

# Generate email body
tmplt = MailTemplate()
body = tmplt.create_body(strategy, images, expected_profit)

# Send email
send("recipient@example.com", "sender@example.com", "Trading Bot Update", body)
```
## Generating a Plot
```python
from utils.plot_stuff import plot_func

# Define a profit function and plot range
profit_function = lambda x: (x < -5 and x - 1) or (x < 5 and -6) or (-11 + x)
plot_func(profit_function, -15, 25, 'profit_plot.png')
```
## Dependencies
* robin-stocks: For interacting with the Robinhood API.
* boto3: For sending emails via Amazon SES.
* matplotlib and numpy: For generating plots.
* pyotp: For generating TOTP codes for two-factor authentication.
* python-dotenv: For managing environment variables.
* Pillow: For handling images.
## License
This project is licensed under the MIT License.

## Disclaimer
This code is intended for educational purposes only. Trading in financial markets involves risk, and it is recommended to perform thorough research or consult a financial advisor before using an automated trading bot.
