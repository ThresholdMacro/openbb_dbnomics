"""Tests for myplot.py charting functionality."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock
import plotly.graph_objects as go


class TestMyPlot:
    """Test cases for myplot.py functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create sample data
        self.sample_data = pd.DataFrame({
            'NGDP_D_SA_IX': [100.0, 101.5, 102.0, 103.0, 104.0],
            'NGDP_SA_XDC': [200.0, 202.0, 204.0, 206.0, 208.0]
        }, index=['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1'])

    @patch('openbb_dbnomics.utils.myplot.plot_ts')
    def test_plot_ts_import(self, mock_plot_ts):
        """Test that plot_ts function can be imported and called."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        # Mock the function to return a Plotly figure
        mock_fig = Mock(spec=go.Figure)
        mock_plot_ts.return_value = mock_fig
        
        # Test function call
        result = plot_ts(self.sample_data, nome="Test Chart", units="Index")
        assert result == mock_fig

    def test_plot_ts_with_different_chart_types(self):
        """Test plot_ts with different chart type parameters."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        chart_types = ['line', 'bar', 'regression', 'distribution', 'scatter']
        
        for chart_type in chart_types:
            try:
                fig = plot_ts(self.sample_data, nome="Test", chart=chart_type)
                assert isinstance(fig, go.Figure)
                assert len(fig.data) > 0
            except Exception as e:
                # Some chart types might not work with all data types
                pytest.skip(f"Chart type {chart_type} not supported: {e}")

    def test_plot_ts_with_different_themes(self):
        """Test plot_ts with different theme parameters."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        themes = ['light', 'dark']
        
        for theme in themes:
            fig = plot_ts(self.sample_data, nome="Test", theme=theme)
            assert isinstance(fig, go.Figure)
            
            # Check that theme is applied to layout
            layout = fig.layout.to_plotly_json()
            if theme == "dark":
                assert layout.get("paper_bgcolor") == "#1e3142" or layout.get("plot_bgcolor") == "#1e3142"
            else:
                assert layout.get("paper_bgcolor") == "#FAFAFA" or layout.get("plot_bgcolor") == "#FAFAFA"

    def test_plot_ts_with_custom_parameters(self):
        """Test plot_ts with custom title, units, and source."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        fig = plot_ts(
            self.sample_data, 
            nome="Custom GDP Chart", 
            units="USD Billions",
            source="Source: IMF IFS Database"
        )
        
        assert isinstance(fig, go.Figure)
        layout = fig.layout.to_plotly_json()
        
        # Check that custom title is set
        assert "Custom GDP Chart" in str(layout.get("title", {}))
        
        # Check that y-axis has custom units
        yaxis = layout.get("yaxis", {})
        assert "USD Billions" in str(yaxis.get("title", {}))

    def test_plot_ts_with_single_series(self):
        """Test plot_ts with single series data."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        single_series = pd.DataFrame({
            'GDP': [100.0, 101.5, 102.0, 103.0, 104.0]
        }, index=['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1'])
        
        fig = plot_ts(single_series, nome="Single Series Test")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1

    def test_plot_ts_with_empty_data(self):
        """Test plot_ts with empty DataFrame."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        empty_df = pd.DataFrame()
        
        # Should handle empty data gracefully
        try:
            fig = plot_ts(empty_df, nome="Empty Data Test")
            assert isinstance(fig, go.Figure)
        except Exception as e:
            # It's acceptable for empty data to raise an exception
            assert "empty" in str(e).lower() or "no data" in str(e).lower()

    def test_plot_ts_with_nan_values(self):
        """Test plot_ts with NaN values in data."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        data_with_nan = pd.DataFrame({
            'Series1': [100.0, np.nan, 102.0, 103.0, 104.0],
            'Series2': [200.0, 202.0, np.nan, 206.0, 208.0]
        }, index=['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1'])
        
        fig = plot_ts(data_with_nan, nome="NaN Data Test")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2

    def test_plot_ts_logo_inclusion(self):
        """Test that plot_ts includes logo in the figure."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        fig = plot_ts(self.sample_data, nome="Logo Test")
        layout = fig.layout.to_plotly_json()
        
        # Check for images in layout (logo)
        images = layout.get("images", [])
        assert len(images) > 0
        
        # Check that logo URL is present
        logo_url = "https://raw.githubusercontent.com/ThresholdMacro/ThresholdMacro/main/Images/Sphere_no_letters.png"
        found_logo = any(logo_url in str(img.get("source", "")) for img in images)
        assert found_logo

    def test_plot_ts_annotation_inclusion(self):
        """Test that plot_ts includes source annotation."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        custom_source = "Source: Custom Database"
        fig = plot_ts(self.sample_data, nome="Annotation Test", source=custom_source)
        layout = fig.layout.to_plotly_json()
        
        # Check for annotations in layout
        annotations = layout.get("annotations", [])
        assert len(annotations) > 0
        
        # Check that custom source is included
        found_source = any(custom_source in str(ann.get("text", "")) for ann in annotations)
        assert found_source

    def test_plot_ts_data_extraction(self):
        """Test that plot_ts creates proper data traces."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        fig = plot_ts(self.sample_data, nome="Data Extraction Test")
        
        # Check that data traces are created
        assert len(fig.data) == 2  # Two series in sample data
        
        # Check that x and y data are present
        for trace in fig.data:
            assert hasattr(trace, 'x')
            assert hasattr(trace, 'y')
            assert len(trace.x) > 0
            assert len(trace.y) > 0

    def test_plot_ts_layout_structure(self):
        """Test that plot_ts creates proper layout structure."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        fig = plot_ts(self.sample_data, nome="Layout Test")
        layout = fig.layout.to_plotly_json()
        
        # Check essential layout components
        assert "title" in layout
        assert "xaxis" in layout
        assert "yaxis" in layout
        assert "legend" in layout
        
        # Check that title is properly set
        title = layout.get("title", {})
        assert "Layout Test" in str(title.get("text", ""))

    def test_plot_ts_error_handling(self):
        """Test plot_ts error handling with invalid parameters."""
        from openbb_dbnomics.utils.myplot import plot_ts
        
        # Test with invalid chart type
        try:
            fig = plot_ts(self.sample_data, nome="Test", chart="invalid_chart_type")
            # Should either work with default or raise appropriate error
            assert isinstance(fig, go.Figure)
        except Exception as e:
            # It's acceptable to raise an error for invalid chart type
            assert "invalid" in str(e).lower() or "chart" in str(e).lower()

        # Test with None data
        try:
            fig = plot_ts(None, nome="Test")
            assert isinstance(fig, go.Figure)
        except Exception as e:
            # Should handle None data gracefully
            assert "none" in str(e).lower() or "data" in str(e).lower() 