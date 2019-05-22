import DTLearner as dt
import numpy as np

class BagLearner(object):

    def __init__(self, learner = dt.DTLearner, kwargs = {"leaf_size":1}, bags = 20, boost = False, verbose = False):
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(0, bags):
            self.learners.append(learner(**self.kwargs))

    def author(self):
        return 'pthakkar7'

    def addEvidence(self, xTrain, yTrain):
        print(len(xTrain[0]))
        for x in range(0, self.bags):
            bagIndices = np.random.choice(xTrain.shape[0], xTrain.shape[0])
            xBag = xTrain[bagIndices]
            yBag = yTrain[bagIndices]
            self.learners[x].addEvidence(xBag, yBag)

    def query(self, xTest):
        predictions = []
        for x in range(0, self.bags):
            pred = self.learners[x].query(xTest)
            predictions.append(pred)

        predictions = np.asarray(predictions)
        predictions = np.mean(predictions, axis=0)
        return predictions