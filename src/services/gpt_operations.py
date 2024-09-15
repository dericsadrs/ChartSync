import json
import re
from services.spotify_playlist_maker import SpotifyPlaylistMaker

class GPTOperations():
    def __init__(self):
        self.spotify = SpotifyPlaylistMaker()

    def fetch_songs(self, prompt: str) -> str:
        """
        Fetch songs based on the user's prompt and return a JSON response with the artist and song.
        """
        # Extract artist name from the prompt
        artist = self.extract_artist(prompt)
        if not artist:
            return json.dumps({"error": "Artist not found in prompt"})

        # Search for top tracks of the artist
        top_tracks = self.get_top_tracks(artist)
        if not top_tracks:
            return json.dumps({"error": f"No top tracks found for {artist}"})

        # Prepare JSON response
        response = [{"artist": artist, "song": track['name']} for track in top_tracks]
        return json.dumps(response)

    def extract_artist(self, prompt: str) -> str:
        """
        Extract artist name from the prompt using regex.
        """
        match = re.search(r"(?i)(?:give me|top songs|songs|tracks|by)\s+([a-zA-Z\s-]+)", prompt)
        if match:
            return match.group(1).strip()
        return None

    def get_top_tracks(self, artist: str) -> list:
        """
        Get top tracks of the artist from Spotify.
        """
        result = self.spotify.sp.search(q=f"artist:{artist}", type='track', limit=10)
        if result['tracks']['items']:
            return result['tracks']['items']
        return []

