# Orby DevTools

**Orby DevTools** is a tool for developing isolated Python applications for the Orby platform. It allows you to create, validate and build applications in a protected `.orby` format for running through Orby-compatible environments.

## Quiq start

### Install
```bash
pip install orby-devtools
```

### Basic usage
1. Create a project:
```bash
orbydev new myapp --template=default
```
2. Build in `.orby`:
```bash
orbydev build myapp
```

CLI Commands

| Command | Description |
|---------|----------|
| `new <name> <path> [--template=...]` | Create a project in the specified directory |
| `build <path> <save_at>` | Build project from the directory in `.orby` |
| `projects` | List all projects |
| `rmproject <name> <rmdir (t/f)>` | Delete a project |
| `templates` | List of all templates |
| `savetemplate <name> <path>` | Save directory as a template |
| `rmtemplate <name>` | Delete template |

## Project structure
```
myapp/
├── main.py              # Entry point
├── manifest.json        # Configuration
```

## Example `manifest.json`
```json
{
  "name": "Orby app",
  "version": "0.1.0",
  "author": "Your name",
  "description": "My Orby app",
  "permissions": {},
  "entry_point": "main.py",
  "requirements": {}
}
```

## Useful
- [Bug Tracker](https://github.com/wladisslaw/orby-devtools/issues)
- Compatibility: Python 3.10+
- Version: 25.5.1
- Status: Alfa