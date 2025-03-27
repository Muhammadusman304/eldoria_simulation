from enum import Enum
from entities.entity import Entity, EntityType
from typing import Tuple


class TreasureType(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


class Treasure(Entity):
    def __init__(self, position: Tuple[int, int], treasure_type: TreasureType):
        super().__init__(EntityType.TREASURE, position)
        self.treasure_type = treasure_type
        self.value = 100.0  # Starting value

        if treasure_type == TreasureType.BRONZE:
            self.symbol = "B"
        elif treasure_type == TreasureType.SILVER:
            self.symbol = "S"
        else:
            self.symbol = "G"

    def update(self, grid):
        # Treasure loses 0.1% of its value each step
        self.value *= 0.999
        return self.value > 0.1  # Returns False if treasure should be removed

    def get_value_increase(self):
        if self.treasure_type == TreasureType.BRONZE:
            return 0.03
        elif self.treasure_type == TreasureType.SILVER:
            return 0.07
        else:
            return 0.13