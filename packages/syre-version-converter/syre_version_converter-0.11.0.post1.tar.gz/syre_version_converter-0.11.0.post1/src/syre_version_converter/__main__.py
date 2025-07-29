from typing import Callable
import argparse
import logging
import sys

from . import common
from . import convert_0_10_0
from . import convert_0_10_1
from . import convert_0_10_2

VERSIONS = [
    "0.10.0",
    "0.10.1",
    "0.10.2",
    "0.11.0",
]

CONVERTERS = {
    "0.10.0": convert_0_10_0.convert,
    "0.10.1": convert_0_10_1.convert,
    "0.10.2": convert_0_10_2.convert,
}

def setup_logging(verbose: bool):
    """Setup logging.

    Args:
        verbose (bool): Output more info. Changes logger level to logging.INFO.
    """
    logging.basicConfig(stream=sys.stdout)
    if verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

def convert_chain(initial: str, final: str) -> list[Callable]:
    """Creates a chain of converters

    Args:
        initial (str): Initial version.
        final (str): Final version.
        
    Returns:
        list[Callable]: List of callables to convert from initial to final version.
    """
    try:
        initial_idx = VERSIONS.index(initial)
    except ValueError:
        raise ValueError("Invalid initial verison")
    
    try:
        final_idx = VERSIONS.index(final)
    except ValueError:
        raise ValueError("Invalid final version")
    
    return [CONVERTERS[version] for version in VERSIONS[initial_idx:final_idx]]
    

parser = argparse.ArgumentParser(
    prog="Syre version converter",
    description="Converts Syre projects between version.",
)

parser.add_argument("initial", help="Current version. (x.y.z)")
parser.add_argument("final", help="Final version. (x.y.z)")
parser.add_argument("--project", "-p", help="Only convert the project at the given path.")
parser.add_argument("--verbose", "-v", action="store_true", help="Output more info.")

args = parser.parse_args()
setup_logging(args.verbose)
logger = logging.getLogger(__name__)

convert_chain = convert_chain(args.initial, args.final)
if len(convert_chain) == 0:
    raise ValueError("No conversion to perform.")

if args.project is None:
    for project in common.project_paths():
        logger.info(f"[{project}]")
        for convert in convert_chain:
            convert(project)
else:
    for convert in convert_chain:
        convert(args.project)
