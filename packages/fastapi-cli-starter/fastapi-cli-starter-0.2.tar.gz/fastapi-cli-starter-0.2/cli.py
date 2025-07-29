import sys
import os
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: create-fastapi-app <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]
    destination = Path.cwd() / project_name
    source = Path(__file__).resolve().parent / "fastapi_template"

    if destination.exists():
        print(f"❌ Directory '{destination}' already exists.")
        sys.exit(1)

    try:
        shutil.copytree(source, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"✅ FastAPI app created at: {destination}")
        print("➡️  Next steps:")
        print(f"   cd {project_name}")
        print("   pip install -r requirements.txt")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
