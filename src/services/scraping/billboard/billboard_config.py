from model.chart_tags import ChartTags

class BillboardConfig:
    # Tag configuration for Billboard TikTok Top Songs
    BILLBOARD_TIKTOK_TOP_SONGS_TAGS = ChartTags(
        chart_item="div.o-chart-results-list-row-container",
        title="h3.c-title",
        artist="span.c-label.a-font-primary-s"
    )

    # Tag configuration for Billboard Top Songs
    BILLBOARD_TOP_SONGS_TAGS = ChartTags(
        chart_item="ul.o-chart-results-list-row",
        title="h3.c-title",
        artist="span.c-label.a-no-trucate.a-font-primary-s"
    )

    # URLs for the charts
    URLs = {
        "billboard_tiktok": "https://www.billboard.com/charts/tiktok-billboard-top-50/",
        "billboard": "https://www.billboard.com/charts/hot-100"
    }

    @classmethod
    def get_tags(cls, chart_type: str) -> ChartTags:
        """Get tags based on the chart type."""
        if chart_type == "billboard_tiktok":
            return cls.BILLBOARD_TIKTOK_TOP_SONGS_TAGS
        elif chart_type == "billboard":
            return cls.BILLBOARD_TOP_SONGS_TAGS
        else:
            raise ValueError("Invalid chart type specified.")

    @classmethod
    def get_url(cls, chart_type: str):
        """Get the URL based on the chart type."""
        if chart_type in cls.URLs:
            return cls.URLs[chart_type]
        else:
            raise ValueError("Invalid chart type specified.")
