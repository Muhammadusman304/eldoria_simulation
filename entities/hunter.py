from enum import Enum
from entities.entity import Entity, EntityType
from entities.treasure import Treasure
from typing import Tuple, List, Dict, Optional
import random
from math import sqrt


class HunterSkill(Enum):
    NAVIGATION = 1
    ENDURANCE = 2
    STEALTH = 3


class TreasureHunter(Entity):
    def __init__(self, position: Tuple[int, int], skill: HunterSkill):
        super().__init__(EntityType.HUNTER, position)
        self.skill = skill
        self.stamina = 100.0  # Percentage
        self.carrying = None  # Currently carried treasure
        self.memory = {
            'treasures': {},  # position: treasure
            'hideouts': {},  # position: hideout
            'knights': {}  # position: last seen
        }
        self.resting = False
        self.survival_steps = 0

        if skill == HunterSkill.NAVIGATION:
            self.symbol = "N"
        elif skill == HunterSkill.ENDURANCE:
            self.symbol = "E"
        else:
            self.symbol = "S"

    def update(self, grid):
        if self.stamina <= 0:
            self.survival_steps += 1
            return self.survival_steps <= 3

        if self.resting:
            self._rest()
            return True

        if self.stamina <= 6:
            self._seek_rest(grid)
            return True

        if self.carrying:
            self._return_to_hideout(grid)
        else:
            self._search_for_treasure(grid)

        # Update memory with current observations
        self._update_memory(grid)

        return True

    def _rest(self):
        self.stamina = min(100.0, self.stamina + 1.0)
        if self.stamina >= 80:  # Resume activity when reasonably rested
            self.resting = False

    def _seek_rest(self, grid):
        # Find nearest hideout
        nearest = self._find_nearest_hideout(grid)
        if nearest:
            if self.position == nearest.position:
                self.resting = True
            else:
                self._move_towards(nearest.position, grid)
        else:
            # No hideout found, keep searching
            self._random_move(grid)

    def _return_to_hideout(self, grid):
        nearest = self._find_nearest_hideout(grid)
        if nearest:
            if self.position == nearest.position:
                # Deposit treasure
                nearest.add_treasure(self.carrying)
                self.carrying = None
            else:
                self._move_towards(nearest.position, grid)
        else:
            # No hideout found, keep searching
            self._random_move(grid)

    def _search_for_treasure(self, grid):
        # Check memory for known treasures
        if self.memory['treasures']:
            # Go for highest value treasure
            highest_value_pos = max(
                self.memory['treasures'].items(),
                key=lambda item: item[1].value
            )[0]
            self._move_towards(highest_value_pos, grid)
        else:
            # Explore randomly
            self._random_move(grid)

    def _move_towards(self, target_pos, grid):
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

        # Check if target cell is empty
        if grid.is_empty((new_x, new_y)):
            grid.move_entity(self.position, (new_x, new_y))
            self.position = (new_x, new_y)
            self.stamina = max(0, self.stamina - 2)

    def _random_move(self, grid):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = (self.position[0] + dx) % grid.width
            new_y = (self.position[1] + dy) % grid.height

            if grid.is_empty((new_x, new_y)):
                grid.move_entity(self.position, (new_x, new_y))
                self.position = (new_x, new_y)
                self.stamina = max(0, self.stamina - 2)
                break

    def _find_nearest_hideout(self, grid):
        if not self.memory['hideouts']:
            return None

        min_dist = float('inf')
        nearest = None

        for pos, hideout in self.memory['hideouts'].items():
            dist = self._distance_to(pos)
            if dist < min_dist:
                min_dist = dist
                nearest = hideout

        return nearest

    def _distance_to(self, pos):
        dx = min(abs(pos[0] - self.position[0]),
                 abs(pos[0] - self.position[0] - self.grid.width),
                 abs(pos[0] - self.position[0] + self.grid.width))
        dy = min(abs(pos[1] - self.position[1]),
                 abs(pos[1] - self.position[1] - self.grid.height),
                 abs(pos[1] - self.position[1] + self.grid.height))
        return sqrt(dx * dx + dy * dy)

    def _update_memory(self, grid):
        self.memory = {'treasures': {}, 'hideouts': {}}
        # Scan 3-cell radius
        scan_radius = 3
        for dx in range(-scan_radius, scan_radius + 1):
            for dy in range(-scan_radius, scan_radius + 1):
                if dx == 0 and dy == 0:
                    continue

                x = (self.position[0] + dx) % grid.width
                y = (self.position[1] + dy) % grid.height
                pos = (x, y)
                entity = grid.get_entity(pos)

                if entity and entity.type == EntityType.TREASURE:
                    self.memory['treasures'][pos] = entity
                elif entity and entity.type == EntityType.HIDEOUT:
                    self.memory['hideouts'][pos] = entity
                elif entity and entity.type == EntityType.KNIGHT:
                    self.memory['knights'][pos] = entity