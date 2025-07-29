"""This module contains the MapProvider class.

The MapProvider class provides the basic functionality to read out brightness
values of pixels on a map by given coordinates.
"""

import numpy as np
import rasterio
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import os
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel
from numpy.typing import NDArray


class MapProvider:
    """This class provides the functionality to read out brightness values by their coordinates."""

    def __init__(self, mapPath: str):
        """Initializes the MapProvider object based on a map file."""
        self.mapPath = mapPath
        self.image = rasterio.open(mapPath)
        self.debug = DebugPipeline.get_debug_pipeline()

    def calculateStartingCoordinates(self, latitude: float, longitude: float) -> tuple[int, int]:
        """
        Calculates the starting coordinates in x and y on the map from the given longitude and latitude.

        RETURNS: x and y coordinates of the starting point on the map
        """
        transform = self.image.transform

        pixel_x, pixel_y = ~transform * (longitude, latitude)

        self.debug.log(f"Starting Coordinates in x and y: {pixel_x}, {pixel_y}", LogLevel.DEBUG)

        return int(pixel_x), int(pixel_y)

    def calculateLengthOfPixel(self, length: float, latitude: float, longitude: float) -> tuple[float, float]:
        """
        Returns the average length of a pixel on the map in meters.

        It is done by calculating three different pixel sizes and
        averaging them by the given length in kilometers and the starting coordinates.
        RETURNS: average pixel width in meters, average pixel height in meters
        """
        length = length / 1000

        transform = self.image.transform

        # Localize the pixel size in degrees
        pixel_width_deg = transform[0]  # width of a pixel in degrees
        pixel_height_deg = -transform[4]  # height of a pixel in degrees

        # Calculate the coordinates of next pixel based on the starting point by adding the pixel size in
        # degrees on the latitude and longitude axis
        start_coord = (latitude, longitude)
        next_long_coord = (latitude, longitude + pixel_width_deg)
        next_lat_coord = (latitude + pixel_height_deg, longitude)

        # Calculate the distance between the starting point and the next pixel in kilometers
        pixel_width_km_start = geodesic(start_coord, next_long_coord).kilometers
        pixel_height_km_start = geodesic(start_coord, next_lat_coord).kilometers

        # Calculate the latitude and longitude of the middle of the given square
        delta_lat = length / 111.32  # 1 degree latitude is approximately 111.32 km
        delta_lon = float(
            length / (111.32 * np.cos(np.radians(latitude)))
        )  # 1 degree longitude is approximately 111.32 km * cos(latitude)

        # Adds the delta values to the given latitude and longitude to get the bottom left corner of the square
        bot_left_lat = latitude - delta_lat
        bot_left_lon = longitude - delta_lon

        # Calculate the coordinates of the middle of the square the same way as the starting point
        bot_left_coord = (bot_left_lat, bot_left_lon)
        bl_next_lat_coord = (bot_left_lat + pixel_width_deg, bot_left_lon)
        bl_next_long_coord = (bot_left_lat, bot_left_lon + pixel_height_deg)

        pixel_width_km_bl = geodesic(bot_left_coord, bl_next_long_coord).kilometers
        pixel_height_km_bl = geodesic(bot_left_coord, bl_next_lat_coord).kilometers

        # Adds the delta values to the given latitude and longitude to get the corner of the square
        top_right_lat = latitude + delta_lat
        top_right_lon = longitude + delta_lon

        # Calculate the coordinates of the corner of the square the same way as the starting point and middle point
        top_right_coord = (top_right_lat, top_right_lon)
        tr_next_long_coord = (top_right_lat, top_right_lon + pixel_width_deg)
        tr_next_lat_coord = (top_right_lat + pixel_height_deg, top_right_lon)

        pixel_width_km_tr = geodesic(top_right_coord, tr_next_long_coord).kilometers
        pixel_height_km_tr = geodesic(top_right_coord, tr_next_lat_coord).kilometers

        # Adds the three calculated pixel sizes and divides them by 3 to get the average pixel size
        avg_pixel_width_m = ((pixel_width_km_start + pixel_width_km_bl + pixel_width_km_tr) / 3) * 1000
        avg_pixel_height_m = ((pixel_height_km_start + pixel_height_km_bl + pixel_height_km_tr) / 3) * 1000

        return avg_pixel_width_m, avg_pixel_height_m

    def getBrightnessOfPixelByCoordinates(
        self, length: float, latitude: float, longitude: float
    ) -> tuple[NDArray[np.float32], float, float]:
        """
        Calculates the brightness of pixels in a square with the given length in meters with given coordinates.

        RETURNS:
            Tuple of size 3.
            The first element is a 2D numpy array containing the brightness values of the map,
            the second is the pixel width in meters and the third is the pixel height in meters
        """
        starting_x, starting_y = self.calculateStartingCoordinates(latitude, longitude)

        pixelWidth, pixelHeight = self.calculateLengthOfPixel(length, latitude, longitude)

        self.debug.log(f"Pixelwidth: {pixelWidth} m", LogLevel.DEBUG)
        self.debug.log(f"Pixelheight: {pixelHeight} m", LogLevel.DEBUG)

        numberOfPixelsWidth = int(np.ceil((length / 1000) / (pixelWidth / 1000)))

        numberOfPixelsHeight = int(np.ceil((length / 1000) / (pixelHeight / 1000)))

        self.debug.log("Starting to calculate the brightness values ...", LogLevel.INFO)

        # calculates all brightness values of the pixels in the given square, the square is defined by the starting
        # coordinates and the number of pixels in width and height, it always starts at the bottom left corner,
        # so from the starting point the square points to north and east
        window = (
            (starting_y - numberOfPixelsHeight, starting_y + numberOfPixelsHeight),
            (starting_x - numberOfPixelsWidth, starting_x + numberOfPixelsWidth),
        )
        brightnessValues = self.image.read(1, window=window)

        self.debug.log("Brightness values calculated.", LogLevel.INFO)

        return brightnessValues, pixelWidth, pixelHeight


"""Example usage of the MapProvider class
Should show the brightness values in a map around Kairo in a square with a length of 4500 kilometers"""
if __name__ == "__main__":
    # \\lightPollutionSimulation
    mapPath = os.path.abspath(os.getcwd()) + "\\maps\\viirs_2023_raw_global.tif"
    mapProvider = MapProvider(mapPath)
    brightnessValues, _, _ = mapProvider.getBrightnessOfPixelByCoordinates(2000000, 38, 126)

    log_brightnessValues = np.log(brightnessValues + 1e-6)  # Kleiner Offset für Werte nahe 0

    # plot the array
    plt.figure(figsize=(8, 6))
    plt.imshow(log_brightnessValues, cmap="gray", origin="upper")
    plt.colorbar(label="Log(Brightness Values)")
    plt.title("logarithmically scaled brightness values ")
    plt.xlabel("X-Pixel (columns)")
    plt.ylabel("Y-Pixel (rows)")
    plt.show()
