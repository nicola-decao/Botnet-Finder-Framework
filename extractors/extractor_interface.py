
import abc


class ExtractorInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract(self, dataset, **kwargs):
        raise NotImplementedError
