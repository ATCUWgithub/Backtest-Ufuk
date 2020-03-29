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
import requests
os.environ['TZ'] = 'US/Eastern'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

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

def get_support(ticker):
    cur = get_current_price(ticker)
    close = get_close_price(ticker)
    return ({'current': cur, 'lastClose': close})

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

def get_drawdown(ticker, current_price=None):
    """
    Gets the current price for the given ticker. Uses Yahoo Finance.
    :params:
        ticker: ticker of stock.
        open_price: The opening price of given stock. If not passed, sets internally.
        current_price: The current price of given stock. If not passed, sets internally.
    :return: the percentage change from open to now. 
    """
    
    try:
        file = pd.read_csv('opens.csv', index_col='ticker')
        open_price = float(file.loc[ticker])
        try:
            if current_price is None:
                current_price = si.get_live_price(ticker)   
            percent = (current_price - open_price) / current_price
            return percent * 100
        except:
            print('Delisted')
    except:
        print('no opens file found')




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
        ticker, current_price=current_price)
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
    est = timezone('EST')
    adate = prev_weekday(datetime.now())
    start1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 9, 0, 0))
    end1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 10, 0, 0))
    barset = api.get_barset(
        ticker, 'minute', start=start1, end=end1, limit=400)
    data = barset[ticker]
    total = []
    tester = False
    test = round(timezone('America/New_York').localize(pd.Timestamp(adate.year,
                                                                    adate.month, adate.day, 9, 30, 0)).timestamp())
    ending = round(timezone('America/New_York').localize(
        pd.Timestamp(adate.year, adate.month, adate.day, 11, 0, 0)).timestamp())
                                                              
    for i in data:
        if tester:
            total.append({'time':round(i.t.timestamp()), 'value': i.c})
        if round(i.t.timestamp()) == test:
            total.append({'time': round(i.t.timestamp()), 'value': i.c})
            tester = True
        if round(i.t.timestamp()) == ending:
            break
    return {'total': total, 'ending': get_pricing(ticker)}


def getBars(ticker):
    est = timezone('EST')
    adate = prev_weekday(datetime.now())
    start1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 9, 0, 0))
    end1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 10, 0, 0))
    barset = api.get_barset(
        ticker, 'minute', start=start1, end=end1, limit=400)
    data = barset[ticker]
    total = []
    tester = False
    test = round(timezone('America/New_York').localize(pd.Timestamp(adate.year,
                                                                    adate.month, adate.day, 9, 30, 0)).timestamp())
    ending = round(timezone('America/New_York').localize(
        pd.Timestamp(adate.year, adate.month, adate.day, 11, 0, 0)).timestamp())

    for i in data:
        if tester:
            total.append({'time': round(i.t.timestamp()), 'value': i.c})
        if round(i.t.timestamp()) == test:
            total.append({'time': round(i.t.timestamp()), 'value': i.c})
            tester = True
        if round(i.t.timestamp()) == ending:
            break
    return total


def get_pricing(ticker):
    current_price = get_current_price(ticker)
    open_price = get_open_price(ticker)
    close_price = get_close_price(ticker)
    drawdown = get_drawdown(ticker, current_price=current_price)
    total = {}
    total['symbol'] = ticker
    total['current_price'] = current_price
    total['drawdown'] = drawdown
    total['prev_close'] = close_price
    total['open_price'] = open_price
    total['Display?'] = bool(drawdown < -1)
    return total

def getBars2(ticker):
    est = timezone('EST')
    adate = prev_weekday(datetime.now())
    start1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 9, 0, 0))
    end1 = est.localize(
        datetime(adate.year, adate.month, adate.day, 10, 0, 0))
    barset = api2.get_barset(
        ticker, 'minute', start=start1, end=end1, limit=400)
    data = barset[ticker]
    total = []
    tester = False
    test = round(timezone('America/New_York').localize(pd.Timestamp(adate.year,
                                                                    adate.month, adate.day, 9, 30, 0)).timestamp())
    ending = round(timezone('America/New_York').localize(
        pd.Timestamp(adate.year, adate.month, adate.day, 11, 0, 0)).timestamp())

    for i in data:
        if tester:
            total.append({'time': round(i.t.timestamp()), 'value': i.c})
        if round(i.t.timestamp()) == test:
            total.append({'time': round(i.t.timestamp()), 'value': i.c})
            tester = True
        if round(i.t.timestamp()) == ending:
            break
    return total




class ch(Thread):

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
                self.results[ticker] = getBars2(ticker)
            finally:
                self.queue.task_done()


class ch2(Thread):

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
                self.results[ticker] = getBars(ticker)
                # self.results.put(getBars2(ticker))
            finally:
                self.queue.task_done()

