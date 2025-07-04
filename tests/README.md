# Testing Suite for OpenBB DBNomics Extension

This directory contains a comprehensive automated testing suite for the DBNomics OpenBB extension.

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_dbnomics_client.py  # Unit tests for DBNomicsClient
├── test_router.py           # Integration tests for FastAPI endpoints
├── test_myplot.py           # Unit tests for charting functionality
├── test_integration.py      # End-to-end workflow tests
└── README.md               # This file
```

## 🧪 Test Categories

### **Unit Tests** (`test_dbnomics_client.py`, `test_myplot.py`)
- **Purpose**: Test individual components in isolation
- **Coverage**: 
  - DBNomicsClient API communication
  - Data processing and transformation
  - Chart generation functionality
  - Error handling for edge cases
- **Dependencies**: Mocked external APIs

### **Integration Tests** (`test_router.py`)
- **Purpose**: Test FastAPI endpoints and data flow
- **Coverage**:
  - All API endpoints (`/providers`, `/datasets`, `/series/*`, etc.)
  - Parameter validation
  - Response format validation
  - Error handling
- **Dependencies**: Mocked DBNomicsClient

### **End-to-End Tests** (`test_integration.py`)
- **Purpose**: Test complete workflows from data discovery to visualization
- **Coverage**:
  - Complete data discovery workflow
  - Multi-indicator data retrieval
  - Chart generation with different parameters
  - Change calculations (YoY, QoQ)
- **Dependencies**: Mocked external services

## 🚀 Running Tests

### **Install Test Dependencies**
```bash
pip install pytest pytest-cov fastapi httpx
```

### **Run All Tests**
```bash
pytest
```

### **Run Specific Test Categories**
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# End-to-end tests only
pytest -m e2e

# Skip slow tests
pytest -m "not slow"
```

### **Run with Coverage**
```bash
pytest --cov=openbb_dbnomics --cov-report=html
```

### **Run Specific Test Files**
```bash
# Test DBNomicsClient only
pytest tests/test_dbnomics_client.py

# Test router endpoints only
pytest tests/test_router.py

# Test charting functionality only
pytest tests/test_myplot.py
```

### **Run with Verbose Output**
```bash
pytest -v
```

## 🎯 Test Coverage

### **DBNomicsClient Tests**
- ✅ API communication with DBNomics.world
- ✅ Data fetching (providers, datasets, series)
- ✅ Series ID construction
- ✅ Multi-series data alignment
- ✅ Error handling for API failures
- ✅ Handling different field names in API responses

### **Router Endpoint Tests**
- ✅ All 7 API endpoints
- ✅ Parameter validation
- ✅ Response format validation
- ✅ Error handling (404, invalid parameters)
- ✅ JSON serialization (NaN handling)
- ✅ Change calculations (YoY, QoQ)

### **Chart Generation Tests**
- ✅ Multiple chart types (line, bar, regression, etc.)
- ✅ Theme customization (light/dark)
- ✅ Logo and annotation inclusion
- ✅ Data with NaN values
- ✅ Empty data handling

### **Integration Workflow Tests**
- ✅ Complete data discovery workflow
- ✅ Multi-indicator analysis
- ✅ Date filtering
- ✅ Series alignment with missing data
- ✅ Parameter validation throughout workflow

## 🔧 Test Configuration

### **Pytest Configuration** (`pytest.ini`)
- Test discovery patterns
- Output formatting
- Warning filters
- Custom markers

### **Fixtures** (`conftest.py`)
- Reusable test data
- Mock objects
- Test clients
- Sample API responses

### **Custom Markers**
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.e2e`: End-to-end tests
- `@pytest.mark.slow`: Slow-running tests

## 📊 Test Data

### **Sample Data Fixtures**
- `sample_series_data`: Time series data for testing
- `sample_dataframe`: Pandas DataFrame for chart testing
- `sample_providers`: Provider data
- `sample_datasets`: Dataset data
- `sample_series`: Series metadata
- `sample_metadata`: Dataset dimensions

### **Mock Objects**
- `mock_plotly_figure`: Mock Plotly figure for testing
- `sample_api_response`: Mock API responses
- `test_parameters`: Common test parameters

## 🐛 Debugging Tests

### **Run Single Test**
```bash
pytest tests/test_router.py::TestRouterEndpoints::test_get_providers -v
```

### **Run with Print Statements**
```bash
pytest -s tests/test_dbnomics_client.py
```

### **Run with Debugger**
```bash
pytest --pdb tests/test_integration.py
```

## 📈 Continuous Integration

### **GitHub Actions Example**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=openbb_dbnomics
```

## 🎯 Best Practices

### **Test Organization**
- Group related tests in classes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### **Mocking Strategy**
- Mock external API calls
- Use realistic test data
- Test both success and failure scenarios

### **Error Testing**
- Test edge cases
- Test invalid parameters
- Test network failures
- Test data validation

### **Performance**
- Use fast-running mocks
- Avoid real API calls in tests
- Mark slow tests appropriately

## 🔍 Test Maintenance

### **Adding New Tests**
1. Create test file following naming convention
2. Add appropriate markers
3. Use existing fixtures when possible
4. Add comprehensive docstrings

### **Updating Tests**
- Update mocks when API changes
- Add tests for new features
- Maintain test coverage above 80%

### **Test Data Management**
- Keep test data realistic
- Update sample data when needed
- Document data sources and assumptions 