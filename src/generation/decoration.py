from random import random

from numpy import ndarray, asarray, empty, ndenumerate, array
from numpy.random import choice, randint
from pygame import Rect
from scipy.ndimage import maximum_filter, minimum_filter

from src.tiles.tile import Tile
from src.utils.constants import GRID_SIZE, FOSSIL_DENSITY, FOSSIL_SPRITES, SPIKE_SPRITES, SPIKE_DENSITY, TILE_SIZE


def generate_decoration(cave: ndarray) -> ndarray:
    """
    Generates decoration grid according to cave.

    :param cave: boolean grid
    :return: tile grid
    """
    fossil_grid: ndarray = _generate_fossils_grid(cave)
    spike_grid: ndarray = _generate_spikes_grid(cave)
    decoration_grid: ndarray = empty(fossil_grid.shape).astype(Tile)

    for (i, j), _ in ndenumerate(cave):

        # fossil
        if fossil_grid[i, j]:
            decoration_grid[i, j] = Tile(
                Rect(array((i, j)) * TILE_SIZE, tuple(TILE_SIZE)),
                FOSSIL_SPRITES[randint(0, len(FOSSIL_SPRITES))]
            )

        # spike
        elif spike_grid[i, j] and random() < SPIKE_DENSITY:
            decoration_grid[i, j] = Tile(
                Rect(array((i, j)) * TILE_SIZE, tuple(TILE_SIZE)),
                SPIKE_SPRITES[randint(0, len(SPIKE_SPRITES))]
            )

        else:
            decoration_grid[i, j] = None

    return decoration_grid


def _generate_fossils_grid(cave: ndarray) -> ndarray:
    """
    Generates the fossils in the cave in random positon where a full neighborhood tile is already present.

    :param cave: boolean grid
    :return: boolean grid
    """
    fossils: ndarray = choice(
        a=(True, False),
        size=GRID_SIZE,
        p=[FOSSIL_DENSITY, 1 - FOSSIL_DENSITY]
    )
    pattern: ndarray = asarray([
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ])
    return cave & fossils & minimum_filter(cave, footprint=pattern, mode='constant')


def _generate_spikes_grid(cave: ndarray) -> ndarray:
    """
    Returns boolean grid indicating placement of spikes in their map.
    Spikes have to possess one top neighbor to be generated.

    :param cave: boolean grid
    :return: boolean grid
    """
    pattern: ndarray = asarray([
        [False, False, False],
        [True, False, False],
        [False, False, False]
    ])
    return ~cave & maximum_filter(cave, footprint=pattern, mode='constant')
