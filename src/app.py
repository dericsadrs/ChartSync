# app.py or any script where you want to use Config
# from config import Config

# # Example Usage
from services.billboard_scraper import BillboardScraper
from services.spotify_playlist_maker import SpotifyPlaylistMaker


# if __name__ == "__main__":
#     # Toggle headless mode by passing False to see the browser window
#     scraper = BillboardScraper(headless=False)  # Change to True for headless mode

#     # Get Hot 100 for a specific date (e.g., January 1, 2020)
#     # hot_100_2020 = scraper.get_hot_100_by_date("2020-01-01")
#     # scraper.display_songs(hot_100_2020)

#     # Get Hot 100 for today
#     # hot_100_today = scraper.get_latest_hot_100()
#     # print("\nHot 100 for today:")
#     # for song in hot_100_today:
#     #     print(f"{song['title']} by {song['artist']}")

#     # # Get the Hot 100 in JSON format for playlist creation
#     # hot_100_json = scraper.get_hot_100_json(hot_100_today)
#     # print("JSON Response:", hot_100_json)
    
#     # Create a new Spotify playlist
#     spotify_maker = SpotifyPlaylistMaker()  # Initialize with your own credentials
#     #spotify_maker.authenticate()  # Authenticate with Spotify
#     print(spotify_maker.search_song(artist='Kendrick Lamar', track='Not Like Us'))
    
    # Setup logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize the Billboard Scraper
    billboard_scraper = BillboardScraper(headless=True)

    # Scrape the latest Billboard Hot 100
    logging.info("Scraping the Billboard Hot 100 chart...")
    hot_100_songs = billboard_scraper.get_latest_hot_100()

    # Initialize Spotify Playlist Maker
    spotify_maker = SpotifyPlaylistMaker()
    
    # Get current user's Spotify ID
    user = spotify_maker.sp.current_user()
    user_id = user['id']
    logging.info(f"Authenticated as Spotify user: {user['display_name']}")

    # Create a Spotify playlist for the Billboard Hot 100
    playlist_name = "Billboard Hot 100 Playlist"
    playlist_description = "Automatically generated Billboard Hot 100 playlist."
    playlist_id = spotify_maker.create_playlist(user_id, playlist_name, playlist_description)

    # Search and collect Spotify URIs for the Billboard Hot 100 songs
    track_uris = []
    for song in hot_100_songs:
        uri = spotify_maker.search_song(artist=song['artist'], track=song['title'])
        if uri:
            track_uris.append(uri)

    # Add tracks to the playlist
    if track_uris:
        spotify_maker.add_tracks_to_playlist(playlist_id, track_uris)
        logging.info(f"Successfully added {len(track_uris)} songs to the Spotify playlist.")
    else:
        logging.error("No songs were added to the playlist. Please check the song search functionality.")

if __name__ == "__main__":
    main()