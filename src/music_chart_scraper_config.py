# Consolidated configuration dictionary for various music charts
MUSIC_CHART_SCRAPER_CONFIG = {
    "billboard_tiktok_top_50": {
        "tags": {
            "chart_item": "div.o-chart-results-list-row-container",  # Main container for chart rows
            "title": "h3.c-title",                                   # Song title tag
            "artist": "span.c-label.a-font-primary-s"                # Artist name tag
        },
        "url": "https://www.billboard.com/charts/tiktok-billboard-top-50/"
    },
    "billboard_hot_100": {
        "tags": {
            "chart_item": "ul.o-chart-results-list-row",              # Main container for chart rows
            "title": "h3.c-title",                                    # Song title tag
            "artist": "span.c-label.a-no-trucate.a-font-primary-s"    # Artist name tag
        },
        "url": "https://www.billboard.com/charts/hot-100"
    },
     "billboard_decade_end_hot_100": {
        "tags": {
            "chart_item": "div.o-chart-results-list-row-container",   # Main container for chart rows
            "title": "h3.c-title",                                    # Song title tag
            "artist": "span.c-label.a-font-primary-s"                 # Artist name tag
        },
        "url": "https://www.billboard.com/charts/decade-end/hot-100"
    } # You can add more chart configurations here from other sources
}