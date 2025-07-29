"""This module calculates the remaining intensity of light after passing through the atmosphere."""

import numpy as np
from numba import njit
from numpy.typing import NDArray

# from scipy.integrate import quad


class LightIntensity:
    """This class calculates the remaining intensity of light after passing through the atmosphere."""

    def __init__(self) -> None:
        """Initializes the LightIntensity class with the necessary constants."""
        # self.g = 9.81                # gravitational acceleration in m/s^2
        # self.M = 0.02896             # molar mass of air in kg/mol
        # self.R = 8.314               # gas constant in J/(mol*K)
        # self.T = 288.15              # earth surface temperature in K
        # self.p = 1013.25             # pressure in hPa
        # self.n = 1.0003              # refractive index of air
        # self.N = 2.547e25            # number of molecules per m^3
        # self.A = 6.022e23            # Avogadro's number in 1/mol
        # self.ma = 0.02897            # mean molar mass of air in kg/mol
        # self.wavelength = 550e-9     # wavelength of the light in cm
        # self.boltzmann = 1.38065e-23 # Boltzmann constant in J/K
        # self.mmm = 4.81e-26          # mean molecular mass of atmosphere (including N2, O2, Ar, CO2) in kg
        # self.numberDensity = 1.225   # number density of air at sea level in kg/m^3
        # self.Planck = 6.626e-34      # Planck constant in J*s
        # self.c = 299792458           # speed of light in m/s
        self.extinctionCoefficient = 0.000025  # extinction coefficient of the atmosphere in 1/m
        self.boltzmann = 1.38065e-23  # Boltzmann constant in J/K
        self.mmm = 4.81e-26  # mean molecular mass of atmosphere (including N2, O2, Ar, CO2) in kg
        self.g = 9.81  # gravitational acceleration in m/s^2
        self.T = 288.15  # earth surface temperature in K


# ------------------------------------------------------------------------------------------------------------------
# Fifth try
# Used a much more simplified approach of calculating the remaining intensity
# The values seem to be correct and good enough for our current model
# reused some of the code from the first try for the air mass factor
# ------------------------------------------------------------------------------------------------------------------

# def remainingIntensity(self, startingIntensity: float, x: float, y: float, z: float):
#     '''Calculates the remaining instensity of the light after travelling through the atmosphere following a given
#     path (vector)
#     NOTE: The angle of the path of the light has a relatively small impact on the remaining intensity,
#     should be higher but is in the current model not possible
#     NOTE: The model is still very simplified, if we find a better model which works, we implement it here
#     RETURNS: The remaining intensity of the light in W/m^2'''

#     result = startingIntensity * np.exp(-self.extinctionCoefficient * self.calculateAirMassFactor(x, y, z) * z)
#     print(f"Result: {result}")

# def calculateAirMassFactor(self, x: float, y: float, z: float):

#     length = np.sqrt(x**2 + y**2 + z**2)
#     theta = np.arccos(z / length)
#     return 1 / np.cos(theta)

extinctionCoefficient = np.float32(0.000012)  # extinction coefficient of the atmosphere in 1/m


def calculateAirMassFactor(
    x: NDArray[np.float32], y: NDArray[np.float32], z: NDArray[np.float32]
) -> NDArray[np.float32]:
    """Calculates the angle between the given vector and the zenith and then uses 1/cos(theta) to calculate"""
    length = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / length)
    result: NDArray[np.float32] = np.float32(1) / np.cos(theta)
    return result


calculateAirMassFactor = njit(parallel=True, inline="always")(calculateAirMassFactor)


def remainingIntensity(
    startingIntensity: NDArray[np.float32],
    x: NDArray[np.float32],
    y: NDArray[np.float32],
    z: NDArray[np.float32],
) -> NDArray[np.float32]:
    """
    Calculates the remaining instensity of the light after travelling through the atmosphere following a given path

    NOTE: The angle of the path of the light has a relatively small impact on the remaining intensity,
    should be higher but is in the current model not possible
    NOTE: The model is still very simplified, if we find a better model which works, we implement it here
    RETURNS: The remaining intensity of the light in W/m^2
    """
    result: NDArray[np.float32] = startingIntensity * np.exp(
        -extinctionCoefficient * calculateAirMassFactor(x, y, z) * z
    )
    return result


remainingIntensity = njit(parallel=True, inline="always")(remainingIntensity)


# if __name__ == "__main__":
#     lightIntensity = LightIntensity()
#     lightIntensity.remainingIntensity(1000, 0, 0, 10000)

if __name__ == "__main__":
    print(
        remainingIntensity(
            np.array([1000], dtype=np.float32),
            np.array([0], dtype=np.float32),
            np.array([0], dtype=np.float32),
            np.array([20000], dtype=np.float32),
        )
    )


