import pytest
from unittest.mock import Mock, patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_auth import SpotifyAuth


class TestSpotifyAuth:
    """Test suite for SpotifyAuth service"""
    
    @pytest.fixture
    def mock_spotipy(self):
        with patch('spotipy.Spotify') as mock:
            yield mock
            
    @pytest.fixture
    def spotify_auth(self, mock_spotipy):
        with patch('config.Config') as mock_config:
            mock_config.return_value.get_client_id.return_value = 'test_client_id'
            mock_config.return_value.get_client_secret.return_value = 'test_secret'
            mock_config.return_value.get_redirect_uri.return_value = 'http://localhost:8000'
            return SpotifyAuth()
    
    def test_authentication_success(self, spotify_auth):
        """Test successful Spotify authentication"""
        assert spotify_auth.sp is not None
        
    def test_refresh_token(self, spotify_auth):
        """Test token refresh functionality"""
        spotify_auth.sp.auth_manager.is_token_expired.return_value = True
        spotify_auth.refresh_token_if_expired()
        spotify_auth.sp.auth_manager.refresh_access_token.assert_called_once()
        
    def test_refresh_token_not_needed(self, spotify_auth):
        """Test when token refresh is not needed"""
        spotify_auth.sp.auth_manager.is_token_expired.return_value = False
        spotify_auth.refresh_token_if_expired()
        spotify_auth.sp.auth_manager.refresh_access_token.assert_not_called()
        
    def test_get_spotify_client_reinit(self, spotify_auth):
        """Test getting Spotify client when not initialized"""
        spotify_auth.sp = None
        client = spotify_auth.get_spotify_client()
        assert client is not None
