class ChartTags:
    def __init__(self, chart_item: str, title: str, artist: str):
        """
        Initialize the ChartTags class with chart item, title, and artist.

        Args:
            chart_item (str): The item being charted.
            title (str): The title of the chart item.
            artist (str): The artist associated with the chart item.
        """
        self.chart_item = chart_item
        self.title = title
        self.artist = artist

    def to_dict(self):
        """
        Convert the ChartTags instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the chart item, title, and artist.
        """
        return {
            "chart_item": self.chart_item,
            "title": self.title,
            "artist": self.artist
        }
