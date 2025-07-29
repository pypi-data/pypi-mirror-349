"""This module contains the main entry point to the LightPollutionSimulation project."""

import argparse
import sys
import lightPollutionSimulation.plotAzimuth as tpa
import lightPollutionSimulation.connector as tc
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel

# Predefined dictionary of locations
PREDEFINED_LOCATIONS = {
    1: {"location": "Helgoland left of island", "lat": 54.183267, "lon": 7.786874},
    2: {"location": "Helgoland below island", "lat": 54.124459, "lon": 7.888723},
    3: {"location": "Helgoland right of island", "lat": 54.181588, "lon": 7.992707},
    4: {"location": "Helgoland above island", "lat": 54.240333, "lon": 7.891469},
    5: {"location": "Heppenheim", "lat": 49.643836, "lon": 8.624884},
    6: {"location": "Netherland west coast", "lat": 51.724054, "lon": 3.706882},
    7: {"location": "Hut in Austria", "lat": 46.995698, "lon": 13.575762},
}


# Custom action for `--loc` print data if location is not provided
class LocAction(argparse.Action):
    """This class contains the custom --loc action for argparse."""

    def __call__(self, parser, namespace, values, option_string=None):  # type: ignore
        """Call method for the custom action."""
        if values is None:
            # Display the list of predefined locations
            print("Available predefined locations:")
            for key, loc in PREDEFINED_LOCATIONS.items():
                print(f"{key}: {loc['location']} (Lat: {loc['lat']}, Lon: {loc['lon']})")
            sys.exit(0)  # Exit after displaying the list
        else:
            # Validate the input against the dictionary keys
            try:
                location_key = int(values)
                if location_key not in PREDEFINED_LOCATIONS:
                    raise ValueError
                setattr(namespace, self.dest, location_key)
            except ValueError:
                print(f"Error: Invalid location key '{values}'. Use --loc with a valid number from the list.")
                sys.exit(1)


def main() -> None:
    """This function is the main entry point for the LightPollutionSimulation project."""
    # Define the parser and the arguments
    parser = argparse.ArgumentParser(prog="LightPollutionSimulation", description="Process some parameters.")
    parser.add_argument(
        "--r",
        "--radius",
        type=float,
        help="Radius around the location",
        metavar="(m)",
        default=30000,
    )
    parser.add_argument(
        "--h",
        "--height",
        type=int,
        help="Atmospheric height",
        metavar="(m)",
        default=10000,
    )
    parser.add_argument(
        "--l",
        "--location",
        type=str,
        help=argparse.SUPPRESS,
        action=LocAction,
        nargs="?",
    )
    parser.add_argument("--g", "--granularity", type=int, help="Granularity", default=2)
    parser.add_argument("--lat", type=float, help="Latitude for custom location", metavar="(54.183)")
    parser.add_argument("--lon", type=float, help="Longitude for custom location", metavar="(7.786)")
    parser.add_argument("--verbose", "--v", action="store_true", help="Enable verbose output")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure either
    if args.l and (args.lat or args.lon):
        sys.stderr.write("Error: You cannot specify both --location and --lat/--lon. Choose one.")
        sys.exit(1)
    elif not args.l and (args.lat is None or args.lon is None):
        sys.stderr.write("Error: You must provide --lat and --lon.")
        sys.exit(1)

    # Enable verbose
    log_level = True if args.verbose else False
    debug = DebugPipeline(verbose=log_level)

    # Display input
    if args.l:
        loc_data = PREDEFINED_LOCATIONS[args.l]
        args.lat = loc_data["lat"]
        args.lon = loc_data["lon"]
        debug.log(
            f"Using predefined location: {loc_data['location']} (Lat: {loc_data['lat']}, Lon: {loc_data['lon']})",
            LogLevel.INFO,
        )
    else:
        debug.log(f"Using custom location: Lat: {args.lat}, Lon: {args.lon}", LogLevel.INFO)

    # Print additional parameters
    if args.r:
        debug.log(f"Radius: {args.r}", LogLevel.INFO)
    if args.h:
        debug.log(f"Atmospheric height: {args.h}", LogLevel.INFO)
    if args.g:
        debug.log(f"Granularity: {args.g}", LogLevel.INFO)

    data = tc.Connector(args.r, args.h, args.lat, args.lon, args.g)
    dataList, skyPollutionMap, brightnessMap = data.main()
    plotter = tpa.Plotter()
    plotter.plotAll(dataList, skyPollutionMap, brightnessMap)


if __name__ == "__main__":
    main()
