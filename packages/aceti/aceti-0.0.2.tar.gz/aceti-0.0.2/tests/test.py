from aceti import import_map, GoogleMapDownloader
import numpy as np
import matplotlib.pyplot as plt
import PIL

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
    print("lat_lon_map shape: ", lat_lon_map.shape)
    print("base_matrix shape: ", base_matrix.shape)
    print("lat_lon_map: ", lat_lon_map[0, 0])
    print("lat_lon_map: ", lat_lon_map[-1, -1])
    map=GoogleMapDownloader(lat_lon_map[0, 0], lat_lon_map[-1, -1], zoom=19, layer="s", server ="arcgis") 
    # map.raw_map_img = PIL.Image.open("AlamilloPlantilla.png")
    plt.imshow(map.map_img)
    plt.savefig("alamillo95x216.png", dpi=600)
    map.show_grid(lat_lon_map, base_matrix)

    # plt.figure()
    # plt.imshow(base_matrix, cmap='gray', interpolation='nearest')
    # plt.show()

    


from aceti.old.maps_utils import csv_to_npy

csv_to_npy("alamillo95x216")

# plot_grid("alamilloaccess11x15")
plot_grid("alamillo95x216")
# plot_grid("alamillo30x49")
