from abc import ABC, abstractmethod


class RuleSystem(ABC):
    """Encapsulates behavior logic for one timestep. Interchangeable per simulation type."""

    @abstractmethod
    def apply(self, world, dt: float = 1.0) -> None:
        """Mutate world state in-place for one timestep."""

    def reset(self) -> None:
        """Reset any internal rule state (e.g. accumulators). Override if needed."""
