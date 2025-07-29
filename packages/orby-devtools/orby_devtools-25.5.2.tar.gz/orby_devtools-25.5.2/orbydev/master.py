from pathlib import Path

MAIN_DIR = Path(__file__).parent
TEMPLATES_DIR = MAIN_DIR / "templates"
if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

DEVTOOLS_DATA = Path.home() / ".orby" / "devtools" 
DEVTOOLS_DATA.mkdir(exist_ok=True, parents=True)

PROJECTS_DB = DEVTOOLS_DATA / "projects.json"
if not PROJECTS_DB.exists():
    PROJECTS_DB.write_text("{}", "utf-8")