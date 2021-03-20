# Discogs marketplace scraper
![Discogs](assets/discogs_logo.jpg)

## Introduction
This program will download items of specific style from Discogs Marketplace, return a pandas dataframe and 
optionally save the data to csv file. Please note it is rate limited to avoid blacklisting, therefore gathering a 
large amount of data might take a very long time.

## Installation
```
pip install git+https://github.com/grigorjevas/Discogs-marketplace-scraper
```

## Usage
```python
from discogs import scraper
scraper = scraper.DiscogsMarketplaceScraper("Experimental", 5)
df = scraper.fetch_items
```

`DiscogsMarketPlaceScraper` params:
- `style` - (str) any style from the official Discogs [styles list](https://blog.discogs.com/en/genres-and-styles/)
- `items_to_fetch` - (int) a number of items to fetch
- `export_to_csv` - (bool), default = False

`DiscogsMarketPlaceScraper` functions:
- `fetch_items` - returns pandas dataframe and optionally exports a csv file to working dir
- `fetch_item_links` - iterates through pagination and creates a list of item links
- `validate_max_items` - validates number of items to fetch against items available for particular style
- `validate_style` - validates requested style against list of available styles
- `pages_to_scrape` - counts how many pages should be scraped to collect requested number of items
- `items_per_page` - counts how many items per page should be requested
- `load_url` - loads a url and returns BeautifulSoup object
- `parse_item` - uses parser functions to parse required fields from the item page
- `export_to_csv` - exports a csv file to current working dir

#### Limitations
You can only scrape a maximum of 10 000 items in one go due to the way the website pagination is built. 
Anything past page 40 will result in a 404 error, so unless Discogs fix this bug, 10 000 is the limit. 


## Troubleshooting
If you encounter an `IndexError` in Google Colab, please check your package versions against `requirements.txt`, it is 
very likely that you might need to install newer version of a package. You can do it like so:
```
! pip install packagename==version
```

## License
This project is licensed under https://tldrlegal.com/license/mit-license
