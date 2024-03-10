from rHoodFuncs import *
from cryptoData import *
import datetime 

debug = True
def debugp(s):
    if(debug):
        print(s)

print('-=-=-=-=-', datetime.datetime.now(), '-=-=-=-=-')
#login to RHood account
login()

#load crypto data
if(0):
    debugp("Instantiating new data:")
    data = cryptoData(100)
    debugp(data)
else:
    debugp("Loading new data")
    data = load_data()

    #get dict of current positions
    positions = get_all_crypto_positions()
    debugp("Getting current positions")
    debugp(positions)

    #update data with new positions
    data.pre_update(positions)
    debugp("data.pre_update")
    debugp(data)

    #get predictions percentage up or down
    predictions = get_predictions()
    debugp("getting predictions")
    debugp(predictions)

    #normalize to current total
    next_positions = normalize(predictions, data.total_value_5min[-1])
    debugp("normalizing predictions to next positions")
    debugp(next_positions)

    #get actions
    actions = get_actions(positions, next_positions)
    debugp("getting actions")
    debugp(actions)

    #execute
    executed_actions = execute(actions)

    #update and save stats
    data.post_update(get_all_crypto_positions(), executed_actions, predictions)
    debugp("data.post_update and saving")
    debugp(data)

data.save()
