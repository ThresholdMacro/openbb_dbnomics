#!/usr/bin/env python3
"""
Installation script for OpenBB DBNomics Data Explorer App
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def get_openbb_extensions_path():
    """Get the OpenBB Platform extensions directory."""
    # Common OpenBB extensions paths
    possible_paths = [
        os.path.expanduser("~/openbb_platform/extensions"),
        os.path.expanduser("~/.openbb/extensions"),
        os.path.expanduser("~/OpenBB/extensions"),
        os.path.expanduser("~/Library/Application Support/OpenBB/extensions"),
        os.path.expanduser("~/.config/openbb/extensions"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If not found, ask user
    print("OpenBB Platform extensions directory not found in common locations.")
    user_path = input("Please enter the path to your OpenBB Platform extensions directory: ").strip()
    
    if os.path.exists(user_path):
        return user_path
    else:
        print(f"Error: Directory '{user_path}' does not exist.")
        return None

def install_dependencies():
    """Install Python dependencies."""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def copy_app_to_extensions(extensions_path):
    """Copy the app to the OpenBB extensions directory."""
    current_dir = Path.cwd()
    app_name = "openbb_dbnomics"
    target_path = Path(extensions_path) / app_name
    
    print(f"Copying app to: {target_path}")
    
    try:
        # Remove existing installation if it exists
        if target_path.exists():
            shutil.rmtree(target_path)
            print("Removed existing installation")
        
        # Copy the app
        shutil.copytree(current_dir, target_path, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', '*.pyc', '.pytest_cache', 'tests', '*.log'
        ))
        print("✅ App copied successfully!")
        return True
    except Exception as e:
        print(f"❌ Error copying app: {e}")
        return False

def create_app_launcher():
    """Create a simple launcher script."""
    launcher_content = '''#!/usr/bin/env python3
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    launcher_path = Path("launch_dbnomics.py")
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    
    # Make executable
    os.chmod(launcher_path, 0o755)
    print("✅ Created launcher script: launch_dbnomics.py")

def main():
    """Main installation function."""
    print("🚀 OpenBB DBNomics Data Explorer App Installer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manifest.json").exists():
        print("❌ Error: Please run this script from the openbb_dbnomics directory")
        return False
    
    # Get OpenBB extensions path
    extensions_path = get_openbb_extensions_path()
    if not extensions_path:
        print("❌ Could not determine OpenBB extensions directory")
        return False
    
    print(f"📁 OpenBB extensions directory: {extensions_path}")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Copy app to extensions
    if not copy_app_to_extensions(extensions_path):
        return False
    
    # Create launcher script
    create_app_launcher()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart OpenBB Platform")
    print("2. Look for 'DBNomics Data Explorer' in the Apps section")
    print("3. Click on the app to open the dashboard")
    print("4. Or run: python launch_dbnomics.py for standalone mode")
    
    print("\n🔗 Useful URLs:")
    print("- Dashboard: http://localhost:8000")
    print("- API Docs: http://localhost:8000/docs")
    print("- Widgets: http://localhost:8000/widgets.json")
    print("- App Config: http://localhost:8000/app.json")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 