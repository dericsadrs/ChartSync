import logging
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
class PlaylistManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.spotify_maker = SpotifyPlaylistMaker()

    def create_playlist(self, chart_type: str):
        """
        Create a Spotify playlist based on the specified chart type.

        :param chart_type: The type of chart to scrape (e.g., "billboard_hot_100" or "tiktok_top_50").
        """
        try:
            # Initialize the appropriate scraper based on chart_type
            scraper = Scraper(headless=True)  # Updated class name

            # Fetch the latest chart data
            logging.info(f"Fetching the latest {chart_type.replace('_', ' ').title()}")
            songs_data = scraper.get_latest_chart()  # Assuming this will always fetch the latest songs

            if not songs_data.songs:
                logging.error(f"No songs found in the {chart_type.replace('_', ' ').title()}.")
                return

            # Get current user's Spotify ID
            user = self.spotify_maker.sp.current_user()
            user_id = user['id']
            logging.info(f"Authenticated as Spotify user: {user['display_name']}")

            # Create a Spotify playlist for the specified chart
            playlist_name = f"{chart_type.replace('_', ' ').title()} Playlist"
            playlist_description = f"Automatically generated {chart_type.replace('_', ' ').title()} playlist."
            playlist_id = self.spotify_maker.create_playlist(user_id, playlist_name, playlist_description)

            # Search and collect Spotify URIs for the songs
            track_uris = []
            for song in songs_data.songs:
                uri = self.spotify_maker.search_song(artist=song.artist, track=song.title)
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