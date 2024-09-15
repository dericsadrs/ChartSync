import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)  # Adjust the logging level as needed

class Config:
    def __init__(self, env_path: Optional[str] = None) -> None:
        """
        Initializes the Config class and loads environment variables from the specified .env file.
        
        :param env_path: Optional path to the .env file. Defaults to 'src/.env'.
        """
        # Default path to your .env file inside the src directory
        self.env_path = env_path or 'src/.env'
        self._load_env_variables()

    def _load_env_variables(self) -> None:
        """Load environment variables from a .env file."""
        load_dotenv()

        # Retrieve variables
        self.SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
        self.SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
        self.GPT_KEY = os.getenv('GPT_KEY')
        # Log if the environment variables are loaded correctly
        self._log_variables()

    def _log_variables(self) -> None:
        """Log the presence (not the actual values) of the environment variables."""
        if self.SPOTIPY_CLIENT_ID:
            logging.info("SPOTIPY_CLIENT_ID is set.")
        else:
            logging.warning("SPOTIPY_CLIENT_ID is missing.")

        if self.SPOTIPY_CLIENT_SECRET:
            logging.info("SPOTIPY_CLIENT_SECRET is set.")
        else:
            logging.warning("SPOTIPY_CLIENT_SECRET is missing.")

        if self.SPOTIPY_REDIRECT_URI:
            logging.info("SPOTIPY_REDIRECT_URI is set.")
        else:
            logging.warning("SPOTIPY_REDIRECT_URI is missing.")
        
        if self.GPT_KEY:
            logging.info("GPT_KEY is set.")
        else:
            logging.warning("GPT_KEY is missing.")

    def get_client_id(self) -> str:
        """Returns the Spotify Client ID."""
        return self.SPOTIPY_CLIENT_ID

    def get_client_secret(self) -> str:
        """Returns the Spotify Client Secret."""
        return self.SPOTIPY_CLIENT_SECRET

    def get_redirect_uri(self) -> str:
        """Returns the Spotify Redirect URI."""
        return self.SPOTIPY_REDIRECT_URI
    
    def get_gpt_key(self) -> str:
        """Returns the Spotify Redirect URI."""
        return self.GPT_KEY