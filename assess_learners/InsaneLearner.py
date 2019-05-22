import BagLearner as bl
import LinRegLearner as lrl
import numpy as np
class InsaneLearner(object):
    def __init__(self, verbose = False):
        self.bag_learners = []
        for x in range(20):
            self.bag_learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))
    def author(self):
        return 'pthakkar7'
    def addEvidence(self, xTrain, yTrain):
        for bl in self.bag_learners:
            bl.addEvidence(xTrain, yTrain)
    def query(self, xTest):
        preds = []
        for bl in self.bag_learners:
            pred = bl.query(xTest)
            preds.append(pred)
        preds = np.mean(np.asarray(preds), axis=0)
        return preds