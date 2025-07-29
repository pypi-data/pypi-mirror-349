"""The CatalogBrowser class is used to load and query astronomical catalogs."""

import os
from lightPollutionSimulation.celestialObject import CelestialObject
from lightPollutionSimulation.debugger import DebugPipeline
from typing import List, Dict


DEFAULT_CATALOG_BASE_DIRECTORY = os.path.join(os.path.abspath(os.getcwd()), "catalogs")
DEFAULT_CATALOG_EXTENSION = ".ocat"
DEFAULT_CATALOG_SEPARATOR = "|"
DEFAULT_RA_INDEX = 0
DEFAULT_DEC_INDEX = 1
DEFAULT_IDENTIFIER_INDEX = 2


class CatalogBrowser:
    """The CatalogBrowser class is used to load and query astronomical catalogs."""

    __slots__ = ["catalogs", "identifiers", "logger"]

    def __init__(
        self,
        loadCatalogs: bool = True,
        catalogBaseDirectory: str = DEFAULT_CATALOG_BASE_DIRECTORY,
    ):
        """
        Initializes the catalog browser object.

        Loading the catalog files can be done from a base directory, that must contain the individual catalog files.

        Parameters:
        loadCatalogs:
            Whether to load the catalogs from the base directory. Defaults to True
        catalogBaseDirectory:
            The base directory where the catalogs are stored. Default value is DEFAULT_CATALOG_BASE_DIRECTORY
        """
        self.catalogs: List[Dict[str, CelestialObject]] = []  # An array containing the dictionaries of the catalogs
        # An dictionary mapping the catalog names to their index in the catalogs array
        self.identifiers: Dict[str, int] = {}
        self.logger = DebugPipeline.get_debug_pipeline()

        if loadCatalogs:
            if catalogBaseDirectory:
                self.loadCatalogs(catalogBaseDirectory)
            else:
                raise ValueError("No catalog base directory provided")

    def loadCatalogs(self, path: str) -> None:
        """
        Loads the catalogs from the specified directory and stores them inside the CatalogBrowser instance.

        Parameters:
        path:
            The path to the directory containing the catalog files
        """
        fileList = os.listdir(path)  # List of all files in the folder
        catalogList = []  # List of all catalog files in the folder, in case there are non-catalog files
        for fileName in fileList:
            if fileName.endswith(DEFAULT_CATALOG_EXTENSION):
                catalogList.append(os.path.join(path, fileName))

        for catalogIndex in range(len(catalogList)):
            file = open(catalogList[catalogIndex], "r")
            lines = file.readlines()
            file.close()

            catalogIdentifier = os.path.basename(catalogList[catalogIndex]).split(".")[0]
            self.identifiers[catalogIdentifier] = catalogIndex

            # Create a new dictionary for the catalog and populate it with the objects
            catalog = {}
            for line in lines:
                # Skip comments and empty lines
                if line.startswith("#") or line == "\n":
                    continue
                # Split the line into the object's data
                objectData = line.replace("\n", "").split(DEFAULT_CATALOG_SEPARATOR)

                if len(objectData) < 3:
                    raise ValueError("Invalid catalog format detected in file " + catalogList[catalogIndex])

                # Strip the whitespace from the data
                for i in range(len(objectData)):
                    objectData[i] = objectData[i].strip()

                # Extract the object's data and create a new celestial object
                objectIdentifier = objectData[DEFAULT_IDENTIFIER_INDEX]
                ra = float(objectData[DEFAULT_RA_INDEX])
                dec = float(objectData[DEFAULT_DEC_INDEX])

                catalog[objectIdentifier] = CelestialObject(catalogIdentifier + objectIdentifier, ra, dec)

            self.catalogs.append(catalog)

    def getObject(self, inputString: str) -> CelestialObject:
        """
        Retrieves the object from the catalog based on the input string.

        Parameters:
        inputString:
            The input string containing the catalog identifier and the object identifier.
            The format is 'catalogName objectIdentifier', case insensitive for the catalog name.
            The object identifier is case sensitive.

        Returns:
            The celestial object with the specified identifier
        """
        catalogIdentifier, objectIdentifier = self.parseInput(inputString)

        if catalogIdentifier not in self.identifiers:
            raise ValueError("Catalog identifier not found")

        # Retrieve the index of the catalog, and then the object itself from the catalog
        catalogIndex = self.identifiers[catalogIdentifier]
        objectEntry = self.catalogs[catalogIndex].get(objectIdentifier)

        if objectEntry is None:
            raise ValueError(f"Object {objectIdentifier} not found in catalog {catalogIdentifier}")

        return objectEntry

    def parseInput(self, inputString: str) -> tuple[str, str]:
        """
        Parses the input string to extract the catalog identifier and the object identifier

        Parameters:
        inputString:
            The input string containing the catalog identifier and the object identifier.
            The format is 'catalogName objectIdentifier', with the catalog name being case insensitive.

        Returns:
            A tuple containing the catalog identifier and the object identifier
        """
        if " " not in inputString:
            raise ValueError(
                "Invalid input string for catalog query. The expected format is 'catalogName objectIdentifier'"
            )

        catalogIdentifier, objectIdentifier = inputString.split(" ")

        # To increase robustness, convert the catalog identifier to uppercase, which is the format standard.
        catalogIdentifier = catalogIdentifier.upper()

        return catalogIdentifier, objectIdentifier


if __name__ == "__main__":
    cb = CatalogBrowser()

    print(cb.identifiers)

    for i in range(len(cb.catalogs)):
        print("Catalog " + str(i) + ": " + str(len(cb.catalogs[i])) + " objects")

    # Simple sanity checks. All values are close to each other, so coordinates should be similar.
    LBNNumbers = [641, 642, 650]
    LDNNumbers = [1356, 1375, 1370]
    NGCNumbers = [1027, 896, 957]
    SAONumbers = [12276, 12277, 12289]
    SH2Numbers = [190]
    VDBNumbers = [15]  # Is way off

    print("LBN Objects:")
    for number in LBNNumbers:
        print("\t" + str(cb.getObject("LBN " + str(number))))

    print("LDN Objects:")
    for number in LDNNumbers:
        print("\t" + str(cb.getObject("LDN " + str(number))))

    print("NGC Objects:")
    for number in NGCNumbers:
        print("\t" + str(cb.getObject("NGC " + str(number))))

    print("SAO Objects:")
    for number in SAONumbers:
        print("\t" + str(cb.getObject("SAO " + str(number))))

    print("SH2 Objects:")
    for number in SH2Numbers:
        print("\t" + str(cb.getObject("SH2 " + str(number))))

    print("VDB Objects:")
    for number in VDBNumbers:
        print("\t" + str(cb.getObject("VDB " + str(number))))
