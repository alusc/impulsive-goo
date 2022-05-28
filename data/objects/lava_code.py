from dataclasses import replace

from numpy import array, ndarray
from pygame import draw
from pygame.rect import Rect
from pygame.surface import Surface

from data.objects.camera_data import Camera
from data.objects.lava_data import Lava
from data.utils.constants import LAVA_SPEED, GRID_WIDTH, LAVA_SPRITES, TILE_EDGE, SCREEN_SIZE, TILE_SIZE
from data.utils.functions import animation_frame, world_to_grid


def display_lava(lava: Lava, screen: Surface, camera: Camera, timer: float) -> None:
    """
    Displays lava on screen.

    :param lava: lava data
    :param screen: screen surface
    :param camera: camera data
    :param timer: game timer
    """
    lava_rect = Rect(0, lava.y + camera.offset[1], SCREEN_SIZE[0], SCREEN_SIZE[1] - (lava.y + camera.offset[1]))
    draw.rect(screen, (254, 56, 7), lava_rect)

    # clipping lava rect position on tile grid...
    grid_pos: ndarray = world_to_grid(lava_rect.topleft + array((0, 1)) - camera.offset)  # converts grid space
    screen_pos: ndarray = grid_pos * TILE_SIZE + camera.offset  # converts back to screen space

    # ...to display lava sprites along the grid
    for i in range(GRID_WIDTH + 1):
        screen.blit(
            animation_frame(LAVA_SPRITES, timer),
            screen_pos + array((TILE_EDGE, 0)) * i + array((0, -1))
        )


def update_lava(lava: Lava, delta: float) -> Lava:
    """
    Increases continuously lava's height.

    :param lava: lava data
    :param delta: delta between two frames
    :return: updated lava rectangle
    """
    y: float = lava.y - LAVA_SPEED * delta
    return replace(lava, y=y)
