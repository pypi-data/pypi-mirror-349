import os
import platform

SYRE_FOLDER = ".syre"
USER_MANIFEST_FILE = "users.json"
PROJECT_MANIFEST_FILE = "project_manifest.json"
LOCAL_CONFIG_FILE = "local_config.json"
PROJECT_PROPERTIES_FILE = "project.json"
PROJECT_ANALYSES_FILE = "analyses.json"
PROJECT_SETTINGS_FILE = "project_settings.json"
CONTAINER_PROPERTIES_FILE = "container.json"
CONTAINER_SETTINGS_FILE = "container_settings.json"
ASSETS_FILE = "assets.json"


def strip_windows_unc(path: str) -> str:
    """Strips a Windows UNC prefix, if present.

    Args:
        path (str): Path to manipulate.

    Returns:
        str: Stripped path.
    """
    UNC = "\\\\?\\"
    return path.removeprefix(UNC)


def get_system() -> str:
    """
    Returns:
        str: Current system.
    """
    system = platform.system()
    if system == "":
        raise RuntimeError("Could not determine OS")

    return system


def system_data_dir() -> str:
    """
    Returns:
        str: Absolute path to the app data directory.
    """
    system = get_system()
    home = os.path.expanduser("~")
    if system == "Windows":
        return os.path.join(home, "AppData", "Roaming")
    elif system == "Darwin":
        return os.path.join(home, "Library", "Application Support")

    raise RuntimeError("Could not get data dir for OS")


def config_local_dir() -> str:
    """
    Returns:
        str: Path of the Syre local config dir.
    """
    system = get_system()
    if system == "Windows":
        return os.path.join(system_data_dir(), "syre", "syre-local")
    elif system == "Darwin":
        return os.path.join(system_data_dir(), "ai.syre.syre-local")

    raise RuntimeError("Could not get Syre local config dir for OS")


def config_desktop_dir() -> str:
    """
    Returns:
        str: Path of the Syre desktop config dir.
    """
    system = get_system()
    if system == "Windows":
        return os.path.join(system_data_dir(), "syre", "syre-desktop")
    elif system == "Darwin":
        return os.path.join(system_data_dir(), "ai.syre.syre-desktop")

    raise RuntimeError("Could not get Syre desktop config dir for OS")


def config_user_manifest() -> str:
    """
    Returns:
        str: Path to the Syre user manifest file.
    """    
    system = get_system()
    if system == "Windows":
        return os.path.join(config_local_dir(), "config", USER_MANIFEST_FILE)
    elif system == "Darwin":
        return os.path.join(config_local_dir(), USER_MANIFEST_FILE)

    raise RuntimeError("Could not get Syre user manifest for OS")


def config_project_manifest() -> str:
    """
    Returns:
        str: Path to the Syre project manifest file.
    """
    system = get_system()
    if system == "Windows":
        return os.path.join(config_local_dir(), "config", PROJECT_MANIFEST_FILE)
    elif system == "Darwin":
        return os.path.join(config_local_dir(), PROJECT_MANIFEST_FILE)

    raise RuntimeError("Could not get Syre project manifest for OS")



def config_local_settings() -> str:
    """
    Returns:
        str: Path to the Syre local config file.
    """
    system = get_system()
    if system == "Windows":
        return os.path.join(config_local_dir(), "config", LOCAL_CONFIG_FILE)
    elif system == "Darwin":
        return os.path.join(config_local_dir(), LOCAL_CONFIG_FILE)

    raise RuntimeError("Could not get Syre local config for OS")


def project_properties_of(base_path: str) -> str:
    """Project properties file of the base path.

    Args:
        base_path (str): Path tot eh project's root folder.

    Returns:
        str: Path to the project's properties file.
    """
    return os.path.join(base_path, SYRE_FOLDER, PROJECT_PROPERTIES_FILE)


def project_analyses_of(base_path: str) -> str:
    """Project analyses file of the base path.

    Args:
        base_path (str): Path to the project's root folder.

    Returns:
        str: Path to the project's analyses file.
    """
    return os.path.join(base_path, SYRE_FOLDER, PROJECT_ANALYSES_FILE)


def project_settings_of(base_path: str) -> str:
    """Project settings file of the base path.

    Args:
        base_path (str): Path to the project's root folder.

    Returns:
        str: Path to the project's settings file.
    """
    return os.path.join(base_path, SYRE_FOLDER, PROJECT_SETTINGS_FILE)


def container_properties() -> str:
    """
    Returns:
        str: Relative path to a container properties file.
    """
    return os.path.join(SYRE_FOLDER, CONTAINER_PROPERTIES_FILE)


def container_properties_of(base_path: str) -> str:
    """Container properties file of the base path.

    Args:
        base_path (str): Path to container folder.

    Returns:
        str: Path to container properties file.
    """
    return os.path.join(base_path, container_properties())


def container_settings() -> str:
    """
    Returns:
        str: Relative path to a container properties file.
    """
    return os.path.join(SYRE_FOLDER, CONTAINER_SETTINGS_FILE)


def container_settings_of(base_path: str) -> str:
    """Container settings file of the base path.

    Args:
        base_path (str): Path to container folder.

    Returns:
        str: Path to container file.
    """
    return os.path.join(base_path, container_settings())


def assets() -> str:
    """
    Returns:
        str: Relative path to an asset file.
    """
    return os.path.join(SYRE_FOLDER, ASSETS_FILE)


def assets_of(base_path: str) -> str:
    """Assets file of the base path.

    Args:
        base_path (str): Path to container folder.

    Returns:
        str: Path to assets file.
    """
    return os.path.join(base_path, assets())
