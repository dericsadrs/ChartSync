class ChartTags:
    def __init__(self, chart_item: str, title: str, artist: str):
        self.chart_item = chart_item
        self.title = title
        self.artist = artist

    def to_dict(self):
        """Convert the tag configuration to a dictionary."""
        return {
            "chart_item": self.chart_item,
            "title": self.title,
            "artist": self.artist
        }
