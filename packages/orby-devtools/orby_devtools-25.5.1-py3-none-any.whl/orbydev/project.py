from pathlib import Path
from typing import Dict, Tuple
import shutil
import json
import zipfile

from .master import TEMPLATES_DIR, PROJECTS_DB


class Projects:
    """
    Provides an interface for working with projects.

    Methods:
        new (name, path, template): Creates a new Orby project and returns the runtime code.
        build (path, save_at): Builds the project into a final .orby application.
        projects_list (): Returns a list of all projects created via `orby-devtools`.
        remove_project (name, remove_dir): Removes a project from the `orby-devtools` project list.
    """

    @staticmethod
    def new(name: str, path: str = "", template: str = "default") -> Tuple[bool, Exception | None]:
        """
        Creates a new Orby project and returns the runtime code.

        Args:
            name (str): The name of the project to be created.
            path (str): The destination directory of the project. If not specified, a directory with the project name will be created.
            template (str, optional): The template to use. The default is `"default"`.
                
        Returns:
            Tuple containing:
                bool: Execution status.
                Exception | None: Exception if an error occurred during project creation, 
                            None if no error occurred.
        """

        try:
            target_dir = Path(path) if path != ""  else Path(name)
            template_dir = TEMPLATES_DIR / template

            if not template_dir.exists():
                raise ValueError(f"Template '{template}' not found!")
            
            exists_projects, e = Projects.projects_list()

            if e is not None:
                raise Exception(f"Problems with general files. Exception: {e}") from e
            
            if name in exists_projects.keys():
                raise Exception(f"Project with name '{name}' already exists. Project path - '{exists_projects[name]['path']}'")
            
            shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)

            manifest_text = (target_dir / "manifest.json").read_text("utf-8")
            manifest_json = json.loads(manifest_text)
            manifest_json["name"] = name
            manifest_text = json.dumps(manifest_json, ensure_ascii=False, indent=4)
            (target_dir / "manifest.json").write_text(manifest_text, "utf-8")

            projects = json.loads(PROJECTS_DB.read_text("utf-8"))
            projects[name] = {"path": str(target_dir.absolute()), "template": template}

            PROJECTS_DB.write_text(json.dumps(projects, indent=4, ensure_ascii=False), "utf-8")

            return True, None
        except Exception as e:
            return False, e
    
    @staticmethod
    def build(path: str, save_at: str = "") -> Tuple[bool, Exception | None]:
        """
        Builds the project into a final .orby application.

        Args:
            path (str): The path to the folder of the project being built.
            save_at (str, optional): Where to save the file. If not specified, it will be saved in the current directory.
            
        Returns:
            Tuple containing:
                bool: Execution status.
                Exception | None: Exception if an error occurred while building the project, 
                            None if no error occurred.
        """

        try:
            project_dir = Path(path)
            manifest = json.loads((project_dir / "manifest.json").read_text())

            if "name" not in manifest:
                raise ValueError("Manifest must contain 'name' field!")
            
            save_path = Path(save_at if save_at != "" else ".").absolute() / f"{manifest['name']}.orby"
            with zipfile.ZipFile(save_path, "w") as zipf:
                for file in project_dir.glob("**/*"):
                    if file.is_file():
                        zipf.write(file, file.relative_to(project_dir))
            
            return True, None
        except Exception as e:
            return False, e
    
    @staticmethod
    def projects_list() -> Tuple[Dict[str, dict], Exception | None]:
        """
        Returns a list of all projects created via `orby-devtools`.

        Returns:
            Tuple containing:
                Dict[str, dict]: A dictionary with information about the projects, where:
                    - key (str): Project name.
                    - value (dict): Information about the project.
                Exception | None: Exception if an error occurred while reading projects, 
                            None if no error occurred.
        """
        try:
            return json.loads(PROJECTS_DB.read_text("utf-8")), None
        except Exception as e:
            return {}, e
    
    @staticmethod
    def remove(name: str, remove_dir: bool = False) -> Tuple[bool, Exception | None]:
        """
        Removes the project from the `orby-devtools` project list.

        Args:
            name (str): The name of the project to be removed.
            remove_dir (bool, optional): Whether to remove the folder where the project is stored. The default is `False`.

        Returns:
            Tuple containing:
                bool: Execution status.
                Exception | None: Exception if an error occurred while deleting the project, 
                            None if no error occurred.
        """

        try:
            projects, e = Projects.projects_list()

            if e is not None:
                raise Exception(f"Problems with general files. Exception: {e}") from e
            if name not in projects.keys():
                raise Exception(f"Project with name '{name}' does not exists.")
            
            project_data = projects[name]
            
            if remove_dir:
                shutil.rmtree(project_data["path"])
            
            projects.pop(name, None)
            PROJECTS_DB.write_text(json.dumps(projects, indent=4, ensure_ascii=False), "utf-8")

            return True, None

        except Exception as e:
            return False, e