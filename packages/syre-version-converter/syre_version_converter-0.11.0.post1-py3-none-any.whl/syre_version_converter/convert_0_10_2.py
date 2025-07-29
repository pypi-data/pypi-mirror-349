"""
Converts a Syre project from version 0.10.2 to 0.11.0.

# Config
+ Changes `users.json` from object to list.
+ Moves local config from `settings.json` to `local_config.json`.
+ Changes local config to only have active user, removing active project.

# Projects
+ Updates `local_version_format` to `0.11.0`.
+ Moves `creator` and `created` fields into settings.

# Containers
+ Moves `creator` and `created` fields into settings.
+ Converts analysis associations to a list.
+ Converts `{ "analyses": { "script": <id>, ... }` to `{ "analyses": { "analysis": <id>, ... }`.
+ Changes assets to a list.
+ Converts permissions to a map.

# Manual conversion
These steps must be performed manually.
+ Move `local/config/runner_settings.json` to `local/config/settings/<USER_ID>.json`.
+ Add `"continue_on_error": false` to `local/config/settings/<USER_ID>.json`.
"""
import os
import json
import logging
import shutil
from glob import glob

from . import paths, common

logger = logging.getLogger(__name__)

def convert_config():
    convert_user_config()
    convert_local_config()


def convert_user_config():
    """Converts `users.json` from an object to a list.
    """
    path = paths.config_user_manifest()
    with open(path, "r+") as f:
        users = json.load(f)
        if isinstance(users, list):
            logger.info("user manifest already a list")
            return
        
        logger.info("backing up user manifest")
        (path_backup, ext) = os.path.splitext(path)
        path_backup = path_backup + ".0_10_2" + ext
        shutil.copyfile(path, path_backup)
        
        logger.info("converting user manifest from object to list")
        users = [user for (_, user) in users.items()]
        common.json_overwrite(users, f)


def convert_local_config():
    """Moves `settings.json` to `local_config.json` and removes `active_project` field.
    """
    path = paths.config_local_settings()
    path_old = os.path.join(os.path.dirname(path), "settings.json")
    (path_old_exists, path_exists) = (os.path.exists(path_old), os.path.exists(path))
    
    if not path_exists and path_old_exists:
        if os.path.exists(path_old):
            logger.info("converting local config")
            with open(path_old, "r+") as f:
                config_old = json.load(f)
                config = { "user": None }
                if "active_user" in config_old:
                    config["user"] = config_old["active_user"]
                    
            with open(path, "a") as f:
                common.json_overwrite(config, f)
            
            os.remove(path_old)
    elif path_exists:
        logger.info("local config file already exists")
    elif not path_old_exists:
        logger.info("local config file does not exist")


def convert_project_properties(base_path: str):
    """Converts the Project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.
    Updates `local_version_format` to `0.11.0`.

    Args:
        base_path (str): Path to the project's root.
    """
    with open(paths.project_properties_of(base_path), "r+") as f_properties:
        with open(paths.project_settings_of(base_path), "r+") as f_settings:
            logger.info(f"converting project properties of {base_path}")
            
            properties = json.load(f_properties)
            settings = json.load(f_settings)
            orig_props = "created" in properties and "creator" in properties
            orig_settings = "created" not in settings and "creator" not in settings
            if orig_props and orig_settings:
                settings["local_format_version"] = "0.11.0"
                settings["created"] = properties["created"]
                settings["creator"] = properties["creator"]["User"]
                del properties["created"]
                del properties["creator"]
                common.json_overwrite(properties, f_properties)
                common.json_overwrite(settings, f_settings)
            elif not orig_props and not orig_settings:
                logger.info(f"project {base_path} config already updated")
            else:
                raise RuntimeError(f"project {base_path} config is corrupt")


def convert_all_containers(project_path: str):
    """Converts all the Containers in a project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.
    Converts analysis associations to a list.
    Converts `{ "analyses": { "script": <id>, ... }` to `{ "analyses": { "analysis": <id>, ... }`
    Changes assets to a list.
    Converts permissions to a map.

    Args:
        project_path (str): Path to the project's root.
    """
    data_path = common.project_data_path(project_path)
    if data_path is None:
        raise ValueError(f"Could not retrieve data root for `{project_path}`")

    glob_pattern = os.path.join(data_path, "**", paths.container_properties())
    for container_properties_path in glob(glob_pattern, recursive=True):
        container_path = os.path.dirname(os.path.dirname(container_properties_path))
        logging.info(f"[{container_path}]")
        convert_container(container_path)
        

