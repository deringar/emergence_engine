"""
Emergence Engine – entry point.

Usage:
    python main.py                    # interactive preset menu
    python main.py <preset_name>      # run a specific preset directly

Available presets:
    conway, glider_gun, highlife, day_and_night, boids, murmuration
"""

import sys
import numpy as np

from core.engine import SimulationEngine
from core.world import GridWorld, AgentWorld
from rendering.matplotlib_renderer import MatplotlibRenderer
from simulations.cellular_automata import (
    CellularAutomataRules,
    CONWAY, HIGHLIFE, SEEDS, DAY_AND_NIGHT,
    random_grid, glider, glider_gun,
)
from simulations.boids import BoidsRules, make_boids
from configs.presets import PRESETS


# --------------------------------------------------------------------------- #
# Preset builder                                                               #
# --------------------------------------------------------------------------- #

_CA_RULES = {
    "conway":       CONWAY,
    "highlife":     HIGHLIFE,
    "seeds":        SEEDS,
    "day_and_night": DAY_AND_NIGHT,
}

_CA_INITS = {
    "random":     random_grid,
    "glider":     glider,
    "glider_gun": glider_gun,
}


def build_simulation(preset: dict) -> SimulationEngine:
    sim_type = preset["sim_type"]
    world_cfg = preset.get("world", {})
    rule_cfg  = preset.get("rules", {})
    engine_cfg = preset.get("engine", {})
    renderer_cfg = preset.get("renderer", {})

    if sim_type == "ca":
        W = world_cfg["width"]
        H = world_cfg["height"]

        rule_name = rule_cfg.pop("rule_name", "conway")
        rule_fn = _CA_RULES.get(rule_name, CONWAY)
        rules = CellularAutomataRules(rule_fn=rule_fn, **rule_cfg)

        init_name = preset.get("init", "random")
        init_fn = _CA_INITS.get(init_name, random_grid)
        init_kwargs = preset.get("init_kwargs", {})
        initial_state = init_fn(W, H, **init_kwargs)

        world = GridWorld(W, H, initial_state=initial_state)

    elif sim_type == "boids":
        W = world_cfg["width"]
        H = world_cfg["height"]
        n = preset.get("n_agents", 150)
        rules = BoidsRules(**rule_cfg)
        factory = lambda: make_boids(n, W, H, max_speed=rule_cfg.get("max_speed", 3.5))
        world = AgentWorld(W, H, agent_factory=factory)

    else:
        raise ValueError(f"Unknown sim_type: {sim_type!r}")

    renderer = MatplotlibRenderer(**renderer_cfg)
    engine = SimulationEngine(world, rules, renderer, config=engine_cfg)
    return engine


# --------------------------------------------------------------------------- #
# Menu                                                                         #
# --------------------------------------------------------------------------- #

def print_menu():
    print("\n┌─────────────────────────────────────────────┐")
    print("│         EMERGENCE ENGINE  v1.0              │")
    print("├─────────────────────────────────────────────┤")
    for i, (key, preset) in enumerate(PRESETS.items(), 1):
        print(f"│  {i}.  {preset['name']:<38} │   ({key})")
    print("├─────────────────────────────────────────────┤")
    print("│  Keyboard controls (in the figure window):  │")
    print("│    Space  pause/resume   r   reset           │")
    print("│    + / -  speed up/down  q   quit            │")
    print("└─────────────────────────────────────────────┘")


def choose_preset() -> dict:
    keys = list(PRESETS.keys())
    print_menu()
    while True:
        choice = input("\nEnter preset name or number [default: conway]: ").strip()
        if not choice:
            return PRESETS["conway"]
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                return PRESETS[keys[idx]]
        if choice in PRESETS:
            return PRESETS[choice]
        print(f"  Unknown preset '{choice}'. Try again.")


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name not in PRESETS:
            print(f"Unknown preset '{name}'. Available: {', '.join(PRESETS)}")
            sys.exit(1)
        preset = PRESETS[name]
    else:
        preset = choose_preset()

    print(f"\nStarting: {preset['name']}  …  close the window or press q to exit.\n")
    engine = build_simulation(preset)
    engine.run()


if __name__ == "__main__":
    np.random.seed(42)
    main()
