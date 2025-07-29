"""Provides functions to calculate the altitude and azimuth of a celestial object"""

import datetime
import math
import numpy as np


def calculateForTimeframe(
    RA: float,
    DEC: float,
    latitude: float,
    longitude: float,
    start_time_str: str,
    end_time_str: str,
) -> list[tuple[datetime.datetime, float]]:
    """
    Calculate the position of a celestial object over a time range.

    Parameters:
        RA (float): Right ascension of the celestial object in degrees.
        DEC (float): Declination of the celestial object in degrees.
        latitude (float): Latitude of the observer in degrees.
        longitude (float): Longitude of the observer in degrees.
        start_time_str (str): Start time of the observation in ISO format (YYYY-MM-DDTHH:MM:SS+00:00).
        end_time_str (str): End time of the observation in ISO format (YYYY-MM-DDTHH:MM:SS+00:00).
        step (float): Time step between observations in seconds.

    Returns:
        list: List of tuples containing the time and altitude of the celestial object.
     ```python
    print("hello world")
    ```
    """
    step = 60
    start_time = datetime.datetime.fromisoformat(start_time_str)
    end_time = datetime.datetime.fromisoformat(end_time_str)
    times = [
        start_time + datetime.timedelta(seconds=i)
        for i in range(0, int((end_time - start_time).total_seconds()), step)
    ]
    altitudes = [calculateAltitudeAndAzimuth(RA, DEC, latitude, longitude, time_str)[0] for time_str in times]
    return list(zip(times, altitudes))


def calculateAltitudeAndAzimuth(
    RA: float,
    DEC: float,
    latitude: float,
    longitude: float,
    time_str: datetime.datetime,
) -> tuple[float, float]:
    """
    Calculate the altitude and Azimuth of a celestial object.

    Parameters:
    RA (float): Right ascension of the celestial object in degrees.
    DEC (float): Declination of the celestial object in degrees.
    latitude (float): Latitude of the observer in degrees.
    longitude (float): Longitude of the observer in degrees.
    time_str (str): Time of observation in ISO format (YYYY-MM-DDTHH:MM:SS+00:00).

    Returns:
    float: Altitude of the celestial object in degrees.
    """
    # time = datetime.datetime.fromisoformat(time_str)
    time = time_str
    HA = calculateHourAngle(longitude, time, RA)
    altitude_sin = np.sin(degToRad(DEC)) * np.sin(degToRad(latitude)) + np.cos(degToRad(DEC)) * np.cos(
        degToRad(latitude)
    ) * np.cos(degToRad(HA))
    altitude_rad = np.arcsin(altitude_sin)
    altitude = radToDeg(altitude_rad)

    azimuth_sin = np.cos(degToRad(DEC)) * np.sin(degToRad(HA)) / np.cos(altitude_rad)
    azimuth_cos = (np.sin(degToRad(DEC)) - np.sin(degToRad(latitude)) * np.sin(altitude_rad)) / (
        np.cos(degToRad(latitude)) * np.cos(altitude_rad)
    )
    azimuth_rad = np.arctan2(azimuth_sin, azimuth_cos)
    azimuth = (radToDeg(azimuth_rad) + 360) % 360

    return altitude, azimuth


def radToDeg(rad: float) -> float:
    """
    Convert radians to degrees.

    Parameters:
        rad (float): Angle in radians.
    Returns:
        float: Angle in degrees.
    """
    return rad * (180 / math.pi)


def degToRad(deg: float) -> float:
    """
    Convert degrees to radians.

    Parameters:
        deg (float): Angle in degrees.
    Returns:
        float: Angle in radians.
    """
    return deg * (math.pi / 180)


def calculateHourAngle(longitude: float, time: datetime.datetime, RA: float) -> float:
    """
    Calculate hour angle of a celestial object.

    Parameters:
        longitude (float): The longitude of the observer in degrees.
        time (datetime.datetime): The time for which to calculate the hour angle.
        RA (float): Right ascension of the celestial object in degrees.
    Returns:
        float: The hour angle in degrees.
    """
    LST = calculateLST(longitude, time)
    HA = LST - RA
    return HA


def calculateLST(longitude: float, time: datetime.datetime) -> float:
    """
    Calculate the Local Sidereal Time (LST) for a given longitude and time.

    Parameters:
        longitude (float): The longitude of the observer in degrees.
        time (datetime.datetime): The time for which to calculate the LST.
    Returns:
        float: The Local Sidereal Time in degrees.
    """
    hours = decimalHoursFromDate(time)
    days = daysSinceJ2000(time)
    LST = 100.46 + 0.985647 * days + longitude + 15 * hours
    if LST < 0:
        LST += 10 * 360
    LST %= 360
    return LST


def decimalHoursFromDate(time: datetime.datetime) -> float:
    """
    Convert a datetime object to decimal hours.

    Parameters:
        time (datetime.datetime): The datetime object to convert.
    Returns:
        float: The time in decimal hours.
    """
    hours = time.hour
    minutes = time.minute
    seconds = time.second
    return hours + minutes / 60 + seconds / 3600


def daysSinceJ2000(time: datetime.datetime) -> float:
    """
    Calculate the number of days since J2000 (January 1, 2000, 12:00 UTC).

    Parameters:
        time (datetime.datetime): The time for which to calculate the number of days since J2000.
    Returns:
        float: The number of days since J2000.
    """
    J2000 = datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    span = time - J2000
    return span.total_seconds() / 86400
