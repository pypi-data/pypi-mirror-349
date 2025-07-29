"""
This module implements the LightPollutionMap class.

The LightPollutionMap class is used to generate a light pollution map based on the given mapArea from the VIIRS light
irradiance data. The sky brightness that is plotted on this map is calculated as the average of the
night sky brightness in different directions for each point of the map.
It uses the LightPropagation class to propagate light sources and calculate the average night sky
brightness in different directions for each point of the map.
"""

import math
import os
from time import time

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from numpy.typing import NDArray

import lightPollutionSimulation.mapCoordinates as mc
import lightPollutionSimulation.lightPropagation as lp
import lightPollutionSimulation.angleClass as ac
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel


class LightPollutionMap:
    """
    This class is used to generate a light pollution map based on the given mapArea from the VIIRS irradiance data.

    The sky brightness that is plotted on this map is calculated as the average of the
    night sky brightness in different directions for each point of the map.
    """

    __slots__ = ["mapArea", "lightPropagator", "logger"]

    def __init__(
        self,
        mapArea: NDArray[np.float32],
        pixelLengthX: float,
        pixelLengthY: float,
        width: float,
        maxAtmosphereHeight: float = 10 * 1e3,
        propagator: lp.LightPropagation | None = None,
    ):
        """
        Initializes the LightPollutionMap object.

        Parameters:
        mapArea:
            The mapArea that is used to generate the light pollution map. It is expected to be a 2D numpy array
            containing the intensity values in linear intensity units.
        pixelLengthX:
            The length of a pixel in the x-direction in meters.
        pixelLengthY:
            The length of a pixel in the y-direction in meters.
        width:
            The width of the mapArea in meters. This must be the length of one side of the quadratic mapArea.
        maxAtmosphereHeight:
            The maximum height of the atmosphere in meters. The default value is 10 * 1e3 meters.
        propagator:
            The light propagator object that is used to propagate the light sources. If this is None, a new
            LightPropagation object is created with the given parameters.
            Pass your own light propagator object, in case you already have one, to avoid unnecessary repetitive
            light propagation.
        """
        self.mapArea = mapArea
        self.logger = DebugPipeline.get_debug_pipeline()

        if propagator is not None:
            self.lightPropagator = propagator
        else:
            self.lightPropagator = lp.LightPropagation(mapArea, pixelLengthX, pixelLengthY, width, maxAtmosphereHeight)
            self.lightPropagator.buildDiscreteVolumeUnits()

            startTime = time()
            self.lightPropagator.propagateLightSources()
            self.logger.log(f"Light propagation took {time() - startTime} seconds", LogLevel.DEBUG)

        self.logger.log("LightPollutionMap object initialized", LogLevel.DEBUG)

    def generateLightPollutionMap(self, altMin: int = 45, altStep: int = 15, azStep: int = 45) -> NDArray[np.float32]:
        """
        Generates a 2d numpy array representing the light pollution map.

        For each point inside the returned light pollution map, the average of the night sky
        brightness in different directions is calculated.

        Parameters:
        altMin:
            The minimum altitude angle in degrees. The default value is 45 degrees, as this
            limits the calculations to a reasonable altitude that is actually relevant.
        altStep:
            The step size of the altitude angle in degrees. The default value is 15 degrees.
        azStep:
            The step size of the azimuth angle in degrees. The default value is 45 degrees.

        Returns:
            A 2D numpy array representing the light pollution map.
        """
        self.logger.log("Generating Light Pollution Map ...", LogLevel.INFO)
        vectorsList = []
        for alt in range(altMin, 90 - altStep, altStep):
            for az in range(0, 360, azStep):
                vectorsList.append(ac.AngleTuple(alt, az).getVector())
        vectorsList.append(ac.AngleTuple(90, 0).getVector())
        vectors = np.array(vectorsList, dtype=np.float32)

        mapWidth, mapHeight, _ = self.lightPropagator.discreteVolumeUnits.shape

        skyBrightnessMap = np.zeros((mapWidth, mapHeight), dtype=np.float32)

        startPoints = np.zeros((skyBrightnessMap.shape[0] * skyBrightnessMap.shape[1], 3), dtype=np.float32)
        for x in range(skyBrightnessMap.shape[1]):
            for y in range(skyBrightnessMap.shape[0]):
                startPoints[y * skyBrightnessMap.shape[1] + x] = np.array([x, y, 0])

        x0 = 0
        y0 = 0
        x1 = skyBrightnessMap.shape[1]
        y1 = skyBrightnessMap.shape[0]

        start = time()
        integratedIntensities = self.lightPropagator.integrateAlongPaths(startPoints, vectors, x0, y0, x1, y1)
        self.logger.log(
            f"Integration along all paths for all points took {time() - start} seconds",
            LogLevel.DEBUG,
        )

        for x in range(skyBrightnessMap.shape[1]):
            for y in range(skyBrightnessMap.shape[0]):
                skyBrightnessMap[y, x] = np.average(integratedIntensities[y, x, :])

        self.logger.log("Sky brightness map statistics", LogLevel.DEBUG)
        self.logger.log(f"\tMedian: {np.median(skyBrightnessMap)}", LogLevel.DEBUG)
        self.logger.log(f"\tAverage: {np.mean(skyBrightnessMap)}", LogLevel.DEBUG)
        self.logger.log(f"\tStandard deviation: {np.std(skyBrightnessMap)}", LogLevel.DEBUG)

        self.logger.log("Finished generating Light Pollution Map.", LogLevel.INFO)

        return skyBrightnessMap

    def generateAndDrawLightPollutionMap(self, altMin: int = 40, altStep: int = 5, azStep: int = 18) -> None:
        """
        Generates the light pollution map and draws it using matplotlib, next to the VIIRS data.

        Parameters:
        altMin:
            The minimum altitude angle in degrees. The default value is 40 degrees.
        altStep:
            The step size of the altitude angle in degrees. The default value is 5 degrees.
        azStep:
            The step size of the azimuth angle in degrees. The default value is 18 degrees.
        """
        lightSourcesMap = self.mapArea + 1e-10

        skyBrightnessMap = self.generateLightPollutionMap(altMin, altStep, azStep)
        skyBrightnessMap += 1e-10

        skyBrightnessMapHeight, skyBrightnessMapWidth = skyBrightnessMap.shape

        skyBrightnessMapHeight, skyBrightnessMapWidth = skyBrightnessMap.shape

        fig, axes = plt.subplots(1, 2, figsize=(14, 7))

        axes[0].imshow(lightSourcesMap, cmap="gray", norm=colors.LogNorm(vmin=0.1, vmax=8000))
        axes[0].set_title("Log(VIIRS data)")
        axes[0].set_xlabel("X Coordinate")
        axes[0].set_ylabel("Y Coordinate")
        axes[0].grid(False)

        axes[1].imshow(skyBrightnessMap, cmap="inferno", norm=colors.LogNorm(vmin=0.1, vmax=8000))
        axes[1].set_title("Log(Sky Brightness Map)")
        axes[1].set_xlabel("X Coordinate")
        axes[1].set_ylabel("Y Coordinate")
        axes[1].grid(False)

        skyBrightnessRect = Rectangle(
            (
                math.floor(skyBrightnessMapWidth * 0.1),
                math.floor(skyBrightnessMapHeight * 0.1),
            ),
            math.floor(skyBrightnessMapWidth * 0.8),
            math.floor(skyBrightnessMapHeight * 0.8),
            edgecolor="white",
            facecolor="none",
            linewidth=1,
        )
        axes[1].add_patch(skyBrightnessRect)

        imagePath = os.path.join(os.getcwd(), "out", "lightPollutionMap.png")
        plt.tight_layout()
        plt.savefig(imagePath, dpi=500)
        plt.show()


if __name__ == "__main__":
    lat0 = 49.643836
    lon0 = 8.624884
    width = 25 * 1e3
    atmosphereHeight = 2 * 1e3

    mapPath = os.path.join(os.getcwd(), "maps", "viirs_2023_raw_global.tif")
    mp = mc.MapProvider(mapPath)
    mapArea, pixelWidth, pixelHeight = mp.getBrightnessOfPixelByCoordinates(width, lat0, lon0)

    lpm = LightPollutionMap(mapArea, pixelWidth, pixelHeight, 2 * width, atmosphereHeight)
    lpm.generateAndDrawLightPollutionMap()
