"""The CelestialObject class represents a celestial object with name and coordinates."""


class CelestialObject:
    """
    A class representing a celestial object.

    Attributes:
    name:
        The name of the object, in the format 'catalogName objectIdentifier'
    ra:
        The right ascension of the object in degrees
    dec:
        The declination of the object in degrees
    """

    __slots__ = ["name", "ra", "dec"]

    def __init__(self, name: str, ra: float, dec: float):
        """
        Initializes the CelestialObject with the given name, RA, and DEC.

        Parameters:
            name: The name of the object, in the format 'catalogName objectIdentifier'
            ra: The right ascension of the object in degrees
            dec: The declination of the object in degrees
        """
        self.name = name
        self.ra = ra
        self.dec = dec

    def __str__(self) -> str:
        """
        Returns a string representation of the celestial object.

        Returns:
            A string representation of the celestial object.
        """
        return self.name + " at RA: " + str(self.ra) + "° and DEC: " + str(self.dec) + "°"
