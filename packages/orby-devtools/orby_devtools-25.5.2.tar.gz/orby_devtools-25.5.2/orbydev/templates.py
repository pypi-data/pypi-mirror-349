from typing import Dict, Tuple
import json
from pathlib import Path
import shutil

from .master import TEMPLATES_DIR


class Templates:
    """
    Provides an interface for working with templates.

    Methods:
        templates_list (): Returns a list of all available development templates.
        savetemplate (name, path): Saves a new template.
        remove (name): Deletes the template.
    """

    @staticmethod
    def templates_list() -> Tuple[Dict[str, str], Exception | None]:
        """
        Returns a list of all available development templates.

        Returns:
            Tuple containing:
                Dict[str, str]: A dictionary of template information, where:
                    - key (str): The name of the template.
                    - value (str): Template description from manifest.json
                            (empty string if manifest is missing or invalid).
                Exception | None: Exception if an error occurred while reading templates, 
                            None if no error occurred.
        """

        try:
            templates = {}
            
            for template_dir in TEMPLATES_DIR.iterdir():
                if template_dir.is_dir():
                    manifest_path = template_dir / "manifest.json"
                    template_info = ""

                    if manifest_path.exists():
                        try:
                            with open(manifest_path, 'r') as f:
                                manifest = json.load(f)
                                template_info = manifest.get("description", "")
                        except json.JSONDecodeError as e:
                            template_info = "Invalid manifest.json"
                    
                    templates[template_dir.name] = template_info
            
            return templates, None

        except Exception as e:
            return {}, e
    
    @staticmethod
    def savetemplate(name: str, path: str) -> Tuple[bool, Exception | None]:
        """
        Saves the new template.

        Args:
            name (str): The name of the template to be saved.
            path (str): The path to the folder being saved as a template.
            
        Returns:
            Tuple containing:
                bool: Execution status.
                Exception | None: Exception if an error occurred while saving the template, 
                            None if no error occurred.
        """

        try:
            exists_templates, exception = Templates.templates_list()
            if exception is not None:
                raise Exception(f"Problems with general files. Exception: {exception}") from exception
            
            if name in exists_templates.keys():
                raise Exception(f"Project with name '{name}' already exists.")
            
            _from = Path(path)
            manifest = _from / "manifest.json"
            if not manifest.exists():
                raise Exception(f"It is no `manifest.json` in '{_from}'")

            target_path = TEMPLATES_DIR / name
            shutil.copytree(_from, target_path)

        except Exception as e:
            return False, e
    
    @staticmethod
    def remove(name: str) -> Tuple[bool, Exception | None]:
        """
        Deletes the template.

        Args:
            name (str): The name of the template to be deleted.

        Returns:
            Tuple containing:
                bool: Execution status.
                Exception | None: Exception if an error occurred while deleting the template, 
                            None if no error occurred.
        """

        try:
            templates, e = Templates.templates_list()

            if e is not None:
                raise Exception(f"Problems with general files. Exception: {e}") from e
            if name not in templates.keys():
                raise Exception(f"Template with name '{name}' does not exists.")
            
            shutil.rmtree(TEMPLATES_DIR / name)

            return True, None

        except Exception as e:
            return False, e