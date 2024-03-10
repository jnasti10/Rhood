from utils.rhoodfuncs import *
import json
from datetime import datetime, timedelta
"""login()
options = getOptionsByDate(name="UPRO", date="2024-03-08")
current_price = get_price("UPRO")
market_data = o.get_option_market_data_by_id(options[85]["id"])
print(f'current price = {current_price}')
print(json.dumps(options[85], indent=4))
print(len(options))
print(json.dumps(market_data, indent=4))
"""

def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = two_fridays_out - curr_date
    print(days_left.days, type(days_left.days))
    return(str(two_fridays_out))

get_days_left()