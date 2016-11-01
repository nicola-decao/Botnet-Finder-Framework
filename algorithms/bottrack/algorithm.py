
import numpy as np

from algorithms import AbstractAlgorithm
from sklearn.cluster import DBSCAN


class BotTrackAlgorithm(AbstractAlgorithm):

    def _build_classifier(self):
        return DBSCAN(min_samples=self.__min_pts, eps=self.__eps)

    def _build_best_classifier(self, x, y):
        return self._build_classifier()

    def _fit(self, clf, x, y, train, test):
        pass

    def _predict(self, clf, x, y, train, test):
        return np.array([l in self.__bot_clusters for l in self.__labels[test]])

    def _pre_folds(self, clf, x, y):
        db = clf.fit(x)
        self.__labels = db.labels_

    def _pre_predict(self, clf, x, y, train, test):
        self.__bot_clusters = set([l for l, f in zip(self.__labels[train], y[train]) if f and l != -1])

    def __init__(self, features, min_pts=4, eps=1e-07):
        AbstractAlgorithm.__init__(self, features)
        self.__min_pts = min_pts
        self.__eps = eps
