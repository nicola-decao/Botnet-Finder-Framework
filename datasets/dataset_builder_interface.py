
import abc


class DatasetBuilderInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def build(self, filename, columns, **kwargs):
        raise NotImplementedError
