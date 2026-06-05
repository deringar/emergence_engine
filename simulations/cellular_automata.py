"""
Cellular automata rule system.

Rules are expressed as callables with signature:
    rule(grid: np.ndarray) -> np.ndarray

This module ships three built-in rules (Conway GoL, HighLife, Seeds) plus a
factory for arbitrary outer-totalistic rules via B/S notation.
"""

from typing import Callable, Optional
import numpy as np

from core.rule_system import RuleSystem
from core.world import GridWorld


def _count_neighbours(grid: np.ndarray) -> np.ndarray:
    """Toroidal 8-neighbour sum via np.roll – no scipy dependency."""
    binary = (grid > 0.5).astype(np.int8)
    n = np.zeros_like(binary)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            n += np.roll(np.roll(binary, dr, axis=0), dc, axis=1)
    return n


def make_bs_rule(born: set, survive: set) -> Callable:
    """Return an outer-totalistic rule function from B/S notation sets."""
    born_arr = np.zeros(9, dtype=bool)
    survive_arr = np.zeros(9, dtype=bool)
    for b in born:
        born_arr[b] = True
    for s in survive:
        survive_arr[s] = True

    def rule(grid: np.ndarray) -> np.ndarray:
        alive = grid > 0.5
        n = _count_neighbours(grid)
        new_alive = (alive & survive_arr[n]) | (~alive & born_arr[n])
        return new_alive.astype(np.float32)

    return rule


# --------------------------------------------------------------------------- #
# Built-in rule presets                                                        #
# --------------------------------------------------------------------------- #

#: Conway's Game of Life  B3/S23
CONWAY = make_bs_rule(born={3}, survive={2, 3})

#: HighLife  B36/S23  – produces replicators, richer variety
HIGHLIFE = make_bs_rule(born={3, 6}, survive={2, 3})

#: Seeds  B2/S  – explosive, chaotic growth
SEEDS = make_bs_rule(born={2}, survive=set())

#: Day & Night  B3678/S34678  – symmetric, stable structures
DAY_AND_NIGHT = make_bs_rule(born={3, 6, 7, 8}, survive={3, 4, 6, 7, 8})


# --------------------------------------------------------------------------- #
# RuleSystem implementation                                                    #
# --------------------------------------------------------------------------- #

class CellularAutomataRules(RuleSystem):
    """
    Applies a grid-transformation rule each timestep.

    Parameters
    ----------
    rule_fn:
        Callable (grid) -> grid.  Defaults to Conway's Game of Life.
    steps_per_tick:
        How many CA generations to advance per engine tick.
    """

    def __init__(
        self,
        rule_fn: Optional[Callable] = None,
        steps_per_tick: int = 1,
    ):
        self.rule_fn = rule_fn or CONWAY
        self.steps_per_tick = steps_per_tick

    def apply(self, world: GridWorld, dt: float = 1.0) -> None:
        for _ in range(self.steps_per_tick):
            world.grid = self.rule_fn(world.grid)

    def swap_rule(self, rule_fn: Callable) -> None:
        """Hot-swap the rule without restarting the simulation."""
        self.rule_fn = rule_fn


# --------------------------------------------------------------------------- #
# Initial-state factories                                                      #
# --------------------------------------------------------------------------- #

def random_grid(width: int, height: int, density: float = 0.35) -> np.ndarray:
    """Uniform random live cells at given density."""
    return (np.random.rand(height, width) < density).astype(np.float32)


def glider(width: int, height: int) -> np.ndarray:
    """Single glider near top-left."""
    g = np.zeros((height, width), dtype=np.float32)
    pattern = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    for r, c in pattern:
        g[r + 2, c + 2] = 1.0
    return g


def glider_gun(width: int, height: int) -> np.ndarray:
    """Gosper glider gun – produces a continuous stream of gliders."""
    g = np.zeros((height, width), dtype=np.float32)
    # Gosper gun cell offsets (row, col)
    cells = [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11),
        (4, 12), (8, 12),
        (3, 13), (9, 13),
        (3, 14), (9, 14),
        (6, 15),
        (4, 16), (8, 16),
        (5, 17), (6, 17), (7, 17),
        (6, 18),
        (3, 21), (4, 21), (5, 21),
        (3, 22), (4, 22), (5, 22),
        (2, 23), (6, 23),
        (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35),
        (3, 36), (4, 36),
    ]
    for r, c in cells:
        if r < height and c < width:
            g[r, c] = 1.0
    return g
