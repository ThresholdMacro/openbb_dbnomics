"""openbb_dbnomics router command example."""

import requests
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (ExtraParams, ProviderChoices,
                                                StandardParams)
from openbb_core.app.query import Query
from openbb_core.app.router import Router
from pydantic import BaseModel, create_model, Field
from fastapi import Query
from openbb_dbnomics.utils.providers import DBNomicsClient
from fastapi.middleware.cors import CORSMiddleware
import re
from openbb_core.provider.abstract.data import Data  # Use this as base for OpenBB compatibility
from openbb_dbnomics.utils.myplot import plot_ts
import pandas as pd
from fastapi.responses import JSONResponse
import json
from datetime import datetime
import numpy as np
from openbb_dbnomics.dashboard import router as dashboard_router

# Main OpenBB router
router = Router(prefix="")
# API router for endpoints
api_router = Router(prefix="")
client = DBNomicsClient()

# Include dashboard router in the API router
api_router.include_router(dashboard_router, prefix="/dashboard")

@api_router.api_router.get("/providers", tags=["Providers"])
def get_providers():
    client = DBNomicsClient()
    return client.get_providers()

@api_router.api_router.get("/datasets", tags=["Datasets"])
def get_datasets(search: str = Query(..., description="Search term for datasets")):
    client = DBNomicsClient()
    return client.get_datasets(search_term=search)

@api_router.api_router.get("/series", tags=["Series"])
def get_series(
    provider: str = Query(..., description="Provider code, e.g., 'IMF'"),
    dataset: str = Query(..., description="Dataset code, e.g., 'IFS'"),
    name_filter: str = Query(None, description="Filter by substring in series_name"),
    ref_area: str = Query(None, description="Filter by REF_AREA code (e.g., 'US')"),
    limit: int = Query(100, description="Max number of series to return")
):
    client = DBNomicsClient()
    # Fetch a large batch of series (API does not support dimension filtering)
    series = client.get_series(provider_code=provider, dataset_code=dataset, limit=10000)
    # Filter by REF_AREA code if provided
    if ref_area:
        series = [s for s in series if s.get("REF_AREA") == ref_area]
    # Filter by name_filter if provided
    if name_filter:
        series = [s for s in series if name_filter.lower() in s.get("series_name", "").lower()]
    # Apply limit
    series = series[:limit]
    # After fetching series
    ref_areas = set(s.get("REF_AREA") for s in series if "REF_AREA" in s)
    # print("Unique REF_AREA codes in first 10,000:", ref_areas)
    return series

@api_router.api_router.get("/series/ref_areas", tags=["Series"])
def get_ref_areas(
    provider: str = Query(..., description="Provider code, e.g., 'IMF'"),
    dataset: str = Query(..., description="Dataset code, e.g., 'IFS'")
):
    client = DBNomicsClient()
    metadata = client.get_dataset_metadata(provider, dataset)
    dimensions = metadata.get("dimensions_values_labels", {})
    ref_area_dict = dimensions.get("REF_AREA", {})
    ref_areas = [{"code": code, "name": name} for code, name in ref_area_dict.items()]
    ref_areas = sorted(ref_areas, key=lambda x: x["name"])
    return ref_areas

@api_router.api_router.get("/series/indicators", tags=["Series"])
def get_indicators(
    provider: str = Query(..., description="Provider code, e.g., 'IMF'"),
    dataset: str = Query(..., description="Dataset code, e.g., 'IFS'")
):
    client = DBNomicsClient()
    metadata = client.get_dataset_metadata(provider, dataset)
    dimensions = metadata.get("dimensions_values_labels", {})
    indicator_dict = dimensions.get("INDICATOR", {})
    indicators = [{"code": code, "name": name} for code, name in indicator_dict.items()]
    indicators = sorted(indicators, key=lambda x: x["name"])
    return indicators

@api_router.api_router.get("/series/table", response_model=list)
def get_series_table(
    provider: str = Query(...),
    dataset: str = Query(...),
    freq: str = Query(...),
    ref_area: str = Query(...),
    indicators: str = Query(...)
):
    indicator_list = [i.strip() for i in indicators.split(",") if i.strip()]
    records = client.get_multi_series_aligned(provider, dataset, freq, ref_area, indicator_list)
    # Dynamically build fields for the model
    fields = {
        "date": (str, Field(title="Date", description="Date of observation"))
    }
    for ind in indicator_list:
        fields[ind] = (float, Field(title=ind, description=f"{ind} value"))
    DynamicData = create_model("DynamicData", __base__=Data, **fields)
    # Convert each record (dict) to a model instance
    return [DynamicData.model_validate(row) for row in records]

