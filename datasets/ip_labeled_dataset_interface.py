
import abc

from datasets.labeled_dataset_interface import LabeledDatasetInterface


class IpLabeledDatasetInterface(LabeledDatasetInterface):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def labeled_ips(self):
        raise NotImplementedError
