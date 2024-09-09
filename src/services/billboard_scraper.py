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

    def _scrape_hot_100(self, date: str) -> List[Dict[str, str]]:
        """Scrapes the Billboard Hot 100 for a specific date."""
        url = f"{self.base_url}/{date}"
        logging.info(f"Starting to scrape Billboard Hot 100 for {date} at {url}")

        with sync_playwright() as p:
            # Launch the browser, using the headless parameter from the constructor
            browser = p.chromium.launch(headless=self.headless)
            logging.info("Browser launched")

            page = browser.new_page()

            # Navigate to the Billboard chart URL with longer timeout and wait for DOM content
            logging.info(f"Navigating to URL: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)  # Wait for DOM content

            # Increase timeout and target the correct selector
            logging.info("Waiting for the chart rows to load")
            try:
                page.wait_for_selector("ul.o-chart-results-list-row", timeout=60000)  # Wait up to 60 seconds
            except Exception as e:
                logging.error("Failed to load chart list", exc_info=e)
                page.screenshot(path="error_screenshot.png")  # Take a screenshot to debug
                raise e

            # Select and scrape song titles and artists from the chart
            logging.info("Extracting song titles and artists")
            chart_items = page.query_selector_all("ul.o-chart-results-list-row")
            songs = []
            for idx, item in enumerate(chart_items, start=1):
                # Extract song title
                title_element = item.query_selector("h3.c-title")
                if title_element:
                    title = title_element.inner_text().strip()
                else:
                    logging.warning(f"Title element not found for item #{idx}. Skipping.")
                    continue  # Skip this entry if title is missing

                # Extract artist
                artist_element = item.query_selector("span.c-label")
                artist = artist_element.inner_text().strip() if artist_element else "Unknown Artist"
                
                songs.append({"title": title, "artist": artist})
                logging.info(f"Extracted #{idx}: {title} by {artist}")

            logging.info(f"Successfully scraped {len(songs)} songs from the chart")
            browser.close()
            logging.info("Browser closed")

        return songs

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
        url = "https://www.billboard.com/charts/hot-100/"
        
        logging.info(f"Fetching the most recent Billboard Hot 100 chart from {url}")
        return self._scrape_hot_100(url)

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

