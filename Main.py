import alpaca_trade_api as tradeapi
API_KEY = "our key here"
API_SECRET_KEY = "our secret key here"
api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

class EquityScreener:
    def __init__(self, stocks, priceEarnings, dividend):
        #self.alpaca = 
        self.stockPool = stocks
        self.priceEarningsRatio = priceEarnings
        self.dividendYield = dividend
    

