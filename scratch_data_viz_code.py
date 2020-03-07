#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd


# In[5]:


msft = yf.Ticker("MSFT")


# In[19]:


msft.history(period="1d", interval = "1m")["Close"]


# In[ ]:


import yfinance as yf
import pandas as pd

def forChart(TICKER):
    obj = yf.Ticker(TICKER)
    data = obj.history(period="1d", interval = "1m")["Close"].to_json()
    return data
    

