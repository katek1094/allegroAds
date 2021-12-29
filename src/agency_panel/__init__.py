from .oop_stats_scraper import Requirement, scrape_stats

r = Requirement('wwwkoomputerypl', 'sponsored', 'last_week', 'offers')


def xd():
    print(scrape_stats(r))
