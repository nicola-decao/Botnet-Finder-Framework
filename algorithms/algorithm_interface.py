
import abc


class AlgorithmInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stratified_k_fold(self, folds, best):
        raise NotImplementedError
