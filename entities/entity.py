from enum import Enum
from typing import Tuple, Optional


class EntityType(Enum):
    EMPTY = 0
    TREASURE = 1
    HUNTER = 2
    HIDEOUT = 3
    KNIGHT = 4


class Entity:
    def __init__(self, entity_type: EntityType, position: Tuple[int, int]):
        self.type = entity_type
        self.position = position
        self.symbol = " "

    def __str__(self):
        return self.symbol

    def update(self, grid):
        pass