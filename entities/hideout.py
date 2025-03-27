from entities.entity import Entity, EntityType
from entities.treasure import Treasure
from entities.hunter import TreasureHunter, HunterSkill
from typing import List, Tuple, Dict
import random


class Hideout(Entity):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(EntityType.HIDEOUT, position)
        self.symbol = "H"
        self.hunters: List[TreasureHunter] = []
        self.treasures: List[Treasure] = []
        self.capacity = 5

    def add_hunter(self, hunter: TreasureHunter):
        if len(self.hunters) < self.capacity:
            self.hunters.append(hunter)
            return True
        return False

    def remove_hunter(self, hunter: TreasureHunter):
        if hunter in self.hunters:
            self.hunters.remove(hunter)
            return True
        return False

    def add_treasure(self, treasure: Treasure):
        self.treasures.append(treasure)

    def update(self, grid):
        # Try to recruit new hunter if there's space and diverse skills
        if self.capacity > len(self.hunters) >= 2:
            skills = {hunter.skill for hunter in self.hunters}
            if len(skills) >= 2 and random.random() < 0.2:
                # Recruit new hunter
                new_skill = random.choice(list(skills))
                new_hunter = TreasureHunter(self.position, new_skill)
                if grid.add_entity(new_hunter, self.position):
                    self.hunters.append(new_hunter)

        # Share information among hunters
        self._share_information()

    def _share_information(self):
        if len(self.hunters) < 2:
            return

        # Combine all memories
        combined_treasures = {}
        combined_hideouts = {}
        combined_knights = {}

        for hunter in self.hunters:
            combined_treasures.update(hunter.memory['treasures'])
            combined_hideouts.update(hunter.memory['hideouts'])
            combined_knights.update(hunter.memory['knights'])

        # Share with all hunters
        for hunter in self.hunters:
            hunter.memory['treasures'].update(combined_treasures)
            hunter.memory['hideouts'].update(combined_hideouts)
            hunter.memory['knights'].update(combined_knights)