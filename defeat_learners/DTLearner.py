import numpy as np
from operator import itemgetter

class DTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.dtree = None

    def author(self):
        return 'pthakkar7'

    def addEvidence(self, xTrain, yTrain):
        tree = self.buildTree(xTrain, yTrain)

        if self.dtree == None:
            self.dtree = tree
        else:
            self.dtree = np.vstack((self.dtree, tree))

    def query(self, xTest):
        predictions = []
        for x in xTest:
            predictions.append(self.dTreeFind(x, row=0))
        return np.asarray(predictions)

    def buildTree(self, xTrain, yTrain):

        if xTrain.shape[0] <= self.leaf_size:
            return np.array([-1, yTrain.mean(), np.nan, np.nan])
        if len(np.unique(yTrain)) == 1:
            return np.array([-1, yTrain.mean(), np.nan, np.nan])
        else:
            correlations = []
            for i in range(xTrain.shape[1]):
                corr = np.corrcoef(xTrain[:, i], yTrain)
                abscorr = abs(corr[0,1])
                correlations.append((i, abscorr))
            bestFeature = max(correlations, key=itemgetter(1))[0]
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

    def dTreeFind(self, test, row):

        feature, splitval = self.dtree[row, 0:2]

        if feature == -1:
            return splitval
        elif test[int(feature)] <= splitval:
            pred = self.dTreeFind(test, row + int(self.dtree[row, 2]))
        else:
            pred = self.dTreeFind(test, row + int(self.dtree[row, 3]))

        return pred