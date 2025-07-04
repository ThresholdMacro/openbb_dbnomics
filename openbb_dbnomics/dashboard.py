"""Dashboard configuration for DBNomics Data Explorer app."""

from typing import Dict, List, Any
from openbb_core.app.router import Router
from fastapi.responses import JSONResponse

router = Router(prefix="")

@router.api_router.get("/dashboard/config", tags=["Dashboard"])
def get_dashboard_config():
    """Get dashboard configuration for the DBNomics app."""
    return JSONResponse({
        "name": "DBNomics Data Explorer",
        "description": "Complete financial data discovery and analysis dashboard",
        "version": "1.0.0",
        "layout": {
            "type": "grid",
            "columns": 40,
            "rows": 50,
            "gap": 16,
            "padding": 16
        },
        "defaultView": "discovery",
        "views": {
            "discovery": {
                "name": "Data Discovery",
                "description": "Explore data providers and datasets",
                "icon": "🔍",
                "widgets": ["providers", "datasets"]
            },
            "selection": {
                "name": "Data Selection", 
                "description": "Choose regions and indicators",
                "icon": "📋",
                "widgets": ["regions", "indicators"]
            },
            "analysis": {
                "name": "Data Analysis",
                "description": "Visualize and analyze time series data",
                "icon": "📊",
                "widgets": ["series_table", "series_chart"]
            },
            "full": {
                "name": "Full Dashboard",
                "description": "Complete data exploration workflow",
                "icon": "🏠",
                "widgets": ["providers", "datasets", "regions", "indicators", "series_table", "series_chart"]
            }
        },
        "widgets": {
            "providers": {
                "name": "Data Providers",
                "description": "Browse available data providers",
                "type": "table",
                "endpoint": "/providers",
                "position": {"x": 0, "y": 0, "w": 20, "h": 15},
                "config": {
                    "title": "Available Data Providers",
                    "subtitle": "Browse 150+ international data sources",
                    "refreshInterval": 300,
                    "maxRows": 50
                }
            },
            "datasets": {
                "name": "Dataset Search",
                "description": "Search datasets by provider or keyword",
                "type": "table", 
                "endpoint": "/datasets",
                "position": {"x": 16, "y": 0, "w": 20, "h": 15},
                "config": {
                    "title": "Dataset Search",
                    "subtitle": "Find datasets within providers",
                    "defaultParams": {"search": "IMF"},
                    "searchEnabled": True
                }
            },
            "regions": {
                "name": "Available Regions",
                "description": "View available countries/regions",
                "type": "table",
                "endpoint": "/series/ref_areas", 
                "position": {"x": 0, "y": 16, "w": 20, "h": 15},
                "config": {
                    "title": "Available Regions",
                    "subtitle": "Countries and regions for selected dataset",
                    "defaultParams": {"provider": "IMF", "dataset": "IFS"},
                    "sortable": True,
                    "filterable": True
                }
            },
            "indicators": {
                "name": "Available Indicators",
                "description": "Browse available indicators",
                "type": "table",
                "endpoint": "/series/indicators",
                "position": {"x": 16, "y": 16, "w": 20, "h": 15},
                "config": {
                    "title": "Available Indicators", 
                    "subtitle": "Economic indicators for selected dataset",
                    "defaultParams": {"provider": "IMF", "dataset": "IFS"},
                    "searchEnabled": True,
                    "sortable": True
                }
            },
            "series_table": {
                "name": "Time Series Table",
                "description": "Display aligned time series data",
                "type": "table",
                "endpoint": "/series/table",
                "position": {"x": 0, "y": 31, "w": 20, "h": 15},
                "config": {
                    "title": "Time Series Data",
                    "subtitle": "Aligned multi-indicator time series",
                    "defaultParams": {
                        "provider": "IMF",
                        "dataset": "IFS", 
                        "freq": "Q",
                        "ref_area": "US",
                        "indicators": "NGDP_D_SA_IX,NGDP_SA_XDC"
                    },
                    "exportable": True,
                    "sortable": True,
                    "resizable": True
                }
            },
            "series_chart": {
                "name": "Dynamic Chart",
                "description": "Create customizable charts",
                "type": "chart",
                "endpoint": "/series/chart",
                "position": {"x": 21, "y": 31, "w": 20, "h": 15},
                "config": {
                    "title": "Time Series Chart",
                    "subtitle": "Interactive multi-indicator visualization",
                    "defaultParams": {
                        "provider": "IMF",
                        "dataset": "IFS",
                        "freq": "Q", 
                        "ref_area": "US",
                        "indicators": "NGDP_D_SA_IX,NGDP_SA_XDC",
                        "nome": "US GDP Analysis",
                        "units": "Index",
                        "chart": "line",
                        "startdate": "1990-01-01",
                        "change": "level",
                        "source": "Source: DBNomics"
                    },
                    "chartTypes": ["line", "bar", "regression", "distribution", "scatter"],
                    "changeTypes": ["level", "yoy", "qoq"],
                    "exportable": True,
                    "interactive": True
                }
            }
        },
        "theme": {
            "primary": "#1e3142",
            "secondary": "#2c5aa0", 
            "accent": "#4caf50",
            "background": "#fafafa",
            "surface": "#ffffff",
            "text": "#0d1018",
            "textSecondary": "#666666"
        },
        "navigation": {
            "showBreadcrumbs": True,
            "showViewSwitcher": True,
            "showWidgetControls": True,
            "showFullscreenToggle": True
        }
    })

