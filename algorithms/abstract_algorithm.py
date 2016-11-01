
import abc
import numpy as np

from algorithms.algorithm_interface import AlgorithmInterface
from sklearn.cross_validation import StratifiedKFold
from util import log


class AbstractAlgorithm(AlgorithmInterface):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _build_classifier(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _build_best_classifier(self, x, y):
        raise NotImplementedError

    def _pre_folds(self, clf, x, y):
        pass

    def _pre_fit(self, clf, x, y, train, test):
        pass

    def _fit(self, clf, x, y, train, test):
        raise NotImplementedError

    def _post_fit(self, clf, x, y, train, test):
        pass

    def _pre_predict(self, clf, x, y, train, test):
        pass

    def _predict(self, clf, x, y, train, test):
        raise NotImplementedError

    def _post_predict(self, clf, x, y, train, test):
        pass

    def _post_folds(self, clf, x, y, y_tests, y_predictions, y_labels):
        pass

    def stratified_k_fold(self, folds=10, best=False):

        log('[START]\tmatrices extraction')
        x, y, l = self.__matrices
        log('[END]\tmatrices extraction')

        log('[START]\tclassifier building')

        if best:
            clf = self._build_best_classifier(x, y)
        else:
            clf = self._build_classifier()

        log('[END]\tclassifier building')

        y_tests = []
        y_predictions = []
        y_labels = []

        log('[START]\tpre folds operations')
        self._pre_folds(clf, x, y)
        log('[END]\tpre folds operations')

        skf = StratifiedKFold(y, n_folds=folds)

        for train, test in skf:
            log('[START]\tpre fit operations')
            self._pre_fit(clf, x, y, train, test)
            log('[END]\tpre fit operations')

            log('[START]\tfit operations')
            self._fit(clf, x, y, train, test)
            log('[END]\tfit operations')

            log('[START]\tpost fit operations')
            self._post_fit(clf, x, y, train, test)
            log('[END]\tpost fit operations')

            log('[START]\tpre predict operations')
            self._pre_predict(clf, x, y, train, test)
            log('[END]\tpre predict operations')

            log('[START]\tpredict operations')
            y_predictions.append(self._predict(clf, x, y, train, test))
            log('[END]\tpredict operations')

            log('[START]\tpost predict operations')
            self._post_predict(clf, x, y, train, test)
            log('[END]\tpost predict operations')

            y_tests.append(y[test])
            y_labels.append(l[test])

        log('[START]\tpost folds operations')
        self._post_folds(clf, x, y, y_tests, y_predictions, y_labels)
        log('[END]\tpost folds operations')

        return np.array(y_tests), np.array(y_predictions), np.array(y_labels)

    @property
    def __matrices(self):
        ips = sorted(self.__features.keys())
        features_keys = sorted(self.__features[ips[0]].keys())

        features_keys.remove('label')

        x = [[self.__features[ip][feature] for feature in features_keys] for ip in ips]
        y = [self.__features[ip]['label'] != '0' for ip in ips]
        labels = [self.__features[ip]['label'] for ip in ips]

        return np.array(x), np.array(y), np.array(labels)

    def __init__(self, features):
        self.__features = features
