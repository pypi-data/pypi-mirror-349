"""
Converts a Syre project from version 0.10.1 to 0.10.2.

# Analysis
+ Moves `.syre/scripts.json` to `.syre/analyses.json`.
+ Adds {"type": "script"} to all existing scripts.

# Containers
+ Renames `Container.scripts` to `Container.analyses`.
"""
# %%
import os
import json
import logging
from glob import glob

from . import paths, common

logger = logging.getLogger(__name__)

# %%
def convert_project_scripts(base_path: str):
    """Convert project .syre/scripts.json to .syre/analyses.json.
    Adds entry {"type": "script"} for each script.
    Flattens Analysis.path to be a basic path, rather than map
    with path type.

    Args:
        path (str): Path to project folder.
    """
    logger.info("converting project scripts")
    from_path = os.path.join(base_path, paths.SYRE_FOLDER, "scripts.json")
    analyses_path = paths.project_analyses_of(base_path)
    if  os.path.exists(from_path) and not os.path.exists(analyses_path):
        os.rename(from_path, analyses_path)

    logger.info("adding type to scripts")
    with open(analyses_path, "r+") as f:
        analyses = json.load(f)
        for analysis in analyses:
            if "type" not in analysis:
                analysis["type"] = "Script"
                
            if isinstance(analysis["path"], dict):
                if "Relative" not in analysis["path"]:
                    rid = analysis["rid"]
                    raise RuntimeError(f"Invalid analysis path for analysis {rid}")
                
                analysis["path"] = analysis["path"]["Relative"]

        f.seek(0)
        json.dump(analyses, f, indent=4)
        f.truncate()


def convert_container_associations(container_properties_path: str):
    """Renames `Container.scripts` to `Container.analyses`.

    Args:
        container_properties_path (str): Path to the container's properties file.
    """
    logging.info("converting Container.scripts to Container.analyses")
    with open(container_properties_path, "r+") as f:
        container = json.load(f)
        if "analyses" in container:
            return
        
        if "scripts" in container:
            container["analyses"] = container.pop("scripts")
        else:
            container["analyses"] = {}

        f.seek(0)
        json.dump(container, f, indent=4)
        f.truncate()


def convert_all_containers(project_path: str):
    """Converts all the Containers in a project from 0.10.1 to 0.10.2.

    Args:
        project_path (str): Path to the project's root.
    """
    data_path = common.project_data_path(project_path)
    if data_path is None:
        raise ValueError(f"Could not retrieve data root for `{project_path}`")

    glob_pattern = os.path.join(data_path, "**", paths.container_properties())
    for container_properties_path in glob(glob_pattern, recursive=True):
        logging.info(f"[{container_properties_path}]")
        convert_container_associations(container_properties_path)


def convert(project: str):
    """Converts the project located at the given path from 0.10.1 to 0.10.2.

    Args:
        project (str): Path to the project.
    """
    logger.info("[0.10.1]")
    convert_project_scripts(project)
    convert_all_containers(project)

