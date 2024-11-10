import pytest
from model.chart_tags import ChartTags

class TestChartTags:
    """Test suite for ChartTags model"""
    
    @pytest.fixture
    def sample_tags(self):
        """Fixture providing sample chart tags"""
        return ChartTags(
            chart_item=".chart-item",
            title=".title-class",
            artist=".artist-class"
        )
    
    def test_chart_tags_initialization(self):
        """Test basic ChartTags initialization"""
        tags = ChartTags(
            chart_item=".chart-item",
            title=".title-class",
            artist=".artist-class"
        )
        assert tags.chart_item == ".chart-item"
        assert tags.title == ".title-class"
        assert tags.artist == ".artist-class"
        
    def test_chart_tags_to_dict(self, sample_tags):
        """Test conversion to dictionary"""
        expected_dict = {
            "chart_item": ".chart-item",
            "title": ".title-class",
            "artist": ".artist-class"
        }
        assert sample_tags.to_dict() == expected_dict
        
    def test_chart_tags_with_complex_selectors(self):
        """Test ChartTags with complex CSS selectors"""
        tags = ChartTags(
            chart_item="div.chart-item > div.content",
            title="span.title[data-type='song']",
            artist="a.artist-link[href*='artist']"
        )
        assert tags.chart_item == "div.chart-item > div.content"
        assert tags.title == "span.title[data-type='song']"
        assert tags.artist == "a.artist-link[href*='artist']"
        
    def test_chart_tags_with_empty_values(self):
        """Test ChartTags with empty values"""
        tags = ChartTags("", "", "")
        assert tags.chart_item == ""
        assert tags.title == ""
        assert tags.artist == ""
        
    def test_chart_tags_immutability(self, sample_tags):
        """Test that ChartTags attributes can't be modified after initialization"""
        with pytest.raises(AttributeError):
            sample_tags.chart_item = "new_value"
            
    def test_chart_tags_equality(self):
        """Test equality comparison between ChartTags instances"""
        tags1 = ChartTags(".item", ".title", ".artist")
        tags2 = ChartTags(".item", ".title", ".artist")
        tags3 = ChartTags(".different", ".title", ".artist")
        
        assert tags1.to_dict() == tags2.to_dict()
        assert tags1.to_dict() != tags3.to_dict()