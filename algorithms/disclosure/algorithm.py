
import numpy as np

from algorithms import AbstractAlgorithm
from sklearn.ensemble import RandomForestClassifier
from sklearn import grid_search


class DisclosureAlgorithm(AbstractAlgorithm):

    def _build_classifier(self):
        return RandomForestClassifier(n_estimators=self.__trees)

    def _build_best_classifier(self, x, y):
        clf = grid_search.GridSearchCV(RandomForestClassifier(), [{'n_estimators': list(range(8, 30))}])
        clf.fit(x, y)

        return clf.best_estimator_

    def _fit(self, clf, x, y, train, test):
        clf.fit(x[train], y[train])

    def _predict(self, clf, x, y, train, test):
        return np.array(clf.predict(x[test]))

    def __init__(self, features, trees=10):
        AbstractAlgorithm.__init__(self, features)
        self.__trees = trees
