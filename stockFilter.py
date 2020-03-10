import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
from pytz import timezone
from datetime import datetime, timedelta
import yfinance as yf


API_KEY = "PK8CRHTYAD6NW2DUW5M0"
API_SECRET_KEY = "V9UJOZoTXcb0oc8Lks/VqD0JSBYoZWeDR5Am8tH/"

api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')

est = timezone('EST')


def get_open_price(ticker):
    """
    Gets the opening price for the given ticker. Uses Polygon through Aplaca.
    :param 
        ticker: ticker of stock.
    :return: the opening price 
    """

    try:
        barset = api.get_barset(ticker, 'day', limit=1)
        barset = barset[ticker]
    except:
        return -1
    return barset[0].o

    today = datetime.now()


def get_current_price(ticker):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :param 
        ticker: ticker of stock.
    :return: the current price 
    """

    current = si.get_live_price(ticker)
    return current


def get_drawdown(ticker, open_price=None, current_price=None):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :params:
        ticker: ticker of stock.
        open_price: The opening price of given stock. If not passed, sets internally.
        current_price: The current price of given stock. If not passed, sets internally.
    :return: the percentage change from open to now. 
    """

    if open_price is None:
        open_price = get_open_price(ticker)
    if current_price is None:
        current_price = si.get_live_price(ticker)
    percent = (current_price - open_price) / current_price
    return percent


def get_close_price(ticker):
    """
    Gets the close price for the given ticker. Uses Polygon through Aplaca.
    :param 
        ticker: ticker of stock.
    :return: the close price 
    """


    stock = yf.Ticker(ticker)

    today = datetime.now()
    last_close_day = prev_weekday(today)
    try:
        rightday = datetime(last_close_day.year, last_close_day.month, last_close_day.day)
        close = stock.history(interval="1m", end=rightday.isoformat().split('T')[0], start=(rightday - timedelta(days=1)).isoformat().split('T')[0]).iloc[-1].Close
    except:
        return -1
    return close


def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


def get_all_data(ticker):
    """
    Calls all the methods within this script to aggregate and return singular dict file for
    API usage and parsing. 
    :param 
        ticker: ticker of stock.
    :return: dict of open, close, current, drawdown percentage, ticker, and boolean to display or not. 
    """
    print('IN THE FUNC')
    data_dictionary = {}
    data_dictionary["Symbol"] = ticker
    open_price = get_open_price(ticker)
    data_dictionary["Open Price"] = open_price
    close_price = get_close_price(ticker)
    data_dictionary["Previous Close Price"] = close_price
    current_price = get_current_price(ticker)
    data_dictionary["Current Price"] = current_price
    drawdown_percentage = get_drawdown(
        ticker, open_price=open_price, current_price=current_price) * 100
    data_dictionary["percent change"] = drawdown_percentage
    display = drawdown_percentage < -1
    data_dictionary['Display?'] = bool(display)
    return data_dictionary
