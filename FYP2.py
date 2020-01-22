#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as pdr
import datetime 
import yfinance as yf
import matplotlib.pyplot as plt
import copy
import numpy as np


# In[3]:


def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["mon_ret"].std() * np.sqrt(12)
    return vol


# In[4]:


def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR


# In[5]:


def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr


# In[6]:


tickers = ["MMM","AXP","T","BA","CAT","CVX","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UTX","UNH","VZ","V","WMT","DIS"]


# In[7]:


ohlc_mon = {}


# In[8]:


attempt = 0 # initializing passthrough variable
drop = [] # initializing list to store tickers whose close price was successfully extracted
    #tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        try:
            ohlc_mon[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(1900),datetime.date.today(),interval='mo')
            ohlc_mon[tickers[i]].dropna(inplace = True)
            print(tickers[i])
            drop.append(tickers[i])       
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1


# In[9]:


tickers = ohlc_mon.keys()


# In[10]:


ohlc = copy.deepcopy(ohlc_mon)


# In[ ]:


print(ohlc_mon)


# In[24]:


monthly_returns_df = pd.DataFrame()
for ticker in tickers:
    ohlc[ticker]["mon_ret"] = ohlc[ticker]["Adj Close"].pct_change()
    monthly_returns_df[ticker] = ohlc[ticker]["mon_ret"]


# In[26]:


def rotationalTrading(monthly_returns_df, x,m):
    portfolio = ["MMM","AXP","T","BA","CAT","CVX"]
    monthly_ret = [0]
    for i in range(1, len(monthly_returns_df)):
        if len(portfolio) > 0:
            monthly_ret.append(monthly_returns_df[portfolio].iloc[i, :].mean())
            bad_stocks = monthly_returns_df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]

        fill = m - len(portfolio)
        new_picks = monthly_returns_df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])
    return monthly_ret_df


# In[27]:


sharpe(rotationalTrading(monthly_returns_df,3,6),0.015)


# In[23]:


CAGR(rotationalTrading(monthly_returns_df,3,6))


# In[ ]:





# In[ ]:




