"""  		   	  			    		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Pranshav Thakkar (replace with your name)
GT User ID: pthakkar7 (replace with your User ID)
GT ID: 903079725 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut  		   	  			    		  		  		    	 		 		   		 		  
import random
from indicators import sma, bbp
import BagLearner as bl
import RTLearner as rt

## Pranshav Thakkar
## pthakkar7
  		   	  			    		  		  		    	 		 		   		 		  
class StrategyLearner(object):
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact  		   	  			    		  		  		    	 		 		   		 		  

    def author(self):
        return 'pthakkar7'

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        leaf_size = 5
        bags = 50
        N = 10
        YBUY = 0.01
        YSELL = -0.01

        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices = ut.get_data(syms, dates)
        prices = prices[syms]

        SMA = sma(prices)
        BBP = bbp(prices, SMA)
        SMA = prices/SMA

        X = pd.concat([SMA, BBP], axis=1)
        X = X[:-N]
        X = X.values

        ndayreturns = (prices.shift(-N)/prices) - 1.0

        Y = ndayreturns.applymap(lambda x: 1.0 if x > (YBUY + self.impact) else (-1.0 if x < (YSELL - self.impact) else 0.0))
        Y = Y.dropna()
        Y = Y.values

        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={'leaf_size':leaf_size}, bags=bags, boost=False, verbose=False)

        self.learner.addEvidence(X, Y)

    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  

        syms = [symbol]
        dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
        prices= ut.get_data(syms, dates)
        prices = prices[syms]

        SMA = sma(prices)
        BBP = bbp(prices, SMA)
        SMA = prices / SMA

        Xtest = pd.concat([SMA, BBP], axis=1)
        Xtest = Xtest.values

        Y = self.learner.query(Xtest)

        trades = pd.DataFrame(0.0, index=prices.index, columns=[symbol])

        holdings = 0.0

        for i in range(0, trades.shape[0] - 1):
            if Y[0][i] >= 0.5:
                trades[symbol].iloc[i] = 1000.0 - holdings
            elif Y[0][i] <= -0.5:
                trades[symbol].iloc[i] = -1000.0 - holdings
            else:
                trades[symbol].iloc[i] = 0.0
            holdings += trades[symbol].iloc[i]


        return trades


def author(self):
    return 'pthakkar7'

if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "One does not simply think up a strategy"  		   	  			    		  		  		    	 		 		   		 		  
