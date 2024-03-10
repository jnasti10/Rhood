import pickle
def load_data():
    with open('/home/ec2-user/Misc/RHood/DataObj', 'rb') as f:
        obj = pickle.load(f)
    return(obj)
    
class cryptoData:
    
    def __init__(self, initial_inv):
        self.day                     = 0
        self.times_loaded            = 0
        self.initial_inv             = initial_inv
        self.cash                    = initial_inv
        self.total_value_5min        = [initial_inv]
        self.total_value_daily       = []
        self.cryptos                 = ['BTC', 'ETH', 'BCH', 'LTC', 'DOGE', 'ETC', 'BSV']
        self.individual_totals_5min  = self.init_stats_dict()
        self.individual_totals_daily = self.init_stats_dict()
        self.correct_prediction_5min = self.init_stats_dict() 
        self.prev_prediction         = self.init_stats_dict() 
        self.percent_correct_daily   = self.init_stats_dict() 
        self.total_percent_correct_daily = []

    def pre_update(self, new_positions):
        new_total = self.cash
        for name, amount in new_positions.items():
            if(self.individual_totals_5min[name]):
                if(self.individual_totals_5min[name][-1] >= amount and self.prev_prediction[name] <= 0):
                    self.correct_prediction_5min[name].append(True)
                elif(self.individual_totals_5min[name][-1] < amount and self.prev_prediction[name] > 0):
                    self.correct_prediction_5min[name].append(True)
                else:
                    self.correct_prediction_5min[name].append(False)
            self.individual_totals_5min[name].append(amount)
            new_total += amount
        self.total_value_5min.append(new_total)

    def post_update(self, new_positions, actions, predictions):
        cash_gain = 0
        for name, amount in actions.items():
            self.prev_prediction[name] = predictions[name]
            self.individual_totals_5min[name].append(new_positions[name])
            cash_gain += amount
        self.cash += cash_gain
            
    def init_stats_dict(self):
        ret_dict = {}
        for name in self.cryptos:
            ret_dict[name] = []
        return(ret_dict)

    def save(self):
        with open('/home/ec2-user/Misc/RHood/DataObj', 'wb') as f:
            obj = pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
    
   
    def __str__(self):
        s = "\n========= CRYPTODATA =========="
        s+= "\n===============================\n"
        s+= "\nintitial investment     = " + str(self.initial_inv)
        s+= "\ncash available          = " + str(self.cash)
        s+= "\ntotal value 5min        = " + str(self.total_value_5min)
        s+= "\ntotal value daily       = " + str(self.total_value_daily)
        s+= "\ncryptos:                  " + str(self.cryptos)
        s+= "\nindividual totals 5min:   \n" + psd(self.individual_totals_5min , ' - ')
        s+= "\nindividual totals daily:  \n" + psd(self.individual_totals_daily, ' - ')
        s+= "\ncorrect predictions 5min: \n" + psd(self.correct_prediction_5min, ' - ')
        s+= "\nprevious prevdiction:     \n" + psd(self.prev_prediction, ' - ')
        s+= "\npercent correct daily:    \n" + psd(self.percent_correct_daily, ' - ')
        s+= "\ntotal percent correct daily = " + str(self.total_percent_correct_daily)
        return(s)
        

def psd(d, prefix=""):
    s = ""
    for key, value in d.items():
        s += prefix + str(key) + " -> " + str(value) + "\n"
    return(s)
