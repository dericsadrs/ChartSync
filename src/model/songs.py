from typing import List
import json
from model.song import Song

class Songs:
    def __init__(self, songs: List[Song]):
        """
        Initialize the Songs class with a list of Song objects.

        Args:
            songs (List[Song]): A list of Song instances.
        """
        self.songs = songs

    def to_json(self) -> str:
        """
        Convert the list of songs to a JSON string.

        Returns:
            str: A JSON string representation of the songs.
        """
        # Convert each song to a dictionary and serialize to JSON
        return json.dumps([song.to_dict() for song in self.songs], indent=4)