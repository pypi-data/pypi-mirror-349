"""
Converts a Syre project from `0.9.x` directly to `0.11.1`.

# Note
This breaks the typical conversion chain by ckipping intermediate versions.

+
"""

# %%
import os
import platform
import datetime as dt
import json
import logging
import subprocess
import warnings
from glob import glob
from uuid import uuid4 as uuid
from typing import Any, Optional

from . import paths, common

logger = logging.getLogger(__name__)

CONTAINER_PATH = "_container.json"
SCRIPTS_PATH = "_scripts.json"
ASSET_PATH = "_asset.json"
DEFAULT_DATA_DIR = "data"
DEFAULT_ANALYSIS_DIR = "analysis"
SCRIPTS_DIR = "scripts"


# %%
def hide_dir(path: str):
    subprocess.run(["attrib", "+H", path], check=True)


def mkdir_syre(path: str) -> str:
    """Creates a hidden `.syre` folder in the given directory.

    Args:
        path (str): Parent directory.

    Returns:
        str: Path to `syre folder.
    """
    syre_path = os.path.join(path, paths.SYRE_FOLDER)
    if not os.path.exists(syre_path):
        os.mkdir(syre_path)
        if platform.system() == "Windows":
            hide_dir(syre_path)

    return syre_path


def create_project_properties(path: str):
    """Create a `.syre/project.json` file.

    Args:
        path (str): Project's base path.
    """
    (head, name) = os.path.split(path)
    if name == "":
        # NOTE: `os.path.basename` returns "" if there is a trailing slash in the path.
        # This accounts for that.
        name = os.path.basename(head)

    project_path = paths.project_properties_of(path)
    with open(project_path, "w") as f:
        properties = {
            "rid": str(uuid()),
            "name": name,
            "description": None,
            "data_root": DEFAULT_DATA_DIR,
            "analysis_root": DEFAULT_ANALYSIS_DIR,
            "meta_level": 0,
        }
        json.dump(properties, f, indent=4)


def create_project_desktop_settings(path: str):
    """Create a `.syre/desktop_settings.json` file.

    Args:
        path (str): Project's base path.
    """
    settings_path = paths.project_desktop_settings_of(path)
    with open(settings_path, "w") as f:
        settings = {
            "asset_drag_drop_kind": None,
            "disable_analysis_after": None,
        }
        json.dump(settings, f, indent=4)


def create_project_runner_settings(path: str):
    """Create a `.syre/runner_settings.json` file.

    Args:
        path (str): Project's base path.
    """
    settings_path = paths.project_runner_settings_of(path)
    with open(settings_path, "w") as f:
        settings = {
            "python_path": None,
            "r_path": None,
            "continue_on_error": None,
            "max_tasks": None,
        }
        json.dump(settings, f, indent=4)


def create_project_settings(path: str):
    """Create a `.syre/project_settings.json` file.

    + Sets the project creation time to the current time.
    + Sets the project creator to the current user and gives them full permissions.

    Args:
        path (str): Project's base path.
    """
    settings_path = paths.project_settings_of(path)
    user = common.current_user()
    with open(settings_path, "w") as f:
        settings = {
            "local_format_version": "0.11.1",
            "created": dt.datetime.now().isoformat() + "Z",
            "creator": {"Id": user},
            "permissions": {},
        }

        if user is not None:
            settings["permissions"][user] = {
                "read": True,
                "write": True,
                "execute": True,
            }

        json.dump(settings, f, indent=4)


def create_project_analyses(path: str) -> dict[str, str]:
    """Convert analyses to `0.11.1`.

    Args:
        path (str): Project's base path.

    Returns:
        dict[str, str]: Map from analysis path to resource id.
    """
    scripts_path = os.path.join(path, SCRIPTS_DIR)
    user = common.current_user()
    analyses = []
    analysis_map = {}
    for child in os.listdir(scripts_path):
        if not child.endswith(".py"):
            # NOTE: Only Python scripts were supported in `0.9.x`.
            continue

        rid = uuid()
        analysis_map[child] = rid
        analysis = {
            "type": "Script",
            "rid": str(rid),
            "path": child,
            "name": None,
            "description": None,
            "env": {"language": "Python", "cmd": "python3", "args": [], "env": {}},
            "creator": user,
            "created": dt.datetime.now().isoformat() + "Z",
        }
        analyses.append(analysis)

    with open(paths.project_analyses_of(path), "w") as f:
        json.dump(analyses, f, indent=4)


def get_analysis_map(path: str) -> dict[str, str]:
    """
    Args:
        path (str): Project's base path.

    Returns:
        Map from analysis paths to resource ids.
    """
    with open(paths.project_analyses_of(path), "r") as f:
        analyses = json.load(f)

    return {analysis["path"]: analysis["rid"] for analysis in analyses}


