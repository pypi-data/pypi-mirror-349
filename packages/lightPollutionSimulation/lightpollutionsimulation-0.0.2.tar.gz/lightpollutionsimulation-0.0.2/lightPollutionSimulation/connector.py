"""Connector class to calculate the light pollution map and the sky brightness values."""

import lightPollutionSimulation.mapCoordinates as fmC
import matplotlib as mpl
from lightPollutionSimulation.lightPropagation import LightPropagation as glp
import lightPollutionSimulation.lightPollutionMap as glpm
from lightPollutionSimulation.skyClasses import Sky
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel
import numpy as np
import os
from numpy.typing import NDArray


class Connector:
    """Connector class to calculate the light pollution map and the sky brightness values."""

    def __init__(
        self,
        radiusAroundLocation: float,
        athmosphereHeight: int,
        latitude: float,
        longitude: float,
        granularity: int,
    ):
        """Initializes the Connector class."""
        self.longitude = longitude
        self.latitude = latitude
        self.athmosphereHeight = athmosphereHeight
        self.radiusAroundLocation = radiusAroundLocation
        self.granularity = granularity
        self.mapPath = os.path.join(os.getcwd(), "maps", "viirs_2023_raw_global.tif")
        self.mapProvider = fmC.MapProvider(self.mapPath)
        self.debug = DebugPipeline.get_debug_pipeline()

    def main(
        self,
    ) -> tuple[
        list[tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32], mpl.colors.Normalize, str]],
        NDArray[np.float32],
        NDArray[np.float32],
    ]:
        """
        Main function to calculate the light pollution map and the sky brightness values.

        The function returns a tuple with the following elements:
        1. A list of tuples with the x and y coordinates, the brightness values, the normalization method and the
           title of the plot
        2. The light pollution map as a numpy array
        3. The brightness values of the map as a numpy array
        """
        # Collect the VIIRS Data Points into an array
        VIIRSDataPoints, pixelWidth, pixelHeight = self.mapProvider.getBrightnessOfPixelByCoordinates(
            self.radiusAroundLocation, self.latitude, self.longitude
        )

        # Get the light propagator to simulate the light propagation
        lightPropagator = self.getLightPropagation(
            VIIRSDataPoints,
            pixelWidth,
            pixelHeight,
            2 * self.radiusAroundLocation,
            self.athmosphereHeight,
        )
        # Create the sky object to predefine all data points on the sky
        skyObj = Sky(lightPropagator, self.granularity)

        lightPollutionObj = glpm.LightPollutionMap(
            VIIRSDataPoints,
            pixelWidth,
            pixelHeight,
            2 * self.radiusAroundLocation,
            self.athmosphereHeight,
            lightPropagator,
        )
        lightPollutionMap = lightPollutionObj.generateLightPollutionMap()

        # Calculate midpoints of the map
        y0 = VIIRSDataPoints.shape[0] / 2
        x0 = VIIRSDataPoints.shape[1] / 2

        # Get the sky brightness values for an x,y pair as arrays for plotting
        x, y, brightness = self.getSkyBrightnessToValues(x0, y0, skyObj)
        VIIRSDataPoints[VIIRSDataPoints.shape[0] // 2, VIIRSDataPoints.shape[1] // 2] = 0

        # Create a list of all data for the plotter
        dataList = [
            (
                x,
                y,
                brightness,
                mpl.colors.PowerNorm(vmin=0.1, vmax=8000, gamma=0.4),
                "Sky Brightness Power",
            ),
            (
                x,
                y,
                brightness,
                mpl.colors.LogNorm(vmin=0.1, vmax=8000),
                "Sky Brightness Log",
            ),
        ]
        return dataList, lightPollutionMap, VIIRSDataPoints

    def getLightPropagation(
        self,
        mapArea: NDArray[np.float32],
        pixelWidth: float,
        pixelHeight: float,
        width: float,
        maxAtmosphereHeight: float,
    ) -> glp:
        """
        Initializes the light propagator object.

        The light propagator is used to simulate the light propagation in the atmosphere.
        The light propagator is used to calculate the brightness values of the sky.
        """
        propagator = glp(mapArea, pixelWidth, pixelHeight, width, maxAtmosphereHeight)
        propagator.buildDiscreteVolumeUnits()
        propagator.propagateLightSources()
        return propagator

    def getSkyBrightnessToValues(
        self, x0: int, y0: int, sky: Sky
    ) -> tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]:
        """
        Calculates the brightness values of the sky for a given x and y coordinate.

        The brightness values are calculated by integrating the light sources in the atmosphere.
        The brightness values are then returned as a 2D numpy array.
        The x and y coordinates are also returned as 2D numpy arrays.
        """
        x, y, brightness = sky.getSkyPlot(x0, y0)
        brightness = brightness[
            0, 0, :
        ]  # We have to extract the brightness values from the 3D array, that is generated for only one point

        median = np.median(brightness)
        average = np.average(brightness)
        sdev = np.std(brightness)

        self.debug.log("Sky plot statistics: ", LogLevel.DEBUG)
        self.debug.log(f"\tMedian             : {median}", LogLevel.DEBUG)
        self.debug.log(f"\tAverage            : {average}", LogLevel.DEBUG)
        self.debug.log(f"\tStandard Deviation : {sdev}", LogLevel.DEBUG)

        return x, y, brightness
