"""
This module implements the LightPropagation class .

The LightPropagation class is used to propagate light sources through a 3D grid
representing the atmosphere. It uses Numba for parallel processing and JIT compilation to speed up the calculations.
It also provides functions to integrate the light intensity along paths defined by direction vectors starting from
given points.
"""

import time

import numpy as np
from numpy.typing import NDArray
from numba import njit, prange, set_num_threads

from lightPollutionSimulation.lightIntensity import remainingIntensity
import lightPollutionSimulation.rayTracing as rt
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel
import psutil


# This controls, whether all cores are used. Set to true to enable
# the use of all cores, false to disable N_CORES_DISABLED cores
FAST_MODE = False

# This is the number of cores that are disabled in fast mode.
# This is used to speed up the calculations, but it is not recommended for production use.
N_CORES_DISABLED = 2


def getUsedProcessorCount() -> int:
    """
    This function returns the number of logical cores that are used for the calculations.

    It uses psutil to find all logical cores and disables N_CORES_DISABLED cores in case the
    FAST_MODE is set to false.
    """
    logicalCoreCountReturnValue = psutil.cpu_count(logical=True)
    logicalCoreCount = logicalCoreCountReturnValue if logicalCoreCountReturnValue is not None else 1

    if not FAST_MODE:
        if logicalCoreCount > N_CORES_DISABLED:
            logicalCoreCount -= N_CORES_DISABLED

    return logicalCoreCount


set_num_threads(getUsedProcessorCount())  # Set the number of threads to use for Numba parallelization


def propagateLightSourcesWorker(
    discreteVolumeValues: NDArray[np.float32],
    y: int,
    nonZeroSources: NDArray[np.float32],
    sourceXMeters: NDArray[np.float32],
    sourceYMeters: NDArray[np.float32],
    unitSideLengthX: float,
    unitSideLengthY: float,
    unitSideLengthZ: float,
    maxDistance: float,
) -> None:
    """
    This function propagates the light emitted from the sources through the atmosphere in one y slice.

    It simplifies the light propagation by assuming that the light is emitted isotropically.
    This worker function has been externalized to facilitate multithreading in numba combined with progress reports.

    Parameters:
    discreteVolumeValues:
        Array containing the discrete volume units as modeled in the atmosphere
    nonZeroSources:
        Array containing the intensity values of the light sources at the positions where they are non-zero
    sourceXMeters:
        Array containing the x-coordinates of the light sources in meters
    sourceYMeters:
        Array containing the y-coordinates of the light sources in meters
    unitSideLengthX:
        The length of a discrete volume unit in the x-direction in meters
    unitSideLengthY:
        The length of a discrete volume unit in the y-direction in meters
    unitSideLengthZ:
        The length of a discrete volume unit in the z-direction in meters
    transmissionPerMeter:
        The transmission rate of the atmosphere per meter of air that the light travels through.
    maxDistance:
        The maximum distance in meters that the light can travel. This is used to avoid artifacts at the
        edges of the modeled area.
    """
    fourPi = np.float32(4 * np.pi)
    maxDistanceSquared = np.float32(maxDistance**2)

    x1, z1 = discreteVolumeValues.shape

    unitYMeters = np.float32(
        (y + 0.5) * unitSideLengthY
    )  # We add 0.5 here, since we are using the center of the unit. This applies to all other occurrences also.
    unitArea = np.float32(unitSideLengthX * unitSideLengthY)  # Take the area of the unit into account

    dy = sourceYMeters - unitYMeters
    dySquared = dy**2  # Pre-compute this only once, since it is constant for each y slice

    for x in prange(x1):
        unitXMeters = (x + 0.5) * unitSideLengthX
        dx = sourceXMeters - unitXMeters

        for z in range(z1):
            unitZMeters = (z + 0.5) * unitSideLengthZ

            distancesSquared = (
                dx**2 + dySquared + unitZMeters**2
            )  # Calculate the distances between each source and the discrete volume unit

            validIndices = (
                distancesSquared <= maxDistanceSquared
            )  # Only consider sources that are within the maximum distance

            validDistancesSquared = distancesSquared[validIndices]
            validSources: NDArray[np.float32] = nonZeroSources[validIndices]

            dyValid = dy[validIndices]
            dxValid = dx[validIndices]
            dzValid = np.array((unitZMeters), dtype=np.float32)

            sphereSurfaceAreas = (
                fourPi * validDistancesSquared
            )  # Calculate the surface areas of the spheres around each source for each source
            unitIntensities = remainingIntensity(
                validSources, dxValid, dyValid, dzValid
            )  # Calculate how much light is actually left after the path and cast it as an array

            unitIntensities /= sphereSurfaceAreas  # Distribute the light over the surface area

            for i in range(len(validSources)):  # In numba, for loops are faster than numpy.sum
                discreteVolumeValues[x, z] += unitIntensities[
                    i
                ]  # Add the intensity of each source to the discrete volume unit

    # Since each discrete volume unit receives light evenly from all directions,
    # we assume the area to be uniform for all units.
    discreteVolumeValues *= unitArea


