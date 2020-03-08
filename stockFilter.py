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


def set_stock_pool():
    data = pd.read_excel('res/stock_pool.xlsx')
    data = data.iloc[2:, 1]
    data = data.tolist()
    data.insert(0, 'A')
    stocks = data
    return stocks


def get_open_price(ticker):
    today = datetime.now()
    try:
        open_price = api.polygon.daily_open_close(ticker, today).open
    except:
        return -1
    return open_price


def get_current_price(ticker):
    current = si.get_live_price(ticker)
    return current


def get_drawdown(ticker, open_price=None, current_price=None):
    if open_price is None:
        open_price = getOpenPrice(ticker)
    if current_price is None:
        current_price = si.get_live_price(ticker)
    print(current_price)
    print(open_price)
    currentOverOpenPrice = current_price / open_price
    percentDrop = -1
    if (0.98 < currentOverOpenPrice and currentOverOpenPrice < 0.99):
        percentDrop = 1.0 - currentOverOpenPrice
    return percentDrop


def get_close_price(ticker):
    today = datetime.now()
    last_close_day = prev_weekday(today)
    try:
        close = api.polygon.daily_open_close(ticker, last_close_day).close
    except:
        return -1
    return close


def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


def get_all_data(ticker):
    data_dictionary = {}
    data_dictionary["Symbol"] = ticker
    open_price = get_open_price(ticker)
    data_dictionary["Open Price"] = open_price
    close_price = get_close_price(ticker)
    data_dictionary["Previous Close Price"] = close_price
    current_price = get_current_price(ticker)
    data_dictionary["Current Price"] = current_price
    drawdown_percentage = get_drawdown(
        ticker, open_price=open_price, current_price=current_price)
    data_dictionary["Drawdown % "] = drawdown_percentage
    display = drawdown_percentage > 1
    data_dictionary['Display?'] = display
    return data_dictionary
