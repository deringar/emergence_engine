"""
Boids-style swarm simulation.

Three steering forces:
    separation  – avoid crowding neighbours
    alignment   – steer toward average heading of neighbours
    cohesion    – steer toward average position of neighbours

All operations are vectorised with NumPy for performance.
"""

import numpy as np
from core.rule_system import RuleSystem
from core.world import AgentWorld
from core.entity import Entity


# --------------------------------------------------------------------------- #
# Agent factory helpers                                                        #
# --------------------------------------------------------------------------- #

def make_boids(
    n: int,
    width: float,
    height: float,
    max_speed: float = 3.0,
    agent_type: str = "boid",
) -> list:
    positions = np.random.rand(n, 2) * [width, height]
    angles = np.random.uniform(0, 2 * np.pi, n)
    velocities = np.stack([np.cos(angles), np.sin(angles)], axis=1) * max_speed
    return [
        Entity(positions[i], velocities[i], agent_type=agent_type)
        for i in range(n)
    ]


# --------------------------------------------------------------------------- #
# RuleSystem                                                                   #
# --------------------------------------------------------------------------- #

class BoidsRules(RuleSystem):
    """
    Vectorised Boids implementation.

    Parameters (all tunable at runtime via attribute assignment):
        separation_radius   : distance below which separation kicks in
        neighbour_radius    : distance for alignment/cohesion
        separation_weight   : steering force scale
        alignment_weight    : steering force scale
        cohesion_weight     : steering force scale
        max_speed           : terminal velocity
        max_force           : max magnitude of steering correction per tick
    """

    def __init__(
        self,
        separation_radius: float = 25.0,
        neighbour_radius: float = 60.0,
        separation_weight: float = 1.8,
        alignment_weight: float = 1.0,
        cohesion_weight: float = 1.0,
        max_speed: float = 3.5,
        max_force: float = 0.15,
    ):
        self.separation_radius = separation_radius
        self.neighbour_radius = neighbour_radius
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.max_speed = max_speed
        self.max_force = max_force

    # ------------------------------------------------------------------ #

    def apply(self, world: AgentWorld, dt: float = 1.0) -> None:
        agents = world.agents
        if len(agents) < 2:
            return

        pos = np.array([a.position for a in agents])   # (N, 2)
        vel = np.array([a.velocity for a in agents])   # (N, 2)

        # Pairwise displacement with toroidal wrapping
        W, H = world.width, world.height
        diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]   # (N, N, 2)
        diff[:, :, 0] = _wrap_diff(diff[:, :, 0], W)
        diff[:, :, 1] = _wrap_diff(diff[:, :, 1], H)

        dist = np.linalg.norm(diff, axis=2)   # (N, N)
        np.fill_diagonal(dist, np.inf)

        sep_mask = (dist < self.separation_radius)                          # (N, N)
        nbr_mask = (dist < self.neighbour_radius) & ~sep_mask               # (N, N)

        sep_force = _separation(diff, dist, sep_mask)
        ali_force = _alignment(vel, nbr_mask)
        coh_force = _cohesion(diff, nbr_mask)

        steering = (
            self.separation_weight * sep_force
            + self.alignment_weight * ali_force
            + self.cohesion_weight * coh_force
        )
        steering = _limit(steering, self.max_force)

        new_vel = _limit(vel + steering, self.max_speed)
        new_pos = (pos + new_vel * dt) % [W, H]

        for i, agent in enumerate(agents):
            agent.position = new_pos[i]
            agent.velocity = new_vel[i]


# --------------------------------------------------------------------------- #
# Vectorised force helpers                                                     #
# --------------------------------------------------------------------------- #

def _wrap_diff(d: np.ndarray, size: float) -> np.ndarray:
    """Wrap difference to [-size/2, size/2]."""
    d = d.copy()
    d[d > size / 2] -= size
    d[d < -size / 2] += size
    return d


def _limit(arr: np.ndarray, max_val: float) -> np.ndarray:
    """Clip each row vector to at most max_val magnitude."""
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    scale = np.where(norms > max_val, max_val / (norms + 1e-8), 1.0)
    return arr * scale


def _separation(diff: np.ndarray, dist: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Steer away from close neighbours (weighted by inverse distance)."""
    weight = np.where(mask, 1.0 / (dist + 1e-8), 0.0)          # (N, N)
    force = (weight[:, :, np.newaxis] * diff).sum(axis=1)        # (N, 2)
    return force


def _alignment(vel: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Steer toward average velocity of neighbours."""
    counts = mask.sum(axis=1, keepdims=True).astype(float)
    avg_vel = (mask[:, :, np.newaxis] * vel[np.newaxis, :, :]).sum(axis=1)
    return np.where(counts > 0, avg_vel / (counts + 1e-8), 0.0)


def _cohesion(diff: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Steer toward centre of mass of neighbours (diff is from self to others, so negate)."""
    counts = mask.sum(axis=1, keepdims=True).astype(float)
    avg_disp = (mask[:, :, np.newaxis] * (-diff)).sum(axis=1)
    return np.where(counts > 0, avg_disp / (counts + 1e-8), 0.0)
