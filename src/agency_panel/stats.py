class Stats:
    pass


class SponsoredStatsMixin:
    labels = ('clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value')
    detail_levels = ('campaigns', 'groups', 'offers')


class GraphicStatsMixin:
    labels = ('clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale', 'pcs sold ',
              'sales value')
    detail_levels = ('campaigns', 'groups', 'ads')


class SponsoredOfferStats(Stats, SponsoredStatsMixin):
    def __init__(self, name: str, id_number: int, campaign_name: str, group_name: str, stats):
        self.name = name
        self.id_number = id_number
        self.campaign_name = campaign_name
        self.group_name = group_name
        self.check_stats(stats)
        self.stats = self.generate_stats_dict(stats)

    def check_stats(self, stats):
        if not len(stats) == len(self.labels):
            raise ValueError(f'length of stats ({len(stats)}) is not equal to length of labels ({len(self.labels)}) !')

    def generate_stats_dict(self, stats):
        zip_iterator = zip(self.labels, stats)
        return dict(zip_iterator)


class SponsoredGroupStats(Stats, SponsoredStatsMixin):
    pass


class SponsoredCampaignStats(Stats, SponsoredStatsMixin):
    pass


class GraphicAdStats(Stats, GraphicStatsMixin):
    pass


class GraphicGroupStats(Stats, GraphicStatsMixin):
    pass


class GraphicCampaignStats(Stats, GraphicStatsMixin):
    pass
