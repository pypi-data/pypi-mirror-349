"""This module implements a ray tracing algorithm to find the indices of all voxels a ray intersects in a 3D grid."""

import numpy as np
from numba import njit
from numpy.typing import NDArray


def traceRay(
    shape: NDArray[np.int32],
    startPoint: NDArray[np.float32],
    directionVector: NDArray[np.float32],
) -> NDArray[np.int32]:
    """
    Trace a ray through a 3D grid and return the indices of the voxels it intersects.

    Parameters
        shape:
            The shape of the 3D grid (x, y, z).
        startPoint:
            The starting point of the ray (x, y, z).
        directionVector:
            The direction vector of the ray (dx, dy, dz).

    Returns
        An array of indices of the voxels that the ray intersects.
    """
    x0, y0, z0 = startPoint
    dx, dy, dz = directionVector
    # Normalize direction vector manually to avoid function call overhead
    norm = np.sqrt(dx * dx + dy * dy + dz * dz)

    if norm == 0:
        return np.empty((0, 3), dtype=np.int32)

    dx /= norm
    dy /= norm
    dz /= norm

    # Voxel indices
    ix = int(np.floor(x0))
    iy = int(np.floor(y0))
    iz = int(np.floor(z0))

    # Direction steps
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    # Compute tMax and tDelta
    tMaxX = ((ix + (step_x > 0)) - x0) / dx if dx != 0 else np.inf
    tMaxY = ((iy + (step_y > 0)) - y0) / dy if dy != 0 else np.inf
    tMaxZ = ((iz + (step_z > 0)) - z0) / dz if dz != 0 else np.inf

    tDeltaX = abs(1 / dx) if dx != 0 else np.inf
    tDeltaY = abs(1 / dy) if dy != 0 else np.inf
    tDeltaZ = abs(1 / dz) if dz != 0 else np.inf

    # Preallocate a large enough array for hitIndices
    max_steps = np.int32(shape[0] + shape[1] + shape[2])
    hitIndices = np.empty((max_steps, 3), dtype=np.int32)
    step = 0

    while 0 <= iy < shape[0] and 0 <= ix < shape[1] and 0 <= iz < shape[2]:
        hitIndices[step, 0] = ix
        hitIndices[step, 1] = iy
        hitIndices[step, 2] = iz
        step += 1

        # Move to next voxel
        if tMaxX < tMaxY and tMaxX < tMaxZ:
            tMaxX += tDeltaX
            ix += step_x
        elif tMaxY < tMaxZ:
            tMaxY += tDeltaY
            iy += step_y
        else:
            tMaxZ += tDeltaZ
            iz += step_z

    return hitIndices[:step]


traceRay = njit()(traceRay)  # Compile the function with Numba


if __name__ == "__main__":
    # Some sanity checks for the function

    shape: NDArray[np.int32] = np.ndarray((3,), dtype=np.int32)
    shape[0] = 10
    shape[1] = 10
    shape[2] = 1

    startPoint: NDArray[np.float32] = np.ndarray((3,), dtype=np.float32)
    startPoint[0] = 0
    startPoint[1] = 0
    startPoint[2] = 0

    direction: NDArray[np.float32] = np.ndarray((3,), dtype=np.float32)
    direction[0] = 1
    direction[1] = 1
    direction[2] = 0

    hitIndices = traceRay(shape, startPoint, direction)

    print("I should go through a 45° angle")
    for i in range(len(hitIndices)):
        print("\t" + str(hitIndices[i]))

    direction = np.array((1, 0, 0), dtype=np.float32)
    hitIndices = traceRay(shape, startPoint, direction)
    print("I should go parallel to the x axis")
    for i in range(len(hitIndices)):
        print("\t" + str(hitIndices[i]))

    direction = np.array((0, 1, 0), dtype=np.float32)
    hitIndices = traceRay(shape, startPoint, direction)
    print("I should go parallel to the y axis")
    for i in range(len(hitIndices)):
        print("\t" + str(hitIndices[i]))

    direction = np.array((-1, -1, 0), dtype=np.float32)
    startPoint = np.array((9, 9, 0), dtype=np.float32)
    hitIndices = traceRay(shape, startPoint, direction)
    print("I should go through a -45° angle")
    for i in range(len(hitIndices)):
        print("\t" + str(hitIndices[i]))
