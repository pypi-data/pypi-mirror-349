"""Provides a class for handling angles in degrees and their projections."""

import numpy as np
import lightPollutionSimulation.projection as tp
from numpy.typing import NDArray


class AngleTuple:
    """
    A class representing a tuple of angles in degrees.

    Attributes:
        altD (float): The altitude angle in degrees.
        azD (float): The azimuth angle in degrees.
    """

    __slots__ = ["altD", "azD"]

    def __init__(self, altD: float | NDArray[np.float32], azD: float | NDArray[np.float32]) -> None:
        """
        Initializes the AngleTuple object.

        Args:
            altD (float): The altitude angle in degrees.
            azD (float): The azimuth angle in degrees.
        """
        self.azD = azD
        self.altD = altD

    def __str__(self) -> str:
        """Returns a string representation of the AngleTuple object."""
        return f"alt: {self.altD}, az: {self.azD}"

    def getAngles(self) -> tuple[float, float]:
        """
        Returns the altitude and azimuth angles.

        Returns:
            tuple: A tuple containing two elements:
                - alt (float): The altitude angle.
                - az (float): The azimuth angle.
        """
        return float(self.altD), float(self.azD)

    def getRadians(self) -> tuple[float | NDArray[np.float32], float | NDArray[np.float32]]:
        """
        Returns the altitude and azimuth angles in radians.

        Returns:
            tuple: A tuple containing two elements:
                - alt (float): The altitude angle in radians.
                - az (float): The azimuth angle in radians.
        """
        return np.radians(self.altD), np.radians(self.azD)

    def getVector(self) -> NDArray[np.float32]:
        """
        Returns the vector representation of the altitude and azimuth angles.

        Radius of the sphere is 1 for simplification.
        Returns:
            np.array: A numpy array containing three elements:
                - x (float): The x component of the vector.
                - y (float): The y component of the vector.
                - z (float): The z component of the vector.
        """
        altRad, azRad = self.getRadians()
        y = np.cos(altRad) * np.cos(azRad)
        x = np.cos(altRad) * np.sin(azRad)
        z = np.sin(altRad)
        return np.array([x, -y, z])

    def getProjection(
        self, centerAlt: int = 90, centerAz: int = 0, r: int = 1
    ) -> tuple[float | NDArray[np.float32], float | NDArray[np.float32]]:
        """
        Returns the projection of the altitude and azimuth angles on a 2D plane.

        Args:
            centerAlt (int, optional): The altitude angle of the center point. Defaults to 90.
            centerAz (int, optional): The azimuth angle of the center point. Defaults to 0.
            r (int, optional): The radius of the projection. Defaults to 1.
        Returns:
            tuple: A tuple containing two elements:
                - x (float): The x coordinate of the projection.
                - y (float): The y coordinate of the projection.
        """
        projector = tp.Projection()
        x, y = projector.azimuthalEquidistantProjection(self.altD, self.azD, centerAlt, centerAz, r)
        return x, y


# if __name__ == "__main__":
#     at = AngleTuple(63, 315)
#     print(at.getAngles())
#     print(at.getVector())
#     print(at.getProjection())
