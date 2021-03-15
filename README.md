# Discogs marketplace scraper

## Introduction
This program will download items of specific style from Discogs Marketplace, return a pandas dataframe and 
optionally save the dump to csv file. Please note it is rate limited, therefore gathering a large amount of data might 
take a vary long time.

## Installation
### Google colab:
```
pip install git+https://github.com/grigorjevas/Discogs-marketplace-scraper
```

## Usage 
```python
from discogs import scraper
scraper = scraper.DiscogsMarketplaceScraper("Experimental", 5)
```

scraper = DiscogsMarketplaceScraper("Experimental", 25, True)
    items_df = scraper.fetch_items

[Styles guide](https://support.discogs.com/hc/en-us/articles/360005055213-Database-Guidelines-9-Genres-Styles#genres)

