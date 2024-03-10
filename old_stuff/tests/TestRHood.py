from rHoodFuncs import *
import time

login()
#print(get_all_crypto_positions())
#actions = get_next_positions()
#print(actions)
#p = get_predictions()
#n = normalize(p, 100)
order_id = buy_crypto_price("DOGE", 100)
info = get_crypto_order_info(order_id)
while(info['state'] != 'filled'):
    info = get_crypto_order_info(order_id)
    print(psd(info))
    time.sleep(10)

