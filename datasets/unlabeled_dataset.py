
from datasets.abstract_dataset import AbstractDataset
from datasets.unlabeled_dataset_interface import UnlabeledDatasetInterface


class UnlabeledDataset(UnlabeledDatasetInterface, AbstractDataset):

    def __init__(self, netflow):
        self.__netflow = netflow

    @property
    def netflow(self):
        return self.__netflow
