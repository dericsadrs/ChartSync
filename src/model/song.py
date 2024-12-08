class Song:
    def __init__(self, title: str, artist: str):
        """
        Initialize the Song class with a title and artist.

        Args:
            title (str): The title of the song.
            artist (str): The artist of the song.
        """
        self.title = title
        self.artist = artist

    def to_dict(self):
        """
        Convert the Song instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the title and artist of the song.
        """
        return {
            "title": self.title,
            "artist": self.artist
        }