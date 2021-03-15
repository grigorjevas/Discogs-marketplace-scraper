import pytest
from discogs import scraper
from bs4 import BeautifulSoup

scraper1 = scraper.DiscogsMarketplaceScraper("Experimental", 25)
scraper2 = scraper.DiscogsMarketplaceScraper("Experimental", 999999999)
scraper3 = scraper.DiscogsMarketplaceScraper("InvalidStyle", 10)


def test_items_per_page():
    assert scraper1.items_per_page == 25


def test_pages_to_scrape():
    assert scraper1.pages_to_scrape == 1


def test_fetch_item_links():
    links = scraper1.fetch_item_links
    assert len(links) == 25


def test_load_url_error():
    with pytest.raises(SystemError) as context:
        scraper1.load_url("https://discogs-with-typo.com/")
    assert str(context.value) == "Catastrophic error. Check your URL."


def test_parser():
    soup = BeautifulSoup(open("test/example_page.html"), "html.parser")
    expected = ('Pascal Hetzel', 'Extra Terra / Fermi Paradox', 'Expansion Unit \u200e– E-UNIT 003', '12"', 2,
                '13 Feb 2017', '8.00', '5.00', '9', '63', '55', 0, 'Mint (M)', 'Near Mint (NM or M-)',
                'https://discogs.com/Pascal-Hetzel-Extra-Terra-Fermi-Paradox/release/9830762?ev=item-vc')
    assert scraper1.parse_item(soup) == expected


def test_max_items_validation():
    with pytest.raises(ValueError) as context:
        scraper2.validate_max_items()
    assert str(context.value) == "999999999 items is more than actually available in the marketplace."


def test_invalid_style():
    with pytest.raises(ValueError) as context:
        scraper3.validate_style()
    assert str(context.value) == "InvalidStyle is not available in the marketplace."
