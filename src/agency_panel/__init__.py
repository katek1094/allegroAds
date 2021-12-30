from .oop_stats_scraper import Requirement, scrape_stats

r = Requirement('handlowiec-rs-pl', 'graphic', 'last_week', 'campaigns')


def xd():
    print(scrape_stats(r))
