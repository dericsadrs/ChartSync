import logging
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from spotipy.exceptions import SpotifyException

class PlaylistManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.spotify_maker = SpotifyPlaylistMaker()

    def create_playlist(self, chart_type: str):
        """
        Create a Spotify playlist based on the specified chart type.

        :param chart_type: The type of chart to scrape (e.g., "billboard_hot_100" or "tiktok_top_50").
        :return: dict with status and message
        """
        try:
            self.logger.info(f"Starting playlist creation for {chart_type}")
            
            # Initialize the scraper
            scraper = Scraper(headless=True, chart_type=chart_type)
            self.logger.info(f"Initialized scraper for {chart_type}")

            # Fetch the latest chart data
            songs_data = scraper.get_latest_chart()
            if not songs_data.songs:
                self.logger.error(f"No songs found in the {chart_type.replace('_', ' ').title()}.")
                return {"status": "error", "message": "No songs found in the chart."}

            self.logger.info(f"Successfully fetched {len(songs_data.songs)} songs from {chart_type}")

            # Get current user's Spotify ID
            try:
                user = self.spotify_maker.sp.current_user()
                user_id = user['id']
                self.logger.info(f"Authenticated as Spotify user: {user['display_name']}")
            except SpotifyException as e:
                self.logger.error(f"Failed to authenticate Spotify user: {str(e)}")
                return {"status": "error", "message": "Failed to authenticate Spotify user."}

            # Create a Spotify playlist
            playlist_name = f"{chart_type.replace('_', ' ').title()} Playlist"
            playlist_description = f"Automatically generated {chart_type.replace('_', ' ').title()} playlist."
            try:
                playlist_id = self.spotify_maker.create_playlist(user_id, playlist_name, playlist_description)
                self.logger.info(f"Created playlist '{playlist_name}' with ID {playlist_id}")
            except SpotifyException as e:
                self.logger.error(f"Failed to create playlist: {str(e)}")
                return {"status": "error", "message": "Failed to create Spotify playlist."}

            # Search and collect Spotify URIs for the songs
            track_uris = []
            for song in songs_data.songs:
                try:
                    uri = self.spotify_maker.search_song(artist=song.artist, track=song.title)
                    if uri:
                        track_uris.append(uri)
                    else:
                        self.logger.warning(f"Could not find '{song.title}' by {song.artist} on Spotify")
                except Exception as e:
                    self.logger.error(f"Error searching for '{song.title}' by {song.artist}: {str(e)}")

            # Add tracks to the playlist
            if track_uris:
                try:
                    self.spotify_maker.add_tracks_to_playlist(playlist_id, track_uris)
                    self.logger.info(f"Successfully added {len(track_uris)} songs to the Spotify playlist.")
                    return {"status": "success", "message": f"Created playlist with {len(track_uris)} songs."}
                except SpotifyException as e:
                    self.logger.error(f"Failed to add tracks to playlist: {str(e)}")
                    return {"status": "error", "message": "Failed to add tracks to Spotify playlist."}
            else:
                self.logger.error("No songs were added to the playlist. Please check the song search functionality.")
                return {"status": "error", "message": "No songs were found on Spotify to add to the playlist."}

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            return {"status": "error", "message": "An unexpected error occurred while creating the playlist."}