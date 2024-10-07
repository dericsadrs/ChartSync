import json
import re
import openai  # Assuming you're using OpenAI's GPT API
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from model.song import Song
from model.songs import Songs
from config import Config

class GPTOperations():
    def __init__(self):
        self.spotify = SpotifyPlaylistMaker()
        self.gpt_key = Config.get_gpt_key()  # Load GPT key
        openai.api_key = self.gpt_key  # Set the API key for OpenAI

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

        # Prepare Song instances and use Songs class to create JSON response
        songs_list = [Song(track['name'], artist) for track in top_tracks]
        songs = Songs(songs_list)
        return songs.to_json()  # This will return the JSON structure as required

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

    def generate_response(self, prompt: str) -> str:
        """
        Use the GPT agent to generate a response based on the prompt.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the model you want to use
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