def convert_container(base_path: str):
    """Converts a Container in a project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.
    Converts analysis associations to a list.
    Converts `{ "analyses": { "script": <id>, ... }` to `{ "analyses": { "analysis": <id>, ... }`
    Converts assets to a list.
    Converts permissions to a map.

    Args:
        base_path (str): Absolute path the the container's folder.
    """
    convert_container_properties(base_path)
    convert_container_analysis_associations(base_path)
    convert_container_assets(base_path)
    convert_container_permissions(base_path)
    
def convert_container_properties(base_path: str):
    """Converts a Container in a project from 0.10.2 to 0.11.0.
    Moves `creator` and `created` fields into settings.

    Args:
        base_path (str): Absolute path the the container's folder.
    """
    with open(paths.container_properties_of(base_path), "r+") as f_properties:
        with open(paths.container_settings_of(base_path), "r+") as f_settings:
            container = json.load(f_properties)
            settings = json.load(f_settings)
            if "properties" in container:
                properties = container["properties"]
                orig_props = "created" in properties and "creator" in properties
                orig_settings = "created" not in settings and "creator" not in settings
                if orig_props and orig_settings:
                    logger.info(f"converting container properties of {base_path}")
                    settings["created"] = properties["created"]
                    settings["creator"] = properties["creator"]["User"]
                    del properties["created"]
                    del properties["creator"]
                    common.json_overwrite(container, f_properties)
                    common.json_overwrite(settings, f_settings)
                elif not orig_props and not orig_settings:
                    logger.info(f"container {base_path} config already updated")
                else:
                    raise RuntimeError(f"container {base_path} config is corrupt")
            else:
                raise RuntimeError(f"container {base_path} properties is corrupt")

def convert_container_analysis_associations(base_path: str):
    """Converts a Container in a project from 0.10.2 to 0.11.0.
    Converts analysis associations to a list.
    Converts `{ "analyses": { "script": <id>, ... }` to `{ "analyses": { "analysis": <id>, ... }`

    Args:
        base_path (str): Absolute path the the container's folder.
    """
    with open(paths.container_properties_of(base_path), "r+") as f:
            container = json.load(f)
            if "analyses" in container:
                analyses = container["analyses"]
                if isinstance(analyses, list):
                    for assoc in analyses:
                        if "script" in assoc:
                            assoc["analysis"] = assoc["script"]
                            del assoc["script"]
                    
                    common.json_overwrite(container, f)
                else:
                    logger.info(f"converting {base_path} analysis associations")
                    updated_analyses = []
                    for (script, assoc) in analyses.items():
                        assoc["analysis"] = script
                        updated_analyses.append(assoc)
                        
                    container["analyses"] = updated_analyses
                    common.json_overwrite(container, f)
            else:
                raise RuntimeError(f"container {base_path} properties is corrupt")


def convert_container_assets(base_path: str):
    """Converts a Container in a project from 0.10.2 to 0.11.0.
    Changes the container's assets from an object to a list.

    Args:
        base_path (str): Absolute path the the container's folder.
    """  
    with open(paths.assets_of(base_path), "r+") as f:
        assets = json.load(f)
        if isinstance(assets, list):
            logger.info("assets already converted to list")
            return
            
        logger.info(f"converting assets of {base_path}")
        assets = [asset for (_, asset) in assets.items()]
        common.json_overwrite(assets, f)
        
        
def convert_container_permissions(base_path: str):
    """Converts a Container in a project from 0.10.2 to 0.11.0.
    Changes the container's permissions from a list to a map.

    Args:
        base_path (str): Absolute path the the container's folder.
        
    Raises:
        ValueError: If permissions are not empty.
            It appears the permissions could not be associated to a user in 0.10.2,
            so was unsure how to handle if permissions existed.
    """  
    with open(paths.container_settings_of(base_path), "r+") as f:
        settings = json.load(f)
        if "permissions" not in settings:
            raise KeyError(f"container {base_path} settings missing `permissions` key")
        
        permissions = settings["permissions"]
        if isinstance(permissions, dict):
            logger.info("permissions already converted to map")
            return
        
        if len(permissions) > 0:
            raise ValueError("expected permissions to be empty")
        
        logger.info(f"converting container permissions of {base_path}")
        settings["permissions"] = {}
        common.json_overwrite(settings, f)


def convert(project: str):
    """Converts the config and project located at the given path from 0.10.2 to 0.11.0.

    Args:
        project (str): Path to the project.
    """
    logger.info("[0.10.2]")
    convert_config()
    convert_project_properties(project)
    convert_all_containers(project)
