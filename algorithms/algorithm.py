
from util import log
from algorithms import AlgorithmInterface
from algorithms.bottrack.algorithm import BotTrackAlgorithm
from algorithms.disclosure.algorithm import DisclosureAlgorithm


class Algorithm(AlgorithmInterface):

    @property
    def __algorithms_map(self):
        return {
            'bottrack': BotTrackAlgorithm,
            'disclosure': DisclosureAlgorithm
        }

    def stratified_k_fold(self, folds=10, best=True):
        log('[START]\tstratified k fold validation')
        output = self.__algorithm.stratified_k_fold(folds, best)
        log('[END]\tstratified k fold validation')

        return output

    def __init__(self, algorithm, **kwargs):
        self.__algorithm = self.__algorithms_map[algorithm](**kwargs)
