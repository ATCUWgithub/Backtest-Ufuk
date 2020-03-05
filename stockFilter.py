import alpaca_trade_api as tradeapi
import pandas as pd
import requests
import json
from yahoo_fin import stock_info as si
from pytz import timezone
from datetime import datetime, timedelta

API_KEY = "PK8CRHTYAD6NW2DUW5M0"
API_SECRET_KEY = "V9UJOZoTXcb0oc8Lks/VqD0JSBYoZWeDR5Am8tH/"

api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

est = timezone('EST')


class EquityScreener:
    # input a pool of stocks, a price to earnings ration, and a dividend yield
    def __init__(self, stocks, priceEarnings, dividend):
        self.stockPool = stocks
        self.priceEarningsRatio = priceEarnings
        self.dividendYield = dividend
        self.finalStockPool = []

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

# reads in a stock pool from a given excel sheet


def get_stock_pool():
    data = pd.read_excel('res/stock_pool.xlsx')
    data = data.iloc[2:, 1]
    data = data.tolist()
    data.insert(0, 'A')
    stocks = data
    return "Updated Stock Tickers to be evaluated."

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


def getOpenPrices():
    updateOpenPrices = {}
    stocks = get_stock_pool()
    for stockSymbol in stocks:
        openPrice = si.get_quote_table(stockSymbol)['Open']
        #print(openPrice)
        updateOpenPrices[stockSymbol] = openPrice
    openPrices = updateOpenPrices
    return("Updated Open Prices for")


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


openPrices = None
getOpenPrices()
stocks = get_stock_pool()

