from abc import ABC, abstractmethod
from pprint import pformat


class Stats(ABC):
    @property
    @abstractmethod
    def labels(self):
        pass

    @property
    @abstractmethod
    def ads_type(self):
        pass

    @property
    @abstractmethod
    def detail_level(self):
        pass

    def __repr__(self):
        return pformat(vars(self))

    def check_stats_len(self, stats):
        if not len(stats) == len(self.labels):
            raise ValueError(f'length of stats ({len(stats)}) is not equal to length of labels ({len(self.labels)}) !')

    def generate_stats_dict(self, stats):
        self.check_stats_len(stats)
        zip_iterator = zip(self.labels, stats)
        return dict(zip_iterator)


class SponsoredStatsMixin:
    ads_type = 'sponsored'
    labels = ('clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value')


class GraphicStatsMixin:
    ads_type = 'graphic'
    labels = ('clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale', 'pcs sold ',
              'sales value')


class SponsoredOfferStats(SponsoredStatsMixin, Stats):
    detail_level = 'offers'

    def __init__(self, name: str, id_number: int, campaign_name: str, group_name: str, stats):
        self.name = name
        self.id_number = id_number
        self.campaign_name = campaign_name
        self.group_name = group_name
        self.stats = self.generate_stats_dict(stats)


class SponsoredGroupStats(SponsoredStatsMixin, Stats):
    detail_level = 'groups'

    def __init__(self, name: str, campaign_name: str, stats):
        self.name = name
        self.campaign_name = campaign_name
        self.stats = self.generate_stats_dict(stats)


class SponsoredCampaignStats(SponsoredStatsMixin, Stats):
    detail_level = 'campaigns'

    def __init__(self, name: str, stats):
        self.name = name
        self.stats = self.generate_stats_dict(stats)


class GraphicAdStats(GraphicStatsMixin, Stats):
    detail_level = 'ads'

    def __init__(self, name: str, stats):
        self.name = name
        self.stats = self.generate_stats_dict(stats)


class GraphicGroupStats(GraphicStatsMixin, Stats):
    detail_level = 'groups'

    def __init__(self, name: str, stats):
        self.name = name
        self.stats = self.generate_stats_dict(stats)


class GraphicCampaignStats(GraphicStatsMixin, Stats):
    detail_level = 'campaigns'

    def __init__(self, name: str, stats):
        self.name = name
        self.stats = self.generate_stats_dict(stats)

