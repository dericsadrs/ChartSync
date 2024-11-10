import pytest
from model.song import Song

class TestSong:
    """Test suite for Song model"""
    
    def test_song_initialization(self):
        """Test basic song initialization"""
        song = Song("Test Title", "Test Artist")
        assert song.title == "Test Title"
        assert song.artist == "Test Artist"
    
    def test_song_to_dict(self):
        """Test conversion to dictionary"""
        song = Song("Test Title", "Test Artist")
        expected_dict = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        assert song.to_dict() == expected_dict
    
    def test_song_with_empty_values(self):
        """Test song creation with empty values"""
        song = Song("", "")
        assert song.title == ""
        assert song.artist == ""
        
    def test_song_with_special_characters(self):
        """Test song creation with special characters"""
        song = Song("Test & Title!", "Test @ Artist #")
        assert song.title == "Test & Title!"
        assert song.artist == "Test @ Artist #"
        
    def test_song_with_unicode_characters(self):
        """Test song creation with unicode characters"""
        song = Song("Título de Prueba", "アーティスト")
        assert song.title == "Título de Prueba"
        assert song.artist == "アーティスト"
