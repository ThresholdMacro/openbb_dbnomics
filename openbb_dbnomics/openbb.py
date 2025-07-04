from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openbb_dbnomics.router import router
from fastapi.responses import JSONResponse
from openbb_core.app.model.extension import Extension
import requests
import pandas as pd

# Create the Extension object for obbject registration
app = Extension(
    name="openbb_dbnomics",
    description="Comprehensive financial and economic data discovery and visualization powered by DBNomics.world"
)

# Create the FastAPI app for the API
api_app = FastAPI(
    title="OpenBB DBNomics Extension",
    description="API for DBNomics data via OpenBB Platform",
    version="0.1.0"
)

# --- CORS middleware ---
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev, "*" is fine. For production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- End CORS middleware ---

api_app.include_router(router.api_router)

@api_app.get("/app.json")
def app_json():
    """Get app configuration for OpenBB Platform."""
    return JSONResponse({
        "name": "DBNomics Data Explorer",
        "description": "Comprehensive financial and economic data discovery and visualization powered by DBNomics.world",
        "version": "1.0.0",
        "author": "OpenBB Community",
        "category": "Data & Analytics",
        "tags": ["economic data", "financial data", "time series", "visualization", "IMF", "World Bank"],
        "logo": "https://raw.githubusercontent.com/ThresholdMacro/ThresholdMacro/main/Images/Sphere_no_letters.png",
        "icon": "📊",
        "color": "#1e3142",
        "repository": "https://github.com/yourusername/openbb-dbnomics",
        "website": "https://dbnomics.world",
        "license": "MIT",
        "dependencies": {
            "python": ">=3.8",
            "openbb": ">=4.0.0"
        },
        "features": [
            "150+ data providers (IMF, World Bank, ECB, BIS, etc.)",
            "Multi-indicator time series analysis",
            "Interactive charts with multiple chart types",
            "Year-over-Year and Quarter-over-Quarter change calculations",
            "Professional charting with custom theming",
            "Real-time data validation",
            "Comprehensive data discovery tools"
        ],
        "dashboard": {
            "name": "DBNomics Data Explorer",
            "description": "Complete financial data discovery and analysis dashboard",
            "layout": "grid",
            "defaultView": "discovery",
            "endpoint": "/dashboard/config"
        }
    })

@api_app.get("/widgets.json")
def widgets_json():
    return JSONResponse([
        {
            "name": "DBNomics Providers Table",
            "description": "Fetch and display DBNomics providers as a table.",
            "category": "data",
            "type": "table",
            "endpoint": "/providers",
            "gridData": { "x": 0, "y": 0, "w": 20, "h": 15 }
        },
        {
            "name": "DBNomics Datasets Table",
            "description": "Search and display datasets by provider code(s) or keyword(s).",
            "category": "data",
            "type": "table",
            "endpoint": "/datasets",
            "params": [
                {
                    "paramName": "search",
                    "label": "Provider code(s) or keyword(s)",
                    "value": "IMF",
                    "show": True,
                    "description": "Enter one or more provider codes or keywords, separated by commas (e.g., IMF, GDP)"
                }
            ],
            "gridData": { "x": 16, "y": 0, "w": 20, "h": 15 }
        },
        {
            "name": "DBNomics REF_AREA Table",
            "description": "Browse available countries/regions for the selected dataset.",
            "category": "data",
            "type": "table",
            "endpoint": "/series/ref_areas",
            "params": [
                {
                    "paramName": "provider",
                    "label": "Provider code",
                    "value": "IMF",
                    "show": True
                },
                {
                    "paramName": "dataset",
                    "label": "Dataset code",
                    "value": "IFS",
                    "show": True
                }
            ],
            "columns": [
                { "field": "code", "label": "Code" },
                { "field": "name", "label": "Country/Region" }
            ],
            "gridData": {"x": 0, "y": 16, "w": 20, "h": 15}
        },
        {
            "name": "DBNomics Indicator Table",
            "description": "Browse available indicators for the selected dataset.",
            "category": "data",
            "type": "table",
            "endpoint": "/series/indicators",
            "params": [
                { "paramName": "provider", "label": "Provider code", "value": "IMF", "show": True },
                { "paramName": "dataset", "label": "Dataset code", "value": "IFS", "show": True }
            ],
            "columns": [
                { "field": "code", "label": "Code" },
                { "field": "name", "label": "Indicator" }
            ],
            "gridData": {"x": 16, "y": 16, "w": 20, "h": 15}
        },
        {
            "name": "Dynamic DBNomics Series Table",
            "description": "Time series for selected indicators and country/region.",
            "category": "data",
            "type": "table",
            "endpoint": "/series/table",
            "params": [
                { "paramName": "provider", "label": "Provider", "value": "IMF", "show": True },
                { "paramName": "dataset", "label": "Dataset", "value": "IFS", "show": True },
                { "paramName": "freq", "label": "Frequency", "value": "Q", "show": True },
                { "paramName": "ref_area", "label": "Reference Area", "value": "US", "show": True },
                { "paramName": "indicators", "label": "Indicators (comma-separated)", "value": "NGDP_D_SA_IX,NGDP_SA_XDC", "show": True }
            ],
            "gridData": {"x": 0, "y": 31, "w": 20, "h": 15}
        },
        {
            "name": "Dynamic DBNomics Series Chart",
            "description": "Plot time series for selected indicators and country/region with customizable chart type.",
            "category": "chart",
            "type": "chart",
            "endpoint": "/series/chart",
            "params": [
                { "paramName": "provider", "label": "Provider", "value": "IMF", "show": True },
                { "paramName": "dataset", "label": "Dataset", "value": "IFS", "show": True },
                { "paramName": "freq", "label": "Frequency", "value": "Q", "show": True },
                { "paramName": "ref_area", "label": "Country/Region", "value": "US", "show": True },
                { "paramName": "indicators", "label": "Indicators", "value": "NGDP_D_SA_IX,NGDP_SA_XDC", "show": True },
                { "paramName": "nome", "label": "Chart Title", "value": "US GDP Chart", "show": True },
                { "paramName": "units", "label": "Y-Axis Units", "value": "Index", "show": True },
                { "paramName": "chart", "label": "Chart Type", "value": "line", "show": True, "options": [
                    { "label": "Line", "value": "line" },
                    { "label": "Bar", "value": "bar" },
                    { "label": "Regression", "value": "regression" },
                    { "label": "Distribution", "value": "distribution" },
                    { "label": "Scatter", "value": "scatter" }
                ]},
                { "paramName": "startdate", "label": "Start Date", "value": "1990-01-01", "show": True },
                { "paramName": "change", "label": "Change Type", "value": "level", "show": True, "options": [
                    { "label": "Level", "value": "level" },
                    { "label": "Year-on-Year Change", "value": "yoy" },
                    { "label": "Quarter-on-Quarter Change", "value": "qoq" }
                ]},
                { "paramName": "source", "label": "Source Caption", "value": "Source: DBNomics", "show": True }
            ],
             "gridData": {"x": 21, "y": 31, "w": 20, "h": 15}
        }
    ])

class DBNomicsClient:
    BASE_URL = "https://api.db.nomics.world/v22"

    def get_providers(self):
        url = f"{self.BASE_URL}/providers"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        providers = data.get("providers", [])
        flat_providers = []
        for item in providers:
            if isinstance(item, dict) and "docs" in item and isinstance(item["docs"], dict):
                flat_providers.append(item["docs"].copy())
        return flat_providers