@router.api_router.get("/dashboard/quick-start", tags=["Dashboard"])
def get_quick_start():
    """Get quick start guide for the dashboard."""
    return JSONResponse({
        "title": "Get Started with DBNomics Data Explorer",
        "description": "Follow these steps to begin exploring economic and financial data",
        "steps": [
            {
                "step": 1,
                "title": "Browse Data Providers",
                "description": "Start by exploring the available data providers. You'll find over 150 sources including IMF, World Bank, ECB, BIS, and national statistical offices.",
                "action": "Click on the 'Data Providers' widget to see all available sources",
                "icon": "🏛️",
                "widget": "providers"
            },
            {
                "step": 2,
                "title": "Search for Datasets",
                "description": "Once you've chosen a provider, search for specific datasets. For example, search 'IFS' for International Financial Statistics from the IMF.",
                "action": "Use the 'Dataset Search' widget with keywords like 'GDP', 'inflation', or 'employment'",
                "icon": "🔍",
                "widget": "datasets"
            },
            {
                "step": 3,
                "title": "Select Your Region",
                "description": "Choose the country or region you want to analyze. You can select from countries like US, EU, JP, or regional groupings.",
                "action": "Use the 'Available Regions' widget to browse and select your target region",
                "icon": "🌍",
                "widget": "regions"
            },
            {
                "step": 4,
                "title": "Choose Indicators",
                "description": "Select the economic indicators you want to analyze. Common indicators include GDP, inflation rates, employment data, and more.",
                "action": "Use the 'Available Indicators' widget to browse and select your indicators",
                "icon": "📈",
                "widget": "indicators"
            },
            {
                "step": 5,
                "title": "Visualize Your Data",
                "description": "Create charts and tables with your selected data. You can compare multiple indicators, apply change calculations, and customize the visualization.",
                "action": "Configure the 'Dynamic Chart' widget with your selected parameters",
                "icon": "📊",
                "widget": "series_chart"
            }
        ],
        "examples": [
            {
                "name": "US GDP Analysis",
                "description": "Compare US GDP indicators over time",
                "config": {
                    "provider": "IMF",
                    "dataset": "IFS",
                    "freq": "Q",
                    "ref_area": "US", 
                    "indicators": "NGDP_D_SA_IX,NGDP_SA_XDC",
                    "chart": "line",
                    "change": "yoy"
                }
            },
            {
                "name": "Inflation Comparison",
                "description": "Compare inflation rates across countries",
                "config": {
                    "provider": "IMF",
                    "dataset": "IFS",
                    "freq": "M",
                    "ref_area": "US,EU,JP",
                    "indicators": "PCPI_PC_PP_PT",
                    "chart": "line",
                    "change": "yoy"
                }
            }
        ]
    })

@router.api_router.get("/dashboard/examples", tags=["Dashboard"])
def get_examples():
    """Get example configurations for common use cases."""
    return JSONResponse({
        "examples": [
            {
                "name": "Economic Growth Analysis",
                "description": "Analyze GDP growth trends across major economies",
                "category": "Macroeconomic",
                "config": {
                    "provider": "IMF",
                    "dataset": "IFS",
                    "freq": "Q",
                    "ref_area": "US,EU,JP,CN",
                    "indicators": "NGDP_R_SA_XDC",
                    "chart": "line",
                    "change": "yoy",
                    "nome": "GDP Growth Comparison",
                    "units": "YoY % Change"
                }
            },
            {
                "name": "Inflation Monitoring",
                "description": "Track consumer price inflation trends",
                "category": "Inflation",
                "config": {
                    "provider": "IMF", 
                    "dataset": "IFS",
                    "freq": "M",
                    "ref_area": "US,EU,JP",
                    "indicators": "PCPI_PC_PP_PT",
                    "chart": "line",
                    "change": "yoy",
                    "nome": "Consumer Price Inflation",
                    "units": "YoY % Change"
                }
            },
            {
                "name": "Employment Trends",
                "description": "Monitor employment and unemployment data",
                "category": "Labor",
                "config": {
                    "provider": "IMF",
                    "dataset": "IFS", 
                    "freq": "Q",
                    "ref_area": "US,EU",
                    "indicators": "LUR_PT",
                    "chart": "bar",
                    "change": "level",
                    "nome": "Unemployment Rates",
                    "units": "Percent"
                }
            },
            {
                "name": "Monetary Policy Indicators",
                "description": "Track interest rates and monetary policy",
                "category": "Monetary",
                "config": {
                    "provider": "IMF",
                    "dataset": "IFS",
                    "freq": "M", 
                    "ref_area": "US,EU,JP",
                    "indicators": "FIDR",
                    "chart": "line",
                    "change": "level",
                    "nome": "Policy Interest Rates",
                    "units": "Percent"
                }
            }
        ]
    }) 