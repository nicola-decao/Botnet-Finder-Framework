
from util import log
from extractors.extractor_interface import ExtractorInterface
from extractors.bottrack.extractor import BotTrackExtractor
from extractors.disclosure.extractor import DisclosureExtractor


class Extractor(ExtractorInterface):

    @property
    def __extractors_map(self):
        return {
            'bottrack': BotTrackExtractor,
            'disclosure': DisclosureExtractor
        }

    def extract(self, dataset, **kwargs):
        log('[START]\tfeatures extraction')
        features = self.__extractor.extract(dataset, **kwargs)
        log('[END]\tfeatures extraction')

        return features

    def __init__(self, extractor):
        self.__extractor = self.__extractors_map[extractor]()
