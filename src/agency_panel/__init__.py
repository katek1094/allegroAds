from .oop_stats_scraper import Requirement, scrape_stats

r = Requirement('starhousegames', 'sponsored', 'last_week', 'campaigns')


def xd():
    print(scrape_stats(r))
