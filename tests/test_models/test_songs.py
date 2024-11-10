import pytest
import json
from model.song import Song
from model.songs import Songs

class TestSongs:
    """Test suite for Songs collection model"""
    
    @pytest.fixture
    def sample_songs(self):
        """Fixture providing sample song list"""
        return [
            Song("Title 1", "Artist 1"),
            Song("Title 2", "Artist 2"),
            Song("Title 3", "Artist 3")
        ]
    
    def test_songs_initialization(self, sample_songs):
        """Test basic Songs collection initialization"""
        songs = Songs(sample_songs)
        assert len(songs.songs) == 3
        assert all(isinstance(song, Song) for song in songs.songs)
        
    def test_songs_initialization_empty(self):
        """Test Songs initialization with empty list"""
        songs = Songs([])
        assert len(songs.songs) == 0
        assert isinstance(songs.songs, list)
        
    def test_songs_to_json(self, sample_songs):
        """Test conversion to JSON"""
        songs = Songs(sample_songs)
        json_output = songs.to_json()
        
        # Verify it's valid JSON
        parsed_json = json.loads(json_output)
        assert len(parsed_json) == 3
        assert parsed_json[0]["title"] == "Title 1"
        assert parsed_json[0]["artist"] == "Artist 1"
        
    def test_songs_iteration(self, sample_songs):
        """Test iteration over Songs collection"""
        songs = Songs(sample_songs)
        titles = []
        for song in songs.songs:
            titles.append(song.title)
        assert titles == ["Title 1", "Title 2", "Title 3"]
        
    def test_songs_with_duplicate_entries(self):
        """Test Songs collection with duplicate entries"""
        duplicate_song = Song("Same Title", "Same Artist")
        songs = Songs([duplicate_song, duplicate_song])
        assert len(songs.songs) == 2
        
    def test_songs_json_formatting(self, sample_songs):
        """Test JSON output formatting"""
        songs = Songs(sample_songs)
        json_output = songs.to_json()
        
        # Verify JSON is properly indented
        assert json_output.count('\n') > 0  # Should have line breaks
        assert '    ' in json_output  # Should have indentation
