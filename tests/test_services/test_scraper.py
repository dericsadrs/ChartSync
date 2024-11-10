import pytest
from unittest.mock import Mock, patch, MagicMock
from services.scraper import Scraper
from model.songs import Songs
from model.song import Song

class TestScraper:
    """Test suite for Scraper service"""
    
    @pytest.fixture
    def mock_playwright(self):
        with patch('playwright.sync_api.sync_playwright') as mock:
            yield mock
            
    @pytest.fixture
    def scraper(self):
        return Scraper(headless=True, chart_type="billboard_hot_100")
    
    def test_scraper_initialization(self):
        """Test scraper initialization with default values"""
        scraper = Scraper()
        assert scraper.headless is True
        assert scraper.chart_type == "billboard_hot_100"
        assert scraper.config is not None
        
    def test_scraper_invalid_chart_type(self):
        """Test scraper initialization with invalid chart type"""
        with pytest.raises(ValueError) as exc_info:
            Scraper(chart_type="invalid_chart")
        assert "Chart type 'invalid_chart' is not supported" in str(exc_info.value)
        
    def test_get_latest_chart(self, scraper, mock_playwright):
        """Test fetching latest chart data"""
        # Mock the browser and page objects
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        
        # Mock the elements and their text content
        mock_title_element = MagicMock()
        mock_title_element.inner_text.return_value = "Test Song"
        mock_artist_element = MagicMock()
        mock_artist_element.inner_text.return_value = "Test Artist"
        
        mock_item = MagicMock()
        mock_item.query_selector.side_effect = lambda selector: {
            '.title': mock_title_element,
            '.artist': mock_artist_element
        }.get(selector)
        
        mock_page.query_selector_all.return_value = [mock_item]
        
        # Execute the method
        result = scraper.get_latest_chart()
        
        # Verify the results
        assert isinstance(result, Songs)
        assert len(result.songs) == 1
        assert result.songs[0].title == "Test Song"
        assert result.songs[0].artist == "Test Artist"
        
    def test_get_latest_chart_empty(self, scraper, mock_playwright):
        """Test behavior when no songs are found"""
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        
        mock_page.query_selector_all.return_value = []
        
        result = scraper.get_latest_chart()
        assert isinstance(result, Songs)
        assert len(result.songs) == 0
        
    def test_display_songs(self, scraper, capsys):
        """Test displaying songs in human-readable format"""
        songs = Songs([
            Song("Test Song 1", "Test Artist 1"),
            Song("Test Song 2", "Test Artist 2")
        ])
        
        scraper.display_songs(songs)
        captured = capsys.readouterr()
        
        assert "1. Test Song 1 by Test Artist 1" in captured.out
        assert "2. Test Song 2 by Test Artist 2" in captured.out