import logging
from model.songs import Songs
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from spotipy.exceptions import SpotifyException

class PlaylistManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[PlaylistManager]: %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.spotify_maker = SpotifyPlaylistMaker()

    def create_playlist(self, chart_type: str = None, songs_data: Songs = None, 
                   playlist_name: str = None, public: bool = True, 
                   cover_image_path: str = None):
        """
        Create a Spotify playlist based on either a chart type or provided Songs object.

        :param chart_type: The type of chart to scrape (e.g., "billboard_hot_100"), optional
        :param songs_data: Songs object containing the songs to add, optional
        :param playlist_name: Custom name for the playlist, optional
        :return: dict with status and message
        """
        try:
            self.logger.info("Starting playlist creation")
            
            # Get songs either from scraper or provided Songs object
            if songs_data is None and chart_type:
                # Initialize the scraper and get chart data
                scraper = Scraper(headless=True, chart_type=chart_type)
                self.logger.info(f"Initialized scraper for {chart_type}")
                songs_data = scraper.get_latest_chart()
                # Use chart type for playlist name if not provided
                playlist_name = playlist_name or f"{chart_type.replace('_', ' ').title()} Playlist"
            elif songs_data is not None:
                # Use provided Songs object
                playlist_name = playlist_name or "Custom Generated Playlist"
            else:
                raise ValueError("Either chart_type or songs_data must be provided")

            if not songs_data.songs:
                self.logger.error("No songs found.")
                return {"status": "error", "message": "No songs found."}

            self.logger.info(f"Processing {len(songs_data.songs)} songs")

            # Get current user's Spotify ID
            try:
                user = self.spotify_maker.sp.current_user()
                user_id = user['id']
                self.logger.info(f"Authenticated as Spotify user: {user['display_name']}")
            except SpotifyException as e:
                self.logger.error(f"Failed to authenticate Spotify user: {str(e)}")
                return {"status": "error", "message": "Failed to authenticate Spotify user."}

            # Create a Spotify playlist
            playlist_description = f"Automatically generated playlist: {playlist_name}"
            try:
                playlist_id = self.spotify_maker.create_playlist(
                user_id=user_id,
                playlist_name=playlist_name,
                description=playlist_description,
                public=public,
                cover_image_path=cover_image_path
            )
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
    
    def get_collaborator_insights(self, playlist_id: str):
        """
        Analyze collaborator contributions for a playlist.
        """
        try:
            playlist_details = self.spotify_maker.get_playlist_details(playlist_id)
            collaborator_stats = {}

            for song in playlist_details['songs']:
                contributor = song['added_by']
                if contributor not in collaborator_stats:
                    collaborator_stats[contributor] = {"songs_added": 0}
                collaborator_stats[contributor]["songs_added"] += 1

            return {
                "playlist_name": playlist_details["name"],
                "description": playlist_details["description"],
                "collaborator_stats": collaborator_stats
            }
        except Exception as e:
            self.logger.error(f"Error analyzing playlist: {str(e)}")
            return {"error": "Failed to analyze playlist"}
    
    def create_mood_or_activity_playlist(self, mood_or_activity: str, playlist_name: str = None, public: bool = True):
        """
        Create a playlist for a specific mood or activity.
        Args:
            mood_or_activity (str): Mood or activity (e.g., "Workout", "Relaxation").
            playlist_name (str): Optional custom playlist name.
            public (bool): Whether the playlist is public.
        Returns:
            dict: Status and message of the operation.
        """
        try:
            self.logger.info(f"Creating playlist for mood/activity: {mood_or_activity}")
            
            # Fetch songs from GPT
            gpt_operations = GPTOperations()
            songs = gpt_operations.fetch_songs_by_mood_or_activity(mood_or_activity)
            
            if not songs.songs:
                return {"status": "error", "message": "No songs generated for the selected mood or activity."}

            # Generate playlist name if not provided
            playlist_name = playlist_name or f"{mood_or_activity.title()} Playlist"

            # Create the playlist
            user = self.spotify_maker.sp.current_user()
            playlist_id = self.spotify_maker.create_playlist(
                user_id=user['id'],
                playlist_name=playlist_name,
                description=f"A playlist tailored for {mood_or_activity}.",
                public=public
            )
            
            # Add songs to the playlist
            track_uris = []
            for song in songs.songs:
                uri = self.spotify_maker.search_song(artist=song.artist, track=song.title)
                if uri:
                    track_uris.append(uri)

            if track_uris:
                self.spotify_maker.add_tracks_to_playlist(playlist_id, track_uris)
                self.logger.info(f"Successfully created {playlist_name} with {len(track_uris)} songs.")
                return {"status": "success", "message": f"Playlist '{playlist_name}' created with {len(track_uris)} songs."}
            else:
                return {"status": "error", "message": "No tracks found on Spotify for the generated songs."}
        except Exception as e:
            self.logger.error(f"Failed to create mood/activity playlist: {str(e)}")
            return {"status": "error", "message": "An error occurred while creating the playlist."}
