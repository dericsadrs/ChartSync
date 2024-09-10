import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.config import Config
import logging

class SpotifyPlaylistMaker():

    def __init__(self, SpotifyOAuth, ):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.config = Config()
        
    def authenticate(self):
        try:
            logging("Authenticating.....")
            self.sp = spotipy.Spotify(client_id=self.config.get_client_id(), 
                                    client_secret=self.config.get_client_secret(), 
                                    redirect_uri=self.config.get_redirect_uri(),
                                    scope='playlist-modify-public')
            logging("Authencation complete")
        except Exception as e:
            print("Error occurred while authenticating:", e)
    
    def create_playlist(self):
        pass
    def add_tracks_to_playlist(self):
        pass
    def search_song(self):
        pass
    def display(self):
        pass    

    
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])