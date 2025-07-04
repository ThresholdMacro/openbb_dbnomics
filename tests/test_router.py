"""Integration tests for FastAPI router endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from openbb_dbnomics.router import router


class TestRouterEndpoints:
    """Test cases for FastAPI router endpoints."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(router)

    @patch('openbb_dbnomics.router.client')
    def test_get_providers(self, mock_client):
        """Test /providers endpoint."""
        mock_client.get_providers.return_value = [
            {"code": "IMF", "name": "International Monetary Fund"},
            {"code": "WB", "name": "World Bank"}
        ]

        response = self.client.get("/providers")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["code"] == "IMF"
        mock_client.get_providers.assert_called_once()

    @patch('openbb_dbnomics.router.client')
    def test_get_datasets(self, mock_client):
        """Test /datasets endpoint."""
        mock_client.get_datasets.return_value = [
            {"code": "IFS", "name": "International Financial Statistics"},
            {"code": "WEO", "name": "World Economic Outlook"}
        ]

        response = self.client.get("/datasets?search=IMF")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["code"] == "IFS"
        mock_client.get_datasets.assert_called_once_with(search_term="IMF")

    @patch('openbb_dbnomics.router.client')
    def test_get_series(self, mock_client):
        """Test /series endpoint."""
        mock_client.get_series.return_value = [
            {
                "id": "IMF/IFS/Q.US.NGDP_D_SA_IX",
                "series_name": "GDP Index",
                "REF_AREA": "US",
                "INDICATOR": "NGDP_D_SA_IX"
            }
        ]

        response = self.client.get("/series?provider=IMF&dataset=IFS&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["REF_AREA"] == "US"
        mock_client.get_series.assert_called_once()

    @patch('openbb_dbnomics.router.client')
    def test_get_ref_areas(self, mock_client):
        """Test /series/ref_areas endpoint."""
        mock_client.get_dataset_metadata.return_value = {
            "dimensions_values_labels": {
                "REF_AREA": {"US": "United States", "EU": "European Union"}
            }
        }

        response = self.client.get("/series/ref_areas?provider=IMF&dataset=IFS")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["code"] == "EU"  # Sorted alphabetically by name
        assert data[1]["code"] == "US"

    @patch('openbb_dbnomics.router.client')
    def test_get_indicators(self, mock_client):
        """Test /series/indicators endpoint."""
        mock_client.get_dataset_metadata.return_value = {
            "dimensions_values_labels": {
                "INDICATOR": {
                    "NGDP_D_SA_IX": "GDP Index",
                    "NGDP_SA_XDC": "GDP USD"
                }
            }
        }

        response = self.client.get("/series/indicators?provider=IMF&dataset=IFS")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["code"] == "NGDP_D_SA_IX"
        assert data[1]["code"] == "NGDP_SA_XDC"

    @patch('openbb_dbnomics.router.client')
    def test_get_series_table(self, mock_client):
        """Test /series/table endpoint."""
        mock_client.get_multi_series_aligned.return_value = [
            {
                "date": "2020-Q1",
                "NGDP_D_SA_IX": 100.0,
                "NGDP_SA_XDC": 200.0
            },
            {
                "date": "2020-Q2", 
                "NGDP_D_SA_IX": 101.5,
                "NGDP_SA_XDC": 202.0
            }
        ]

        response = self.client.get(
            "/series/table?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX,NGDP_SA_XDC"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert "date" in data[0]
        assert "NGDP_D_SA_IX" in data[0]
        assert "NGDP_SA_XDC" in data[0]

    @patch('openbb_dbnomics.router.client')
    @patch('openbb_dbnomics.router.plot_ts')
    def test_get_series_chart_success(self, mock_plot_ts, mock_client):
        """Test /series/chart endpoint success."""
        # Mock data
        mock_client.get_multi_series_aligned.return_value = [
            {"date": "2020-Q1", "NGDP_D_SA_IX": 100.0},
            {"date": "2020-Q2", "NGDP_D_SA_IX": 101.5}
        ]

        # Mock Plotly figure
        mock_fig = Mock()
        mock_fig.data = [Mock()]
        mock_fig.data[0].x = ["2020-Q1", "2020-Q2"]
        mock_fig.data[0].y = [100.0, 101.5]
        mock_fig.data[0].name = "NGDP_D_SA_IX"
        mock_fig.layout.to_plotly_json.return_value = {
            "title": {"text": "Test Chart"},
            "yaxis": {},
            "xaxis": {},
            "legend": {}
        }
        mock_plot_ts.return_value = mock_fig

        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=level&source=Test"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "layout" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "NGDP_D_SA_IX"

    @patch('openbb_dbnomics.router.client')
    def test_get_series_chart_no_data(self, mock_client):
        """Test /series/chart endpoint with no data."""
        mock_client.get_multi_series_aligned.return_value = []

        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "No data found" in data["error"]

    @patch('openbb_dbnomics.router.client')
    @patch('openbb_dbnomics.router.plot_ts')
    def test_get_series_chart_with_yoy_change(self, mock_plot_ts, mock_client):
        """Test /series/chart endpoint with YoY change calculation."""
        # Mock data
        mock_client.get_multi_series_aligned.return_value = [
            {"date": "2020-Q1", "NGDP_D_SA_IX": 100.0},
            {"date": "2020-Q2", "NGDP_D_SA_IX": 101.5},
            {"date": "2021-Q1", "NGDP_D_SA_IX": 102.0},
            {"date": "2021-Q2", "NGDP_D_SA_IX": 103.0}
        ]

        # Mock Plotly figure
        mock_fig = Mock()
        mock_fig.data = [Mock()]
        mock_fig.data[0].x = ["2020-Q1", "2020-Q2", "2021-Q1", "2021-Q2"]
        mock_fig.data[0].y = [None, None, 2.0, 1.48]  # YoY changes
        mock_fig.data[0].name = "NGDP_D_SA_IX"
        mock_fig.layout.to_plotly_json.return_value = {
            "title": {"text": "Test Chart"},
            "yaxis": {},
            "xaxis": {},
            "legend": {}
        }
        mock_plot_ts.return_value = mock_fig

        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=yoy&source=Test"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "layout" in data
        # Check that title includes YoY change
        assert "Year-on-Year" in data["layout"]["title"]["text"]

    @patch('openbb_dbnomics.router.client')
    @patch('openbb_dbnomics.router.plot_ts')
    def test_get_series_chart_with_qoq_change(self, mock_plot_ts, mock_client):
        """Test /series/chart endpoint with QoQ change calculation."""
        # Mock data
        mock_client.get_multi_series_aligned.return_value = [
            {"date": "2020-Q1", "NGDP_D_SA_IX": 100.0},
            {"date": "2020-Q2", "NGDP_D_SA_IX": 101.5},
            {"date": "2020-Q3", "NGDP_D_SA_IX": 102.0}
        ]

        # Mock Plotly figure
        mock_fig = Mock()
        mock_fig.data = [Mock()]
        mock_fig.data[0].x = ["2020-Q1", "2020-Q2", "2020-Q3"]
        mock_fig.data[0].y = [None, 1.5, 0.49]  # QoQ changes
        mock_fig.data[0].name = "NGDP_D_SA_IX"
        mock_fig.layout.to_plotly_json.return_value = {
            "title": {"text": "Test Chart"},
            "yaxis": {},
            "xaxis": {},
            "legend": {}
        }
        mock_plot_ts.return_value = mock_fig

        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=qoq&source=Test"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "layout" in data
        # Check that title includes QoQ change
        assert "Quarter-on-Quarter" in data["layout"]["title"]["text"]

    def test_apply_change_function(self):
        """Test apply_change function with different scenarios."""
        from openbb_dbnomics.router import apply_change
        
        # Test data
        df = pd.DataFrame({
            'NGDP_D_SA_IX': [100.0, 101.5, 102.0, 103.0, 104.0],
            'NGDP_SA_XDC': [200.0, 202.0, 204.0, 206.0, 208.0]
        }, index=['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1'])

        # Test level (no change)
        result_level = apply_change(df.copy(), 'level', 'Q')
        assert result_level['NGDP_D_SA_IX'].iloc[0] == 100.0

        # Test YoY change
        result_yoy = apply_change(df.copy(), 'yoy', 'Q')
        assert pd.isna(result_yoy['NGDP_D_SA_IX'].iloc[0])  # First 4 periods should be NaN
        assert not pd.isna(result_yoy['NGDP_D_SA_IX'].iloc[4])  # 5th period should have YoY change

        # Test QoQ change
        result_qoq = apply_change(df.copy(), 'qoq', 'Q')
        assert pd.isna(result_qoq['NGDP_D_SA_IX'].iloc[0])  # First period should be NaN
        assert not pd.isna(result_qoq['NGDP_D_SA_IX'].iloc[1])  # Second period should have QoQ change

    def test_date_filtering(self):
        """Test date filtering functionality."""
        from openbb_dbnomics.router import get_series_chart
        import re

        # Test quarterly date format
        assert re.match(r"^\d{4}-Q\d$", "2020-Q1")
        assert re.match(r"^\d{4}-Q\d$", "2021-Q4")
        assert not re.match(r"^\d{4}-Q\d$", "2020-01-01")

        # Test date comparison
        assert "2020-Q1" >= "1990-Q1"
        assert "2021-Q1" >= "2020-Q4" 