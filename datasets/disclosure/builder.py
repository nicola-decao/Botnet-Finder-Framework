
from datasets.abstract_dataset import AbstractDataset
from datasets.abstract_dataset_builder import AbstractDatasetBuilder
from datasets.disclosure.dataset import DisclosureDataset


class DisclosureDatasetBuilder(AbstractDatasetBuilder):

    def _build(self, netflow, columns, **kwargs):
        labels = netflow[:, len(columns) - 1]
        netflow = netflow[:, range(0, len(columns) - 1)]

        return DisclosureDataset(netflow, labels, **kwargs)

    @property
    def columns(self):
        return [AbstractDataset.Field.DateFlowStart, AbstractDataset.Field.Duration, AbstractDataset.Field.SourceIPAddress, AbstractDataset.Field.SourceIPPort, AbstractDataset.Field.DestinationIPAddress, AbstractDataset.Field.DestinationIPPort, AbstractDataset.Field.Bytes, AbstractDataset.Field.Labels]
