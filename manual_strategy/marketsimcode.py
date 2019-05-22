import pandas as pd
from util import get_data

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input

    orders.sort_index(ascending=True, inplace=True)
    start_date = orders.index.min()
    end_date = orders.index.max()
    dates = pd.date_range(start_date, end_date)

    symbols = ['JPM']

    prices = get_data(symbols, dates)
    prices = prices[symbols]
    prices['CASH'] = 1.0
    trades = prices.copy()
    trades[:] = 0

    for index, row in orders.iterrows():
        date = index
        sym = 'JPM'
        shares = row['Shares']
        netholdings = trades[sym].sum()
        if shares == 1000:
            if netholdings == -1000:
                trades[sym][date] += 2000
                trades['CASH'][date] -= (prices[sym][date] * 2000 * (1 + impact)) + commission
            elif netholdings == 0:
                trades[sym][date] += 1000
                trades['CASH'][date] -= (prices[sym][date] * 1000 * (1 + impact)) + commission
            elif netholdings == 1000:
                trades[sym][date] += 0
                trades['CASH'][date] -= (prices[sym][date] * 0 * (1 + impact)) + commission
        elif shares == -1000:
            if netholdings == -1000:
                trades[sym][date] -= 0
                trades['CASH'][date] += (prices[sym][date] * 0 * (1 - impact)) - commission
            elif netholdings == 0:
                trades[sym][date] -= 1000
                trades['CASH'][date] += (prices[sym][date] * 1000 * (1 - impact)) - commission
            elif netholdings == 1000:
                trades[sym][date] -= 2000
                trades['CASH'][date] += (prices[sym][date] * 2000 * (1 - impact)) - commission
        # if ord == "BUY":
        #     trades[sym][date] += shares
        #     trades['CASH'][date] -= (prices[sym][date] * shares * (1 + impact)) + commission
        # elif ord == "SELL":
        #     trades[sym][date] -= shares
        #     trades['CASH'][date] += (prices[sym][date] * shares * (1 - impact)) - commission

    holdings = trades.copy()
    holdings['CASH'][start_date] += start_val
    holdings = holdings.cumsum()

    value = prices * holdings

    portval = value.sum(axis=1)

    #computestats

    dailyReturns = portval.copy()
    dailyReturns[1:] = (portval[1:] / portval[:-1].values) - 1
    dailyReturns.iloc[0] = 0

    dailyReturns = dailyReturns[1:]

    cr = (portval[-1] / portval[0]) - 1

    adr = dailyReturns.mean()

    sddr = dailyReturns.std()

    return portval, cr, adr, sddr