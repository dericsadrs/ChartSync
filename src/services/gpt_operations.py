from openai import OpenAI
import json
import logging
from config import Config
from model.song import Song
from model.songs import Songs

class GPTOperations:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - [GPTOperations] - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        self.config = Config()
        self.client = OpenAI(api_key=self.config.get_gpt_key())
        self.model = self.config.get_gpt_model()

    def fetch_songs(self, prompt: str) -> Songs:
        """
        Fetch songs based on the user's prompt using the OpenAI API.
        Returns a Songs object containing Song objects with title and artist information.
        """
        try:
            self.logger.info(f"Fetching songs for prompt: {prompt}")
            
            formatted_prompt = f"""
            Based on this request: "{prompt}"
            Return a list of relevant songs in JSON format:
            [{{"title": "Song Name", "artist": "Artist Name"}}, ...]
            Provide exactly 5 songs that best match the request.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a music recommendation system. Respond only with valid JSON arrays containing song information."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            self.logger.info("Successfully received response from OpenAI")
            
            song_list = self._parse_response(response_text)
            songs_obj = Songs([Song(title=song['title'], artist=song['artist']) for song in song_list])
            self.logger.info(f"Successfully created Songs object with {len(song_list)} songs")
            
            return songs_obj
            
        except Exception as e:
            self.logger.error(f"Error fetching songs: {str(e)}")
            return Songs([])  # Return empty Songs object in case of error

    def _parse_response(self, response_text: str) -> list:
        """
        Parse the GPT response text to extract song information.
        Ensures the response is in the correct JSON format.
        """
        try:
            response_text = response_text.strip()
            if not response_text.startswith('['):
                self.logger.warning("Response text not in expected format, attempting to extract JSON array")
                start = response_text.find('[')
                end = response_text.rfind(']') + 1
                if start != -1 and end != 0:
                    response_text = response_text[start:end]
                else:
                    raise ValueError("Could not find JSON array in response")

            songs = json.loads(response_text)
            
            validated_songs = []
            for song in songs:
                if isinstance(song, dict) and 'title' in song and 'artist' in song:
                    validated_songs.append({
                        'title': song['title'],
                        'artist': song['artist']
                    })
                else:
                    self.logger.warning(f"Skipping invalid song format: {song}")
            
            return validated_songs
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Error parsing response: {str(e)}")
            return []