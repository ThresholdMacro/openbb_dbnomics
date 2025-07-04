#!/bin/bash

echo "🚀 Starting DBNomics Data Explorer Dashboard..."
echo "📊 Access the dashboard at: http://localhost:8000/dashboard/config"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "🎯 App configuration at: http://localhost:8000/app.json"
echo "📋 Widgets configuration at: http://localhost:8000/widgets.json"
echo ""
echo "💡 Quick Access:"
echo "- Full Dashboard: http://localhost:8000/dashboard/config"
echo "- Quick Start: http://localhost:8000/dashboard/quick-start"
echo "- Examples: http://localhost:8000/dashboard/examples"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the dashboard
cd /Users/meyrick/OpenBB_HA_Extensions/openbb_dbnomics
python start_dashboard.py 