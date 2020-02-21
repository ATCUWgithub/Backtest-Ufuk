import alpaca_trade_api as tradeapi
import pandas as pd
import requests
from yahoo_fin import stock_info as si

API_KEY = "PK8CRHTYAD6NW2DUW5M0"
API_SECRET_KEY = "V9UJOZoTXcb0oc8Lks/VqD0JSBYoZWeDR5Am8tH/"

api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

class EquityScreener:
    def __init__(self, stocks, priceEarnings, dividend):
        #self.alpaca = 
        self.stockPool = ["MSFT"]
        self.priceEarningsRatio = priceEarnings
        self.dividendYield = dividend
        self.finalStockPool = []

    def getFinancials(self):
        dictionaryEarnings = api.polygon.financials(self.stockPool)
        for stock in self.stockPool:
            stockFinancials = dictionaryEarnings[stock]
            print(stockFinancials)
            stockResults = stockFinancials["results"]
            stockFinancialInfo = stockResults[0]
            stockPtoE = stockFinancialInfo["priceToEarningsRatio"]
            stockDividend = stockFinancialInfo["dividendYield"]
            if self.priceEarningsRatio < stockPtoE and self.dividendYield > stockDividend:
                self.finalStockPool.append(stock)

class DropScreener:
    def __init__(self, stocks, previousPrice, percentDrop):
        self.stocks = stocks
        self.previousPrices = previousPrice
        self.percentDrop = percentDrop
    
    def getStockTargetPrices(self):
        stockToTargetPriceDictionary = {}
        for stock in self.stocks:
            stockPreviousPrice = self.previousPrices[stock]
            stockToTargetPrice = stockPreviousPrice * (1.0 - self.percentDrop)
            stockToTargetPriceDictionary[stock] = stockToTargetPrice
        return stockToTargetPriceDictionary
            

#screener = EquityScreener([], .5, 1)
#screener.getFinancials()
#possibleStockPool = screener.finalStockPool
#print(possibleStockPool)

def get_stock_pool():
    data = pd.read_excel('res/stock_pool.xlsx')
    data = data.iloc[2:, 1]
    data = data.tolist()
    data.insert(0, 'A')
    return data

def momentum(stock):
    #TODO: calculate momentum for stock and return True if it passes threshold
    pass

#company should be ticker ex: "AAPL" date should be "2018-3-2"
#returns JSON as seen in polygon documentation
def openClose(company, date):
    url = "https://api.polygon.io/v1/open-close/"
    url = url + company + "/"
    url = url + date
    data = requests.get(url, headers={'apiKey':API_KEY, 'secretKey':API_SECRET_KEY})
    return data

possibleStockPool = get_stock_pool()
prevStockPrices = openClose("AAPL", "2019-2-21")
print(prevStockPrices.json())
dropScreener = DropScreener(possibleStockPool, prevStockPrices, 0.01)
#targetPrices = dropScreener.getStockTargetPrices()
#targetPrices = dropScreener.getStockTargetPrices()
#get stock prices for each stock at market open or previous close
#targetPrices = create a map from ticker symbol -> (tickerSymbol price) - 1% drop
screenedStockPool = possibleStockPool #TODO: screening

#while the time is between 6:00 and 6:15
    #for each stock in possibleStockPool
        #if current price is less than or equal to target price
            #if momentum is what we want:
                #print ticker symbol
momentum = False #TODO: calculate momentums
while (True): #TODO: change True to time constraints
    for stock in screenedStockPool:
        open_price = si.get_quote_table(stock)['Open']
        current = si.get_live_price(stock)
        if .98 < current / open_price < .99 and momentum(stock):
            print(stock)
