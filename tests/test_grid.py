import unittest
from world.grid import EldoriaGrid
from entities.entity import Entity, EntityType


class TestEldoriaGrid(unittest.TestCase):
    def setUp(self):
        self.grid = EldoriaGrid(10, 10)
        self.entity = Entity(EntityType.TREASURE, (0, 0))

    def test_add_entity(self):
        self.assertTrue(self.grid.add_entity(self.entity, (0, 0)))
        self.assertEqual(self.grid.get_entity((0, 0)), self.entity)

    def test_move_entity(self):
        self.grid.add_entity(self.entity, (0, 0))
        self.assertTrue(self.grid.move_entity((0, 0), (1, 1)))
        self.assertIsNone(self.grid.get_entity((0, 0)))
        self.assertEqual(self.grid.get_entity((1, 1)), self.entity)

    def test_remove_entity(self):
        self.grid.add_entity(self.entity, (0, 0))
        self.assertTrue(self.grid.remove_entity((0, 0)))
        self.assertIsNone(self.grid.get_entity((0, 0)))

    def test_wrap_around(self):
        self.grid.add_entity(self.entity, (0, 0))
        self.assertTrue(self.grid.move_entity((0, 0), (9, 9)))
        self.assertEqual(self.grid.get_entity((9, 9)), self.entity)


if __name__ == "__main__":
    unittest.main()