# ------------------------------------------------------------------------------------------------------------------
# Fourth try
# Used other formulas with a more simplified approach
# Still didn't work
# ------------------------------------------------------------------------------------------------------------------


# def __init__(self):
#         self.extinctionCoefficient = 0.15  # extinction coefficient in 1/m
#         self.boltzmann = 1.38065e-23       # Boltzmann constant in J/K
#         self.mmm = 4.81e-26                # mean molecular mass in kg
#         self.g = 9.81                      # gravitational acceleration in m/s^2
#         self.T = 288.15                    # surface temperature in K

# def calculateBeer(self, height: float, startingIntensity: float):
#     optical_depth = self.calculateOpticalDepth(height)
#     remaining_intensity = startingIntensity * np.exp(-optical_depth)
#     print(f"Remaining Intensity: {remaining_intensity} W/m^2")
#     return remaining_intensity

# def calculateOpticalDepth(self, height: float):
#     scale_height = self.calculateScaleHeight()
#     print(f"Scale Height: {scale_height} m")
#     # Analytical solution for optical depth
#     tau = self.extinctionCoefficient * scale_height * (1 - np.exp(-height / scale_height))
#     print(f"Optical Depth (Analytical): {tau}")
#     return tau

# def calculateScaleHeight(self):
#     scale_height = (self.boltzmann * self.T) / (self.mmm * self.g)
#     return scale_height


# ------------------------------------------------------------------------------------------------------------------
# Third try of calculating the remaining intensity of the light going through the atmosphere
# Found some other formulas to calculate the remaining intensity
# Still didn't work
# ------------------------------------------------------------------------------------------------------------------

#     def calculateBeer(self, height: float, startingIntensity: float):
#         return startingIntensity * np.exp(-self.calculateOpticalDepth(height))

#     def calculateOpticalDepth(self, height: float):
#         #result, error = quad(self.functionToIntegrate, 0, height)
#         scaleHeight = (self.boltzmann * self.T) / (self.mmm * self.g)
#         print(f"Scale Height: {scaleHeight}")
#         result, _ = quad(
#             lambda h: self.extinctionCoefficient * np.exp(-h / scaleHeight),
#             0,
#             height
#         )
#         print(f"Optical Depth: {result}")
#         return result

#     # def functionToIntegrate(self, height: float):
#     #     scaleHeight = (self.boltzmann * self.T) / (self.mmm * self.g)
#     #     print(f"Scale Height: {scaleHeight}")
#     #     return self.extinctionCoefficient * np.exp(-height / scaleHeight)

# if __name__ == "__main__":
#     lightIntensity = LightIntensity()
#     print(f"Remaining Intensity: {lightIntensity.calculateBeer(5000, 1000)}")


# ------------------------------------------------------------------------------------------------------------------
# Second try of calculating the remaining intensity of the light going through the atmosphere
# used the Rayleigh scattering and the Planck radiation law to calculate the remaining intensity
# Integrated the Rayleigh scattering over the height of the atmosphere
# ------------------------------------------------------------------------------------------------------------------

# def calculateTemperatureAtHeight(self, height: float):
#     """Calculates the temperature at the given height using the standard atmosphere model.
#     RETURNS: The temperature at the given height in K"""
#     if height < 11000:
#         return self.T - 0.0065 * height
#     elif height >= 11000 and height < 20000:
#         return 216.65
#     else:
#         return 216.65 + 0.001 * (height - 20000)


# def calculateScaleHeight(self, height: float):
#     return (self.boltzmann * self.calculateTemperatureAtHeight(height)) / (self.mmm * self.g)


# def calculateCrossSection(self):
#     """Calculates the cross section of the given wavelength using the formula for the Rayleigh scattering.
#     cross section = (24 * pi^3 * (n^2 - 1)^2) / (wavelength^4 * N^2 * (n^2 + 2)^2)
#     NOTE: The formula is an approximation for the Rayleigh scattering. Maybe add the polarizability of the molecules
#     to the formula later.
#     RETURNS: The cross section of the given wavelength in m^2"""

#     return (24 * np.pi**3 * (self.n**2 - 1)**2) / (self.wavelength**4 * self.N**2 * (self.n**2 + 2)**2)

# def calcN(self, height: float):
#     return self.numberDensity * np.exp(-height / self.calculateScaleHeight(height))

# def calculateOpticalDensity(self, height: float):
#     tau = self.calculateCrossSection() * self.numberDensity * self.calculateScaleHeight(height)
#     print(f"Optical density: {tau}")
#     return tau #* (1-np.exp(-height / self.calculateScaleHeight(height)))

