from pygame.math import Vector2

from data.game_objects.displayable import Displayable
from data.game_objects.tile import Tile


class Projectile(Displayable):
    """
    A projectile is a moving displayable object
    going in one direction at a target position.\n
    It disappears when colliding with a tile or an entity.\n
    """

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int],
                 direction: Vector2, speed: float) -> None:

        super(Projectile, self).__init__(pos, size, color)
        self.__pos: Vector2 = Vector2(pos)
        self.__direction: Vector2 = direction.normalize()
        self.__velocity: Vector2 = self.__direction * speed
        self.alive: bool = True

    @property
    def strength(self) -> Vector2:
        return self.__velocity * 1.2

    def update(self, tiles: list[Tile], delta_time: float) -> None:

        self.__pos += self.__velocity * delta_time
        self.rect.centerx = int(self.__pos.x)
        self.rect.centery = int(self.__pos.y)

        # tiles collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.alive = False