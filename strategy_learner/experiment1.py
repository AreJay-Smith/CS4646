import StrategyLearner as sl
import ManualStrategy as ms
from marketsimcode import compute_portvals
import datetime as dt
import random
import numpy as np
random.seed(1481090000)
np.random.seed(1481090000)
import matplotlib.pyplot as plt

## Pranshav Thakkar
## pthakkar7

def author():
    return 'pthakkar7'

if __name__ == '__main__':
    symbol = 'JPM'
    startval = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)

    manual_trades = ms.testPolicy(symbol, sd, ed, startval)

    manPortvals, manCR, manMean, manSTD = compute_portvals(manual_trades, startval, commission=0.0, impact=0.0)

    learner = sl.StrategyLearner(verbose=False, impact=0.0)
    learner.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner_trades = learner.testPolicy(symbol, sd, ed, startval)

    learnPortvals, learnCR, learnMean, learnSTD = compute_portvals(learner_trades, startval, commission=0.0, impact=0.0)

    normmanual = manPortvals / manPortvals.iloc[0]
    normlearner = learnPortvals / learnPortvals.iloc[0]

    plt.title("Manual Strategy vs. Strategy Learner")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Value of Portfolio")

    plt.plot(normmanual, 'k', label="Manual")
    plt.plot(normlearner, 'b', label="Learner")
    plt.legend()
    plt.savefig("Manual vs Strategy.png")
    plt.clf()
