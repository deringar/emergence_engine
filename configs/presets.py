"""
Named simulation presets.  Each preset is a dict consumed by build_simulation().

Keys:
    name        : human-readable label
    sim_type    : "ca" | "boids"
    world       : kwargs forwarded to GridWorld or AgentWorld
    rules       : kwargs forwarded to the rule system
    engine      : kwargs forwarded to SimulationEngine
    renderer    : kwargs forwarded to MatplotlibRenderer
    init        : "random" | "glider" | "glider_gun"  (CA only)
    init_kwargs : extra kwargs for the init factory  (e.g. density)
"""

PRESETS: dict = {

    # ------------------------------------------------------------------
    # Conway's Game of Life – random soup stabilising into still-lifes,
    # oscillators, and gliders.
    # ------------------------------------------------------------------
    "conway": {
        "name": "Conway's Game of Life",
        "sim_type": "ca",
        "world": {"width": 120, "height": 120},
        "rules": {},                         # defaults to CONWAY rule
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {"interval_ms": 80, "figsize": (7, 7), "title": "Game of Life"},
        "init": "random",
        "init_kwargs": {"density": 0.35},
    },

    # ------------------------------------------------------------------
    # Gosper glider gun – clean demonstration of persistent structures
    # spawning indefinitely.
    # ------------------------------------------------------------------
    "glider_gun": {
        "name": "Gosper Glider Gun",
        "sim_type": "ca",
        "world": {"width": 100, "height": 60},
        "rules": {},
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {"interval_ms": 100, "figsize": (10, 6), "title": "Glider Gun"},
        "init": "glider_gun",
        "init_kwargs": {},
    },

    # ------------------------------------------------------------------
    # HighLife – same rules as GoL but B6 lets replicators appear.
    # ------------------------------------------------------------------
    "highlife": {
        "name": "HighLife",
        "sim_type": "ca",
        "world": {"width": 120, "height": 120},
        "rules": {"rule_name": "highlife"},
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {"interval_ms": 60, "figsize": (7, 7), "title": "HighLife"},
        "init": "random",
        "init_kwargs": {"density": 0.35},
    },

    # ------------------------------------------------------------------
    # Day & Night – symmetric rule producing dense, crystalline patterns.
    # ------------------------------------------------------------------
    "day_and_night": {
        "name": "Day & Night",
        "sim_type": "ca",
        "world": {"width": 120, "height": 120},
        "rules": {"rule_name": "day_and_night"},
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {"interval_ms": 60, "figsize": (7, 7), "title": "Day & Night"},
        "init": "random",
        "init_kwargs": {"density": 0.5},
    },

    # ------------------------------------------------------------------
    # Boids flocking – emergent collective motion from three local rules.
    # ------------------------------------------------------------------
    "boids": {
        "name": "Boids Flocking",
        "sim_type": "boids",
        "world": {"width": 600.0, "height": 600.0},
        "rules": {
            "separation_radius": 25.0,
            "neighbour_radius": 60.0,
            "separation_weight": 1.8,
            "alignment_weight": 1.0,
            "cohesion_weight": 1.0,
            "max_speed": 3.5,
            "max_force": 0.15,
        },
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {
            "interval_ms": 30,
            "figsize": (7, 7),
            "title": "Boids Flocking",
            "agent_colors": {"boid": "steelblue"},
        },
        "n_agents": 180,
    },

    # ------------------------------------------------------------------
    # Dense boids – tighter parameters, stronger cohesion, big murmuration
    # ------------------------------------------------------------------
    "murmuration": {
        "name": "Murmuration (dense boids)",
        "sim_type": "boids",
        "world": {"width": 600.0, "height": 600.0},
        "rules": {
            "separation_radius": 18.0,
            "neighbour_radius": 80.0,
            "separation_weight": 2.2,
            "alignment_weight": 1.4,
            "cohesion_weight": 0.7,
            "max_speed": 4.0,
            "max_force": 0.18,
        },
        "engine": {"dt": 1.0, "steps_per_frame": 1},
        "renderer": {
            "interval_ms": 30,
            "figsize": (7, 7),
            "title": "Murmuration",
            "agent_colors": {"boid": "#e8c14e"},
        },
        "n_agents": 350,
    },
}
