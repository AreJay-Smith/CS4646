import datetime as dt
from util import get_data
import pandas as pd
import numpy as np
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

def testPolicy(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    relativePrices = pd.Series(np.nan, index=prices.index)
    relativePrices[:-1] = prices[:-1] / prices.values[1:] - 1
    signs = (-1) * relativePrices.apply(np.sign)
    orders = signs.diff() / 2
    orders[0] = signs[0]


    trades = []
    for date in orders.index:
        if orders.loc[date] == 1:
            trades.append((date, 1000))
        elif orders.loc[date] == -1:
            trades.append((date, -1000))
        elif orders.loc[date] == 0:
            trades.append((date, 0))

    df_trades = pd.DataFrame(trades, columns=["Date", "Shares"])
    df_trades.set_index("Date", inplace=True)

    return df_trades

if __name__ == "__main__":

    startval = 100000
    symbol = 'JPM'
    startdate = dt.datetime(2008,1,1)
    enddate = dt.datetime(2009,12,31)

    benchmark_prices = get_data([symbol], pd.date_range(startdate, enddate))
    benchmark_prices = benchmark_prices[symbol]

    benchmark_trades = np.zeros(len(benchmark_prices.index))
    benchmark_trades[0] = 1000
    benchmark_trades = pd.DataFrame(data=benchmark_trades, index=benchmark_prices.index, columns=['Shares'])
    #benchmark_trades.set_index('Date', inplace=True)


    benchportvals, benchCR, benchMean, benchSTD = compute_portvals(benchmark_trades, startval, 0.0, 0.0)

    trades = testPolicy()

    optimalportvals, optimalCR, optimalMean, optimalSTD = compute_portvals(trades, startval, 0.0, 0.0)
    print("Benchmark CR: ", benchCR)
    print("Benchmark ADR: ", benchMean)
    print("Benchmark SDDR: ", benchSTD)
    print("Optimal CR: ", optimalCR)
    print("Optimal ADR: ", optimalMean)
    print("Optimal SDDR: ", optimalSTD)

    normopt = optimalportvals/optimalportvals.iloc[0]
    normbench = benchportvals/benchportvals.iloc[0]

    plt.title("Optimal Strategy vs. Benchmark")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Value of Portfolio")

    plt.plot(normopt, 'k', label="Optimal")
    plt.plot(normbench, 'b', label="Benchmark")
    plt.legend()
    plt.savefig("optimal.png")
    plt.clf()