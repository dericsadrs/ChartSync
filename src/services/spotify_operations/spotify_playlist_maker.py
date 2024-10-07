import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
import logging

class SpotifyPlaylistMaker():

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.config = Config()
        self.authenticate()
    
    def authenticate(self):
        """
        Authenticate account to Spotify using 2.0 authentication
        """
        self.sp = spotipy.Spotify(
                                    auth_manager=SpotifyOAuth(
                                    client_id=self.config.get_client_id(), 
                                    client_secret=self.config.get_client_secret(), 
                                    redirect_uri=self.config.get_redirect_uri(),
                                    scope='playlist-modify-public'))
    
    def create_playlist(self, user_id: str, playlist_name: str, description: str) -> str:
        """
        Create a Spotify playlist and return its ID.
        """
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=description)
        logging.info(f"Created playlist '{playlist_name}' with ID {playlist['id']}")
        return playlist['id']

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list):
        """
        Add a list of tracks Spotify Url's to the playlist.
        """
        try:
            self.sp.playlist_add_items(playlist_id, track_uris)
            logging.info(f"Added {len(track_uris)} tracks to the playlist with ID {playlist_id}.")
        except Exception as e:
            logging.error(f"Failed to add tracks to playlist {playlist_id}: {e}")

    def search_song(self, artist: str, track: str) -> str:
        """
        Search Spotify for a track by its artist and title.
        Returns the Spotify URI for the first match found.
        """
        try:
            query = f"artist:{artist} track:{track}"
            result = self.sp.search(q=query, type='track', limit=1)
            if result['tracks']['items']:
                return result['tracks']['items'][0]['uri']
            logging.info(f"No match found for {artist} - {track}")
            return None
        except Exception as e:
            logging.error(f"Error searching for track '{track}' by artist '{artist}': {e}")
            return None
