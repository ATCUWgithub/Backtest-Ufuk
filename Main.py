import alpaca_trade_api as tradeapi
import pandas as pd
import requests
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

def get_stock_pool(self):
    data = pd.read_excel('res/stock_pool.xlsx')
    data = data.iloc[2:, 1]
    data = data.tolist()
    data.insert(0, 'A')
    return data

possibleStockPool = get_stock_pool()
prevStockPrices = requests.get("https://api.polygon.io/v1/open-close/AAPL/2018-3-2")
print(prevStockPrices.json())
dropScreener = DropScreener(possibleStockPool, prevStockPrices, 0.01)
#targetPrices = dropScreener.getStockTargetPrices()
#targetPrices = dropScreener.getStockTargetPrices()
#get stock prices for each stock at market open or previous close
#targetPrices = create a map from ticker symbol -> (tickerSymbol price) - 1% drop

#while the time is between 6:00 and 6:15
    #for each stock in possibleStockPool
        #if current price is less than or equal to target price
            #if momentum is what we want:
                #print ticker symbol