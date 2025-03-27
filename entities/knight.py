from entities.entity import Entity, EntityType
from typing import Tuple, Optional
import random


class Knight(Entity):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(EntityType.KNIGHT, position)
        self.energy = 100.0  # Percentage
        self.symbol = "K"
        self.resting = False

    def update(self, grid):
        if self.energy <= 20:
            self._retreat_to_garrison(grid)
            return True

        if self.resting:
            self.energy = min(100.0, self.energy + 10.0)
            if self.energy >= 100:
                self.resting = False
            return True

        # Look for hunters in 3-cell radius
        hunter = self._find_hunter_in_range(grid, 3)
        if hunter:
            self._chase_hunter(hunter, grid)
        else:
            self._patrol(grid)

        return True

    def _retreat_to_garrison(self, grid):
        # For simplicity, we'll treat hideouts as garrisons
        garrison = self._find_nearest_hideout(grid)
        if garrison:
            if self.position == garrison.position:
                self.resting = True
            else:
                self._move_towards(garrison.position, grid)
        else:
            # No garrison found, just rest in place
            self.resting = True

    def _find_hunter_in_range(self, grid, radius):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue

                x = (self.position[0] + dx) % grid.width
                y = (self.position[1] + dy) % grid.height
                entity = grid.get_entity((x, y))

                if entity and entity.type == EntityType.HUNTER:
                    return entity
        return None

    def _chase_hunter(self, hunter, grid):
        # Move towards hunter
        self._move_towards(hunter.position, grid)
        self.energy = max(0, self.energy - 20)

        # If caught the hunter
        if self.position == hunter.position:
            self._interact_with_hunter(hunter)

    def _interact_with_hunter(self, hunter):
        # Randomly choose to detain or challenge
        if random.random() < 0.5:
            # Detain
            hunter.stamina = max(0, hunter.stamina - 5)
            if hunter.carrying:
                hunter.carrying = None
        else:
            # Challenge
            hunter.stamina = max(0, hunter.stamina - 20)
            if hunter.carrying:
                hunter.carrying = None

    def _patrol(self, grid):
        # Random patrol movement
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = (self.position[0] + dx) % grid.width
            new_y = (self.position[1] + dy) % grid.height

            if grid.is_empty((new_x, new_y)):
                grid.move_entity(self.position, (new_x, new_y))
                self.position = (new_x, new_y)
                break

    def _move_towards(self, target_pos, grid):
        # Similar to hunter's movement but simpler
        dx = (target_pos[0] - self.position[0]) % grid.width
        dy = (target_pos[1] - self.position[1]) % grid.height

        if dx > grid.width // 2:
            dx -= grid.width
        if dy > grid.height // 2:
            dy -= grid.height

        move_x = 0
        move_y = 0

        if abs(dx) > abs(dy):
            move_x = 1 if dx > 0 else -1
        else:
            move_y = 1 if dy > 0 else -1

        new_x = (self.position[0] + move_x) % grid.width
        new_y = (self.position[1] + move_y) % grid.height

        if grid.is_empty((new_x, new_y)):
            grid.move_entity(self.position, (new_x, new_y))
            self.position = (new_x, new_y)

    def _find_nearest_hideout(self, grid):
        # Simplified version - in a real implementation would scan the grid
        return None