from pprint import pformat
from abc import ABC, abstractmethod


class Stats(ABC):
    @property
    @abstractmethod
    def labels(self):
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
    labels = ('clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value')
    detail_levels = ('campaigns', 'groups', 'offers')


class GraphicStatsMixin:
    labels = ('clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale', 'pcs sold ',
              'sales value')
    detail_levels = ('campaigns', 'groups', 'ads')


class SponsoredOfferStats(SponsoredStatsMixin, Stats):
    def __init__(self, name: str, id_number: int, campaign_name: str, group_name: str, stats):
        self.name = name
        self.id_number = id_number
        self.campaign_name = campaign_name
        self.group_name = group_name
        self.stats = self.generate_stats_dict(stats)


class SponsoredGroupStats(SponsoredStatsMixin, Stats):
    def __init__(self, name: str, campaign_name: str, stats):
        self.name = name
        self.campaign_name = campaign_name
        self.stats = self.generate_stats_dict(stats)


class SponsoredCampaignStats(SponsoredStatsMixin, Stats):
    def __init__(self, name: str, stats):
        self.name = name
        self.stats = self.generate_stats_dict(stats)


class GraphicAdStats(GraphicStatsMixin, Stats):
    pass


class GraphicGroupStats(GraphicStatsMixin, Stats):
    pass


class GraphicCampaignStats(GraphicStatsMixin, Stats):
    pass
