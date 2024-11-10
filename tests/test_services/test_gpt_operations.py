import pytest
from unittest.mock import Mock, patch, MagicMock
from services.gpt_operations import GPTOperations

class TestGPTOperations:
    """Test suite for GPTOperations service"""
    
    @pytest.fixture
    def mock_openai(self):
        with patch('openai.OpenAI') as mock:
            yield mock
            
    @pytest.fixture
    def gpt_operations(self, mock_openai):
        return GPTOperations()
        
    def test_fetch_songs_success(self, gpt_operations, mock_openai):
        """Test successful song fetching from GPT"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''[
            {"title": "Test Song 1", "artist": "Test Artist 1"},
            {"title": "Test Song 2", "artist": "Test Artist 2"}
        ]'''
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        result = gpt_operations.fetch_songs("happy songs")
        assert result["status"] == "success"
        assert len(result["data"]) == 2
        assert result["data"][0]["title"] == "Test Song 1"
        
    def test_fetch_songs_invalid_response(self, gpt_operations, mock_openai):
        """Test handling of invalid GPT response"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Invalid JSON response"
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        result = gpt_operations.fetch_songs("happy songs")
        assert result["status"] == "error"
        assert isinstance(result["message"], str)
        
    def test_fetch_songs_api_error(self, gpt_operations, mock_openai):
        """Test handling of API errors"""
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")
        
        result = gpt_operations.fetch_songs("happy songs")
        assert result["status"] == "error"
        assert "API Error" in result["message"]