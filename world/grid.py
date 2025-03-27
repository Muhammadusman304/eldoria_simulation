from typing import Dict, Tuple, List, Optional
from entities.entity import Entity, EntityType
import random


class EldoriaGrid:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.entities = []

    def add_entity(self, entity: Entity, position: Tuple[int, int]) -> bool:
        x, y = position
        if self.grid[x][y] is not None:
            return False

        entity.position = position
        self.grid[x][y] = entity
        self.entities.append(entity)
        return True

    def move_entity(self, old_pos: Tuple[int, int], new_pos: Tuple[int, int]) -> bool:
        old_x, old_y = old_pos
        new_x, new_y = new_pos

        entity = self.grid[old_x][old_y]
        if entity is None or self.grid[new_x][new_y] is not None:
            return False

        self.grid[old_x][old_y] = None
        self.grid[new_x][new_y] = entity
        entity.position = (new_x, new_y)
        return True

    def remove_entity(self, position: Tuple[int, int]) -> bool:
        x, y = position
        entity = self.grid[x][y]
        if entity is None:
            return False

        self.grid[x][y] = None
        if entity in self.entities:
            self.entities.remove(entity)
        return True

    def get_entity(self, position: Tuple[int, int]) -> Optional[Entity]:
        x, y = position
        return self.grid[x][y]

    def is_empty(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return self.grid[x][y] is None

    def update(self):
        # Update all entities
        for entity in self.entities[:]:  # Create a copy for iteration
            if not entity.update(self):
                # Entity should be removed
                self.remove_entity(entity.position)

    def display(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                entity = self.grid[x][y]
                row.append(str(entity) if entity else ".")
            print(" ".join(row))