from abc import ABC, abstractmethod


class Renderer(ABC):
    """Abstract renderer. Plug in matplotlib, pygame, or a web backend."""

    @abstractmethod
    def animate(self, engine) -> None:
        """Drive the animation loop for the given SimulationEngine."""
