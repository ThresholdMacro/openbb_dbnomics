"""Pytest configuration and fixtures for DBNomics tests."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock
from fastapi.testclient import TestClient
from openbb_dbnomics.router import router
from openbb_dbnomics.utils.providers import DBNomicsClient


@pytest.fixture
def test_client():
    """Create a test client for FastAPI endpoints."""
    return TestClient(router)


@pytest.fixture
def db_client():
    """Create a DBNomicsClient instance for testing."""
    return DBNomicsClient()


@pytest.fixture
def sample_series_data():
    """Sample time series data for testing."""
    return [
        {"date": "2020-Q1", "NGDP_D_SA_IX": 100.0, "NGDP_SA_XDC": 200.0},
        {"date": "2020-Q2", "NGDP_D_SA_IX": 101.5, "NGDP_SA_XDC": 202.0},
        {"date": "2020-Q3", "NGDP_D_SA_IX": 102.0, "NGDP_SA_XDC": 204.0},
        {"date": "2020-Q4", "NGDP_D_SA_IX": 103.0, "NGDP_SA_XDC": 206.0},
        {"date": "2021-Q1", "NGDP_D_SA_IX": 104.0, "NGDP_SA_XDC": 208.0}
    ]


@pytest.fixture
def sample_dataframe():
    """Sample pandas DataFrame for testing."""
    return pd.DataFrame({
        'NGDP_D_SA_IX': [100.0, 101.5, 102.0, 103.0, 104.0],
        'NGDP_SA_XDC': [200.0, 202.0, 204.0, 206.0, 208.0]
    }, index=['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1'])


@pytest.fixture
def sample_providers():
    """Sample providers data for testing."""
    return [
        {"code": "IMF", "name": "International Monetary Fund"},
        {"code": "WB", "name": "World Bank"},
        {"code": "ECB", "name": "European Central Bank"}
    ]


@pytest.fixture
def sample_datasets():
    """Sample datasets data for testing."""
    return [
        {"code": "IFS", "name": "International Financial Statistics"},
        {"code": "WEO", "name": "World Economic Outlook"},
        {"code": "BOP", "name": "Balance of Payments"}
    ]


@pytest.fixture
def sample_series():
    """Sample series data for testing."""
    return [
        {
            "id": "IMF/IFS/Q.US.NGDP_D_SA_IX",
            "series_name": "GDP Index",
            "REF_AREA": "US",
            "INDICATOR": "NGDP_D_SA_IX"
        },
        {
            "id": "IMF/IFS/Q.US.NGDP_SA_XDC",
            "series_name": "GDP USD",
            "REF_AREA": "US",
            "INDICATOR": "NGDP_SA_XDC"
        }
    ]


@pytest.fixture
def sample_metadata():
    """Sample dataset metadata for testing."""
    return {
        "dimensions_values_labels": {
            "REF_AREA": {
                "US": "United States",
                "EU": "European Union",
                "JP": "Japan"
            },
            "INDICATOR": {
                "NGDP_D_SA_IX": "GDP Index",
                "NGDP_SA_XDC": "GDP USD",
                "PCPI_PC_PP_PT": "Consumer Price Index"
            }
        }
    }


@pytest.fixture
def mock_plotly_figure():
    """Mock Plotly figure for testing."""
    mock_fig = Mock()
    mock_fig.data = [Mock(), Mock()]
    
    # First trace
    mock_fig.data[0].x = ["2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4", "2021-Q1"]
    mock_fig.data[0].y = [100.0, 101.5, 102.0, 103.0, 104.0]
    mock_fig.data[0].name = "NGDP_D_SA_IX"
    
    # Second trace
    mock_fig.data[1].x = ["2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4", "2021-Q1"]
    mock_fig.data[1].y = [200.0, 202.0, 204.0, 206.0, 208.0]
    mock_fig.data[1].name = "NGDP_SA_XDC"
    
    # Layout
    mock_fig.layout.to_plotly_json.return_value = {
        "title": {"text": "Test Chart"},
        "yaxis": {"title": {"text": "Index"}},
        "xaxis": {"title": {"text": "Date"}},
        "legend": {"title": {"text": "Indicator"}},
        "annotations": [{"text": "Source: DBNomics"}],
        "images": [{"source": "logo_url"}]
    }
    
    return mock_fig


@pytest.fixture
def sample_api_response():
    """Sample API response data for testing."""
    return {
        "series": {
            "values": [
                {"period": "2020-Q1", "value": 100.0},
                {"period": "2020-Q2", "value": 101.5},
                {"period": "2020-Q3", "value": 102.0},
                {"period": "2020-Q4", "value": 103.0},
                {"period": "2021-Q1", "value": 104.0}
            ]
        }
    }


@pytest.fixture
def sample_api_response_alt_fields():
    """Sample API response with alternative field names for testing."""
    return {
        "series": {
            "values": [
                {"periods": "2020-Q1", "values": 100.0},
                {"periods": "2020-Q2", "values": 101.5},
                {"periods": "2020-Q3", "values": 102.0},
                {"periods": "2020-Q4", "values": 103.0},
                {"periods": "2021-Q1", "values": 104.0}
            ]
        }
    }


@pytest.fixture
def sample_api_response_daily():
    """Sample API response with daily dates for testing."""
    return {
        "series": {
            "values": [
                {"period_start_day": "2020-01-01", "value": 100.0},
                {"period_start_day": "2020-01-02", "value": 101.5},
                {"period_start_day": "2020-01-03", "value": 102.0}
            ]
        }
    }


@pytest.fixture
def test_parameters():
    """Common test parameters for endpoints."""
    return {
        "provider": "IMF",
        "dataset": "IFS",
        "freq": "Q",
        "ref_area": "US",
        "indicators": "NGDP_D_SA_IX,NGDP_SA_XDC",
        "nome": "Test Chart",
        "units": "Index",
        "chart": "line",
        "startdate": "1990-01-01",
        "change": "level",
        "source": "Source: DBNomics"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their names."""
    for item in items:
        if "test_dbnomics_client" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_router" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
        elif "test_myplot" in item.nodeid:
            item.add_marker(pytest.mark.unit) 