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


def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = two_fridays_out - curr_date
    print(days_left.days, type(days_left.days))
    return(str(two_fridays_out))

get_days_left()

l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

print([(a,b,c,d) for i0, a in enumerate(l) for i1, b in enumerate(l[i0+1:]) for i2, c in enumerate(l[i1+i0+2:]) for d in l[i2+i1+i0+3:]])
"""
print( -1 + 
      (1< 0 and 8) + 
      (1> 0 and 5))