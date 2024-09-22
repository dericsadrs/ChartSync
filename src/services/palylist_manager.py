import logging
from services.billboard_scraper import BillboardScraper
from services.spotify_playlist_maker import SpotifyPlaylistMaker
import re  # Add this import for regex validation

class PlaylistManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.billboard_scraper = BillboardScraper(headless=True)
        self.spotify_maker = SpotifyPlaylistMaker()

    def create_billboard_playlist(self, date: str = None):
        """
        Create a Spotify playlist with the Billboard Hot 100 songs.
        """
        try:
            # Validate date format
            if date and not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
                logging.error("Invalid date format. Please use 'YYYY-MM-DD'.")
                return

            if date:
                logging.info(f"Fetching Billboard Hot 100 for {date}")
                hot_100_songs = self.billboard_scraper.get_hot_100_by_date(date)
            else:
                logging.info("Fetching the latest Billboard Hot 100 chart")
                hot_100_songs = self.billboard_scraper.get_latest_hot_100()

            if not hot_100_songs:
                logging.error("No songs found in the Billboard Hot 100 chart.")
                return

            # Get current user's Spotify ID
            user = self.spotify_maker.sp.current_user()
            user_id = user['id']
            logging.info(f"Authenticated as Spotify user: {user['display_name']}")

            # Create a Spotify playlist for the Billboard Hot 100
            playlist_name = f"Billboard Hot 100 Playlist {date if date else 'Latest'}"
            playlist_description = "Automatically generated Billboard Hot 100 playlist."
            playlist_id = self.spotify_maker.create_playlist(user_id, playlist_name, playlist_description)

            # Search and collect Spotify URIs for the Billboard Hot 100 songs
            track_uris = []
            for song in hot_100_songs:
                uri = self.spotify_maker.search_song(artist=song['artist'], track=song['title'])
                if uri:
                    track_uris.append(uri)

            # Add tracks to the playlist
            if track_uris:
                self.spotify_maker.add_tracks_to_playlist(playlist_id, track_uris)
                logging.info(f"Successfully added {len(track_uris)} songs to the Spotify playlist.")
            else:
                logging.error("No songs were added to the playlist. Please check the song search functionality.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

