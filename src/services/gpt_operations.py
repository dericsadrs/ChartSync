import openai
import json
import logging
from config import Config

class GPTOperations:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.get_gpt_key()
        self.model = self.config.get_gpt_model()  # Assuming you add this to your Config class
        openai.api_key = self.api_key

    def fetch_songs(self, prompt: str) -> dict:
        """
        Fetch songs based on the user's prompt using the specified GPT model.
        Returns a JSON response with the artist and song.
        """
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
            )
            songs = self._parse_response(response.choices[0].text)
            return {"status": "success", "data": songs}
        except Exception as e:
            logging.error(f"Error fetching songs: {e}")
            return {"status": "error", "message": str(e)}

    def _parse_response(self, response_text: str) -> list:
        """
        Parse the GPT response text to extract song information.
        """
        # This is a simple example. You might need to adjust the parsing logic based on the response format.
        lines = response_text.strip().split('\n')
        songs = []
        for line in lines:
            if '-' in line:
                artist, song = line.split('-', 1)
                songs.append({"artist": artist.strip(), "song": song.strip()})
        return songs

# # Example usage
# if __name__ == "__main__":
#     gpt_operations = GPTOperations()
#     prompt = "Give me Ed-Sheeran's top songs"
#     result = gpt_operations.fetch_songs(prompt)
#     print(json.dumps(result, indent=2))