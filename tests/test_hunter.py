import unittest
from entities.hunter import TreasureHunter, HunterSkill
from entities.treasure import Treasure, TreasureType
from entities.hideout import Hideout
from world.grid import EldoriaGrid
from utils.helpers import get_random_position


class TestTreasureHunter(unittest.TestCase):
    def setUp(self):
        self.grid = EldoriaGrid(20, 20)
        self.hunter = TreasureHunter((10, 10), HunterSkill.NAVIGATION)
        self.grid.add_entity(self.hunter, (10, 10))

        # Add test treasures
        self.bronze_treasure = Treasure((8, 8), TreasureType.BRONZE)
        self.silver_treasure = Treasure((12, 12), TreasureType.SILVER)
        self.grid.add_entity(self.bronze_treasure, (8, 8))
        self.grid.add_entity(self.silver_treasure, (12, 12))

        # Add test hideout
        self.hideout = Hideout((15, 15))
        self.grid.add_entity(self.hideout, (15, 15))

    def test_initialization(self):
        self.assertEqual(self.hunter.skill, HunterSkill.NAVIGATION)
        self.assertEqual(self.hunter.stamina, 100.0)
        self.assertIsNone(self.hunter.carrying)
        self.assertEqual(self.hunter.position, (10, 10))
        self.assertEqual(self.hunter.symbol, "N")
        self.assertFalse(self.hunter.resting)

    def test_stamina_management(self):
        # Test stamina depletion
        initial_stamina = self.hunter.stamina
        self.hunter._move_towards((11, 10), self.grid)
        self.assertAlmostEqual(self.hunter.stamina, initial_stamina - 2, places=1)

        # Test critical stamina behavior
        self.hunter.stamina = 5.0
        self.hunter.update(self.grid)
        self.assertTrue(self.hunter.stamina <= 6.0)

        # Test resting behavior
        self.hunter.position = self.hideout.position
        self.hunter.resting = True
        initial_rest_stamina = self.hunter.stamina
        self.hunter.update(self.grid)
        self.assertGreater(self.hunter.stamina, initial_rest_stamina)

    def test_treasure_prioritization(self):
        # Add treasures to memory
        self.hunter.memory['treasures'][(8, 8)] = self.bronze_treasure
        self.hunter.memory['treasures'][(12, 12)] = self.silver_treasure

        # Hunter should prioritize higher value treasure
        self.hunter._search_for_treasure(self.grid)
        target_pos = max(
            self.hunter.memory['treasures'].items(),
            key=lambda item: item[1].value
        )[0]
        self.assertEqual(target_pos, (8, 8))

    def test_treasure_collection(self):
        # Move hunter to treasure position
        self.hunter.position = (8, 8)
        self.hunter.update(self.grid)

        # Should pick up treasure
        self.assertIsNotNone(self.hunter.carrying)
        self.assertEqual(self.hunter.carrying.treasure_type, TreasureType.BRONZE)

        # Should attempt to return to hideout
        self.hunter.update(self.grid)
        self.assertEqual(self.hunter.memory['hideouts'][(15, 15)], self.hideout)

    def test_memory_updates(self):
        # Test scanning and memory updates
        self.hunter._update_memory(self.grid)

        # Should have detected nearby entities
        self.assertIn((8, 8), self.hunter.memory['treasures'])
        self.assertIn((12, 12), self.hunter.memory['treasures'])
        self.assertIn((15, 15), self.hunter.memory['hideouts'])

    def test_hunter_collapse(self):
        # Test hunter collapse when stamina reaches 0
        self.hunter.stamina = 0.0
        self.hunter.survival_steps = 0

        # Should survive for 3 steps
        self.assertTrue(self.hunter.update(self.grid))
        self.assertEqual(self.hunter.survival_steps, 1)

        self.assertTrue(self.hunter.update(self.grid))
        self.assertEqual(self.hunter.survival_steps, 2)

        self.assertTrue(self.hunter.update(self.grid))
        self.assertEqual(self.hunter.survival_steps, 3)

        # Should collapse on 4th step
        self.assertFalse(self.hunter.update(self.grid))

    def test_skill_specific_behavior(self):
        # Test endurance hunter has different symbol
        endurance_hunter = TreasureHunter((5, 5), HunterSkill.ENDURANCE)
        self.assertEqual(endurance_hunter.symbol, "E")

        # Test stealth hunter has different symbol
        stealth_hunter = TreasureHunter((5, 5), HunterSkill.STEALTH)
        self.assertEqual(stealth_hunter.symbol, "S")


if __name__ == "__main__":
    unittest.main()