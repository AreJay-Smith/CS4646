import StrategyLearner as sl
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

    #impact of 0.0
    learner1 = sl.StrategyLearner(verbose=False, impact=0.0)
    learner1.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner1_trades = learner1.testPolicy(symbol, sd, ed, startval)

    learn1Portvals, learn1CR, learn1Mean, learn1STD = compute_portvals(learner1_trades, startval, commission=0.0, impact=0.0)

    #impact of 0.02
    learner2 = sl.StrategyLearner(verbose=False, impact=0.02)
    learner2.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner2_trades = learner2.testPolicy(symbol, sd, ed, startval)

    learn2Portvals, learn2CR, learn2Mean, learn2STD = compute_portvals(learner2_trades, startval, commission=0.0,
                                                                       impact=0.02)

    # impact of 0.04
    learner3 = sl.StrategyLearner(verbose=False, impact=0.04)
    learner3.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner3_trades = learner3.testPolicy(symbol, sd, ed, startval)

    learn3Portvals, learn3CR, learn3Mean, learn3STD = compute_portvals(learner3_trades, startval, commission=0.0,
                                                                       impact=0.04)

    # impact of 0.06
    learner4 = sl.StrategyLearner(verbose=False, impact=0.06)
    learner4.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner4_trades = learner4.testPolicy(symbol, sd, ed, startval)

    learn4Portvals, learn4CR, learn4Mean, learn4STD = compute_portvals(learner4_trades, startval, commission=0.0,
                                                                       impact=0.06)

    # impact of 0.08
    learner5 = sl.StrategyLearner(verbose=False, impact=0.08)
    learner5.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner5_trades = learner5.testPolicy(symbol, sd, ed, startval)

    learn5Portvals, learn5CR, learn5Mean, learn5STD = compute_portvals(learner5_trades, startval, commission=0.0,
                                                                       impact=0.08)

    # impact of 0.1
    learner6 = sl.StrategyLearner(verbose=False, impact=0.1)
    learner6.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=startval)
    learner6_trades = learner6.testPolicy(symbol, sd, ed, startval)

    learn6Portvals, learn6CR, learn6Mean, learn6STD = compute_portvals(learner6_trades, startval, commission=0.0,
                                                                       impact=0.1)


    learn1norm = learn1Portvals / learn1Portvals.iloc[0]
    learn2norm = learn2Portvals / learn2Portvals.iloc[0]
    learn3norm = learn3Portvals / learn3Portvals.iloc[0]
    learn4norm = learn4Portvals / learn4Portvals.iloc[0]
    learn5norm = learn5Portvals / learn5Portvals.iloc[0]
    learn6norm = learn6Portvals / learn6Portvals.iloc[0]

    plt.title("Impact of Impact on Strategy Learner")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Value of Portfolio")

    plt.plot(learn1norm, label="0.0")
    plt.plot(learn2norm, label="0.02")
    plt.plot(learn3norm, label="0.04")
    plt.plot(learn4norm, label="0.06")
    plt.plot(learn5norm, label="0.08")
    plt.plot(learn6norm, label="0.1")
    plt.legend()
    plt.savefig("Impact.png")
    plt.clf()