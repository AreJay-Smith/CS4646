import datetime as dt
from util import get_data
import pandas as pd
import numpy as np
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from indicators import sma, bbp

## Pranshav Thakkar
## pthakkar7

def author():
    return 'pthakkar7'

def testPolicy(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    SMA = sma(prices)
    BBP = bbp(prices, SMA)
    SMA = prices / SMA

    orders = prices.copy()
    orders[:] = 0

    orders[(SMA < 0.95) & (BBP < 0)] = 1
    orders[(SMA > 1.05) & (BBP > 1)] = -1

    holdings = 0.0

    trades = []
    for date in orders.index:
        trade = 0
        if orders.loc[date] == 1:
            trade = 1000 - holdings
            trades.append((date, trade))
        elif orders.loc[date] == -1:
            trade = -1000 - holdings
            trades.append((date, trade))
        elif orders.loc[date] == 0:
            trade = 0
            trades.append((date, trade))
        holdings = holdings + trade

    df_trades = pd.DataFrame(trades, columns=["Date", symbol])
    df_trades.set_index("Date", inplace=True)

    return df_trades

if __name__ == "__main__":
    startval = 100000
    symbol = 'JPM'
    startdate = dt.datetime(2008, 1, 1)
    enddate = dt.datetime(2009, 12, 31)

    benchmark_prices = get_data([symbol], pd.date_range(startdate, enddate))
    benchmark_prices = benchmark_prices[symbol]

    benchmark_trades = np.zeros(len(benchmark_prices.index))
    benchmark_trades[0] = 1000
    benchmark_trades = pd.DataFrame(data=benchmark_trades, index=benchmark_prices.index, columns=[symbol])

    benchportvals, benchCR, benchMean, benchSTD = compute_portvals(benchmark_trades, startval, 9.95, 0.005)

    trades = testPolicy()

    optimalportvals, optimalCR, optimalMean, optimalSTD = compute_portvals(trades, startval, 9.95, 0.005)
    print("Benchmark CR: ", benchCR)
    print("Optimal CR: ", optimalCR)
    print(benchportvals)

    normopt = optimalportvals / optimalportvals.iloc[0]
    normbench = benchportvals / benchportvals.iloc[0]

    plt.title("Manual Strategy vs. Benchmark")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Value of Portfolio")

    plt.plot(normopt, 'k', label="Manual")
    plt.plot(normbench, 'b', label="Benchmark")
    plt.legend()
    plt.savefig("ManualStrategy.png")
    plt.clf()