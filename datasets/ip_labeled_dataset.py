
import abc

from util import log
from datasets.ip_labeled_dataset_interface import IpLabeledDatasetInterface
from datasets.labeled_dataset import LabeledDataset


class IpLabeledDataset(IpLabeledDatasetInterface, LabeledDataset):

    __metaclass__ = abc.ABCMeta

    def _associate_labels(self, ips):

        log('[START]\tassociate labels to IPs')

        log('IPs are ' + str(len(ips)))

        labels = {ip: '0' for ip in ips}

        for row, label in zip(self.netflow, self.labels):
            if row[self.Field.DestinationIPAddress] in labels and label != '0':
                labels[row[self.Field.DestinationIPAddress]] = label

            if row[self.Field.SourceIPAddress] in labels and label != '0':
                labels[row[self.Field.SourceIPAddress]] = label

        log('botnet IPs are: ' + str(sum([i != '0' for i in labels.values()])))

        log('[END]\tassociate labels to IPs')

        return labels

    @abc.abstractmethod
    def _extract_ips(self, netflow, labels, **kwargs):
        raise NotImplementedError

    @property
    def labeled_ips(self):
        return self.__labeled_ip

    def __init__(self, netflow, labels, **kwargs):
        LabeledDataset.__init__(self, netflow, labels)
        self.__labeled_ip = self._associate_labels(self._extract_ips(netflow, labels, **kwargs))
