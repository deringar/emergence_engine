# Emergence Engine

A modular Python simulation framework for emergent behavior — complex global patterns arising from simple local rules. The engine supports multiple simulation paradigms, each demonstrating a different face of emergence, with real-time visualization and keyboard controls.

---

## What is Emergence?

Emergence is the phenomenon where a system exhibits properties or behaviors that none of its individual components possess on their own. A single ant has no blueprint for a colony. A single neuron has no thought. A single boid has no idea what a flock looks like. Yet from the repeated application of simple, local rules across many interacting agents, coherent global structure appears — unprogrammed, unplanned, and often surprising.

The simulations in this engine are not demonstrations of complex code. They are demonstrations of complex *behavior* produced by remarkably simple rules. That distinction is the point.

---

## Running the Engine

```bash
python main.py               # interactive preset menu
python main.py conway        # run a specific preset directly
```

**Keyboard controls** (inside the figure window):

| Key | Action |
|-----|--------|
| `Space` | Pause / resume |
| `r` | Reset to initial state |
| `+` / `=` | Speed up (more steps per frame) |
| `-` | Slow down |
| `q` | Quit |

---

## Simulation Types

### 1. Cellular Automata

**Background**

Cellular automata (CA) were formalized by John von Neumann in the 1940s and popularized by John Conway's Game of Life in 1970. A CA is a grid of cells, each in one of a finite number of states, updated simultaneously at each timestep according to a fixed rule that depends only on the cell's own state and the states of its immediate neighbors. There is no central controller — each cell computes its next state independently from purely local information.

Stephen Wolfram's landmark work in the 1980s and his 2002 book *A New Kind of Science* demonstrated that even one-dimensional CA with just two states and three-cell neighborhoods can produce behavior equivalent to universal computation. Two-dimensional CA vastly expand this space.

**Significance**

CA are among the cleanest possible models for studying emergence because the local-to-global causal chain is completely transparent: you can read the rule in ten seconds and still be surprised by what it produces after a thousand generations. They have been applied to model biological morphogenesis, crystal growth, fluid dynamics, traffic flow, and the spread of disease. Conway's Game of Life is Turing complete — meaning it can, in principle, simulate any computation — despite having only four rules.

**How emergence works here**

The grid begins in a disordered state (random live/dead cells). Over successive generations, cells with unfavorable neighbor counts die while others are born. Local order propagates outward. Globally, the system self-organizes: chaotic regions collapse into stable structures, oscillating patterns lock into fixed periods, and moving configurations (gliders) emerge that carry information across the grid. None of these structures were specified. They are attractors of the rule system — states the dynamics inevitably find.

---

#### Preset: Conway's Game of Life (`conway`)

**Rules (B3/S23):** A dead cell with exactly 3 live neighbors is born. A live cell with 2 or 3 live neighbors survives. All others die.

From a random 35% density starting grid, the system rapidly self-organizes. Within ~50 generations, the initial noise has resolved into a stable ecology of recognizable structures:

- **Still lifes** — configurations that do not change (blocks, beehives, loaves)
- **Oscillators** — patterns that repeat on a fixed period (blinkers, toads, pulsars)
- **Gliders** — five-cell patterns that translate diagonally across the grid at c/4

The remarkable fact is that these classes of structures were not designed. They are emergent consequences of four simple rules applied to a binary grid.

---

#### Preset: Gosper Glider Gun (`glider_gun`)

A hand-crafted 36-cell initial configuration discovered by Bill Gosper in 1970, the Glider Gun was the first known finite pattern with unbounded population growth. It produces a new glider every 30 generations indefinitely.

This preset highlights a different face of emergence: **constructive structure**. Rather than order appearing from disorder, a stable "machine" embedded in the grid manufactures output continuously. The gun itself is an oscillator (period 30); each cycle it ejects a glider that travels away across the grid. It demonstrated for the first time that GoL could sustain infinite growth, resolving an open conjecture by Conway.

---

#### Preset: HighLife (`highlife`)

**Rules (B36/S23):** Same as Conway's GoL, but cells are also born with 6 live neighbors.

The single additional birth condition (B6) dramatically changes the emergent behavior class. HighLife supports **replicators** — patterns that produce copies of themselves — which do not exist in standard GoL. The grid evolves more explosively and sustains higher long-term density. Structures that would stabilize in GoL continue to propagate and replicate in HighLife.

This preset illustrates how sensitive emergent behavior is to rule structure. One extra condition shifts the system from one that finds equilibrium to one capable of self-reproduction — a property with deep implications for models of biological life.

---

#### Preset: Day & Night (`day_and_night`)

**Rules (B3678/S34678):** A cell is born with 3, 6, 7, or 8 live neighbors; it survives with 3, 4, 6, 7, or 8.

Day & Night is a *symmetric* rule: if you invert the entire grid (swap live and dead), the rule produces the same evolution. This means live cells and dead cells are governed by equivalent logic — dead space is just as structured as live space.

