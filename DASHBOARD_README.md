# DBNomics Data Explorer Dashboard

A comprehensive financial and economic data discovery and visualization dashboard powered by DBNomics.world.

## Quick Start

### Option 1: Simple Shell Script
```bash
./start.sh
```

### Option 2: Python Script
```bash
python start_dashboard.py
```

### Option 3: Direct Uvicorn
```bash
uvicorn start_dashboard:app --host 0.0.0.0 --port 8000 --reload
```

## Dashboard Access

Once running, access the dashboard at:
- **Main Dashboard**: http://localhost:8000/api/v1/openbb_dbnomics/dashboard/dashboard/config
- **Quick Start Guide**: http://localhost:8000/api/v1/openbb_dbnomics/dashboard/dashboard/quick-start
- **Examples**: http://localhost:8000/api/v1/openbb_dbnomics/dashboard/dashboard/examples
- **API Documentation**: http://localhost:8000/docs
- **Root URL**: http://localhost:8000/ (redirects to dashboard)

## Dashboard Features

The dashboard includes 6 main widgets arranged in a grid layout:

1. **Data Providers** - Browse 150+ international data sources
2. **Dataset Search** - Find datasets within providers
3. **Available Regions** - Countries and regions for selected dataset
4. **Available Indicators** - Economic indicators for selected dataset
5. **Time Series Table** - Display aligned time series data
6. **Dynamic Chart** - Create customizable charts with multiple chart types

## Widget Layout

The dashboard uses a 24-column grid layout with widgets positioned as follows:

- **Providers**: x=0, y=0, w=12, h=8
- **Datasets**: x=12, y=0, w=12, h=8
- **Regions**: x=0, y=8, w=12, h=8
- **Indicators**: x=12, y=8, w=12, h=8
- **Series Table**: x=0, y=16, w=12, h=10
- **Series Chart**: x=12, y=16, w=12, h=10

## Data Sources

The dashboard connects to DBNomics.world API, providing access to:
- IMF (International Monetary Fund)
- World Bank
- ECB (European Central Bank)
- BIS (Bank for International Settlements)
- National statistical offices
- And 150+ other data providers

## Chart Types

Available chart types:
- Line charts
- Bar charts
- Regression analysis
- Distribution plots
- Scatter plots

## Change Calculations

Support for:
- Level data
- Year-over-Year changes
- Quarter-over-Quarter changes

## Stop the Server

Press `Ctrl+C` in the terminal to stop the dashboard server. 