# def calculatePlanck(self, temperature: float):
#     print(f"Planck:{(2 * self.Planck * self.c**2) / (self.wavelength**5) * 1 / (np.exp((self.Planck * self.c) /
#     (self.wavelength * self.boltzmann * temperature)) - 1)}")
#     return (2 * self.Planck * self.c**2) / (self.wavelength**5) * 1 / (np.exp((self.Planck * self.c) /
#     (self.wavelength * self.boltzmann * temperature)) - 1)

# # def calculateIntensity(self, height: float):
# #     return self.calculatePlanck(self.calculateTemperatureAtHeight(height)) *
#           np.exp(-self.calculateOpticalDensity(height)) + self.calculatePlanck(self.T) *
#           sp.integrate.quad(self.calculateOpticalDensity, 0, height)[0]


# def calculateRemaingIntensity(self, height: float):
#     return self.calculatePlanck(self.T) * np.exp(-self.calculateOpticalDensity(height) *
#       1 - height / self.calculateScaleHeight(height))) +
#       self.calculatePlanck(self.calculateTemperatureAtHeight(height)) *
#       (1 - np.exp(-self.calculateOpticalDensity(height) *
#       (1 - np.exp(height / self.calculateScaleHeight(height)))))


# ------------------------------------------------------------------------------------------------------------------
# First try of calculating the remaining intensity of the light going through the atmosphere
# used the Lambert-Beer law and the Rayleigh scattering to calculate the remaining intensity
# cut the atmosphere into small slices and calculate the intensity of the light at every slice
# ------------------------------------------------------------------------------------------------------------------

# def calculateAirMassFactor(self, x: float, y: float, z: float):
#     """Calculates the angle between the given vector and the zenith and then uses 1/cos(theta) to calculate
#     the air mass factor.
#     RETURNS: The air mass factor as a float"""

#     zenith = np.array([0, 0, 1])
#     vector = np.array([x, y, z])
#     scalarProduct = np.dot(zenith, vector)
#     vectorLength = np.linalg.norm(vector)
#     zenithLength = np.linalg.norm(zenith)
#     theta = np.arccos(scalarProduct / (vectorLength * zenithLength))
#     return 1 / np.cos(theta)

# def calculateBarometricAirPressure(self, height: float):
#     """Uses the formula for the barometric air pressure to calculate the pressure at the given height.
#     pressure = p * exp(-M * g * height / (R * temperature at the given height))
#     NOTE: The pressure behaves differently at heights above 11000m, so the function is a approximation for
#           every height above 11km.
#     RETURNS: The pressure at the given height in hPa"""

#     temperature = self.calculateTemperatureAtHeight(height)

#     return self.p * np.exp(-self.M * self.g * height / (self.R * temperature))


# def calculateRayleighOpticalDepth(self, height: float):
#     """Calculates the Rayleigh optical depth at the given height and wavelength.
#     optical depth = cross section * (airPressure * Avogadro's number)/(ma * g)
#     NOTE: The gravitational constant changes with the height, so the formula is an approximation
#     RETURNS: The Rayleigh optical depth at the given height and wavelength in m^-1"""
#     crossSection = self.calculateCrossSection()
#     airPressure = self.calculateBarometricAirPressure(height)
#     #print(f"Rayleigh optical depth: {crossSection * (airPressure * self.A) / (self.ma * self.g)}")
#     return crossSection * (airPressure * self.A) / (self.ma * self.g)


# def calculateLambertBeer(self, startingIntensity: float, x: float, y: float, z: float):
#     """Calculates the intensity of the light going through the atmosphere using the Lambert-Beer law.
#     TODO: Loop for every height to add the intensity of the light at every height
#     TODO: check the height component of the vector
#     TODO: Maybe add the calculation of remaining optical depths
#     RETURNS: The intensity of the light going through the atmosphere as a float"""


#     numberOfSteps = 1000
#     airMassFactor = self.calculateAirMassFactor(x, y, z) / numberOfSteps
#     lengthOfVector = np.sqrt(x**2 + y**2 + z**2)

#     for i in range(0, numberOfSteps):
#         #print(f"{i}")
#         opticalDepth = self.calculateRayleighOpticalDepth((lengthOfVector / numberOfSteps) * i)
#         startingIntensity = startingIntensity * np.exp(-airMassFactor * opticalDepth)
#         print(f"Intensity at height {i}: {startingIntensity}")

#     print(f"Remaining intensity: {startingIntensity}")


# ------------------------------------------------------------------------------------------------------------------


# if __name__ == "__main__":
#     lightIntensity = LightIntensity()
#     print(f"Remaining Intensity: {lightIntensity.calculateBeer(5000, 1000)}")
