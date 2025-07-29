"""Offers various map projections."""

import numpy as np
import lightPollutionSimulation.angleClass as tac
from numpy.typing import NDArray


class Projection:
    """
    Projection class for various map projections.

    This class contains methods for different map projections, including
    Lambert Azimuthal Equal-Area Projection.
    """

    def __init__(self) -> None:
        """Initializes the Projection class."""
        pass

    def __str__(self) -> str:
        """
        Returns a string representation of the Projection class.

        Returns:
            str: A string describing the Projection class.
        """
        return "Projection class for various map projections."

    def azimuthalEquidistantProjection(
        self,
        alt: float | NDArray[np.float32],
        az: float | NDArray[np.float32],
        alt_center: int = 90,
        az_center: int = 0,
        r: int = 1,
    ) -> tuple[float | NDArray[np.float32], float | NDArray[np.float32]]:
        """
        Azimuthal Equidistant Projection

        This method performs the Azimuthal Equidistant Projection
        for given altitude and azimuth angles.
        Args:
            alt (float): Altitude angle in degrees.
            az (float): Azimuth angle in degrees.
            alt_center (int, optional): Altitude center angle in degrees. Defaults to 90.
            az_center (int, optional): Azimuth center angle in degrees. Defaults to 0.
            r (int, optional): Radius of the projection. Defaults to 1.
        Returns:
            tuple: A tuple containing two elements:
                - x (float): x-coordinate of the projection.
                - y (float): y-coordinate of the projection.
        """
        # Azimuthal Equidistant Projection
        coords = tac.AngleTuple(alt, az)
        alt, az = coords.getRadians()
        alt_center = np.radians(alt_center)
        az_center = np.radians(az_center)

        sin_alt_center = np.sin(alt_center)
        cos_alt_center = np.cos(alt_center)
        sin_alt = np.sin(alt)
        cos_alt = np.cos(alt)
        delta_az = az - az_center
        cos_delta_az = np.cos(delta_az)

        cos_c = sin_alt_center * sin_alt + cos_alt_center * cos_alt * cos_delta_az

        c = np.arccos(np.clip(cos_c, -1.0, 1.0))
        x = np.zeros_like(alt)
        y = np.zeros_like(alt)
        x = r * c * np.sin(delta_az)
        y = r * c * np.cos(delta_az)

        return x, y
