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
            
screener = EquityScreener("", .5, 1)
screener.getFinancials()
print(screener.finalStockPool)