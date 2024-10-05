
from services.playlist_manager import PlaylistManager

if __name__ == "__main__":
    # manager = PlaylistManager()
    # # manager.create_billboard_playlist()
    # manager.create_tiktok_playlist()
    playlist_manager = PlaylistManager()

    # Create a playlist for the latest Billboard Hot 100
    playlist_manager.create_playlist(chart_type="billboard_hot_100")