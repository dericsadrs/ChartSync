import pytest
from unittest.mock import Mock, patch, MagicMock
from services.spotify_operations.user_info_viewer import UserInfoViewer


class TestUserInfoViewer:
    """Test suite for UserInfoViewer service"""
    
    @pytest.fixture
    def mock_spotify_auth(self):
        with patch('services.spotify_operations.spotify_auth.SpotifyAuth') as mock:
            mock.return_value.get_spotify_client.return_value = MagicMock()
            yield mock
            
    @pytest.fixture
    def user_info_viewer(self, mock_spotify_auth):
        return UserInfoViewer()
        
    def test_get_user_info_success(self, user_info_viewer):
        """Test successful user info retrieval"""
        mock_user_info = {
            'id': 'test_user',
            'display_name': 'Test User',
            'email': 'test@example.com'
        }
        user_info_viewer.sp.current_user.return_value = mock_user_info
        
        result = user_info_viewer.get_user_info()
        assert result == mock_user_info
        
    def test_get_user_info_error(self, user_info_viewer):
        """Test handling of user info retrieval error"""
        user_info_viewer.sp.current_user.side_effect = Exception("API Error")
        
        result = user_info_viewer.get_user_info()
        assert result is None
        
    def test_display_user_info(self, user_info_viewer, capsys):
        """Test displaying user info"""
        mock_user_info = {'display_name': 'Test User'}
        user_info_viewer.display_user_info(mock_user_info)
        
        captured = capsys.readouterr()
        assert 'Test User' in captured.out