propagateLightSourcesWorker = njit(parallel=True)(propagateLightSourcesWorker)  # Compile the function with Numba


def integrateVectorsWorker(
    scaledDirectionVectors: NDArray[np.float32],
    discreteVolumeUnits: NDArray[np.float32],
    startPoint: NDArray[np.float32],
    startPointMeters: NDArray[np.float32],
    discreteVolumeUnitSideLengthX: float,
    discreteVolumeUnitSideLengthY: float,
    discreteVolumeUnitSideLengthZ: float,
    maxDistance: float,
) -> NDArray[np.float32]:
    """
    Integrates the intensities for all vectors starting at a given single start point.

    Parameters:
    scaledDirectionVectors:
        The direction vectors scaled to align with the internally used coordinate system. It
        is expected to be in the format (n, 3), where n is the number of direction vectors
        and the 3 values are (x, y, z) in this order.
    discreteVolumeUnits:
        The discrete volume units as modeled in the atmosphere
    startPoint:
        The starting point of the vectors in discrete volume unit coordinates. It is expected
        to be in the format (x, y, z).
    startPointMeters:
        The starting point of the vectors scaled to meters. It is expected to be in the format (x, y, z).
    discreteVolumeUnitSideLengthX:
        The length of a discrete volume unit in the x-direction in meters
    discreteVolumeUnitSideLengthY:
        The length of a discrete volume unit in the y-direction in meters
    discreteVolumeUnitSideLengthZ:
        The length of a discrete volume unit in the z-direction in meters
    maxDistance:
        The maximum distance in meters that the light can travel. This is used to avoid artifacts
        at the edges of the modeled area.

    Returns:
        An array containing the intensities of the paths for each direction vector.
    """
    pathIntensities = np.zeros(len(scaledDirectionVectors), dtype=np.float32)

    for directionVectorIndex in prange(scaledDirectionVectors.shape[0]):
        directionVector = scaledDirectionVectors[directionVectorIndex, :]

        # We skip the first element, since it is the starting point itself with a radius of 0
        hitCoordinates = rt.traceRay(
            np.array(discreteVolumeUnits.shape, dtype=np.int32),
            startPoint,
            directionVector,
        )[1:]

        # The vector immediately leaves the simulated atmosphere. In this case, the intensity is 0 and we can skip
        if len(hitCoordinates) == 0:
            continue

        # Extract the x, y and z indices of the hit coordinates
        xIndices = hitCoordinates[:, 0]
        yIndices = hitCoordinates[:, 1]
        zIndices = hitCoordinates[:, 2]

        totalIntensity = np.zeros(1, dtype=np.float32)
        for coordinateIndex in range(len(xIndices)):
            xIndex = xIndices[coordinateIndex]
            yIndex = yIndices[coordinateIndex]
            zIndex = zIndices[coordinateIndex]

            # Convert the current unit index to meters
            xMeters = xIndex * discreteVolumeUnitSideLengthX
            yMeters = yIndex * discreteVolumeUnitSideLengthY
            zMeters = zIndex * discreteVolumeUnitSideLengthZ

            # Calculate the distance between the discrete volume unit and the starting point
            radius = np.sqrt(
                (xMeters - startPointMeters[0]) ** 2
                + (yMeters - startPointMeters[1]) ** 2
                + (zMeters - startPointMeters[2]) ** 2
            )

            if radius > maxDistance:
                break

            # Calculate the remaining intensity of the light after the path
            remaining = remainingIntensity(
                discreteVolumeUnits[yIndex, xIndex, zIndex],
                xMeters - startPointMeters[0],
                yMeters - startPointMeters[1],
                zMeters - startPointMeters[2],
            )

            # and add it to the total intensity
            totalIntensity += remaining

        pathIntensities[directionVectorIndex] = totalIntensity[0]

    return pathIntensities


