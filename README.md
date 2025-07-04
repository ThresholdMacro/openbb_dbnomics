# OpenBB DBNomics Extension

## 🎯 Project Objective

This OpenBB Platform extension provides comprehensive access to **DBNomics.world** - a vast repository of economic and financial time series data from over 150 international data providers including IMF, World Bank, ECB, BIS, and national statistical offices.

### **Primary Goals:**
1. **Universal Data Access**: Browse and search across all available data providers
2. **Dataset Discovery**: Explore what datasets each provider offers
3. **Series Construction**: Build valid series identifiers by selecting provider, dataset, frequency, region, and indicators
4. **Multi-Indicator Analysis**: Retrieve and align multiple indicators simultaneously for comparative analysis
5. **Flexible Visualization**: Display data in both tabular and chart formats with advanced customization

---

## 🔍 Data Discovery & Series Construction Methodology

### **1. Provider Discovery**
- **Endpoint**: `/providers`
- **Method**: Fetches complete list of all data providers from DBNomics API
- **Result**: Comprehensive catalog of available data sources (IMF, World Bank, ECB, etc.)

### **2. Dataset Exploration**
- **Endpoint**: `/datasets?search={term}`
- **Method**: Searches datasets by provider with keyword filtering
- **Result**: Discover available datasets within each provider (e.g., IFS, WEO, BOP for IMF)

### **3. Series Search & Filtering**
- **Endpoint**: `/series?provider={}&dataset={}&name_filter={}&ref_area={}&limit={}`
- **Method**: 
  - Fetches large batches of series (up to 10,000)
  - Filters by REF_AREA (country/region codes)
  - Filters by series name patterns
  - Returns structured series metadata
- **Result**: Identifiable series with their complete metadata

### **4. Dimension Discovery**
- **Endpoints**: `/series/ref_areas` and `/series/indicators`
- **Method**: Extracts available dimensions from dataset metadata
- **Purpose**: Enables users to construct valid series identifiers
- **Result**: Lists of valid country codes and indicator codes for series construction

### **5. Multi-Series Data Retrieval**
- **Endpoints**: `/series/table` and `/series/chart`
- **Method**: 
  - Constructs series IDs using provider/dataset/frequency/region/indicator combinations
  - Fetches multiple series simultaneously
  - Aligns data by date for comparative analysis
  - Handles missing data and different series lengths
- **Result**: Aligned time series data ready for analysis

---

## 🛠 Technical Implementation

### **Backend Architecture**
```python
# Core Components:
- DBNomicsClient: Handles API communication with dbnomics.world
- FastAPI Router: Provides RESTful endpoints for OpenBB UI
- Data Processing: Aligns and transforms time series data
- Chart Generation: Creates Plotly figures with custom theming
```

### **Key Technical Features**

#### **Robust Data Handling**
- **Series Alignment**: Automatically aligns multiple indicators by date
- **Missing Data**: Graceful handling of incomplete series
- **JSON Serialization**: Proper handling of NaN values for OpenBB compatibility
- **Error Recovery**: Validates series IDs before fetching to avoid 404 errors

#### **Advanced Chart Capabilities**
- **Multiple Chart Types**: Line, bar, regression, distribution, scatter
- **Change Calculations**: Level, Year-over-Year (YoY), Quarter-over-Quarter (QoQ)
- **Date Filtering**: Customizable start dates with smart tick adjustment
- **Professional Styling**: Custom themes, branding, annotations, and logos

#### **Dynamic Series Construction**
- **Flexible Parameters**: Provider, dataset, frequency, region, indicators
- **Real-time Validation**: Ensures series combinations are valid before fetching
- **Batch Processing**: Efficiently handles multiple indicators in single requests

---

## 📊 Widget Ecosystem

### **Data Discovery Widgets**
1. **Providers Browser** (`/providers`)
   - Lists all 150+ data providers
   - Enables exploration of available data sources

2. **Dataset Search** (`/datasets`)
   - Searches datasets within providers
   - Keyword-based filtering for discovery

3. **Series Explorer** (`/series`)
   - Discovers available time series
   - Filters by region and name patterns
   - Shows series metadata and structure

### **Series Construction Widgets**
4. **Region Selector** (`/series/ref_areas`)
   - Shows valid country/region codes for selected dataset
   - Enables precise series targeting

5. **Indicator Browser** (`/series/indicators`)
   - Lists available indicators for selected dataset
   - Facilitates multi-indicator selection

### **Data Visualization Widgets**
6. **Time Series Table** (`/series/table`)
   - Displays aligned multi-indicator data
   - Dynamic column generation based on selected indicators
   - Pydantic model-based structure for OpenBB compatibility

7. **Dynamic Chart** (`/series/chart`)
   - Multi-indicator visualization with customizable chart types
   - Change calculations (Level, YoY, QoQ)
   - Professional styling with branding and annotations

---

## 🔄 Workflow Example

### **Complete Analysis Workflow:**
1. **Browse Providers** → Select "IMF"
2. **Search Datasets** → Find "IFS" (International Financial Statistics)
3. **Explore Regions** → See available countries (US, EU, JP, etc.)
4. **Browse Indicators** → Find GDP-related indicators
5. **Construct Series** → Select multiple indicators (NGDP_D_SA_IX, NGDP_SA_XDC)
6. **Visualize Data** → Create comparative charts and tables

