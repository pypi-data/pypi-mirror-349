from aceti import import_map
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
from tqdm.auto import tqdm
import os
import urllib.request
import pyproj

class GoogleMapDownloader:
    """
        A class which generates high resolution google maps image given
        Northwest and Southeast points in [Lat Lon] and zoom level
        You can change the quality of the image by changing the zoom and layer values
        
        19 is a valid zoom value knowing the size of our drone
        
        for the maps you have available
        ROADMAP = "v"
        TERRAIN = "p"
        ALTERED_ROADMAP = "r"
        SATELLITE = "s"
        TERRAIN_ONLY = "t"
        HYBRID = "y"
        
        
    """

    def __init__(self, Northwest, Southeast, zoom=19, layer="s", server="google"):
        """
            GoogleMapDownloader Constructor
            Args:
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
        """
        self.Northwest = Northwest
        self.Southeast = Southeast
        if zoom < 0 or zoom > 22:
            raise ValueError("Zoom level must be between 0 and 22")
        self._zoom = zoom
        self._layer = layer

        if server not in ["google", "arcgis"]:
            raise ValueError("Server must be either 'google' or 'arcgis'")
        self._server = server

        # Set up transformers, EPSG:3857 is metric, same as EPSG:900913
        self.to_proxy_transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3857')
        self.to_original_transformer = pyproj.Transformer.from_crs('epsg:3857', 'epsg:4326')
        
        # Check if the coordinates are valid
        if not (isinstance(Northwest, np.ndarray) or isinstance(Northwest, list)) or not (isinstance(Southeast, np.ndarray)  or isinstance(Southeast, list)):
            raise ValueError("Northwest and Southeast must be tuples")
        if Northwest[0]<=Southeast[0] or Northwest[1]>=Southeast[1]:
            raise ValueError("you didn't provide a valid rectangle, check your coordinates")
        
        
        self.get_tile_coordinates()
        
        if (abs(self.nw_tile[0]-self.se_tile[0]) == 0) or (abs(self.nw_tile[1]-self.se_tile[1]) == 0):
            raise ValueError("Insuficient zoom, points are too close, i am lazy to program this, increase zoom")
        self.generateImage()
        

    def get_tile_coordinates(self):
        """
            Generates an X,Y tile and pixel coordinate based on the latitude, longitude
            and zoom level
        """

        tile_size = 256 #each tile has 256 pixels

        # Use a left shift to get the power of 2, zoom 0 is a world map, zoom 1 is wold map divided in 4 tiles, zoom 2 is world map divided in 16 tiles
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles as coordinate sistem divides axis in 4 (x+y+,x-y+,x-y-,x+y-)
        numTiles = 1 << self._zoom

        ########################
        # For Northwest corner 
        ########################
        # Find the x_pixel given the longitude
        x_pixel = (tile_size / 2 + self.Northwest[1] * tile_size / 360.0) * numTiles 
        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self.Northwest[0] * (math.pi / 180.0))
        # Calulate the y_pixel
        y_pixel = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(tile_size / (2 * math.pi))) * numTiles 
        
        self.nw_pixel=[x_pixel, y_pixel]
        self.nw_tile=[int(x_pixel // tile_size), int(y_pixel // tile_size)]
    
        ########################
        # For Southeast corner 
        ########################
        # Find the x_pixel given the longitude
        x_pixel = (tile_size / 2 + self.Southeast[1] * tile_size / 360.0) * numTiles 
        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self.Southeast[0] * (math.pi / 180.0))
        # Calulate the y_pixel
        y_pixel = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(tile_size / (2 * math.pi))) * numTiles 
        
        self.se_pixel=[x_pixel, y_pixel]
        self.se_tile=[math.ceil(x_pixel // tile_size)+1, math.ceil(y_pixel // tile_size)+1]
            
    def generateImage(self):
        """
            Generates an image by stitching a number of google map tiles together. after executing self.get_tile_coordinates
            Returns:
                A high-resolution Goole Map image.
        """

        tile_width = abs(self.nw_tile[0]-self.se_tile[0])
        tile_height = abs(self.nw_tile[1]-self.se_tile[1])
        
        # Determine the size of the image, for simplicity, we will print the whole image and later crop it
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the size required
        map_img = Image.new('RGB', (width, height))
        
        
        # calculate northwest pixel of the tile
        start_x=self.nw_tile[0]
        start_y=self.nw_tile[1]

        # print the map and report using tdqm
        pbar = tqdm(total=tile_width*tile_height, unit="tiles")
        pbar.set_description("Downloading map")
        pbar.set_postfix_str(f"Zoom: {self._zoom}, Layer: {self._layer}")
        pbar.refresh()
        for x in range(0, tile_width):
            for y in range(0, tile_height):
                current_tile = str(x) + '-' + str(y)
                try:
                    if self._server == "google":
                        url = f'https://mt0.google.com/vt?lyrs={self._layer}&x=' + str(start_x + x) + '&y=' + str(start_y + y) + '&z=' + str(self._zoom)
                        urllib.request.urlretrieve(url, current_tile)
                    elif self._server == "arcgis":
                        url = f"http://services.arcgisonline.com/ArcGis/rest/services/World_Imagery/MapServer/tile/{self._zoom}/{start_y + y}/{start_x + x}.png"
                        urllib.request.urlretrieve(url, current_tile)
                    else:
                        raise ValueError("Server not available")
                except :
                    raise ValueError("Server not available")
                im = Image.open(current_tile)
                map_img.paste(im, (x * 256, y * 256))

                os.remove(current_tile)
                pbar.update(1)
                pbar.refresh()
        
        print("map downloaded")

        self.raw_map_img = map_img.copy()
        # cut corners
        left=abs(self.nw_tile[0] * 256 - self.nw_pixel[0])
        top=abs(self.nw_tile[1] * 256 - self.nw_pixel[1])
        right=left + abs(self.se_pixel[0] - self.nw_pixel[0])
        bottom=top + abs(self.nw_pixel[1] - self.se_pixel[1])
        
        
        map_img = map_img.crop((left, top, right, bottom))
        self.map_img = map_img


    def to_pixel(self, GPS_point):
        """
            Generates an X,Y pixel coordinate based on the latitude, longitude
            and zoom level
            Returns:    An X,Y pixel coordinate
        """
        #check if we are inside the map
        self.pole=[None,None]
        if self.Northwest[0]>self.Southeast[0]:
            self.pole[0]="N"
        else:
            self.pole[0]="S"
        if self.Northwest[1]>self.Southeast[1]:
            self.pole[1]="W"
        else:
            self.pole[1]="E"


        if self.pole[1]=="W":
            if ((self.Southeast[1])>(GPS_point[1])>(self.Northwest[1])):
                raise ValueError(f"point {GPS_point} 1W is outside the map {[self.Northwest,self.Southeast]}")
        else:
            if ((self.Southeast[1])<(GPS_point[1])<(self.Northwest[1])):
                raise ValueError(f"point {GPS_point} 1E is outside the map {[self.Northwest,self.Southeast]}")
        if self.pole[0]=="N":
            if ((self.Southeast[0])>(GPS_point[0])>(self.Northwest[0])):
                raise ValueError(f"point {GPS_point} 0N is outside the map {[self.Northwest,self.Southeast]}")
        else:
            if ((self.Southeast[0])<(GPS_point[0])<(self.Northwest[0])):
                raise ValueError(f"point {GPS_point} 0S is outside the map {[self.Northwest,self.Southeast]}")



        tile_size = 256 #each tile has 256 pixels

        # Use a left shift to get the power of 2, zoom 0 is a world map, zoom 1 is wold map divided in 4 tiles, zoom 2 is world map divided in 16 tiles
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles as coordinate sistem divides axis in 4 (x+y+,x-y+,x-y-,x+y-)
        numTiles = 1 << self._zoom

        # Find the x_pixel given the longitude
        x_pixel = (tile_size / 2 + GPS_point[1] * tile_size / 360.0) * numTiles 

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(GPS_point[0] * (math.pi / 180.0))

        # Calulate the y_pixel
        y_pixel = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles 
        
        return [x_pixel-self.nw_pixel[0], y_pixel-self.nw_pixel[1]]
    
    def show_grid(self, lat_lon_map, base_matrix):

        # if lat_lon_map.shape[0] == base_matrix.shape[0] and lat_lon_map.shape[1] == base_matrix.shape[1]:
        #     print("base_matrix and lat_lon_map have the same shape, extending last column and row")
        #     # Extend the last column and row of lat_lon_map
        #     lat_lon_map = np.concatenate((lat_lon_map, lat_lon_map[-1:, :]), axis=0)
        #     lat_lon_map = np.concatenate((lat_lon_map, lat_lon_map[:, -1:]), axis=1)
        #     for i in range(lat_lon_map.shape[0]):
        #         lat_lon_map[i, -1] = lat_lon_map[i, -2] +( lat_lon_map[i, -2] - lat_lon_map[i, -3])
        #     for i in range(lat_lon_map.shape[1]):
        #         lat_lon_map[-1, i] = lat_lon_map[-2, i] + (lat_lon_map[-2, i] - lat_lon_map[-3, i])
        #     print("lat_lon_map shape: ", lat_lon_map.shape)
            

        # cut corners
        p1=self.to_pixel(lat_lon_map[0, 0])
        p2=self.to_pixel(lat_lon_map[1, 1])
        distance=min(abs(p1[0]-p2[0]),abs(p1[1]-p2[1]))
        left=abs(self.nw_tile[0] * 256 - self.nw_pixel[0] -distance)
        top=abs(self.nw_tile[1] * 256 - self.nw_pixel[1] +distance)
        right=left + abs(self.se_pixel[0] - self.nw_pixel[0] + distance)
        bottom=top + abs(self.nw_pixel[1] - self.se_pixel[1] -distance)
        print("distance: ", distance)


        map_img = self.raw_map_img.crop((left, top, right, bottom))
            
            
        plt.figure()
        plt.imshow(self.map_img, cmap=plt.get_cmap('binary'))
        #obtain xy points of the base matrix
        points = np.argwhere(base_matrix == 1)
                
        for point in points:
            try:
                x=[]
                y=[]
                center = self.to_pixel(lat_lon_map[point[0], point[1]])
                p1=[center[0]-distance/2, center[1]-distance/2]
                p2=[center[0]+distance/2, center[1]-distance/2]
                p3=[center[0]-distance/2, center[1]+distance/2]
                p4=[center[0]+distance/2, center[1]+distance/2]
                x.append(p1[0])
                y.append(p1[1])
                x.append(p2[0])
                y.append(p2[1])
                x.append(p4[0])
                y.append(p4[1])
                x.append(p3[0])
                y.append(p3[1])
                x.append(p1[0])
                y.append(p1[1])
                plt.plot(x,y,'b-', linewidth=distance/20)
            except Exception as e:
                continue
        plt.savefig("map.png", dpi=400)
        plt.show()
