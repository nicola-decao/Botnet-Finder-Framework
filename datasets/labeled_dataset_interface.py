
import abc

from datasets.unlabeled_dataset_interface import UnlabeledDatasetInterface


class LabeledDatasetInterface(UnlabeledDatasetInterface):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def labels(self):
        raise NotImplementedError