@api_router.api_router.get("/series/chart")
def get_series_chart(
    provider: str = Query(...),
    dataset: str = Query(...),
    freq: str = Query(...),
    ref_area: str = Query(...),
    indicators: str = Query(...),
    nome: str = Query("DBNomics Chart", description="Chart title"),
    units: str = Query("", description="Y-axis units"),
    chart: str = Query("line", description="Chart type: line, bar, regression, distribution, etc."),
    source: str = Query("Source: DBNomics", description="Source annotation"),
    theme: str = Query("light", description="Theme: light or dark"),
    startdate: str = Query("1990-01-01", description="Start date for chart (YYYY-MM-DD or YYYY-Qn)"),
    change: str = Query("level", description="Change type: level, yoy, qoq")
):
    indicator_list = [i.strip() for i in indicators.split(",") if i.strip()]
    records = client.get_multi_series_aligned(provider, dataset, freq, ref_area, indicator_list)
    if not records:
        return JSONResponse({"error": "No data found for the given parameters."}, status_code=404)
    df = pd.DataFrame(records)
    if "date" in df.columns:
        df = df.set_index("date")
        # Filter by startdate (support YYYY-MM-DD and YYYY-Qn)
        def date_filter(date_str):
            if re.match(r"^\d{4}-Q\d$", startdate):
                # Quarterly format
                return date_str >= startdate
            else:
                # Try to parse as date
                try:
                    return date_str >= startdate
                except Exception:
                    return True
        df = df[df.index.map(date_filter)]
    
    # Apply change calculations BEFORE plotting
    df = apply_change(df, change, freq)
    
    # Update title and y-axis label BEFORE plotting
    if change == "yoy":
        nome += " (Year-on-Year % Change)"
        units = "YoY %"
    elif change == "qoq":
        nome += " (Quarter-on-Quarter % Change)"
        units = "QoQ %"

    # Clean NaN values for JSON serialization
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.where(pd.notnull(df), None)
    
    # Adjust nticks for xaxis based on number of visible points
    n_points = len(df)
    nticks = min(10, max(4, n_points // 20)) if n_points > 0 else 4

    fig = plot_ts(df, nome=nome, units=units, chart=chart, source=source, theme=theme)
    # Extract series and layout for OpenBB chart widget
    series = []
    for trace in fig.data:
        if hasattr(trace, 'x') and hasattr(trace, 'y') and trace.x is not None and trace.y is not None:
            # Clean NaN values from y data before JSON serialization
            y_clean = []
            for val in trace.y:
                if isinstance(val, (int, float)) and (np.isnan(val) or np.isinf(val)):
                    y_clean.append(None)
                else:
                    y_clean.append(val)
            
            series.append({
                "name": getattr(trace, 'name', None) or '',
                "x": list(trace.x),
                "y": y_clean,
                "type": "line"
            })
    layout = fig.layout.to_plotly_json()
    layout_filtered = {
        "title": {
            "text": nome,
            "font": {"size": 22, "color": "#FFFFFF" if theme == "dark" else "#0D1018"},
            "x": 0.5,  # Center the title
            "xanchor": "center"
        },
        "yaxis": {**layout.get("yaxis", {}), "nticks": 8},
        "xaxis": {**layout.get("xaxis", {}), "nticks": 4, "tickangle": 0},
        "legend": layout.get("legend", {}),
        "annotations": [{
            "text": source,
            "xref": "paper",
            "yref": "paper",
            "x": 0,
            "y": -0.25,  # Lowered to ensure visibility
            "showarrow": False,
            "font": {"size": 12, "color": "#cccccc"},
            "align": "left"
        }],
        "images": [
            {
                "source": "https://raw.githubusercontent.com/ThresholdMacro/ThresholdMacro/main/Images/Sphere_no_letters.png",
                "xref": "paper",
                "yref": "paper",
                "x": 1.0,
                "y": -0.25,
                "sizex": 0.13,  # Slightly smaller for more space
                "sizey": 0.13,
                "xanchor": "right",
                "yanchor": "bottom",
                "sizing": "contain",
                "opacity": 1,
                "layer": "below"
            }
        ]
    }
    if theme == "dark":
        layout_filtered["paper_bgcolor"] = "#1e3142"
        layout_filtered["plot_bgcolor"] = "#1e3142"
        layout_filtered["font"] = {"color": "#FFFFFF"}
    else:
        layout_filtered["paper_bgcolor"] = "#FAFAFA"
        layout_filtered["plot_bgcolor"] = "#FAFAFA"
        layout_filtered["font"] = {"color": "#0D1018"}
    return {"data": series, "layout": layout_filtered}

def apply_change(df, change_type, freq):
    df = df.copy()
    if change_type == "yoy":
        periods = 4 if freq.upper() == "Q" else 12 if freq.upper() == "M" else 1
        for col in df.columns:
            if col != "date":
                df[col] = df[col].astype(float).pct_change(periods=periods) * 100
    elif change_type == "qoq":
        periods = 1
        for col in df.columns:
            if col != "date":
                df[col] = df[col].astype(float).pct_change(periods=periods) * 100
    # else: do nothing for 'level'
    return df

# Register the API router with the main OpenBB router
router.include_router(api_router)
