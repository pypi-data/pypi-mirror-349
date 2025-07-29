import numpy as np
import os
import sys
from matplotlib import pyplot as plt


if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files() function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources
pkg = importlib_resources.files("aceti")

def import_map(map_name: str):
    """
    Import a map from a file and return the base matrix and lat/lon map.
    Args:
        map_name (str): The name of the map to import.
    Returns:
        tuple: A tuple containing the base matrix and lat/lon map.
    """
    map_name = map_name.lower()
    if os.path.exists(pkg.joinpath("maps", f"{map_name}mask.npy")):
        print(f"Loading map {map_name} from package directory")
    else:
        raise FileNotFoundError(f"Map {map_name} not found in package directory")

    base_matrix = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))

    # Load the lat/lon map
    lat_lon_map = np.load(pkg.joinpath("maps", f"{map_name}latlon.npy"))

    return base_matrix, lat_lon_map


def plot_map(map_name):
    ''' Convert a CSV file to a binary image. '''
    if isinstance(map_name, str):
        binary_image = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))
    elif isinstance(map_name, np.ndarray):
        #check map is 1 and 0
        if np.all(np.isin(map_name, [0, 1])):
            binary_image = map_name
        else:
            raise ValueError("map_name must be a string or a numpy array of 0s and 1s")
    else:
        raise ValueError("map_name must be a string or a numpy array")
    # Load the CSV file
    binary_image = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))

    # Convert the binary image to 0s and 255s
    binary_image = np.where(binary_image > 0, 255, 0)

    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')
    plt.show()

def map_downsize(map_name, factor=2):
    ''' Downsize a map. '''
    if isinstance(map_name, str):
       binary_image = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))
    elif isinstance(map_name, np.ndarray):
       binary_image = map_name
    else:
        raise ValueError("map_name must be a string or a numpy array")
    # Downsize the binary image
    return binary_image[::factor, ::factor]

def csv_shrink(map_name, init_column=0, final_column=None, init_row=0, final_row=None):
    ''' Shrink a map. '''
    if isinstance(map_name, str):
       binary_image = np.load(pkg.joinpath("maps", f"{map_name}mask.npy"))
    elif isinstance(map_name, np.ndarray):
       binary_image = map_name
    else:
        raise ValueError("map_name must be a string or a numpy array")

    # Set the final column and row if they are None
    if final_column is None:
        final_column = binary_image.shape[1]
    if final_row is None:
        final_row = binary_image.shape[0]

    # Shrink the binary image
    return binary_image[init_row:final_row, init_column:final_column]

def plot_grid(map):
    ''' Plot a grid on top of a map. '''

    #check map properties
    if isinstance(map, str):
        base_matrix, lat_lon_map  = import_map(map)
    elif isinstance(map, tuple):
        base_matrix, lat_lon_map  = map
        if isinstance(base_matrix, np.ndarray) and isinstance(lat_lon_map, np.ndarray):
            if not np.all(np.isin(base_matrix, [0, 1])):
                raise ValueError("base_matrix must be a numpy array of 0s and 1s")
            if base_matrix.shape != lat_lon_map.shape:
                raise ValueError("base_matrix and lat_lon_map must have the same shape")
            if not np.all(np.apply_along_axis(lambda x: isinstance(x, tuple) and len(x) == 2 and all(isinstance(i, float) for i in x), 1, lat_lon_map)):
                raise ValueError("lat_lon_map must be a numpy array of tuples of 2 coordinates, [lat, lon]")
        else:
            raise ValueError("map must be a string or a tuple of [base_matrix, lat_lon_map]")
    else:
        raise ValueError("map must be a string or a tuple of [base_matrix, lat_lon_map]")
    # Plot the map