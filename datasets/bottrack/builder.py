
from datasets.abstract_dataset import AbstractDataset
from datasets.abstract_dataset_builder import AbstractDatasetBuilder
from datasets.bottrack.dataset import BotTrackDataset


class BotTrackDatasetBuilder(AbstractDatasetBuilder):

    def _build(self, netflow, columns, **kwargs):
        labels = netflow[:, len(columns) - 1]
        netflow = netflow[:, range(0, len(columns) - 1)]

        return BotTrackDataset(netflow, labels)

    @property
    def columns(self):
        return [AbstractDataset.Field.SourceIPAddress, AbstractDataset.Field.DestinationIPAddress, AbstractDataset.Field.Labels]