def create_project(path: str):
    """Create the project `.syre` folder.

    + Create a `.syre` folder.
    + Create `.syre/project.json`, `.syre/desktop_settings.json`,
    `.syre/runner_settings.json`, and `.syre/project_settings.json` files.

    Args:
        path (str): Project root path.
    """
    if not os.path.exists(path):
        raise RuntimeError(f"Project `{path}` does not exist")

    children = os.listdir(path)
    if paths.SYRE_FOLDER not in children:
        syre_path = mkdir_syre(path)
    else:
        syre_path = paths.syre_dir_of(path)

    children_syre = os.listdir(syre_path)
    if paths.PROJECT_PROPERTIES_FILE not in children_syre:
        create_project_properties(path)
    if paths.PROJECT_DESKTOP_SETTINGS_FILE not in children_syre:
        create_project_desktop_settings(path)
    if paths.PROJECT_RUNNER_SETTINGS_FILE not in children_syre:
        create_project_runner_settings(path)
    if paths.PROJECT_SETTINGS_FILE not in children_syre:
        create_project_settings(path)


def convert_analyses(path: str) -> dict[str, str]:
    """Convert project analyses.

    + Converts analyses.
    + Renames `scripts` dir to `analysis`.

    Args:
        path (str): Project's base path.
    """

    if not os.path.exists(paths.project_analyses_of(path)):
        create_project_analyses(path)

    if SCRIPTS_DIR in os.listdir(path):
        src = os.path.join(path, SCRIPTS_DIR)
        dst = os.path.join(path, DEFAULT_ANALYSIS_DIR)
        os.rename(src, dst)


def convert_metadata(
    metadata: dict[str, Any], parent: Optional[str] = None
) -> dict[str, Any]:
    """Convert metadata into valid values.

    + Converts metadata values that are objects into individual top level items recursively.
    Adds a `.` between keys at each level of recursion.
    e.g. `{"my_obj": {"lvl_1": true}}` becomes `{"myobj.lvl_1": true}`
    e.g. `{"my_list": [true, {"child": 1}]}` becomes `{"my_list.0": true, "my_list.1.child": 1}`

    Args:
        metadata (dict[str, Any]): Input metadata.
        parent (Optional[str], optional): Parent key. Defaults to None.

    Returns:
        dict[str,Any]: Metadata with valid values.
    """
    converted = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            for idx, item in enumerate(value):
                if isinstance(item, dict):
                    converted = {**converted, **convert_metadata(item, f"{key}.{idx}")}
        elif isinstance(value, dict):
            converted = {**converted, **convert_metadata(value, key)}
        else:
            if parent is not None:
                key = f"{parent}.{key}"
            converted[key] = value

    return converted


def create_container_properties(path: str, analysis_map: dict[str, str]):
    """Create container properties from `_container.json` and `_scripts.json`.

    + Transfers container properties.
        - Creates new resource id.
        - Converts metadata.
    + Transfers container scripts to analyses.
    + Creates `.syre/container.json` file.
    + Removes `_container.json` and `_scripts.json` files.

    Args:
        path (str): Container base path.
        analysis_map (dict[str, str]): Map from analysis path to resource id.

    Raises:
        ValueError: If unexpected script path is encountered.
    """
    SCRIPT_ROOT_PREFIX = "root:/../scripts/"

    with open(os.path.join(path, CONTAINER_PATH), "r") as f:
        container = json.load(f)

    if SCRIPTS_PATH in os.listdir(path):
        with open(os.path.join(path, SCRIPTS_PATH), "r") as f:
            scripts = json.load(f)
    else:
        scripts = []

    try:
        metadata = convert_metadata(container.get("metadata", {}))
    except NotImplementedError as err:
        err.add_note(path)
        raise err
    
    properties = {
        "name": container.get("name"),
        "kind": container.get("type"),
        "description": container.get("description"),
        "tags": container.get("tags", []),
        "metadata": metadata,
    }

    analyses = []
    for script in scripts:
        script_path: str = script.get("script")
        if script_path.startswith(SCRIPT_ROOT_PREFIX):
            script_path = script_path.removeprefix(SCRIPT_ROOT_PREFIX)
        else:
            # NOTE: Not sure what other values exist.
            # This is used as a break
            raise ValueError(
                f"[{path}] Script path does not begin with `{SCRIPT_ROOT_PREFIX}`, found `{script_path}`"
            )

        analyses.append(
            {
                "analysis": analysis_map[script_path],
                "autorun": script["autorun"],
                "priority": script["priority"],
            }
        )

    properties = {"rid": str(uuid()), "properties": properties, "analyses": analyses}
    with open(paths.container_properties_of(path), "w") as f:
        json.dump(properties, f, indent=4)

    os.remove(os.path.join(path, CONTAINER_PATH))
    if SCRIPTS_PATH in os.listdir(path):
        os.remove(os.path.join(path, SCRIPTS_PATH))


def create_container_settings(path: str):
    """Create container settings file.

    Args:
        path (str): Container base path.
    """
    settings = {
        "creator": None,
        "created": dt.datetime.now().isoformat() + "Z",
        "permissions": {},
    }

    with open(paths.container_settings_of(path), "w") as f:
        json.dump(settings, f, indent=4)