integrateVectorsWorker = njit(parallel=True, inline="always")(integrateVectorsWorker)


def integratePointsWorker(
    scaledDirectionVectors: NDArray[np.float32],
    discreteVolumeUnits: NDArray[np.float32],
    startPoints: NDArray[np.int32],
    startPointsMeters: NDArray[np.float32],
    discreteVolumeUnitSideLengthX: float,
    discreteVolumeUnitSideLengthY: float,
    discreteVolumeUnitSideLengthZ: float,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    maxDistance: float,
) -> NDArray[np.float32]:
    """
    Integrates the intensities for all vectors from all starting points that are provided.

    Parameters:
    scaledDirectionVectors:
        The direction vectors scaled to align with the internally used coordinate system.
        It is expected to be in the format (n, 3), where n is the number of direction vectors
        and the 3 values are (x, y, z).
    discreteVolumeUnits:
        The discrete volume units as modeled in the atmosphere.
    startPoints:
        The starting points of the vectors in discrete volume unit coordinates. It is expected
        to be a 2d array with the format (n, 3), where n is the number of starting points and
        the 3 values are (x, y, z).
    startPointsMeters:
        The starting points of the vectors scaled to meters. It is expected to be a 2d array
        with the format (n, 3), where n is the number of starting points and the 3 values are (x, y, z).
    discreteVolumeUnitSideLengthX:
        The length of a discrete volume unit in the x-direction in meters
    discreteVolumeUnitSideLengthY:
        The length of a discrete volume unit in the y-direction in meters
    discreteVolumeUnitSideLengthZ:
        The length of a discrete volume unit in the z-direction in meters
    x0:
        The x-coordinate of the lower left corner of the area that is modeled, inclusive
    y0:
        The y-coordinate of the lower left corner of the area that is modeled, inclusive
    x1:
        The x-coordinate of the upper right corner of the area that is modeled, exclusive
    y1:
        The y-coordinate of the upper right corner of the area that is modeled, exclusive
    maxDistance:
        The maximum distance in meters that the light can travel. This is used to avoid
        artifacts at the edges of the modeled area.

    Returns:
    intensitiesPerPoint:
        A 3D numpy array containing the intensities for all starting points and all
        direction vectors. The shape is (y1 - y0, x1 - x0, len(scaledDirectionVectors)).
        For each pair of coordinates (x, y) in the area that is modeled, the intensities
        for all direction vectors are stored in the third dimension.
    """
    intensitiesPerPoint = np.zeros((y1 - y0, x1 - x0, scaledDirectionVectors.shape[0]), dtype=np.float32)

    for startPointIndex in prange(startPoints.shape[0]):
        startPoint = startPoints[startPointIndex, :]
        startPointMeters = startPointsMeters[startPointIndex, :]

        intensitiesPerPoint[np.int32(startPoint[1] - y0), np.int32(startPoint[0] - x0), :] = integrateVectorsWorker(
            scaledDirectionVectors,
            discreteVolumeUnits,
            startPoint.astype(np.float32),
            startPointMeters,
            discreteVolumeUnitSideLengthX,
            discreteVolumeUnitSideLengthY,
            discreteVolumeUnitSideLengthZ,
            maxDistance,
        )

    return intensitiesPerPoint


integratePointsWorker = njit(parallel=True)(integratePointsWorker)


