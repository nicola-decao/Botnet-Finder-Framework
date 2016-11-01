
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score


class Metrics:

    @staticmethod
    def accuracy(y_tests, y_predictions):
        accuracy = [accuracy_score(yt, yp) for yt, yp in zip(y_tests, y_predictions)]
        return accuracy, np.mean(accuracy), np.std(accuracy) / np.mean(accuracy) if np.mean(accuracy) else 0

    @staticmethod
    def precision(y_tests, y_predictions):
        precision = [precision_score(yt, yp) for yt, yp in zip(y_tests, y_predictions)]
        return precision, np.mean(precision), np.std(precision) / np.mean(precision) if np.mean(precision) else 0

    @staticmethod
    def recall(y_tests, y_predictions):
        recall = [recall_score(yt, yp) for yt, yp in zip(y_tests, y_predictions)]
        return recall, np.mean(recall), np.std(recall) / np.mean(recall) if np.mean(recall) else 0

    @staticmethod
    def roc_auc(y_tests, y_predictions):
        roc_auc = [roc_auc_score(yt, yp) for yt, yp in zip(y_tests, y_predictions)]
        return roc_auc, np.mean(roc_auc), np.std(roc_auc) / np.mean(roc_auc) if np.mean(roc_auc) else 0
