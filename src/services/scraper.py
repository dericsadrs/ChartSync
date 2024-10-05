import logging
from typing import List
from playwright.sync_api import sync_playwright 
from model.song import Song
from model.songs import Songs
from model.chart_tags import ChartTags
from music_chart_scraper_config import MUSIC_CHART_SCRAPER_CONFIG  # Assuming ChartTags is also in the model

class Scraper:
    def __init__(self, headless: bool = True, chart_type: str = "billboard_hot_100"):
        """
        Initialize the BillboardScraper class.

        :param headless: Whether to run the browser in headless mode (default True).
        :param chart_type: The type of Billboard chart to scrape (default 'billboard_hot_100').
        """
        self.chart_type = chart_type
        self.config = MUSIC_CHART_SCRAPER_CONFIG.get(chart_type)
        
        if not self.config:
            raise ValueError(f"Chart type '{chart_type}' is not supported.")
        
        tags = self.config['tags']
        # Use the ChartTags model to store tag configuration
        self.tags = ChartTags(tags["chart_item"], tags["title"], tags["artist"])
        self.base_url = self.config['url']
        self.headless = headless
        logging.info(f"Initialized BillboardScraper with headless={self.headless} and chart_type={self.chart_type}")

    def _scrape_chart(self, url: str) -> Songs:
        """Scrapes the configured Billboard chart for the latest songs."""

        logging.info(f"Starting to scrape Billboard chart from {url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                logging.info("Browser launched")

                page = browser.new_page()
                logging.info(f"Navigating to URL: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)

                # Wait for the chart rows to load using the tag configuration from the ChartTags model
                logging.info("Waiting for the chart rows to load")
                page.wait_for_selector(self.tags.chart_item, timeout=60000)

                # Extract song titles and artists using the tag configuration from the ChartTags model
                chart_items = page.query_selector_all(self.tags.chart_item)
                songs = []
                for idx, item in enumerate(chart_items, start=1):
                    # Extract song title
                    title_element = item.query_selector(self.tags.title)
                    title = title_element.inner_text().strip() if title_element else "Unknown Title"

                    # Extract artist
                    artist_element = item.query_selector(self.tags.artist)
                    artist = artist_element.inner_text().strip() if artist_element else "Unknown Artist"

                    songs.append(Song(title, artist))
                    logging.info(f"Extracted #{idx}: {title} by {artist}")

                logging.info(f"Successfully scraped {len(songs)} songs from the chart")
                browser.close()

            return Songs(songs)

        except Exception as e:
            logging.error(f"An error occurred while scraping Billboard chart: {e}")
            return Songs([])

    def get_latest_chart(self) -> Songs:
        """
        Get the latest available Billboard chart.

        :return: A Songs object containing a list of Song objects.
        """
        logging.info(f"Fetching the most recent Billboard chart from {self.base_url}")
        return self._scrape_chart(self.base_url)

    def display_songs(self, songs: Songs) -> None:
        """
        Display the fetched Billboard songs in a human-readable format.

        :param songs: A Songs object containing a list of Song objects.
        """
        logging.info(f"Displaying {len(songs.songs)} songs")
        for idx, song in enumerate(songs.songs, start=1):
            print(f"{idx}. {song.title} by {song.artist}")