The emergent patterns reflect this symmetry: the grid produces dense, crystalline structures with clear geometric organization. Regions of live and dead cells are mirror images of each other. The global visual symmetry is a direct consequence of the rule's mathematical symmetry — an example of how algebraic properties of rules propagate into macroscopic pattern properties.

---

### 2. Agent-Based Swarm (Boids)

**Background**

Craig Reynolds introduced the Boids model in 1987 to simulate the coordinated group motion of birds and fish. Unlike CA, which operate on a fixed grid, Boids is an agent-based model: each agent (boid) is an autonomous entity with continuous position and velocity, moving through open space and perceiving only a local neighborhood around itself.

The model applies three steering forces to each agent at each timestep:

1. **Separation** — steer away from agents that are too close (avoid crowding)
2. **Alignment** — steer toward the average heading of nearby agents (match direction)
3. **Cohesion** — steer toward the average position of nearby agents (stay together)

No agent knows the shape of the flock. No agent is designated the leader. The flock is entirely a product of local interactions.

**Significance**

Reynolds' Boids was a landmark in computer graphics and in the science of collective behavior. It was among the first computational demonstrations that realistic flocking could be reproduced without any centralized control or global state. The model has since been validated against biological data for fish schools and starling murmurations, and has been applied in robotics (swarm robotics), crowd simulation for film and games, and the study of collective intelligence.

The deeper significance is philosophical: Boids showed that the apparent purposefulness of a flock — its ability to maintain cohesion, avoid obstacles, and respond as a unit — requires no planner. Purposeful-looking global behavior can be entirely epiphenomenal, an artifact of local rules with no awareness of the whole.

**How emergence works here**

Each boid sees only the agents within a fixed radius. It computes three small corrections to its velocity and moves. That's all. From this, across 180+ agents, sustained coordinated motion emerges: the swarm spontaneously forms cohesive groups, the groups develop shared headings, and the flock as a whole executes smooth collective turns with no agent initiating or leading them.

**Visualization note:** Dot color encodes velocity direction (hue = angle in the HSV color wheel). When boids are disordered, the field is a mix of colors. As alignment emerges, color regions converge — patches of uniform hue mark agents that have synchronized direction. You can watch the phase transition from disorder to collective motion in real time.

---

#### Preset: Boids Flocking (`boids`)

180 agents in a 600×600 toroidal space (agents that exit one edge re-enter from the opposite side). Parameters are tuned for clear, readable flocking: moderate separation radius, balanced alignment and cohesion weights.

From a random scatter, agents quickly aggregate into groups, the groups develop shared directions, and flocking behavior stabilizes within a few hundred steps. Occasional collisions between sub-flocks cause temporary breakups that re-coalesce — the same dynamics seen in biological schools of fish when a predator strikes.

---

#### Preset: Murmuration (`murmuration`)

350 agents, tighter separation, stronger alignment weight, and a larger neighbor radius than the standard Boids preset. Inspired by the murmurations of European starlings — dense flocks of hundreds of thousands of birds that move as a single fluid entity, producing wave-like ripples of direction change.

The larger neighbor radius means information (a direction change in one part of the swarm) propagates faster through the group — each agent influences and is influenced by more others. The result is a more tightly coupled, more reactive swarm. Direction waves visibly ripple across the flock, exactly as they do in filmed murmuration footage. This is not programmed wave behavior; it is an emergent consequence of information propagating through a densely connected local network.

---

## Architecture

```
emergence_engine/
├── core/
│   ├── engine.py          # Timestep loop, pause/speed controls
│   ├── world.py           # GridWorld (CA) and AgentWorld (swarms)
│   ├── entity.py          # Agent base class (position, velocity, state)
│   ├── rule_system.py     # RuleSystem abstract base class
│   └── renderer.py        # Renderer abstract base class
├── simulations/
│   ├── cellular_automata.py   # CA rules, B/S factory, grid initializers
│   └── boids.py               # Vectorised Boids rule system
├── rendering/
│   └── matplotlib_renderer.py # FuncAnimation renderer, keyboard controls
├── configs/
│   └── presets.py             # Named simulation configurations
└── main.py                    # Entry point, preset builder
```

The engine core (`engine.py`, `world.py`, `rule_system.py`, `renderer.py`) knows nothing about specific simulations. To add a new simulation type, subclass `RuleSystem`, supply a `World`, add a preset to `configs/presets.py`, and register it in `main.py`. Nothing in the core changes.

---

## Dependencies

```
numpy
matplotlib
```

Install with:

```bash
pip install numpy matplotlib
```

---

## Further Reading

- Conway's Game of Life — Gardner, M. (1970). *Mathematical Games.* Scientific American.
- Cellular Automata — Wolfram, S. (2002). *A New Kind of Science.* Wolfram Media.
- Boids — Reynolds, C. (1987). *Flocks, Herds, and Schools: A Distributed Behavioral Model.* SIGGRAPH.
- Emergence — Holland, J. (1998). *Emergence: From Chaos to Order.* Perseus Books.
- Starling Murmurations — Cavagna et al. (2010). *Scale-free correlations in starling flocks.* PNAS.
