import random
from typing import Tuple, List, Dict, Any
from math import sqrt
from enum import Enum


def get_random_position(width: int, height: int) -> Tuple[int, int]:
    """Generate a random position within grid bounds"""
    return (random.randint(0, width - 1), random.randint(0, height - 1))


def calculate_wrapped_distance(pos1: Tuple[int, int], pos2: Tuple[int, int],
                               width: int, height: int) -> float:
    """
    Calculate the shortest distance between two positions in a wrapped grid
    """
    dx = min(abs(pos1[0] - pos2[0]), width - abs(pos1[0] - pos2[0]))
    dy = min(abs(pos1[1] - pos2[1]), height - abs(pos1[1] - pos2[1]))
    return sqrt(dx ** 2 + dy ** 2)


def get_adjacent_positions(position: Tuple[int, int],
                           width: int, height: int) -> List[Tuple[int, int]]:
    """
    Get all 8 adjacent positions (including diagonals) with grid wrapping
    """
    x, y = position
    positions = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip current position
            new_x = (x + dx) % width
            new_y = (y + dy) % height
            positions.append((new_x, new_y))
    return positions


def get_positions_in_radius(position: Tuple[int, int], radius: int,
                            width: int, height: int) -> List[Tuple[int, int]]:
    """
    Get all positions within given radius (Manhattan distance) with wrapping
    """
    x, y = position
    positions = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue  # Skip center position
            if abs(dx) + abs(dy) > radius:
                continue  # Manhattan distance check
            new_x = (x + dx) % width
            new_y = (y + dy) % height
            positions.append((new_x, new_y))
    return positions


def get_direction_towards(source: Tuple[int, int], target: Tuple[int, int],
                          width: int, height: int) -> Tuple[int, int]:
    """
    Calculate best direction to move from source to target in wrapped grid
    Returns tuple (dx, dy) where each is -1, 0, or 1
    """
    # Calculate both possible wrapped directions
    dx1 = (target[0] - source[0]) % width
    dx2 = dx1 - width
    dy1 = (target[1] - source[1]) % height
    dy2 = dy1 - height

    # Choose shortest path
    dx = dx1 if abs(dx1) <= abs(dx2) else dx2
    dy = dy1 if abs(dy1) <= abs(dy2) else dy2

    # Normalize to unit direction
    move_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    move_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    return (move_x, move_y)


def random_enum_value(enum_class: Enum) -> Enum:
    """Return a random value from an Enum class"""
    return random.choice(list(enum_class))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Restrict value to be between min and max"""
    return max(min_val, min(value, max_val))


def weighted_choice(choices: Dict[Any, float]) -> Any:
    """Make a random choice with weighted probabilities"""
    total = sum(choices.values())
    r = random.uniform(0, total)
    upto = 0
    for item, weight in choices.items():
        if upto + weight >= r:
            return item
        upto += weight
    return list(choices.keys())[0]