def create_container_assets(path: str, analysis_map: dict[str, str]):
    """Move assets into base folder and transfer their properties.

    + Moves asset properties into container's assets.
    + Moves files from asset folder to container root.
    + Removes asset folders.

    Args:
        path (str): Container base path.
        analysis_map (dict[str, str]): Map from script path to analysis resource id.
    """
    assets = []
    asset_folders = {}
    for child in os.listdir(path):
        asset_folder = os.path.join(path, child)
        if not os.path.isdir(asset_folder):
            continue
        if ASSET_PATH not in os.listdir(asset_folder):
            continue

        with open(os.path.join(asset_folder, ASSET_PATH), "r") as f:
            asset: dict[str, Any] = json.load(f)

        if "file" not in asset:
            print(path, child, asset)
        asset_file = asset.get("file", child)
        creator = {"User": None}
        if "creator_type" in asset:
            creator_type = asset["creator_type"]
            if creator_type == "script":
                creator_script = asset.get("creator")
                if creator_script is not None:
                    creator_script = os.path.basename(creator_script)
                    if creator_script in analysis_map:
                        creator = {"Script": analysis_map[creator_script]}
            elif creator_type == "user":
                creator = {"User": None}
            else:
                # NOTE: Not sure what other values exist.
                # This is used aas a break
                raise ValueError(
                    f"[{os.path.join(path, child)}] Unknown creator type `{creator_type}`"
                )

        try:
            metadata = convert_metadata(asset.get("metadata", {}))
        except NotImplementedError as err:
            err.add_note(f"{path}, {child}")
            raise err
        
        assets.append(
            {
                "rid": str(uuid()),
                "properties": {
                    "created": dt.datetime.now().isoformat(timespec="seconds") + "Z",
                    "creator": creator,
                    "name": asset.get("name"),
                    "kind": asset.get("type"),
                    "description": asset.get("description"),
                    "tags": asset.get("tags", []),
                    "metadata": metadata,
                },
                "path": asset_file,
            }
        )

        asset_folders[asset_folder] = asset_file

    with open(paths.assets_of(path), "a+") as f:
        f_size = f.seek(0, os.SEEK_END)
        f.seek(0)
        container_assets = []
        if f_size > 0:
            try:
                container_assets = json.load(f)
            except Exception as err:
                err.add_note(f"[{paths.assets_of(path)}]")
                raise err

        container_assets += assets
        common.json_overwrite(container_assets, f)

    for folder, child in asset_folders.items():
        # NOTE: Rename folder incase file has same name.
        folder_tmp = folder + ".tmp"
        os.rename(folder, folder_tmp)

        src = os.path.join(folder_tmp, child)
        dst = os.path.join(path, child)
        os.rename(src, dst)
        os.remove(os.path.join(folder_tmp, ASSET_PATH))
        try:
            os.rmdir(folder_tmp)
        except OSError:
            warnings.warn(
                f"[{os.path.join(path, folder)}] Additional files found in asset folder, moving to `.syre`"
            )
            os.rename(
                folder_tmp,
                os.path.join(paths.syre_dir_of(path), os.path.basename(folder)),
            )


def convert_container_recursive(path: str, analysis_map: dict[str, str]):
    """Converts Containers to `0.11.1` recursively.

    + Creates a `.syre` folder.
    + Converts a container properties.
    + Converts scripts to analyses.
    + Creates container settings file.
    + Removes `_container.json` and `_scripts.json` files.
    + Converts assets.
    + Recurses on children.

    Args:
        path (str): Base path of container.
        analysis_map (dict[str, str]): Map from analysis path to resource id.
    """
    children = os.listdir(path)
    if (CONTAINER_PATH not in children) and (paths.SYRE_FOLDER not in children):
        raise RuntimeError(f"Invalid container `{path}`")

    if paths.SYRE_FOLDER not in children:
        mkdir_syre(path)

    if CONTAINER_PATH in children:
        create_container_properties(path, analysis_map)
        create_container_settings(path)
        create_container_assets(path, analysis_map)

    for child in children:
        child_path = os.path.join(path, child)
        if not os.path.isdir(child_path):
            continue
        if CONTAINER_PATH in os.listdir(child_path):
            convert_container_recursive(child_path, analysis_map)


def convert_all_containers(project_path: str):
    """Converts all the Containers in a project to `0.11.1`.

    Args:
        project_path (str): Path to the project's root.
    """
    data_path = os.path.join(project_path, "data")
    analysis_map = get_analysis_map(project_path)
    convert_container_recursive(data_path, analysis_map)


def convert(project: str):
    """Converts the project located at the given path to `0.11.1`.

    Args:
        project (str): Path to the project.
    """
    logger.info("[0.9.x] (to `0.11.1`)")
    create_project(project)
    convert_analyses(project)
    convert_all_containers(project)
