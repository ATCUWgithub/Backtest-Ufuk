import alpaca_trade_api as tradeapi
import pandas as pd
import requests
import json
from yahoo_fin import stock_info as si
from pytz import timezone
from datetime import datetime, timedelta
import os

API_KEY = "PK8CRHTYAD6NW2DUW5M0"
API_SECRET_KEY = "V9UJOZoTXcb0oc8Lks/VqD0JSBYoZWeDR5Am8tH/"

api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

est = timezone('EST')


class EquityScreener:
    # input a pool of stocks, a price to earnings ration, and a dividend yield
    def __init__(self):
        print('constructed')
    # screens stocks based in earnings and dividend yields
    def getFinancials(self):
        dictionaryEarnings = api.polygon.financials(self.stockPool)
        for stock in self.stockPool:
            stockFinancials = dictionaryEarnings[stock]
            print(stockFinancials)
            stockResults = stockFinancials["results"]
            stockFinancialInfo = stockResults[0]
            stockPtoE = stockFinancialInfo["priceToEarningsRatio"]
            stockDividend = stockFinancialInfo["dividendYield"]
            # if STOCK'S price/earnings ratio is lower than input, and dividend yield greater than input
            # then stock has passed screening
            if self.priceEarningsRatio >= stockPtoE and self.dividendYield <= stockDividend:
                self.finalStockPool.append(stock)


    def serveData(self):
        return self.stocks

    def getCurPrice(self, ticker):
        barset = api.get_barset(ticker, 'minute', limit=10, start=datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 0, 0, 0).isoformat())
        a = barset[ticker][-1].c
        self.tested = a
        return a

    def updateCurPrices(self):
        curPrices = {}
        for stockSymbol in self.get_stock_pool():
            try:
                stockPrice = self.getCurPrice(stockSymbol)
            except:
                print("No price")
                stockPrice = -1
            # print(openPrice)
            curPrices[stockSymbol] = stockPrice
        try:
            os.remove('curPrices.json')
            print('cleared')
        except:
            print('cleared')
        with open('curPrices.json', 'w') as json_file:
            json.dump(curPrices, json_file)
        return curPrices



    def get_stock_pool(self):
        data = pd.read_csv('stock_pool.csv')
        #data = data.iloc[2:, 1]
        #data = data.tolist()
        #data.insert(0, 'A')
        #stocks = data
        return data['A']


    def getOpenPrice(self, ticker):
        barset = api.get_barset(ticker, 'day', limit=1)
        barset = barset[ticker]
        return barset[0].o


    def getOpenPrices(self):

        updateOpenPrices = {}
        for i in self.get_stock_pool():
            try:
                stockOpenPrice = self.getOpenPrice(i)
                print('open price is %s', stockOpenPrice)
            except:
                print("No open price")
                stockOpenPrice = -1
            updateOpenPrices[i] = stockOpenPrice

        with open('openPrices.json', 'w') as json_file:
            json.dump(updateOpenPrices, json_file)
        return updateOpenPrices


def dd():
    cur = serveCurPrices()
    op = serveOpenPrices()
    dd = {}
    s = pd.read_csv('stock_pool.csv')
    s = s['A']
    for i in s:
        pr = cur[i]
        oR = op[i]
        dd[i] = (oR - pr)/pr
    try:
        os.remove('drawdown.json')
        print('cleared')
    except:
        print('cleared')
    with open('drawdown.json', 'w') as json_file:
        json.dump(dd, json_file)
    return dd

def serveOpenPrices():
    with open('openPrices.json') as f:
        data = json.load(f)
    return data


def serveCurPrices():
    with open('curPrices.json') as f:
        data = json.load(f)
    return data

# todo: change to 14 days of market open
# stock is a string representing ticker symbol


def momentum(stock):
    date_2wks_ago = datetime.now(est) - timedelta(weeks=2)
    date_2wks_ago = date_2wks_ago.strftime('%m/%d/%Y')
    date_today = datetime.now(est) - timedelta(days=1)
    date_today = date_today.strftime('%m/%d/%Y')
    two_week_data = si.get_data(stock, date_2wks_ago, date_today, True, "1d")

    # Get the difference in price from previous step
    delta = two_week_data.diff()
    # Get rid of the first row, which is NaN since it did not have a previous
    # row to calculate the differences
    delta = delta[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm().mean()
    roll_down1 = down.abs().ewm().mean()

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    hasHighMomentum = RSI1 > 70.0  # change momentum screening here
    return (hasHighMomentum, RSI1)

# list of stock symbols from pool
#stockPool = get_stock_pool()

# openPrices is a dictionary of (stockSymbol) -> (stocks opening price)





# During 6:00 - 6:15 compare opening price to current, printing a stock symbol if
# the drop criteria and the momentum criteria is met

#date_now = datetime.now(est)
#lower_bound = date_now.replace(hour=9, minute=1)
#upper_bound = date_now.replace(hour=9, minute=15)
# while lower_bound < datetime.now(est) < upper_bound:
# for stock in stockPool:
#open_price = openPrices[stock]
#current = si.get_live_price(stock)
#currentOverOpenPrice = current / open_price
#stockMomentum = momentum(stock)
# if .98 < currentOverOpenPrice < .99 and stockMomentum[0]: #change drop parameters here
#percentDrop = 1.0 - currentOverOpenPrice
#rsi = stockMomentum[1]
# stockInfo = {
# symbol": stock,
# "percentDrop": percentDrop,
# "rsi": rsi
# }
#stockInfoJson = json.dumps(stockInfo)
# print(stockInfoJson)


def get_drawdowns():
    currentDictionary = {}
    for ticker in stocks:
        open_price = openPrices[ticker]
        current = si.get_live_price(ticker)
        currentOverOpenPrice = current / open_price
        if (0.98 < currentOverOpenPrice and currentOverOpenPrice < 0.99):
            percentDrop = 1.0 - currentOverOpenPrice
            currentDictionary[ticker] = percentDrop
    stockInfoJson = json.dumps(currentDictionary)
    return stockInfoJson
