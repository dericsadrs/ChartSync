class Song:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist
        }