import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
from model.songs import Songs
import logging
from typing import List, Dict, Optional

class SpotifyPlaylistMaker:
    def __init__(self):
        """Initialize SpotifyPlaylistMaker with logging configuration."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.config = Config()
        self.authenticate()
    
    def authenticate(self):
        """Authenticate account to Spotify using OAuth 2.0."""
        try:
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.config.get_client_id(), 
                    client_secret=self.config.get_client_secret(), 
                    redirect_uri=self.config.get_redirect_uri(),
                    scope='playlist-modify-public'
                )
            )
            self.logger.info("[SpotifyPlaylistMaker] Successfully authenticated with Spotify")
        except Exception as e:
            self.logger.error(f"[SpotifyPlaylistMaker] Authentication failed: {str(e)}")
            raise
    
    def create_playlist(self, user_id: str, playlist_name: str, description: str) -> str:
        """Create a Spotify playlist and return its ID."""
        try:
            playlist = self.sp.user_playlist_create(
                user=user_id, 
                name=playlist_name, 
                public=True, 
                description=description
            )
            self.logger.info(f"[SpotifyPlaylistMaker] Created playlist '{playlist_name}' with ID {playlist['id']}")
            return playlist['id']
        except Exception as e:
            self.logger.error(f"[SpotifyPlaylistMaker] Failed to create playlist: {str(e)}")
            raise

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list):
        """Add tracks to the playlist in batches."""
        try:
            # Spotify has a limit of 100 tracks per request
            batch_size = 100
            for i in range(0, len(track_uris), batch_size):
                batch = track_uris[i:i + batch_size]
                self.sp.playlist_add_items(playlist_id, batch)
                self.logger.info(
                    f"[SpotifyPlaylistMaker] Added batch of {len(batch)} tracks to playlist {playlist_id}"
                )
        except Exception as e:
            self.logger.error(f"[SpotifyPlaylistMaker] Failed to add tracks to playlist {playlist_id}: {str(e)}")
            raise

    def search_song(self, artist: str, track: str) -> Optional[str]:
        """
        Search Spotify for a track by its artist and title.
        Returns the Spotify URI for the first match found.
        """
        try:
            query = f"artist:{artist} track:{track}"
            result = self.sp.search(q=query, type='track', limit=1)
            
            if result['tracks']['items']:
                track_uri = result['tracks']['items'][0]['uri']
                self.logger.info(
                    f"[SpotifyPlaylistMaker] Found match for '{track}' by {artist}: {track_uri}"
                )
                return track_uri
                
            self.logger.warning(f"[SpotifyPlaylistMaker] No match found for '{track}' by {artist}")
            return None
            
        except Exception as e:
            self.logger.error(
                f"[SpotifyPlaylistMaker] Error searching for track '{track}' by {artist}: {str(e)}"
            )
            return None

    def create_playlist_from_songs(self, songs: Songs, playlist_name: str, description: str) -> Dict:
        """
        Create a playlist from a Songs object and return playlist information.
        
        Args:
            songs (Songs): Songs object containing the tracks to add
            playlist_name (str): Name for the new playlist
            description (str): Description for the new playlist
            
        Returns:
            Dict: Playlist information including ID, track count, and success status
        """
        try:
            # Get current user's ID
            user = self.sp.current_user()
            user_id = user['id']
            
            # Create the playlist
            playlist_id = self.create_playlist(user_id, playlist_name, description)
            
            # Search and collect track URIs
            track_uris = []
            failed_tracks = []
            
            for song in songs.songs:
                uri = self.search_song(artist=song.artist, track=song.title)
                if uri:
                    track_uris.append(uri)
                else:
                    failed_tracks.append({"title": song.title, "artist": song.artist})
            
            # Add tracks to playlist if any were found
            if track_uris:
                self.add_tracks_to_playlist(playlist_id, track_uris)
                
            return {
                "playlist_id": playlist_id,
                "tracks_added": len(track_uris),
                "tracks_failed": failed_tracks,
                "success_rate": len(track_uris) / len(songs.songs) if songs.songs else 0
            }
            
        except Exception as e:
            self.logger.error(f"[SpotifyPlaylistMaker] Failed to create playlist from songs: {str(e)}")
            raise