from discogs import scraper
from icecream import ic

scraper = scraper.DiscogsMarketplaceScraper("Electronic", "Electro", 1)


def test_fetch_item_links():
    item_links = scraper.fetch_item_links
    ic(item_links)