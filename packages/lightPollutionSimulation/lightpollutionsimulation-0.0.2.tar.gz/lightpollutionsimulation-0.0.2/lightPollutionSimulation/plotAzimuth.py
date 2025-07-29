"""Provides a class for plotting azimuthal projections and sky brightness maps."""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import lightPollutionSimulation.projection as tp
import lightPollutionSimulation.angleClass as tac
import matplotlib as mpl
import os
from lightPollutionSimulation.debugger import DebugPipeline, LogLevel
from numpy.typing import NDArray


class Plotter:
    """A class for plotting azimuthal projections and sky brightness maps."""

    def __init__(self) -> None:
        """Initializes the Plotter object."""
        self.debug = DebugPipeline.get_debug_pipeline()
        pass

    def plotProjectedCircle(self, ax: mpl.axes.Axes, radius: float, color: str) -> None:
        """
        Plots a projected circle on the given axis.

        Args:
            ax (mpl.axes.Axes): The axis to plot on.
            radius (float): The radius of the circle.
            color (mpl.colors): The color of the circle.
        """
        theta = np.linspace(0, 2 * np.pi, 100)
        projector = tp.Projection()
        xCircle, yCircle = projector.azimuthalEquidistantProjection(np.full_like(theta, radius), np.degrees(theta))
        ax.plot(xCircle, yCircle, color=color, linestyle="--", linewidth=1)

    def plotIndicatorsAndBackground(self, ax: mpl.axes.Axes) -> None:
        """
        Plots the background and indicators on the given axis.

        Args:
            ax (mpl.axes.Axes): The axis to plot on.
        """
        # filled_circle = Circle((0, 0), 1.58, color=mpl.cm.viridis(0))
        # Add the circle to the current axis
        # ax.add_patch(filled_circle)
        # North indicator
        ax.arrow(0, 0, 0, 1.58, head_width=0.1, head_length=0.1, fc="black", ec="none")
        ax.text(0, 1.7, "N", fontsize=12, ha="center", color="black")

        # East indicator
        ax.arrow(0, 0, 1.58, 0, head_width=0.1, head_length=0.1, fc="black", ec="none")
        ax.text(1.7, 0, "E", fontsize=12, va="center", color="black")

        # Bottom values
        ax.text(1.7, -1.7, "0°", fontsize=12, ha="center", color="black")
        ax.text(0, -1.7, "90°", fontsize=12, ha="center", color="black")
        # Corner value
        ax.text(-1.7, 1.7, "0°", fontsize=12, ha="right", color="black")
        # Left values
        ax.text(-1.7, -0.05, "90°", fontsize=12, ha="right", color="black")
        ax.text(-1.7, -1.7, "0°", fontsize=12, ha="right", color="black")

    def plotCenterAxis(self, ax: mpl.axes.Axes) -> None:
        """
        Plots the center axis on the given axis.

        Args:
            ax (mpl.axes.Axes): The axis to plot on.
        """
        x, y = [], []
        skyArray: NDArray[np.float32] = np.ndarray((45, 4), dtype=object)
        for az in [0, 90, 180, 270]:
            for alt in range(45):
                skyArray[alt, az // 90] = tac.AngleTuple(alt * 2, az)

        for row in skyArray:
            for angle in row:
                x1, y1 = angle.getProjection()
                x.append(x1)
                y.append(y1)
        ax.scatter(x, y, s=0.2, color="white", alpha=0.7)

    def plotData(
        self,
        ax: mpl.axes.Axes,
        x: NDArray[np.float32],
        y: NDArray[np.float32],
        brightness: NDArray[np.float32],
        norm: mpl.colors.Normalize,
    ) -> mpl.collections.PathCollection:
        """
        Plots the data on the given axis.

        Args:
            ax (mpl.axes.Axes): The axis to plot on.
            x (int): The x-coordinate of the data point.
            y (int): The y-coordinate of the data point.
            brightness (float): The brightness value of the data point.
            norm (mpl.colors): Normalization for color mapping.
        Returns:
            mpl.collections.PathCollection: The scatter plot object.
        """
        scatter = ax.scatter(x, y, c=brightness, cmap="viridis", alpha=0.5, s=10, norm=norm)
        return scatter

    def plotAll(
        self,
        data_list: list[
            tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32], mpl.colors.Normalize, str]
        ],
        skyBrightnessMap: NDArray[np.float32],
        VIIRSData: NDArray[np.float32],
    ) -> None:
        """
        Combine plots from two codes into one figure with multiple subplots.

        Parameters:
            data_list: List of tuples [(x, y, brightness, norm, title), ...] for azimuthal projection plots.
            skyBrightnessMap: Sky brightness map data for imshow.
            VIIRSData: Map area data for imshow.
        """
        self.debug.log("Plotting Projection ...", LogLevel.INFO)
        fig = plt.figure(figsize=(10, 10))
        gs = mpl.gridspec.GridSpec(2, 2, height_ratios=[1, 2])

        # First row: Sky brightness and map area
        ax1 = fig.add_subplot(gs[0, 0])
        VIIRSData = VIIRSData + 1e-10  # Avoid log(0)
        im1 = ax1.imshow(VIIRSData, cmap="gray", norm=mpl.colors.LogNorm(vmin=0.1, vmax=8000))
        ax1.set_title("VIIRS data log")
        ax1.set_xlabel("X Coordinate")
        ax1.set_ylabel("Y Coordinate")
        ax1.grid(False)
        ax1.set_aspect("equal")
        fig.colorbar(im1, ax=ax1, orientation="vertical")

        ax2 = fig.add_subplot(gs[0, 1])
        skyBrightnessMapHeight, skyBrightnessMapWidth = skyBrightnessMap.shape
        im2 = ax2.imshow(
            skyBrightnessMap,
            cmap="inferno",
            norm=mpl.colors.LogNorm(vmin=0.1, vmax=8000),
        )
        ax2.set_title("Sky Brightness Map log")
        ax2.set_xlabel("X Coordinate")
        ax2.set_ylabel("Y Coordinate")
        ax2.grid(False)
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
        ax2.add_patch(skyBrightnessRect)
        fig.colorbar(im2, ax=ax2, orientation="vertical").set_label("Brightness Intensity")

        # Second row: Projected azimuthal plots
        for i, data in enumerate(data_list):
            ax = fig.add_subplot(gs[1, i])
            x, y, brightness, norm, title = data

            radiiRed, radiiBlue = [35, 45], [0, 15, 30, 45, 60, 75]

            for radius in radiiBlue:
                self.plotProjectedCircle(ax, radius, "blue")
            for radius in radiiRed:
                self.plotProjectedCircle(ax, radius, "red")

            self.plotIndicatorsAndBackground(ax)
            scatter = self.plotData(ax, x, y, brightness, norm)
            self.plotCenterAxis(ax)
            fig.colorbar(scatter, ax=ax, label="Brightness", orientation="vertical")
            ax.set_facecolor("white")
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_title(title, loc="left")

        imagePath = os.path.join(os.getcwd(), "out", "skyPlot.png")
        plt.tight_layout()
        plt.savefig(imagePath, dpi=500)
        plt.show()
