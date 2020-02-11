import alpaca_trade_api as tradeapi
API_KEY = "PKNQBGSA5TOCCDP2G5FD"
API_SECRET_KEY = "0UAzXe7EZ6ZxMMZnb0gNVoy7ESzgpcdWBODDIAtP"
api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

class EquityScreener:
    def __init__(self, stocks, priceEarnings, dividend):
        #self.alpaca = 
        self.stockPool = ["MSFT", "AAPL", "AMZN"]
        self.priceEarningsRatio = priceEarnings
        self.dividendYield = dividend
        self.finalStockPool = []

    def getFinancials(self):
        dictionaryEarnings = api.polygon.financials(self.stockPool)
        for stock in self.stockPool:
            stockFinancials = dictionaryEarnings[stock]
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
        stockToTargetPrice = []
        for stock in self.stocks:
            stockPreviousPrice = self.previousPrices[stock]
            stockToTargetPrice = stockPreviousPrice * (1.0 - self.percentDrop)
        return stockToTargetPrice
            

screener = EquityScreener([], .5, 1)
screener.getFinancials()
possibleStockPool = screener.finalStockPool
#prevStockPrices = ...
dropScreener = DropScreener(possibleStockPool, prevStockPrices, 0.01)
targetPrices = dropScreener.getStockTargetPrices()
#get stock prices for each stock at market open or previous close
#targetPrices = create a map from ticker symbol -> (tickerSymbol price) - 1% drop

#while the time is between 6:00 and 6:15
    #for each stock in possibleStockPool
        #if current price is less than or equal to target price
            #if momentum is what we want:
                #print ticker symbol