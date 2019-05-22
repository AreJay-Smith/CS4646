"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import math
import time
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import util
import matplotlib.pyplot as plt

def author():
    return 'pthakkar7'
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  

    author()

    data = np.genfromtxt(util.get_learner_data_file('Istanbul.csv'), delimiter=',')
    data = data[1:, 1:]

    # compute how much of the data is training and testing  		   	  			    		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]  		   	  			    		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]  		   	  			    		  		  		    	 		 		   		 		  

  	#Experiment 1
    inSamples = np.zeros((50, 1))
    outSamples = np.zeros((50,1))
    for x in range(1, 51):

        learner = dt.DTLearner(leaf_size=x, verbose=False)  # constructor
        learner.addEvidence(trainX, trainY)  # training step
  		   	  			    		  		  		    	 		 		   		 		  
        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        inSamples[x - 1, 0] = rmse
        c = np.corrcoef(predY, y=trainY)
  		   	  			    		  		  		    	 		 		   		 		  
        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        outSamples[x - 1,0] = rmse
        c = np.corrcoef(predY, y=testY)
    xaxis = np.arange(1, 51)
    plt.plot(xaxis, inSamples, label="In Sample")
    plt.plot(xaxis, outSamples, label="Out of Samples")
    plt.xlabel("Leaf Sizes")
    plt.ylabel("RMSE")
    plt.legend()
    plt.title("Experiment 1 - DT Learners Overfitting")
    plt.savefig("Exp1.png")
    plt.clf()

    # Experiment 2
    inSamples = np.zeros((50, 1))
    outSamples = np.zeros((50, 1))
    for x in range(1, 51):
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size":x}, bags=20, boost=False, verbose=False)  # constructor
        learner.addEvidence(trainX, trainY)  # training step

        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        inSamples[x - 1, 0] = rmse
        c = np.corrcoef(predY, y=trainY)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        outSamples[x - 1, 0] = rmse
        c = np.corrcoef(predY, y=testY)
    xaxis = np.arange(1, 51)
    plt.plot(xaxis, inSamples, label="In Sample")
    plt.plot(xaxis, outSamples, label="Out of Samples")
    plt.xlabel("Leaf Sizes")
    plt.ylabel("RMSE")
    plt.legend()
    plt.title("Experiment 2 - DT Learners w/Bagging Overfitting")
    plt.savefig("Exp2.png")
    plt.clf()

    #Experiment 3

    dtTimes = np.zeros((50, 1))
    for x in range(1, 51):
        start = time.time()
        learner = dt.DTLearner(leaf_size=x, verbose=False)  # constructor
        learner.addEvidence(trainX, trainY)  # training step

        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        end = time.time()
        dtTimes[x - 1, 0] = end - start

    rtTimes = np.zeros((50, 1))
    for x in range(1, 51):
        start = time.time()
        learner = rt.RTLearner(leaf_size=x, verbose=False)  # constructor
        learner.addEvidence(trainX, trainY)  # training step

        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        end = time.time()
        rtTimes[x - 1, 0] = end - start

    xaxis = np.arange(1, 51)
    plt.plot(xaxis, dtTimes, label="DTLearner Times")
    plt.plot(xaxis, rtTimes, label="RTLearner Times")
    plt.xlabel("Leaf Sizes")
    plt.ylabel("Times")
    plt.legend()
    plt.title("Experiment 3 - DT Learners vs. RT Learners wrt Time")
    plt.savefig("Exp3.png")
    plt.clf()