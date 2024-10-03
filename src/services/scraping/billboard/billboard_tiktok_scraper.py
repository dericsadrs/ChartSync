from typing import List, Dict
import logging
from playwright.sync_api import sync_playwright
from model.song import Song
from model.billboard_chart import BillboardChart
import json

class BillboardTikTokScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _scrape_tiktok_chart(self, url: str) -> str:
        """Scrapes the TikTok Billboard Top 50 and returns JSON data."""
        
        logging.info(f"Starting to scrape TikTok chart from {url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                page.wait_for_selector("div.chart-results-list", timeout=60000)

                # Extract song titles and artists
                chart_items = page.query_selector_all("div.o-chart-results-list-row-container")
                songs = []
                for idx, item in enumerate(chart_items, start=1):
                    # Extract song title
                    title_element = item.query_selector("h3.c-title")
                    title = title_element.inner_text().strip() if title_element else "Unknown Title"

                    # Extract artist
                    artist_element = item.query_selector("span.c-label.a-font-primary-s")
                    artist = artist_element.inner_text().strip() if artist_element else "Unknown Artist"

                    songs.append(Song(title, artist))
                    logging.info(f"Extracted #{idx}: {title} by {artist}")

                logging.info(f"Successfully scraped {len(songs)} songs from the TikTok chart")
                browser.close()

            # Create a BillboardChart object and return its JSON representation
            billboard_chart = BillboardChart(songs)
            return billboard_chart.to_json()

        except Exception as e:
            logging.error(f"An error occurred while scraping TikTok chart: {e}")
            return json.dumps([])

    def get_top_50(self) -> str:
        """
        Get the TikTok Billboard Top 50 chart.
        """
        url = self.base_url  # Use the base URL as the default value
        return self._scrape_tiktok_chart(url)
