import pickle

def load_data():
    with open('/home/ec2-user/Misc/RHood/StockDataObj', 'rb') as f:
        obj = pickle.load(f)
    return(obj)

class StockData:
    
    def __init__(self, initial_inv):
        self.stocks = ['SPY']

        for stock in stocks:
            self.weeklyReport[stock] = []
            self.dailyReport[stock] = []
            self.predictors[stock] = None
        self.weeklyReport['total'] = []
        self.dailyReport['total'] = [] 
        self.weeklyReport['cash'] = []
        self.dailyReport['cash'] = []
        
        self.cashOustanding = 0.0
        self.outstandingXactions = []

        self.lastPositions = {}

def getOldPositions(): 
      return(self.lastPositions)

        

