from bs4 import BeautifulSoup
from discogs import parser, available_styles
from datetime import datetime
import requests
import pandas as pd
import time
import random
import re


class DiscogsMarketplaceScraper:
    def __init__(self, style: str, items_to_scrape: int, export_to_csv: bool = False):
        """
        Discogs.com marketplace scraper class.
        Available methods:
            * fetch_items
            * fetch_item_links
            * validate_max_items
            * validate_styles
            * pages_to_scrape
            * items_per_page
            * load_url
            * parse_item
            * export_to_csv
        """
        self.__style = style
        self.__currency = "EUR"
        self.__format = "Vinyl"
        self.__columns = ["artist", "title", "label", "release_format", "number_of_tracks", "release_date", "price",
                          "rating", "votes", "have", "want", "limited_edition", "media_condition", "sleeve_condition",
                          "release_page"]
        self.__items_to_scrape = items_to_scrape
        self.__export_to_csv = export_to_csv

    @property
    def fetch_items(self) -> pd.DataFrame:
        """
        Fetches items from Discogs marketplace collecting a specified number of examples.
        :return: pandas DataFrame
        """
        self.validate_max_items()
        self.validate_style()
        records = []
        count = 1
        item_links = self.fetch_item_links
        for item_link in item_links:
            time.sleep(random.randint(1, 2))
            url = f"https://www.discogs.com{item_link['href']}"
            print(f"Processing item {count}/{len(item_links)}: {url}")
            records.extend([self.parse_item(self.load_url(url))])
            count += 1

        df = pd.DataFrame(records, columns=self.__columns)
        if self.__export_to_csv:
            self.export_to_csv(df)
        return df

    @property
    def fetch_item_links(self) -> list:
        """
        Fetches item links and builds a list.
        :return: list of item links
        """
        item_links = []
        for i in range(1, self.pages_to_scrape+1):
            time.sleep(random.randint(1, 2))
            url = f"https://www.discogs.com/sell/list?sort=listed%2Cdesc" \
                  f"&limit={self.items_per_page}" \
                  f"&currency={self.__currency}" \
                  f"&format={self.__format}" \
                  f"&style={self.__style.title().replace(' ', '+')}" \
                  f"&page={i}"
            soup = self.load_url(url)
            item_links.extend(soup.find_all("a", class_="item_description_title"))

        return item_links[0:self.__items_to_scrape]

    def validate_max_items(self) -> None:
        """
        Validates number of items to fetch.
        :raise: ValueError if items to fetch value is higher than items actually available at the marketplace.
        :return: None
        """
        url = f"https://www.discogs.com/sell/list?sort=listed%2Cdesc" \
              f"&limit={self.items_per_page}" \
              f"&currency={self.__currency}" \
              f"&format={self.__format}" \
              f"&style={self.__style}" \
              f"&page=1"
        soup = self.load_url(url)
        max_items = int(re.search("of (.*)", soup.find("strong", class_="pagination_total").text.strip())
                        .group(1).replace(",", ""))
        if self.__items_to_scrape > max_items:
            raise ValueError(f"{self.__items_to_scrape} items is more than actually available in the marketplace.")
        return

    def validate_style(self) -> None:
        """
        Validates style against all available styles list in available_styles.py
        :raise: ValueError if invalid style provided
        :return: None
        """
        if self.__style.title() not in available_styles.available_styles:
            raise ValueError(f"{self.__style} is not available in the marketplace.")
        return

    @property
    def pages_to_scrape(self) -> int:
        """
        Counts how many pages to scrape.
        :return: int number of pages to scrape
        """
        if self.__items_to_scrape >= 250:
            return int(self.__items_to_scrape / 250+1)
        return 1

    @property
    def items_per_page(self) -> int:
        if self.__items_to_scrape <= 250:
            items_per_page_options = [25, 50, 100, 250]
            key = next(key for key, val in enumerate(items_per_page_options) if val >= self.__items_to_scrape)
            return items_per_page_options[key]
        return 250

    @staticmethod
    def load_url(url: str) -> BeautifulSoup:
        """
        Loads and parses an url using BeautifulSoup Python library.

        :param url: str, valid url, for example: https://turingcollege.com/
        :return: BeautifulSoup object
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except requests.exceptions.RequestException:
            raise SystemError("Catastrophic error. Check your URL.")

    @staticmethod
    def parse_item(soup: object) -> tuple:
        """
        Parses record data into the column.

        :param soup: BeautifulSoup object
        :return: tuple
        """
        parse = parser.DiscogsMarketplaceParser(soup)
        return parse.artist, \
            parse.title, \
            parse.label, \
            parse.release_format, \
            parse.number_of_tracks, \
            parse.release_date, \
            parse.price, \
            parse.rating, \
            parse.votes, \
            parse.have, \
            parse.want, \
            parse.limited_edition, \
            parse.media_condition, \
            parse.sleeve_condition, \
            parse.release_page_url

    def export_to_csv(self, df: pd.DataFrame) -> None:
        """
        Exports a dataframe to a .csv file in working dir.

        :param df: pandas dataframe
        :return: None
        """
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        df.to_csv(f"{self.__style}_{timestamp}.csv", index=False, header=self.__columns)
        return
