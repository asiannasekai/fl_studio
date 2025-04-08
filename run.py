import streamlit.web.cli as stcli
import sys
import os
from pathlib import Path

def main():
    try:
        # Get the absolute path to the project root
        project_root = Path(__file__).parent.absolute()
        
        # Add src directory to Python path
        src_path = str(project_root / "src")
        if src_path not in sys.path:
            sys.path.append(src_path)
        
        # Verify the app file exists
        app_path = project_root / "src" / "frontend" / "app.py"
        if not app_path.exists():
            print(f"Error: Could not find app.py at {app_path}")
            sys.exit(1)
        
        # Run the Streamlit app
        sys.argv = [
            "streamlit",
            "run",
            str(app_path),
            "--global.developmentMode=false",
            "--server.headless=true",
            "--browser.serverAddress=localhost",
            "--server.port=8501"
        ]
        sys.exit(stcli.main())
    except Exception as e:
        print(f"Error running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 