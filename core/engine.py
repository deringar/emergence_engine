from core.world import World
from core.rule_system import RuleSystem
from core.renderer import Renderer


class SimulationEngine:
    """
    Orchestrates the timestep loop.  Owns World + RuleSystem + Renderer;
    none of those know about each other directly.
    """

    def __init__(self, world: World, rule_system: RuleSystem, renderer: Renderer, config: dict = None):
        cfg = config or {}
        self.world = world
        self.rule_system = rule_system
        self.renderer = renderer

        self.dt: float = float(cfg.get("dt", 1.0))
        self.steps_per_frame: int = int(cfg.get("steps_per_frame", 1))
        self.step_count: int = 0
        self.paused: bool = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def step(self) -> None:
        if self.paused:
            return
        for _ in range(self.steps_per_frame):
            self.rule_system.apply(self.world, self.dt)
            self.step_count += 1

    def reset(self) -> None:
        self.world.reset()
        self.rule_system.reset()
        self.step_count = 0

    def run(self) -> None:
        self.renderer.animate(self)

    # ------------------------------------------------------------------
    # Interactive controls (called by renderer key handlers)
    # ------------------------------------------------------------------

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def increase_speed(self) -> None:
        self.steps_per_frame = min(self.steps_per_frame + 1, 30)

    def decrease_speed(self) -> None:
        self.steps_per_frame = max(self.steps_per_frame - 1, 1)
