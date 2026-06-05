from abc import ABC, abstractmethod
from typing import Callable, List, Optional

import numpy as np


class World(ABC):
    """Holds global simulation state and exposes a normalised render-data contract."""

    @abstractmethod
    def reset(self) -> None: ...

    @abstractmethod
    def get_render_data(self) -> dict: ...

    @property
    @abstractmethod
    def state(self): ...


# ---------------------------------------------------------------------------
# Grid world  (cellular automata, reaction-diffusion)
# ---------------------------------------------------------------------------

class GridWorld(World):
    """
    2-D grid of float32 values in [0, 1].
    initial_state is captured at construction and replayed on reset().
    """

    def __init__(self, width: int, height: int, initial_state=None):
        self.width = width
        self.height = height
        self._initial_state: Optional[np.ndarray] = (
            np.array(initial_state, dtype=np.float32) if initial_state is not None else None
        )
        self.grid: np.ndarray = np.empty(0)
        self.reset()

    def reset(self) -> None:
        if self._initial_state is not None:
            self.grid = self._initial_state.copy()
        else:
            self.grid = np.zeros((self.height, self.width), dtype=np.float32)

    @property
    def state(self) -> np.ndarray:
        return self.grid

    def get_render_data(self) -> dict:
        return {
            "type": "grid",
            "data": self.grid,
            "colormap": "binary_r",
            "vmin": 0.0,
            "vmax": 1.0,
        }


# ---------------------------------------------------------------------------
# Agent world  (boids, predator-prey)
# ---------------------------------------------------------------------------

class AgentWorld(World):
    """
    Continuous 2-D space populated by Entity objects.
    agent_factory() is called on each reset() so simulations start fresh.
    """

    def __init__(self, width: float, height: float, agent_factory: Callable[[], List] = None):
        self.width = width
        self.height = height
        self._agent_factory = agent_factory or (lambda: [])
        self.agents: List = []
        self.reset()

    def reset(self) -> None:
        self.agents = self._agent_factory()

    def add_agent(self, agent) -> None:
        self.agents.append(agent)

    @property
    def state(self) -> List:
        return self.agents

    def get_render_data(self) -> dict:
        if not self.agents:
            return {
                "type": "agents",
                "positions": np.zeros((0, 2)),
                "velocities": np.zeros((0, 2)),
                "types": [],
                "bounds": (self.width, self.height),
            }
        positions = np.array([a.position for a in self.agents])
        velocities = np.array([a.velocity for a in self.agents])
        types = [a.agent_type for a in self.agents]
        return {
            "type": "agents",
            "positions": positions,
            "velocities": velocities,
            "types": types,
            "bounds": (self.width, self.height),
        }
