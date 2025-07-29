import numpy as np
import os
import sys
if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files() function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

def import_map(map_name: str):
    """
    Import a map from a file and return the base matrix and lat/lon map.
    Args:
        map_name (str): The name of the map to import.
    Returns:
        tuple: A tuple containing the base matrix and lat/lon map.
    """
    map_name = map_name.lower()
    pkg = importlib_resources.files("aceti_maps")
    if os.path.exists(pkg.joinpath("maps", f"{map_name}mask.npy")):
        print(f"Loading map {map_name} from repo directory")

    base_matrix = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))

    # Load the lat/lon map
    lat_lon_map = np.load(pkg.joinpath("maps", f"{map_name}latlon.npy"))

    return base_matrix, lat_lon_map