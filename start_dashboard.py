#!/usr/bin/env python3
"""
Simple DBNomics Dashboard Launcher
Run with: uvicorn start_dashboard:app --host 0.0.0.0 --port 8000 --reload
"""

import sys
import os
from pathlib import Path

# Add the app to Python path
app_path = Path(__file__).parent / "openbb_dbnomics"
sys.path.insert(0, str(app_path))

# Import the FastAPI app and include dashboard
from openbb import api_app
from dashboard import router as dashboard_router

# Include dashboard router
api_app.include_router(dashboard_router.api_router, prefix="/dashboard")

app = api_app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DBNomics Dashboard...")
    print("📊 Dashboard: http://localhost:8000/dashboard/config")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🎯 App Config: http://localhost:8000/app.json")
    print("📋 Widgets: http://localhost:8000/widgets.json")
    print("\n💡 Quick Access:")
    print("- Full Dashboard: http://localhost:8000/dashboard/config")
    print("- Quick Start: http://localhost:8000/dashboard/quick-start")
    print("- Examples: http://localhost:8000/dashboard/examples")
    print("\nℹ️  For auto-reload, run:")
    print("   uvicorn start_dashboard:app --host 0.0.0.0 --port 8000 --reload")
    print("   (instead of python start_dashboard.py)")
    uvicorn.run(app, host="0.0.0.0", port=8000) 