def getCharts():
    file1 = pd.read_csv('sliced1.csv', header=None)[0]
    file2 = pd.read_csv('sliced2.csv', header=None)[0]
    file3 = pd.read_csv('sliced3.csv', header=None)[0]
    file4 = pd.read_csv('sliced4.csv', header=None)[0]
    file5 = pd.read_csv('sliced5.csv', header=None)[0]
    # Create a queue to communicate with the worker threads
    queue = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()
    queue5 = Queue()
    # results = Queue()
    results = {}
    print('created queues')
    # Create 8 worker threads
    for i in range(3):
        worker = ch(queue, results)
        worker2 = ch2(queue2, results)
        worker3 = ch(queue3, results)
        worker4 = ch2(queue4, results)
        worker5 = ch(queue5, results)
        print('workers created')
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        worker2.daemon = True
        worker2.start()
        worker3.daemon = True
        worker3.start()
        worker4.daemon = True
        worker4.start()
        worker5.daemon = True
        worker5.start()
    # Put the tasks into the queue as a tuple

    print('finished all workers')
    for i in range(len(file2)):
        try:
            queue.put(file1.iloc[i])
            queue2.put(file2.iloc[i])
            queue3.put(file3.iloc[i])
            queue4.put(file4.iloc[i])
            queue5.put(file5.iloc[i])
        finally:
            print('nope')
    print('finished puts')
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()


    return {'charts': results}

                
def getDDs():
    def helper():

        # file1 = pd.read_csv('stocks1.csv', header=None)[0]
        # file2 = pd.read_csv('stocks2.csv', header=None)[0]
        file1 = pd.read_csv('sliced1.csv', header=None)[0]
        file2 = pd.read_csv('sliced2.csv', header=None)[0]
        file3 = pd.read_csv('sliced3.csv', header=None)[0]
        file4 = pd.read_csv('sliced4.csv', header=None)[0]
        file5 = pd.read_csv('sliced5.csv', header=None)[0]
        # Create a queue to communicate with the worker threads
        queue = Queue()
        queue2 = Queue()
        queue3 = Queue()
        queue4 = Queue()
        queue5 = Queue()

        results = Queue()
        # Create 8 worker threads
        for i in range(7):
            worker = dder(queue, results)
            worker2 = dder(queue2, results)
            worker3 = dder(queue3, results)
            worker4 = dder(queue4, results)
            worker5 = dder(queue5, results)

            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()
            worker2.daemon = True
            worker2.start()
            worker3.daemon = True
            worker3.start()
            worker4.daemon = True
            worker4.start()
            worker5.daemon = True
            worker5.start()
        # Put the tasks into the queue as a tuple
        for i in range(len(file1)):
            try:
                queue.put(file1.iloc[i])
                queue2.put(file2.iloc[i])
                queue3.put(file3.iloc[i])
                queue4.put(file4.iloc[i])
                queue5.put(file5.iloc[i])

            finally:
                print('nope')
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()
        a = list(results.queue)
        print(a)
        return {'disp': list(results.queue)}

    data = helper()
    return data


class dder(Thread):

    def __init__(self, queue, results):
        Thread.__init__(self)
        self.queue = queue
        self.results = results

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            try:
                ticker = self.queue.get()
                file = pd.read_csv('opens.csv', index_col='ticker')
                open_price = float(file.loc[ticker])
                current_price = si.get_live_price(ticker)
                percent = (current_price - open_price) / current_price
                dd = percent * 100
                check = dd < -1
                if check:
                    self.results.put({'ticker': ticker, 'dd':dd, 'open': open_price })
            finally:
                self.queue.task_done()

def getOpens():
    try:
        os.remove("opens.csv")
    except:
        print('no file to remove')

    file1 = pd.read_csv('sliced1.csv', header=None)[0]
    file2 = pd.read_csv('sliced2.csv', header=None)[0]
    file3 = pd.read_csv('sliced3.csv', header=None)[0]
    file4 = pd.read_csv('sliced4.csv', header=None)[0]
    file5 = pd.read_csv('sliced5.csv', header=None)[0]
    # Create a queue to communicate with the worker threads
    queue = Queue()
    queue2 = Queue()
    queue3 = Queue()
    queue4 = Queue()
    queue5 = Queue()

    results = Queue()
    # Create 8 worker threads
    for i in range(3):
        worker = opener(queue, results)
        worker2 = opener2(queue2, results)
        worker3 = opener(queue3, results)
        worker4 = opener2(queue4, results)
        worker5 = opener(queue5, results)
        print('workers created')
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        worker2.daemon = True
        worker2.start()
        worker3.daemon = True
        worker3.start()
        worker4.daemon = True
        worker4.start()
        worker5.daemon = True
        worker5.start()
    # Put the tasks into the queue as a tuple

    print('finished all workers')
    for i in range(len(file2)):
        try:
            queue.put(file1.iloc[i])
            queue2.put(file2.iloc[i])
            queue3.put(file3.iloc[i])
            queue4.put(file4.iloc[i])
            queue5.put(file5.iloc[i])
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


class opener(Thread):

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


class opener2(Thread):

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
                self.results.put(
                    {'ticker': ticker, 'open': get_open_price2(ticker)})
            finally:
                self.queue.task_done()