class LightPropagation:
    """
    The LightPropagation class models the propagation of light through the atmosphere by using discrete blocks.

    It also offers functions to integrate along paths through the atmosphere.
    """

    __slots__ = [
        "lightSourceMap",
        "discreteVolumeUnits",
        "maxAtmosphereHeight",
        "x1",
        "y1",
        "z1",
        "discreteVolumeUnitSideLengthX",
        "discreteVolumeUnitSideLengthY",
        "discreteVolumeUnitSideLengthZ",
        "mapPixelXLength",
        "mapPixelYLength",
        "width",
        "maxDistance",
        "logger",
    ]

    def __init__(
        self,
        lightSourceMap: NDArray[np.float32],
        mapPixelXLength: float,
        mapPixelYLength: float,
        width: float,
        maxAtmosphereHeight: float,
        maxDistance: float = 0.0,
    ):
        """
        This function initializes the LightPropagation object.

        Parameters:
        lightSourceMap:
            2D array containing the intensity values of the light sources as provided from the VIIRS maps.
        mapPixelXLength:
            The length of a pixel of the VIIRS map in the x-direction in meters
        mapPixelYLength:
            The length of a pixel of the VIIRS map in the y-direction in meters
        width:
            The width of the area that is modeled in meters, one side length
        maxAtmosphereHeight:
            The height of the atmosphere that is modeled in meters
        maxDistance:
            The maximum distance in meters that the light can travel. This is used to avoid artifacts at
            the edges of the modeled area. The default is 0.0, in which case self.width/2 is used.
        """
        self.lightSourceMap = lightSourceMap.astype(np.float32)

        self.maxAtmosphereHeight = maxAtmosphereHeight
        self.mapPixelXLength = mapPixelXLength
        self.mapPixelYLength = mapPixelYLength
        self.width = width

        if maxDistance == 0.0:
            self.maxDistance = width / 2
        else:
            self.maxDistance = maxDistance

        self.logger = DebugPipeline.get_debug_pipeline()

    def buildDiscreteVolumeUnits(self) -> None:
        """
        Initializes the internal atmosphere model.

        Needs to be called before propagating the light sources.
        """
        self.discreteVolumeUnitSideLengthX = self.mapPixelXLength
        self.discreteVolumeUnitSideLengthY = self.mapPixelYLength
        self.discreteVolumeUnitSideLengthZ = np.min(
            [self.discreteVolumeUnitSideLengthX, self.discreteVolumeUnitSideLengthY]
        )

        # Calculate the number of DiscreteVolumeUnits in each dimension
        self.x1 = int(np.ceil(self.width / self.discreteVolumeUnitSideLengthX))
        self.y1 = int(np.ceil(self.width / self.discreteVolumeUnitSideLengthY))
        self.z1 = int(np.ceil(self.maxAtmosphereHeight / self.discreteVolumeUnitSideLengthZ))

        self.discreteVolumeUnits = np.zeros((self.y1, self.x1, self.z1), dtype=np.float32)

        self.logger.log("LightPropagation object created\n", LogLevel.DEBUG)

    def propagateLightSources(self) -> None:
        """
        Propagates the light sources through the atmosphere.

        Needs to be called after buildDiscreteVolumeUnits.
        """
        self.logger.log("Propagating light sources ...", LogLevel.INFO)

        nonZeroIndices = np.nonzero(self.lightSourceMap)
        sourceYIndices, sourceXIndices = nonZeroIndices
        sourceXMeters = (sourceXIndices * self.mapPixelXLength).astype(np.float32)
        sourceYMeters = (sourceYIndices * self.mapPixelYLength).astype(np.float32)

        nonZeroIntensities = self.lightSourceMap[nonZeroIndices]

        realStartTime = time.time()
        for y in range(self.y1):
            propagateLightSourcesWorker(
                self.discreteVolumeUnits[y, :, :],
                y,
                nonZeroIntensities,
                sourceXMeters,
                sourceYMeters,
                self.discreteVolumeUnitSideLengthX,
                self.discreteVolumeUnitSideLengthY,
                self.discreteVolumeUnitSideLengthZ,
                self.maxDistance,
            )
            text = f"""Progress: {'%4.f' % (y + 1)}/{self.y1} => {'%6.2f' % np.round((y + 1) / self.y1 * 100, 2)}% \
                    Approximate time left {'%.2f' % ((time.time() - realStartTime) / (y + 1) * (self.y1 - y + 1))}s """
            self.logger.log(text, LogLevel.UPDATED)
        print("")

    def integrateAlongPaths(
        self,
        startPoints: NDArray[np.float32],
        directionVectors: NDArray[np.float32],
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> NDArray[np.float32]:
        """
        Integrate the intensity along all paths defined by all direction vectors starting from all the starting points.

        Parameters:
        startPoints:
            The starting points of the vectors in discrete volume unit coordinates. It is expected to be a 2d array
            with the format (n, 3), where n is the number of starting points and the 3 values are (x, y, z).
        directionVectors:
            The direction vectors along which the light intensity is integrated. It is expected to be in the
            format (n, 3), where n is the number of direction vectors and the 3 values are (x, y, z).
        x0:
            The x-coordinate of the lower left corner of the area that is modeled, inclusive
        y0:
            The y-coordinate of the lower left corner of the area that is modeled, inclusive
        x1:
            The x-coordinate of the upper right corner of the area that is modeled, exclusive
        y1:
            The y-coordinate of the upper right corner of the area that is modeled, exclusive

        Returns:
            A 3D numpy array containing the intensities for all starting points and all direction vectors.
            The shape is (y1 - y0, x1 - x0, len(scaledDirectionVectors)).
            For each pair of coordinates (x, y) in the area that is modeled, the intensities for all direction
            vectors are stored in the third dimension.
        """
        scalingIntoMeters = np.array(
            [
                self.mapPixelXLength,
                self.mapPixelYLength,
                self.discreteVolumeUnitSideLengthZ,
            ]
        )

        scaledDirectionVectors = np.zeros((len(directionVectors), 3), dtype=np.float32)
        for i in range(len(scaledDirectionVectors)):
            scaledDirectionVectors[i, :] = (
                directionVectors[i] / scalingIntoMeters
            )  # Scale the direction vectors to meters
            scaledDirectionVectors[i, :] /= np.sqrt(
                np.sum(scaledDirectionVectors[i] ** 2)
            )  # Normalize the direction vectors

        startPointsMeters = startPoints * np.array(
            [
                self.mapPixelXLength,
                self.mapPixelYLength,
                self.discreteVolumeUnitSideLengthZ,
            ]
        )

        integratedIntensitiesPerPoint: NDArray[np.float32] = integratePointsWorker(
            scaledDirectionVectors,
            self.discreteVolumeUnits,
            startPoints.astype(np.int32),
            startPointsMeters,
            self.discreteVolumeUnitSideLengthX,
            self.discreteVolumeUnitSideLengthY,
            self.discreteVolumeUnitSideLengthZ,
            x0,
            y0,
            x1,
            y1,
            self.maxDistance,
        )

        return integratedIntensitiesPerPoint


if __name__ == "__main__":
    # Initialization parameters
    pixelWidth = 334.0
    pixelHeight = 462.0
    width = 25 * 1e3
    atmosphereHeight = 10 * 1e3

    # Create sourcesMap with random sources at random positions
    sourcesMap = np.zeros((int(width / pixelHeight), int(width / pixelWidth)), dtype=np.float32)
    n = 100
    for _ in range(n):
        y = np.random.randint(0, sourcesMap.shape[0])
        x = np.random.randint(0, sourcesMap.shape[1])
        sourcesMap[y, x] += np.random.rand()

    # Instantiate LightPropagation
    lp = LightPropagation(sourcesMap, pixelWidth, pixelHeight, width, atmosphereHeight)

    startBuilding = time.time()
    lp.buildDiscreteVolumeUnits()
    print("Building the DiscreteVolumeUnits took: ", time.time() - startBuilding)

    startPropagation = time.time()
    lp.propagateLightSources()
    print("Propagating the light sources took   : ", time.time() - startPropagation)

    print("Shape of the discrete volume units   : ", lp.discreteVolumeUnits.shape)
    print("Shape of the sources map             : ", sourcesMap.shape)

    # lightPollutionMap = lpm.LightPollutionMap(sourcesMap, pixelWidth, pixelHeight, width, atmosphereHeight, lp)
    # lightPollutionMap.generateAndDrawLightPollutionMap()
