import numpy as np
import random
from scipy import stats

## Pranshav Thakkar
## pthakkar7

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.rtree = None

    def author(self):
        return 'pthakkar7'

    def addEvidence(self, xTrain, yTrain):
        tree = self.buildTree(xTrain, yTrain)

        if self.rtree == None:
            self.rtree = tree
        else:
            self.rtree = np.vstack((self.rtree, tree))

    def query(self, xTest):
        predictions = []
        for x in xTest:
            predictions.append(self.rTreeFind(x, row=0))
        return np.asarray(predictions)

    def buildTree(self, xTrain, yTrain):

        if xTrain.shape[0] <= self.leaf_size:
            return np.array([-1, yTrain.mean(), np.nan, np.nan])
        if len(np.unique(yTrain)) == 1:
            return np.array([-1, yTrain.mean(), np.nan, np.nan])
        else:

            bestFeature = random.randint(0, xTrain.shape[1] - 1)
            splitVal = np.median(xTrain[:, bestFeature])
            if (np.all(xTrain[:, bestFeature] <= splitVal)):
                return np.array([-1, yTrain.mean(), np.nan, np.nan])
            leftTree = self.buildTree(xTrain[xTrain[:,bestFeature]<= splitVal], yTrain[xTrain[:,bestFeature]<= splitVal])
            rightTree = self.buildTree(xTrain[xTrain[:,bestFeature]> splitVal], yTrain[xTrain[:,bestFeature]> splitVal])
            if leftTree.ndim == 1:
                rightStartIndex = 2
            elif leftTree.ndim > 1:
                rightStartIndex = leftTree.shape[0] + 1
            root = np.array([bestFeature, splitVal, 1, rightStartIndex])

            return np.vstack((root, leftTree, rightTree))

    def rTreeFind(self, test, row):

        feature, splitval = self.rtree[row, 0:2]

        if feature == -1:
            return splitval
        elif test[int(feature)] <= splitval:
            pred = self.rTreeFind(test, row + int(self.rtree[row, 2]))
        else:
            pred = self.rTreeFind(test, row + int(self.rtree[row, 3]))

        return pred