### **Multi-Indicator Analysis:**
```
Provider: IMF
Dataset: IFS  
Frequency: Q (Quarterly)
Region: US
Indicators: NGDP_D_SA_IX, NGDP_SA_XDC, PCPI_PC_PP_PT

Result: Aligned time series showing:
- Nominal GDP (Index)
- Nominal GDP (USD)
- Consumer Price Index (% change)
```

---

## 🎨 Advanced Features

### **Chart Customization**
- **Chart Types**: Line, bar, regression, distribution, scatter
- **Change Analysis**: Level, YoY, QoQ percentage changes
- **Date Ranges**: Customizable start dates with smart formatting
- **Professional Styling**: Custom themes, logos, and annotations

### **Data Processing**
- **Automatic Alignment**: Multiple series aligned by date
- **Missing Data Handling**: Graceful treatment of incomplete data
- **Frequency Support**: Quarterly, monthly, annual data
- **Multi-Region**: Compare indicators across countries

### **OpenBB Integration**
- **Dynamic Tables**: Pydantic model-based column generation
- **Chart Widgets**: Native OpenBB chart rendering
- **Parameter Validation**: Real-time series ID validation
- **Error Handling**: User-friendly error messages

---

## 🚀 Getting Started

### **Installation**
```bash
# Install the extension
pip install openbb-dbnomics

# Or from source
git clone <repository>
cd openbb_dbnomics
pip install -e .
```

### **Basic Usage**
```python
# In OpenBB Platform
from openbb import obb

# Browse providers
providers = obb.dbnomics.providers()

# Search datasets
datasets = obb.dbnomics.datasets(search="GDP")

# Get series data
series = obb.dbnomics.series_table(
    provider="IMF",
    dataset="IFS", 
    freq="Q",
    ref_area="US",
    indicators="NGDP_D_SA_IX,NGDP_SA_XDC"
)
```

---

## 📈 Use Cases

### **Economic Research**
- **GDP Analysis**: Compare nominal vs real GDP across countries
- **Inflation Studies**: Analyze CPI and PPI trends
- **Employment Data**: Track unemployment rates and labor statistics

### **Financial Analysis**
- **Cross-Country Comparison**: Compare economic indicators across regions
- **Time Series Analysis**: Study trends and patterns in economic data
- **Policy Impact**: Analyze effects of monetary and fiscal policies

### **Data Exploration**
- **Discovery**: Find new datasets and indicators
- **Validation**: Verify data availability before analysis
- **Documentation**: Access comprehensive metadata for data sources

---

## 🐛 Debugging

### **Enabling Debug Print Statements**

The codebase includes comprehensive debugging print statements that are commented out by default for production use. To enable debugging:

#### **1. API Communication Debugging**
In `openbb_dbnomics/utils/providers.py`:
```python
# Uncomment these lines to debug API calls:
# print("Status:", response.status_code)
# print("Fetching:", url)
# print("Final requested URL:", resp.url)
# print("Raw API response for", series_id, ":", data)
```

#### **2. Data Processing Debugging**
```python
# Uncomment to debug data processing:
# print("Fetching series directly for:", indicators)
# print(f"No docs for {series_id}")
# print(f"No data for {series_id}")
# print("Returning records:", df_merged.to_dict(orient="records"))
```

#### **3. Series Discovery Debugging**
In `openbb_dbnomics/router.py`:
```python
# Uncomment to debug series discovery:
# print("Unique REF_AREA codes in first 10,000:", ref_areas)
```

#### **4. Quick Debug Mode**
Create a debug configuration by uncommenting all debug statements:
```bash
# In providers.py, search for "# print(" and remove the "# " prefix
# This will enable comprehensive logging for troubleshooting
```

### **Debugging Workflow**

1. **Enable Debug Statements**: Uncomment relevant print statements
2. **Run Your Query**: Execute the problematic operation
3. **Check Console Output**: Look for debug information
4. **Analyze Issues**: Use debug output to identify problems
5. **Disable Debug**: Re-comment print statements when done

### **Common Debug Scenarios**

#### **API Connection Issues**
```python
# Enable these to debug API connectivity:
# print("Status:", response.status_code)
# print("Fetching:", url)
```

#### **Data Retrieval Problems**
```python
# Enable these to debug data fetching:
# print("Raw API response for", series_id, ":", data)
# print(f"No docs for {series_id}")
# print(f"No data for {series_id}")
```

#### **Series Alignment Issues**
```python
# Enable this to debug multi-series alignment:
# print("Returning records:", df_merged.to_dict(orient="records"))
```

### **Logging Alternative**

For more sophisticated debugging, consider using Python's logging module:
```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace print statements with:
logger.debug("Fetching series directly for: %s", indicators)
logger.info("API response received")
logger.error("No data found for series: %s", series_id)
```

---

## 🔧 Technical Requirements

- **Python**: 3.8+
- **OpenBB Platform**: v4.0+
- **Dependencies**: FastAPI, pandas, plotly, requests
- **External API**: DBNomics.world (free, no authentication required)

---

🦋 Made with [openbb cookiecutter](https://github.com/openbb-finance/openbb-cookiecutter).
