import pandas as pd
import numpy as np
import datetime as dt
import util
import matplotlib.pyplot as plt

## Pranshav Thakkar
## pthakkar7

def author():
    return 'pthakkar7'

def sma(prices, lookback=14):
    normed_prices = prices / prices.iloc[0]
    sma = prices.rolling(window=lookback, min_periods=1).mean()
    psma = sma / normed_prices
    return sma


def bbp(prices, sma, lookback=14):
    normed_prices = prices / prices.iloc[0]
    rolling_std = prices.rolling(window=lookback, min_periods=lookback).std()
    top_bb = sma + (2 * rolling_std)
    bottom_bb = sma - (2 * rolling_std)
    bbp = (prices - bottom_bb) / (top_bb - bottom_bb)
    return bbp

def momentum(prices, lookback=14):
    #momentum = prices[t]/prices[t-n] -1, where n is the lookback window (number of days)
    normed_prices = prices / prices.iloc[0]
    momentum = pd.DataFrame(data=0, index=prices.index, columns=['Momentum'])
    momentum.ix[lookback:] = prices.ix[lookback:] / prices.values[:-lookback] - 1
    return momentum

if __name__ == "__main__":
    syms = ['JPM']
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    dates = pd.date_range(start_date, end_date)
    prices = util.get_data(syms, dates)
    prices = prices[syms]
    normed_prices = prices / prices.ix[0, :]

    SMA = sma(prices)
    bbp(prices, SMA)
    momentum(prices)
