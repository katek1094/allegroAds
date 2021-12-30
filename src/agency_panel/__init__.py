from .oop_stats_scraper import Requirement, find_scraper, AgencyDriver


def scrape_stats(requirement: Requirement):
    driver = AgencyDriver()
    scraper = find_scraper(driver, requirement)

    return scraper.scrape_stats()
