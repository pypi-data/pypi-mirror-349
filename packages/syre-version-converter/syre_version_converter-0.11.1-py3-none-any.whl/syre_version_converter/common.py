import os
import io
import json
from typing import Optional, Any

from . import paths


def project_data_path(project_path: str) -> Optional[str]:
    """Returns the relative path to the project's data root.

    Args:
        project_path (str): Path to the project's root.

    Returns:
        Optional[str]: Relative path to the project's data root.
    """
    with open(paths.project_properties_of(project_path), "r") as f:
        project = json.load(f)

    data_root = project["data_root"]
    if not data_root:
        return None

    return os.path.join(project_path, data_root)


def project_paths() -> list[str]:
    """
    Returns:
        list[str]: All registered project paths.
    """
    with open(paths.config_project_manifest(), "r") as f:
        projects = json.load(f)

    return projects

def current_user() -> Optional[str]:
    """
    Returns:
        Optional[str]: Current user.
    """
    with open(paths.config_local_settings(), "r") as f:
        config = json.load(f)
        return config["user"]

def json_overwrite(obj: Any, f: io.TextIOWrapper):
    """Overwrite a file's contents with the JSON serialization of the object.
    """
    f.seek(0)
    json.dump(obj, f, indent=4)
    f.truncate()