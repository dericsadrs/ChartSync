from services.spotify_operations.spotify_auth import SpotifyAuth
import logging
import base64
from typing import Optional

class SpotifyPlaylistMaker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[SpotifyPlaylistMaker]: %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.auth = SpotifyAuth()
        self.sp = self.auth.get_spotify_client()

    def create_playlist(
        self, 
        user_id: str, 
        playlist_name: str, 
        description: str,
        public: bool = True,
        cover_image_path: Optional[str] = None
    ) -> str:
        """
        Create a Spotify playlist with customization options.
        
        Args:
            user_id: Spotify user ID
            playlist_name: Name of the playlist
            description: Playlist description
            public: Whether the playlist should be public (default True)
            cover_image_path: Path to JPEG image file for playlist cover (optional)
            
        Returns:
            str: Playlist ID
        """
        try:
            self.auth.refresh_token_if_expired()
            
            # Create the playlist
            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=public,
                description=description
            )
            
            playlist_id = playlist['id']
            self.logger.info(f"Created playlist '{playlist_name}' with ID {playlist_id}")

            # Upload cover image if provided
            if cover_image_path:
                self._upload_playlist_cover(playlist_id, cover_image_path)
                
            return playlist_id
            
        except Exception as e:
            self.logger.error(f"Failed to create playlist '{playlist_name}': {str(e)}")
            raise

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list):
        """
        Add a list of tracks Spotify URIs to the playlist.
        """
        try:
            self.auth.refresh_token_if_expired()
            self.sp.playlist_add_items(playlist_id, track_uris)
            self.logger.info(f"Added {len(track_uris)} tracks to the playlist with ID {playlist_id}.")
        except Exception as e:
            self.logger.error(f"Failed to add tracks to playlist {playlist_id}: {str(e)}")
            raise

    def search_song(self, artist: str, track: str) -> str:
        """
        Search Spotify for a track by its artist and title.
        Returns the Spotify URI for the first match found.
        """
        try:
            self.auth.refresh_token_if_expired()
            query = f"artist:{artist} track:{track}"
            result = self.sp.search(q=query, type='track', limit=1)
            if result['tracks']['items']:
                self.logger.info(f"Found match for '{track}' by {artist}")
                return result['tracks']['items'][0]['uri']
            self.logger.warning(f"No match found for {artist} - {track}")
            return None
        except Exception as e:
            self.logger.error(f"Error searching for track '{track}' by artist '{artist}': {str(e)}")
            raise

    def _upload_playlist_cover(self, playlist_id: str, image_path: str) -> None:
        """
        Upload a cover image for a playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            image_path: Path to JPEG image file
        """
        try:
            # Read and encode image file
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                
            self.sp.playlist_upload_cover_image(playlist_id, encoded_image)
            self.logger.info(f"Successfully uploaded cover image for playlist {playlist_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to upload cover image for playlist {playlist_id}: {str(e)}")
            # Don't raise the exception - playlist creation should succeed even if cover upload fails

    def update_playlist_details(
        self,
        playlist_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[bool] = None,
        cover_image_path: Optional[str] = None
    ) -> None:
        """
        Update an existing playlist's details.
        
        Args:
            playlist_id: Spotify playlist ID
            name: New playlist name (optional)
            description: New playlist description (optional)
            public: New public/private status (optional)
            cover_image_path: New cover image path (optional)
        """
        try:
            self.auth.refresh_token_if_expired()
            
            # Prepare update details
            update_dict = {}
            if name is not None:
                update_dict['name'] = name
            if description is not None:
                update_dict['description'] = description
            if public is not None:
                update_dict['public'] = public
                
            # Update playlist details if any changes
            if update_dict:
                self.sp.playlist_change_details(playlist_id, **update_dict)
                self.logger.info(f"Updated playlist details for {playlist_id}")
                
            # Update cover image if provided
            if cover_image_path:
                self._upload_playlist_cover(playlist_id, cover_image_path)
                
        except Exception as e:
            self.logger.error(f"Failed to update playlist {playlist_id}: {str(e)}")
            raise