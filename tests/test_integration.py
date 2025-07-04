"""End-to-end integration tests for the complete DBNomics workflow."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from openbb_dbnomics.router import router
from openbb_dbnomics.utils.providers import DBNomicsClient


class TestCompleteWorkflow:
    """End-to-end integration tests for complete workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(router)
        self.db_client = DBNomicsClient()

    @patch('openbb_dbnomics.router.client')
    def test_complete_data_discovery_workflow(self, mock_client):
        """Test complete data discovery workflow."""
        # Mock providers
        mock_client.get_providers.return_value = [
            {"code": "IMF", "name": "International Monetary Fund"}
        ]
        
        # Mock datasets
        mock_client.get_datasets.return_value = [
            {"code": "IFS", "name": "International Financial Statistics"}
        ]
        
        # Mock series
        mock_client.get_series.return_value = [
            {
                "id": "IMF/IFS/Q.US.NGDP_D_SA_IX",
                "series_name": "GDP Index",
                "REF_AREA": "US",
                "INDICATOR": "NGDP_D_SA_IX"
            }
        ]

        # Test 1: Get providers
        response = self.client.get("/providers")
        assert response.status_code == 200
        providers = response.json()
        assert len(providers) == 1
        assert providers[0]["code"] == "IMF"

        # Test 2: Get datasets
        response = self.client.get("/datasets?search=IMF")
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) == 1
        assert datasets[0]["code"] == "IFS"

        # Test 3: Get series
        response = self.client.get("/series?provider=IMF&dataset=IFS&limit=10")
        assert response.status_code == 200
        series = response.json()
        assert len(series) == 1
        assert series[0]["REF_AREA"] == "US"

    @patch('openbb_dbnomics.router.client')
    def test_complete_data_selection_workflow(self, mock_client):
        """Test complete data selection workflow."""
        # Mock dataset metadata
        mock_client.get_dataset_metadata.return_value = {
            "dimensions_values_labels": {
                "REF_AREA": {"US": "United States", "EU": "European Union"},
                "INDICATOR": {
                    "NGDP_D_SA_IX": "GDP Index",
                    "NGDP_SA_XDC": "GDP USD"
                }
            }
        }

        # Test 1: Get available regions
        response = self.client.get("/series/ref_areas?provider=IMF&dataset=IFS")
        assert response.status_code == 200
        regions = response.json()
        assert len(regions) == 2
        assert regions[0]["code"] == "EU"
        assert regions[1]["code"] == "US"

        # Test 2: Get available indicators
        response = self.client.get("/series/indicators?provider=IMF&dataset=IFS")
        assert response.status_code == 200
        indicators = response.json()
        assert len(indicators) == 2
        assert indicators[0]["code"] == "NGDP_D_SA_IX"
        assert indicators[1]["code"] == "NGDP_SA_XDC"

    @patch('openbb_dbnomics.router.client')
    @patch('openbb_dbnomics.router.plot_ts')
    def test_complete_visualization_workflow(self, mock_plot_ts, mock_client):
        """Test complete visualization workflow."""
        # Mock multi-series data
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

        # Mock Plotly figure
        mock_fig = Mock()
        mock_fig.data = [Mock(), Mock()]
        mock_fig.data[0].x = ["2020-Q1", "2020-Q2"]
        mock_fig.data[0].y = [100.0, 101.5]
        mock_fig.data[0].name = "NGDP_D_SA_IX"
        mock_fig.data[1].x = ["2020-Q1", "2020-Q2"]
        mock_fig.data[1].y = [200.0, 202.0]
        mock_fig.data[1].name = "NGDP_SA_XDC"
        mock_fig.layout.to_plotly_json.return_value = {
            "title": {"text": "Test Chart"},
            "yaxis": {},
            "xaxis": {},
            "legend": {}
        }
        mock_plot_ts.return_value = mock_fig

        # Test 1: Get table data
        response = self.client.get(
            "/series/table?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX,NGDP_SA_XDC"
        )
        assert response.status_code == 200
        table_data = response.json()
        assert len(table_data) == 2
        assert "date" in table_data[0]
        assert "NGDP_D_SA_IX" in table_data[0]
        assert "NGDP_SA_XDC" in table_data[0]

        # Test 2: Get chart data
        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX,NGDP_SA_XDC&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=level&source=Test"
        )
        assert response.status_code == 200
        chart_data = response.json()
        assert "data" in chart_data
        assert "layout" in chart_data
        assert len(chart_data["data"]) == 2

    @patch('openbb_dbnomics.router.client')
    @patch('openbb_dbnomics.router.plot_ts')
    def test_change_calculation_workflow(self, mock_plot_ts, mock_client):
        """Test complete workflow with change calculations."""
        # Mock data with enough periods for YoY calculation
        mock_client.get_multi_series_aligned.return_value = [
            {"date": "2020-Q1", "NGDP_D_SA_IX": 100.0},
            {"date": "2020-Q2", "NGDP_D_SA_IX": 101.5},
            {"date": "2020-Q3", "NGDP_D_SA_IX": 102.0},
            {"date": "2020-Q4", "NGDP_D_SA_IX": 103.0},
            {"date": "2021-Q1", "NGDP_D_SA_IX": 104.0},
            {"date": "2021-Q2", "NGDP_D_SA_IX": 105.0}
        ]

        # Mock Plotly figure
        mock_fig = Mock()
        mock_fig.data = [Mock()]
        mock_fig.data[0].x = ["2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4", "2021-Q1", "2021-Q2"]
        mock_fig.data[0].y = [None, None, None, None, 4.0, 3.45]  # YoY changes
        mock_fig.data[0].name = "NGDP_D_SA_IX"
        mock_fig.layout.to_plotly_json.return_value = {
            "title": {"text": "Test Chart"},
            "yaxis": {},
            "xaxis": {},
            "legend": {}
        }
        mock_plot_ts.return_value = mock_fig

        # Test YoY change
        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=yoy&source=Test"
        )
        assert response.status_code == 200
        chart_data = response.json()
        assert "Year-on-Year" in chart_data["layout"]["title"]["text"]

        # Test QoQ change
        mock_fig.data[0].y = [None, 1.5, 0.49, 0.98, 0.97, 0.96]  # QoQ changes
        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX&nome=Test&units=Index&chart=line&startdate=1990-01-01&change=qoq&source=Test"
        )
        assert response.status_code == 200
        chart_data = response.json()
        assert "Quarter-on-Quarter" in chart_data["layout"]["title"]["text"]

    @patch('openbb_dbnomics.router.client')
    def test_error_handling_workflow(self, mock_client):
        """Test error handling throughout the workflow."""
        # Test 1: No providers available
        mock_client.get_providers.return_value = []
        response = self.client.get("/providers")
        assert response.status_code == 200
        providers = response.json()
        assert len(providers) == 0

        # Test 2: No datasets found
        mock_client.get_datasets.return_value = []
        response = self.client.get("/datasets?search=nonexistent")
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) == 0

        # Test 3: No series data
        mock_client.get_multi_series_aligned.return_value = []
        response = self.client.get(
            "/series/chart?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX"
        )
        assert response.status_code == 404
        error_data = response.json()
        assert "error" in error_data
        assert "No data found" in error_data["error"]

    @patch('openbb_dbnomics.router.client')
    def test_parameter_validation_workflow(self, mock_client):
        """Test parameter validation throughout the workflow."""
        # Test with invalid provider
        mock_client.get_datasets.return_value = []
        response = self.client.get("/datasets?search=invalid_provider")
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) == 0

        # Test with invalid dataset
        mock_client.get_series.return_value = []
        response = self.client.get("/series?provider=IMF&dataset=invalid_dataset&limit=10")
        assert response.status_code == 200
        series = response.json()
        assert len(series) == 0

        # Test with invalid indicators
        mock_client.get_multi_series_aligned.return_value = []
        response = self.client.get(
            "/series/table?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=invalid_indicator"
        )
        assert response.status_code == 200
        table_data = response.json()
        assert len(table_data) == 0

    def test_series_id_construction(self):
        """Test series ID construction with various parameters."""
        # Test valid series ID construction
        series_id = self.db_client.construct_series_id("IMF", "IFS", "Q", "US", "NGDP_D_SA_IX")
        assert series_id == "IMF/IFS/Q.US.NGDP_D_SA_IX"

        # Test with different frequency
        series_id = self.db_client.construct_series_id("IMF", "IFS", "M", "US", "NGDP_D_SA_IX")
        assert series_id == "IMF/IFS/M.US.NGDP_D_SA_IX"

        # Test with different region
        series_id = self.db_client.construct_series_id("IMF", "IFS", "Q", "EU", "NGDP_D_SA_IX")
        assert series_id == "IMF/IFS/Q.EU.NGDP_D_SA_IX"

    @patch('openbb_dbnomics.router.client')
    def test_data_alignment_workflow(self, mock_client):
        """Test data alignment with different series lengths."""
        # Mock data with different lengths
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
            },
            {
                "date": "2020-Q3",
                "NGDP_D_SA_IX": 102.0,
                "NGDP_SA_XDC": None  # Missing data
            }
        ]

        response = self.client.get(
            "/series/table?provider=IMF&dataset=IFS&freq=Q&ref_area=US&indicators=NGDP_D_SA_IX,NGDP_SA_XDC"
        )
        assert response.status_code == 200
        table_data = response.json()
        assert len(table_data) == 3
        assert table_data[2]["NGDP_SA_XDC"] is None  # Should handle missing data

    def test_date_filtering_workflow(self):
        """Test date filtering functionality."""
        import re
        
        # Test quarterly date format validation
        assert re.match(r"^\d{4}-Q\d$", "2020-Q1")
        assert re.match(r"^\d{4}-Q\d$", "2021-Q4")
        assert not re.match(r"^\d{4}-Q\d$", "2020-01-01")

        # Test date comparison logic
        assert "2020-Q1" >= "1990-Q1"
        assert "2021-Q1" >= "2020-Q4"
        assert "2020-Q1" < "2021-Q1" 