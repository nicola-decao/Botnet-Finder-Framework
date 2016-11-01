
from util import log
from datasets.dataset_builder_interface import DatasetBuilderInterface
from datasets.bottrack.builder import BotTrackDatasetBuilder
from datasets.disclosure.builder import DisclosureDatasetBuilder


class DatasetBuilder(DatasetBuilderInterface):

    @property
    def __dataset_builders_map(self):
        return {
            'bottrack': BotTrackDatasetBuilder,
            'disclosure': DisclosureDatasetBuilder
        }

    def build(self, filename, **kwargs):
        log('[START]\tbuilding dataset')
        dataset = self.__dataset_builder.build(filename, **kwargs)
        log('[END]\tbuilding dataset')

        return dataset

    def __init__(self, builder):
        self.__dataset_builder = self.__dataset_builders_map[builder]()
