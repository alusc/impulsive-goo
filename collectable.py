from config import TILE_SCALE
from displayable import Displayable


class Collectable(Displayable):

    def __init__(self, pos: tuple[int, int], sprite: str) -> None:
        super(Collectable, self).__init__(pos, (int(TILE_SCALE / 2), int(TILE_SCALE / 2)), sprite)
        self.is_active: bool = True

    def display(self) -> None:
        if self.is_active:
            super(Collectable, self).display()