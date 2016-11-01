
import numpy as np

from datasets.ip_labeled_dataset import IpLabeledDataset


class BotTrackDataset(IpLabeledDataset):

    def _extract_ips(self, netflow, labels, **kwargs):
        return set(np.concatenate((self.netflow[:, self.Field.SourceIPAddress], self.netflow[:, self.Field.DestinationIPAddress])))

    class Field:
        SourceIPAddress = 0
        DestinationIPAddress = 1
        Labels = 2
