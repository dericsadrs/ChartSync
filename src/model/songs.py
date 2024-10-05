from typing import List
import json
from model.song import Song

class Songs:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def to_json(self) -> str:
        return json.dumps([song.to_dict() for song in self.songs], indent=4)