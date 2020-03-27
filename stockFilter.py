import os
import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
from pytz import timezone
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from datetime import tzinfo
from queue import Queue
from threading import Thread
import csv



API_KEY = "PK8CRHTYAD6NW2DUW5M0"
API_SECRET_KEY = "V9UJOZoTXcb0oc8Lks/VqD0JSBYoZWeDR5Am8tH/"

API_KEY2 = "PKARW6ER28W2JWN3QVGZ"
API_SECRET_KEY2 = "f94LcilKrJTjlasa/Kzg1IXEJPJ9PIjU1A6O9RZO"

api = tradeapi.REST(API_KEY, API_SECRET_KEY, api_version='v2')
api2 = tradeapi.REST(API_KEY2, API_SECRET_KEY2, api_version='v2')
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
        return barset[0].o

    except:
        return -1


def get_open_price2(ticker):
    """
    Gets the opening price for the given ticker. Uses Polygon through Aplaca.
    :param 
        ticker: ticker of stock.
    :return: the opening price 
    """

    try:
        barset = api2.get_barset(ticker, 'day', limit=1)
        barset = barset[ticker]
        return barset[0].o
    except:
        return -1



def get_current_price(ticker):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :param 
        ticker: ticker of stock.
    :return: the current price 
    """
    try:
        current = si.get_live_price(ticker)
        return current
    except:
        print('Delisted')

def get_drawdown(ticker, open_price=None, current_price=None):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :params:
        ticker: ticker of stock.
        open_price: The opening price of given stock. If not passed, sets internally.
        current_price: The current price of given stock. If not passed, sets internally.
    :return: the percentage change from open to now. 
    """
    try:
        if open_price is None:
            open_price = get_open_price(ticker)
        if current_price is None:
            current_price = si.get_live_price(ticker)
        percent = (current_price - open_price) / current_price
        return percent * 100
    except:
        print('Delisted')


def get_drawdown2(ticker, open_price=None, current_price=None):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :params:
        ticker: ticker of stock.
        open_price: The opening price of given stock. If not passed, sets internally.
        current_price: The current price of given stock. If not passed, sets internally.
    :return: the percentage change from open to now. 
    """
    try:
        if open_price is None:
            open_price = get_open_price2(ticker)
        if current_price is None:
            current_price = si.get_live_price(ticker)
        percent = (current_price - open_price) / current_price
        return percent * 100
    except:
        print('Delisted')

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
        ticker, open_price=open_price, current_price=current_price)
    data_dictionary["percent change"] = drawdown_percentage
    display = drawdown_percentage < -1
    data_dictionary['Display?'] = bool(display)
    return data_dictionary


def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate

def get_chart_data(ticker):
    today = prev_weekday(datetime.now())
    today = datetime(today.year, today.month, today.day,
                     9, 0, 0).astimezone(est)
    end = datetime(today.year, today.month, today.day,
                   16, 0, 0).astimezone(est)
    print('START = ', today)
    barset = api.get_barset(ticker, 'minute', start=today, end=end, limit=389)
    data = barset[ticker]
    total = []
    print('1st RETURNED BY ALPACA = ', barset[ticker][0].t)
    print('last RETURNED BY ALPACA = ', barset[ticker][-1].t)
    # for i in range(len(data)):
    for i in range(len(data)):
        row = data[i]
        # total[i] = [i, row.c]
        total.append(row.c)
    return {'total': total, 'ending': get_pricing(ticker)}


def get_pricing(ticker):
    current_price = get_current_price(ticker)
    open_price = get_open_price(ticker)
    close_price = get_close_price(ticker)
    drawdown = get_drawdown(ticker, open_price=open_price, current_price=current_price)
    total = {}
    total['symbol'] = ticker
    total['current_price'] = current_price
    total['drawdown'] = drawdown
    total['prev_close'] = close_price
    total['open_price'] = open_price
    total['Display?'] = bool(drawdown < -1)
    return total

class DownloadWorker(Thread):

    def __init__(self, queue, results):
        Thread.__init__(self)
        self.queue = queue
        self.results = results

    # def run(self):
    #     while True:
    #         # Get the work from the queue and expand the tuple
    #         try:
    #             ticker = self.queue.get()
    #             self.results.put({ticker: get_drawdown(ticker)})
    #         finally:
    #             self.queue.task_done()

    def run(self):
        while True:
        # Get the work from the queue and expand the tuple
            try:
                ticker = self.queue.get()
                self.results.put(
                    {'ticker': ticker, 'open': get_open_price(ticker)})
            finally:
                self.queue.task_done()

class DownloadWorker2(Thread):

    def __init__(self, queue, results):
        Thread.__init__(self)
        self.queue = queue
        self.results = results

    # def run(self):
    #     while True:
    #         # Get the work from the queue and expand the tuple
    #         try:
    #             ticker = self.queue.get()
    #             self.results.put({ticker: get_drawdown2(ticker)})
    #         finally:
    #             self.queue.task_done()

    def run(self):
        while True: 
            # Get the work from the queue and expand the tuple
            try:
                ticker = self.queue.get()
                self.results.put({'ticker': ticker, 'open': get_open_price2(ticker)})
            finally:
                self.queue.task_done()
                
def prep_all():


    def helper():
        file1 = pd.read_csv('stocks1.csv', header=None)[0]
        file2 = pd.read_csv('stocks2.csv', header=None)[0]
        # Create a queue to communicate with the worker threads
        queue = Queue()
        queue2 = Queue()
        results = Queue()
        # Create 8 worker threads
        for i in range(7):
            worker = DownloadWorker(queue, results)
            worker2 = DownloadWorker2(queue2, results)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()
            worker2.daemon = True
            worker2.start()
        # Put the tasks into the queue as a tuple
        for i in range(len(file2)):
            try:
                queue.put(file1[i])
                queue2.put(file2[i])
            finally:
                print('nope')
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()
        return list(results.queue)

    data = helper()
    return data
    

def getOpens():
    try:
        os.remove("opens.csv")
    except:
        print('no file to remove')

    file1 = pd.read_csv('stocks1.csv', header=None)[0]
    file2 = pd.read_csv('stocks2.csv', header=None)[0]
    print('read in file')
    queue = Queue()
    queue2 = Queue()
    results = Queue()
    print('created queues')
    # Create 8 worker threads
    for i in range(3):
        worker = DownloadWorker(queue, results)
        worker2 = DownloadWorker2(queue2, results)
        print('workers created')
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        worker2.daemon = True
        worker2.start()
    # Put the tasks into the queue as a tuple

    print('finished all workers')
    for i in range(len(file2)):
        try:
            queue.put(file1[i])
            queue2.put(file2[i])
        finally:
            print('nope')
    print('finished puts')
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()


    rows_list = list(results.queue)
    print('rows_list done')
    # for i in range(len(file1)):
    #     try:
    #         data = get_open_price(i)
    #         row = {}
    #         row['Ticker'] = i
    #         row['Open'] = data
    #         rows_list.append(row)
    #     except:
    #         print('no Open')
    data = pd.DataFrame(rows_list)
    print('printing data')
    for i in data:
        print(i)
    data.to_csv('opens.csv', index=False)
