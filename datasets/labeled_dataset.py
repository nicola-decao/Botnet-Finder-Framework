
from datasets.labeled_dataset_interface import LabeledDatasetInterface
from datasets.unlabeled_dataset import UnlabeledDataset


class LabeledDataset(LabeledDatasetInterface, UnlabeledDataset):

    def __init__(self, netflow, labels):
        UnlabeledDataset.__init__(self, netflow)
        self.__labels = labels

    @property
    def labels(self):
        return self.__labels
