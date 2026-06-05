import numpy as np


class Entity:
    """
    Base unit for agent-based simulations.
    Subclass to add domain-specific state (energy, species, etc.).
    """

    def __init__(self, position, velocity=None, state=None, agent_type: str = "default"):
        self.position = np.asarray(position, dtype=np.float64)
        self.velocity = np.asarray(
            velocity if velocity is not None else [0.0, 0.0], dtype=np.float64
        )
        self.state = state or {}
        self.agent_type = agent_type

    def clone(self) -> "Entity":
        return Entity(
            self.position.copy(),
            self.velocity.copy(),
            dict(self.state),
            self.agent_type,
        )
