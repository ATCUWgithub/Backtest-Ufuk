
import alpaca_trade_api as tradeapi
import pandas as pd
import requests
import json
from yahoo_fin import stock_info as si
from pytz import timezone
from datetime import datetime, timedelta
import os

from stockFilter import EquityScreener
from stockFilter import serveOpenPrices
from stockFilter import serveCurPrices

#calculate the drawdown and write it to a file every minute
#make sure the two needed files are there.

#the initial calls to /updateOpenPrices + /updateCurPrices 
   #guarentee that the two files are there.

es = EquityScreener()
openPrices = es.getOpenPrices() #will update the curPrices file

def dd():
   es = EquityScreener()
   openPrices = es.getOpenPrices()  # will update the curPrices file
   s = pd.read_csv('stock_pool.csv')['A']
   with open('curPrices.json') as f:
      p = json.load(f)
   with open('openPrices.json') as f:
      o = json.load(f)

   dd = {}
   for i in s:
      pr = p[i]
      oR = o[i]
      dd[i] = (oR - pr)/pr

   with open('drawdown.json', 'w') as json_file:
         json.dump(dd, json_file)

   return dd
