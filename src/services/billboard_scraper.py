import json
import logging
from datetime import datetime
from typing import List, Dict
from playwright.sync_api import sync_playwright

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
class BillboardScraper:
    def __init__(self, headless: bool = True):
        """
        Initialize the BillboardScraper class.

        :param headless: Whether to run the browser in headless mode (default True).
        """
        self.base_url = "https://www.billboard.com/charts/hot-100"
        self.headless = headless  # Store the headless mode preference
        logging.info(f"Initialized BillboardScraper with headless={self.headless}")

    def _scrape_hot_100(self, url: str) -> List[Dict[str, str]]:
        """Scrapes the Billboard Hot 100 for a specific date or the latest chart."""

        logging.info(f"Starting to scrape Billboard Hot 100 from {url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                logging.info("Browser launched")

                page = browser.new_page()
                logging.info(f"Navigating to URL: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)

                # Wait for the chart rows to load
                logging.info("Waiting for the chart rows to load")
                page.wait_for_selector("ul.o-chart-results-list-row", timeout=60000)

                # Extract song titles and artists
                chart_items = page.query_selector_all("ul.o-chart-results-list-row")
                songs = []
                for idx, item in enumerate(chart_items, start=1):
                    # Extract song title
                    title_element = item.query_selector("h3.c-title")
                    title = title_element.inner_text().strip() if title_element else "Unknown Title"

                    # Extract artist using the refined selector
                    artist_element = item.query_selector("span.c-label.a-no-trucate.a-font-primary-s")
                    artist = artist_element.inner_text().strip() if artist_element else "Unknown Artist"

                    songs.append({"title": title, "artist": artist})
                    logging.info(f"Extracted #{idx}: {title} by {artist}")

                logging.info(f"Successfully scraped {len(songs)} songs from the chart")
                browser.close()

            return songs

        except Exception as e:
            logging.error(f"An error occurred while scraping Billboard Hot 100: {e}")
            return []

    def get_hot_100_by_date(self, date: str) -> List[Dict[str, str]]:
        """
        Get Billboard Hot 100 chart for the specified date.

        :param date: The date of the chart in 'YYYY-MM-DD' format.
        :return: A list of dictionaries containing song titles and artists.
        """
        logging.info(f"Fetching Billboard Hot 100 for {date}")
        return self._scrape_hot_100(date)

    def get_latest_hot_100(self) -> List[Dict[str, str]]:
        """
        Get the latest available Billboard Hot 100 chart.
        
        :return: A list of dictionaries containing song titles and artists.
        """
    
        logging.info(f"Fetching the most recent Billboard Hot 100 chart from {self.base_url}")
        return self._scrape_hot_100(self.base_url)

    def display_songs(self, songs: List[Dict[str, str]]) -> None:
        """
        Display the fetched Hot 100 songs in a human-readable format.

        :param songs: A list of dictionaries containing song titles and artists.
        """
        logging.info(f"Displaying {len(songs)} songs")
        for idx, song in enumerate(songs, start=1):
            print(f"{idx}. {song['title']} by {song['artist']}")

    def get_hot_100_json(self, songs: List[Dict[str, str]]) -> str:
        """
        Convert the fetched Hot 100 songs into a JSON format string.

        :param songs: A list of dictionaries containing song titles and artists.
        :return: A JSON string of the song data.
        """
        logging.info("Converting songs to JSON format")
        return json.dumps(songs, indent=4)


