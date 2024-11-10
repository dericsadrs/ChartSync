import pytest
from unittest.mock import Mock, MagicMock, patch
from model.song import Song
from model.songs import Songs

@pytest.fixture
def mock_spotify_client():
    """Fixture for mocked Spotify client"""
    with patch('spotipy.Spotify') as mock:
        mock.current_user.return_value = {'id': 'test_user', 'display_name': 'Test User'}
        yield mock

@pytest.fixture
def mock_playwright():
    """Fixture for mocked Playwright"""
    with patch('playwright.sync_api.sync_playwright') as mock:
        yield mock

@pytest.fixture
def mock_openai_client():
    """Fixture for mocked OpenAI client"""
    with patch('openai.OpenAI') as mock:
        mock.chat.completions.create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content='[{"title": "Test Song", "artist": "Test Artist"}]'
                    )
                )
            ]
        )
        yield mock

@pytest.fixture
def sample_songs():
    """Fixture for sample song data"""
    return Songs([
        Song("Test Song 1", "Test Artist 1"),
        Song("Test Song 2", "Test Artist 2")
    ])

@pytest.fixture
def mock_config():
    """Fixture for mocked configuration"""
    with patch('config.Config') as mock:
        mock.return_value.get_client_id.return_value = 'test_client_id'
        mock.return_value.get_client_secret.return_value = 'test_client_secret'
        mock.return_value.get_redirect_uri.return_value = 'http://localhost:8000'
        mock.return_value.get_gpt_key.return_value = 'test_gpt_key'
        yield mock