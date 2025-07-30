"""PEH-model package"""

import os
import pathlib

__version__ = "0.0.1a1"


def get_schema_path():
    """Return the path to the schema file.

    Returns:
        pathlib.Path: Path to the peh.yaml schema file
    """
    return pathlib.Path(os.path.join(os.path.dirname(__file__), "schema", "peh.yaml"))
