"""Unit tests for DBNomicsClient."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from openbb_dbnomics.utils.providers import DBNomicsClient


class TestDBNomicsClient:
    """Test cases for DBNomicsClient."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = DBNomicsClient()
        self.base_url = "https://api.db.nomics.world/v22"

    def test_init(self):
        """Test client initialization."""
        assert self.client.base_url == self.base_url
        assert hasattr(self.client, 'session')

    @patch('requests.Session.get')
    def test_get_providers_success(self, mock_get):
        """Test successful providers fetch."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "providers": [
                {"code": "IMF", "name": "International Monetary Fund"},
                {"code": "WB", "name": "World Bank"}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test
        providers = self.client.get_providers()
        
        # Assertions
        assert len(providers) == 2
        assert providers[0]["code"] == "IMF"
        assert providers[1]["code"] == "WB"
        mock_get.assert_called_once_with(f"{self.base_url}/providers")

    @patch('requests.Session.get')
    def test_get_providers_error(self, mock_get):
        """Test providers fetch with API error."""
        mock_get.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            self.client.get_providers()

    @patch('requests.Session.get')
    def test_get_datasets_success(self, mock_get):
        """Test successful datasets fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "datasets": [
                {"code": "IFS", "name": "International Financial Statistics"},
                {"code": "WEO", "name": "World Economic Outlook"}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        datasets = self.client.get_datasets(search_term="IMF")
        
        assert len(datasets) == 2
        assert datasets[0]["code"] == "IFS"
        mock_get.assert_called_once()

    @patch('requests.Session.get')
    def test_get_series_success(self, mock_get):
        """Test successful series fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "series": [
                {
                    "id": "IMF/IFS/Q.US.NGDP_D_SA_IX",
                    "series_name": "GDP Index",
                    "REF_AREA": "US",
                    "INDICATOR": "NGDP_D_SA_IX"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        series = self.client.get_series("IMF", "IFS", limit=10)
        
        assert len(series) == 1
        assert series[0]["id"] == "IMF/IFS/Q.US.NGDP_D_SA_IX"
        assert series[0]["REF_AREA"] == "US"

    @patch('requests.Session.get')
    def test_get_series_data_success(self, mock_get):
        """Test successful series data fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "series": {
                "values": [
                    {"period": "2020-Q1", "value": 100.0},
                    {"period": "2020-Q2", "value": 101.5}
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = self.client.get_series_data("IMF/IFS/Q.US.NGDP_D_SA_IX")
        
        assert len(data) == 2
        assert data[0]["period"] == "2020-Q1"
        assert data[0]["value"] == 100.0

    @patch('requests.Session.get')
    def test_get_dataset_metadata_success(self, mock_get):
        """Test successful dataset metadata fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "dimensions_values_labels": {
                "REF_AREA": {"US": "United States", "EU": "European Union"},
                "INDICATOR": {"NGDP_D_SA_IX": "GDP Index", "NGDP_SA_XDC": "GDP USD"}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        metadata = self.client.get_dataset_metadata("IMF", "IFS")
        
        assert "REF_AREA" in metadata["dimensions_values_labels"]
        assert "INDICATOR" in metadata["dimensions_values_labels"]
        assert metadata["dimensions_values_labels"]["REF_AREA"]["US"] == "United States"

    def test_construct_series_id(self):
        """Test series ID construction."""
        series_id = self.client.construct_series_id("IMF", "IFS", "Q", "US", "NGDP_D_SA_IX")
        assert series_id == "IMF/IFS/Q.US.NGDP_D_SA_IX"

    @patch.object(DBNomicsClient, 'get_series_data')
    def test_get_multi_series_aligned_success(self, mock_get_data):
        """Test successful multi-series alignment."""
        # Mock data for two series
        mock_get_data.side_effect = [
            [{"period": "2020-Q1", "value": 100.0}, {"period": "2020-Q2", "value": 101.5}],
            [{"period": "2020-Q1", "value": 200.0}, {"period": "2020-Q2", "value": 202.0}]
        ]

        with patch.object(self.client, 'construct_series_id') as mock_construct:
            mock_construct.side_effect = [
                "IMF/IFS/Q.US.NGDP_D_SA_IX",
                "IMF/IFS/Q.US.NGDP_SA_XDC"
            ]

            result = self.client.get_multi_series_aligned(
                "IMF", "IFS", "Q", "US", ["NGDP_D_SA_IX", "NGDP_SA_XDC"]
            )

            assert len(result) == 2
            assert "date" in result[0]
            assert "NGDP_D_SA_IX" in result[0]
            assert "NGDP_SA_XDC" in result[0]

    def test_handle_different_value_fields(self):
        """Test handling of different value field names in API response."""
        # Test with 'value' field
        data_with_value = [{"period": "2020-Q1", "value": 100.0}]
        result = self.client._extract_values_and_periods(data_with_value)
        assert result["values"] == [100.0]
        assert result["periods"] == ["2020-Q1"]

        # Test with 'values' field
        data_with_values = [{"period": "2020-Q1", "values": 100.0}]
        result = self.client._extract_values_and_periods(data_with_values)
        assert result["values"] == [100.0]
        assert result["periods"] == ["2020-Q1"]

    def test_handle_different_period_fields(self):
        """Test handling of different period field names in API response."""
        # Test with 'period' field
        data_with_period = [{"period": "2020-Q1", "value": 100.0}]
        result = self.client._extract_values_and_periods(data_with_period)
        assert result["periods"] == ["2020-Q1"]

        # Test with 'periods' field
        data_with_periods = [{"periods": "2020-Q1", "value": 100.0}]
        result = self.client._extract_values_and_periods(data_with_periods)
        assert result["periods"] == ["2020-Q1"]

        # Test with 'period_start_day' field
        data_with_start_day = [{"period_start_day": "2020-01-01", "value": 100.0}]
        result = self.client._extract_values_and_periods(data_with_start_day)
        assert result["periods"] == ["2020-01-01"] 