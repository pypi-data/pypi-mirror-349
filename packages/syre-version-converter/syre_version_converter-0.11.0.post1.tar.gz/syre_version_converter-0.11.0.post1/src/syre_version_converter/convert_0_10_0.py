"""
Converts a Syre project to version 0.10.0.

+ Changes `.thot` folders to `.syre`

# Assets
+ Removes `Relative` path enum identifier.
"""
# %%
import os
import json
import logging
from glob import glob

from . import paths, common

logger = logging.getLogger(__name__)

# %%
def convert_thot_to_syre(root: str):
    """Convert all `.thot` folders to `.syre`.

    Args:
        root (str): Root path to convert. All subdirectories are converted.
    """
    logger.info("renaming `.thot` to `.syre`")
    glob_pattern = os.path.join(root, "**", ".thot")
    thot_paths = glob(glob_pattern, recursive=True)
    syre_paths = [os.path.join(os.path.dirname(path), ".syre") for path in thot_paths]
    for thot_path, syre_path in zip(thot_paths, syre_paths):
        os.rename(thot_path, syre_path)


def remove_relative_path_enum(assets_path: str):
    """Remove Relative path enum from Asset.path.

    Args:
        assets (str): Path to an assets.json file.
    """
    logging.info("removing Relative enum from asset paths")
    with open(assets_path, "r+") as f:
        assets = json.load(f)
        for asset in assets.values():
            if "Relative" in asset["path"]:
                asset["path"] = asset["path"]["Relative"]

        f.seek(0)
        json.dump(assets, f, indent=4)
        f.truncate()



def convert_all_containers(project_path: str):
    """Converts all the Containers in a project to 0.10.0.

    Args:
        project_path (str): Path to the project's root.
    """
    data_path = common.project_data_path(project_path)
    if data_path is None:
        raise ValueError(f"Could not retrieve data root for `{project_path}`")

    glob_pattern = os.path.join(data_path, "**", paths.assets())
    for assets_path in glob(glob_pattern, recursive=True):
        logging.info(f"[{assets_path}]")
        remove_relative_path_enum(assets_path)


def convert(project: str):
    """Converts the project located at the given path to 0.10.0.

    Args:
        project (str): Path to the project.
    """
    logger.info("[0.10.0]")
    convert_thot_to_syre(project)
    convert_all_containers(project)

