#!/usr/bin/env python3
"""
DBNomics Data Explorer App Launcher
"""

import sys
import os
from pathlib import Path

# Add the app to Python path
app_path = Path(__file__).parent / "openbb_dbnomics"
sys.path.insert(0, str(app_path))

# Import and run the app
from openbb_dbnomics.openbb import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DBNomics Data Explorer...")
    print("📊 Access the dashboard at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🎯 App configuration at: http://localhost:8000/app.json")
    print("📋 Widgets configuration at: http://localhost:8000/widgets.json")
    print("\n💡 Tips:")
    print("- Use Ctrl+C to stop the server")
    print("- The app will automatically reload when you make changes")
    print("- Check the dashboard endpoints for guided workflows")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 