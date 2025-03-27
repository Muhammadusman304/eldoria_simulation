from entities.entity import EntityType
from world.grid import EldoriaGrid
from entities.treasure import Treasure, TreasureType
from entities.hunter import TreasureHunter, HunterSkill
from entities.knight import Knight
from entities.hideout import Hideout
import random
from typing import Tuple


class EldoriaSimulation:
    def __init__(self, width: int = 20, height: int = 20):
        self.grid = EldoriaGrid(width, height)
        self.steps = 0
        self.initialize_world()

    def initialize_world(self):
        # Place hideouts (3-5)
        num_hideouts = random.randint(3, 5)
        for _ in range(num_hideouts):
            pos = self._get_random_empty_position()
            hideout = Hideout(pos)
            self.grid.add_entity(hideout, pos)

            # Add 1-3 hunters to each hideout
            num_hunters = random.randint(1, 3)
            for _ in range(num_hunters):
                skill = random.choice(list(HunterSkill))
                hunter = TreasureHunter(pos, skill)
                self.grid.add_entity(hunter, pos)
                hideout.add_hunter(hunter)

        # Place treasures (15-25% of grid)
        num_treasures = random.randint(
            int(self.grid.width * self.grid.height * 0.15),
            int(self.grid.width * self.grid.height * 0.25)
        )
        for _ in range(num_treasures):
            pos = self._get_random_empty_position()
            treasure_type = random.choice(list(TreasureType))
            treasure = Treasure(pos, treasure_type)
            self.grid.add_entity(treasure, pos)

        # Place knights (5-10% of hunters)
        num_hunters = sum(1 for e in self.grid.entities if e.type == EntityType.HUNTER)
        num_knights = random.randint(
            max(1, int(num_hunters * 0.05)),
            max(1, int(num_hunters * 0.10))
        )
        for _ in range(num_knights):
            pos = self._get_random_empty_position()
            knight = Knight(pos)
            self.grid.add_entity(knight, pos)

    def _get_random_empty_position(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            if self.grid.is_empty((x, y)):
                return (x, y)

    def step(self):
        self.grid.update()
        self.steps += 1

    def is_running(self) -> bool:
        # Check if there are still treasures or active hunters
        has_treasures = any(
            e.type == EntityType.TREASURE for e in self.grid.entities
        )
        has_active_hunters = any(
            e.type == EntityType.HUNTER and e.stamina > 0 for e in self.grid.entities
        )
        return has_treasures and has_active_hunters

    def get_stats(self) -> dict:
        stats = {
            'steps': self.steps,
            'hunters': 0,
            'active_hunters': 0,
            'knights': 0,
            'treasures': 0,
            'collected_treasures': 0,
            'hideouts': 0
        }

        for entity in self.grid.entities:
            if entity.type == EntityType.HUNTER:
                stats['hunters'] += 1
                if entity.stamina > 0:
                    stats['active_hunters'] += 1
            elif entity.type == EntityType.KNIGHT:
                stats['knights'] += 1
            elif entity.type == EntityType.TREASURE:
                stats['treasures'] += 1
            elif entity.type == EntityType.HIDEOUT:
                stats['hideouts'] += 1
                stats['collected_treasures'] += len(entity.treasures)

        return stats