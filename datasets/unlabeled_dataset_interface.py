
import abc


class UnlabeledDatasetInterface:

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def netflow(self):
        raise NotImplementedError
