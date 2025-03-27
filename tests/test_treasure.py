import unittest
from entities.treasure import Treasure, TreasureType
from world.grid import EldoriaGrid


class TestTreasure(unittest.TestCase):
    def setUp(self):
        self.grid = EldoriaGrid(20, 20)
        self.treasures = {
            TreasureType.BRONZE: Treasure((5, 5), TreasureType.BRONZE),
            TreasureType.SILVER: Treasure((10, 10), TreasureType.SILVER),
            TreasureType.GOLD: Treasure((15, 15), TreasureType.GOLD)
        }

        for treasure in self.treasures.values():
            self.grid.add_entity(treasure, treasure.position)

    def test_initialization(self):
        self.assertEqual(self.treasures[TreasureType.BRONZE].symbol, "B")
        self.assertEqual(self.treasures[TreasureType.SILVER].symbol, "S")
        self.assertEqual(self.treasures[TreasureType.GOLD].symbol, "G")

        self.assertEqual(self.treasures[TreasureType.BRONZE].value, 100.0)
        self.assertEqual(self.treasures[TreasureType.SILVER].value, 100.0)
        self.assertEqual(self.treasures[TreasureType.GOLD].value, 100.0)

    def test_value_decay(self):
        bronze = self.treasures[TreasureType.BRONZE]
        initial_value = bronze.value

        # Test single step decay
        bronze.update(self.grid)
        self.assertAlmostEqual(bronze.value, initial_value * 0.999, places=5)

        # Test multiple steps until removal
        steps = 0
        while bronze.update(self.grid):
            steps += 1
            self.assertGreater(bronze.value, 0.0)

        self.assertLess(bronze.value, 0.1)
        self.assertGreater(steps, 500)  # Should take many steps to fully decay

    def test_value_increase(self):
        self.assertEqual(
            self.treasures[TreasureType.BRONZE].get_value_increase(),
            0.03
        )
        self.assertEqual(
            self.treasures[TreasureType.SILVER].get_value_increase(),
            0.07
        )
        self.assertEqual(
            self.treasures[TreasureType.GOLD].get_value_increase(),
            0.13
        )

    def test_position_handling(self):
        self.assertEqual(self.treasures[TreasureType.BRONZE].position, (5, 5))
        self.assertEqual(self.treasures[TreasureType.SILVER].position, (10, 10))
        self.assertEqual(self.treasures[TreasureType.GOLD].position, (15, 15))

    def test_string_representation(self):
        self.assertEqual(str(self.treasures[TreasureType.BRONZE]), "B")
        self.assertEqual(str(self.treasures[TreasureType.SILVER]), "S")
        self.assertEqual(str(self.treasures[TreasureType.GOLD]), "G")

    def test_treasure_types(self):
        self.assertEqual(TreasureType.BRONZE.value, 1)
        self.assertEqual(TreasureType.SILVER.value, 2)
        self.assertEqual(TreasureType.GOLD.value, 3)


if __name__ == "__main__":
    unittest.main()