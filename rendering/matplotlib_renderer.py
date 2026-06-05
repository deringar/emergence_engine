"""
Matplotlib-based renderer.

Keyboard controls (when the figure window is focused):
    Space   – pause / resume
    r       – reset simulation
    +/=     – speed up  (more steps per frame)
    -       – slow down (fewer steps per frame)
    q       – quit
"""

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from core.renderer import Renderer


def _direction_colors(vel: np.ndarray) -> np.ndarray:
    """Map velocity angle to HSV hue so aligned agents share colour."""
    angles = np.arctan2(vel[:, 1], vel[:, 0])   # -π … π
    hues = (angles + np.pi) / (2 * np.pi)        # 0 … 1
    return plt.cm.hsv(hues)                       # (N, 4) RGBA


class MatplotlibRenderer(Renderer):
    """
    Drives a FuncAnimation loop.  Handles both 'grid' and 'agents' render-data types.

    Parameters
    ----------
    interval_ms : int
        Target milliseconds between frames (lower = faster redraw).
    figsize : tuple
        Matplotlib figure size in inches.
    title : str
        Window / figure title.
    agent_colors : dict
        Reserved for future multi-type sims.  Boids use direction-based HSV colouring.
    """

    def __init__(
        self,
        interval_ms: int = 50,
        figsize: tuple = (7, 7),
        title: str = "Emergence Engine",
        agent_colors: dict = None,
    ):
        self.interval_ms = interval_ms
        self.figsize = figsize
        self.title = title
        self.agent_colors = agent_colors or {}

    # ------------------------------------------------------------------ #
    # Renderer contract                                                    #
    # ------------------------------------------------------------------ #

    def animate(self, engine) -> None:
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")
        fig.canvas.manager.set_window_title(self.title)

        render_data = engine.world.get_render_data()
        draw_fn, artists, use_blit = self._init_artists(ax, render_data, engine.world)

        status_text = ax.text(
            0.01, 0.98, "",
            transform=ax.transAxes,
            color="white", fontsize=8,
            va="top", ha="left",
            fontfamily="monospace",
        )

        def update(_frame):
            engine.step()
            rd = engine.world.get_render_data()
            draw_fn(rd, artists)
            label = (
                f"step={engine.step_count:>6}  "
                f"spf={engine.steps_per_frame}  "
                f"{'PAUSED' if engine.paused else 'running'}"
            )
            status_text.set_text(label)
            return list(artists.values()) + [status_text]

        def on_key(event):
            if event.key == " ":
                engine.toggle_pause()
            elif event.key == "r":
                engine.reset()
            elif event.key in ("+", "="):
                engine.increase_speed()
            elif event.key == "-":
                engine.decrease_speed()
            elif event.key == "q":
                plt.close(fig)

        fig.canvas.mpl_connect("key_press_event", on_key)

        ani = animation.FuncAnimation(
            fig,
            update,
            interval=self.interval_ms,
            blit=use_blit,
            cache_frame_data=False,
        )
        self._ani = ani
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------------ #
    # Internal: set up artists per render-data type                       #
    # ------------------------------------------------------------------ #

    def _init_artists(self, ax, render_data: dict, world):
        kind = render_data["type"]

        if kind == "grid":
            im = ax.imshow(
                render_data["data"],
                cmap=render_data.get("colormap", "binary_r"),
                vmin=render_data.get("vmin", 0.0),
                vmax=render_data.get("vmax", 1.0),
                interpolation="nearest",
                origin="upper",
                animated=True,
            )
            ax.axis("off")
            artists = {"im": im}

            def draw(rd, a):
                a["im"].set_data(rd["data"])

            return draw, artists, True   # blit OK for grid

        elif kind == "agents":
            W, H = render_data["bounds"]
            ax.set_xlim(0, W)
            ax.set_ylim(0, H)
            ax.set_aspect("equal")
            ax.axis("off")

            pos = render_data["positions"]   # (N, 2)
            vel = render_data["velocities"]  # (N, 2)
            n = len(pos)

            # Seed scatter with real initial data so blit frame-0 is consistent
            init_colors = _direction_colors(vel) if n > 0 else np.zeros((0, 4))
            sc = ax.scatter(
                pos[:, 0] if n > 0 else [],
                pos[:, 1] if n > 0 else [],
                s=20,
                c=init_colors,
                alpha=0.9,
                lw=0,
                animated=True,
            )
            artists = {"sc": sc}

            def draw(rd, a):
                p = rd["positions"]
                v = rd["velocities"]
                if len(p) == 0:
                    return
                a["sc"].set_offsets(p)
                a["sc"].set_facecolors(_direction_colors(v))

            return draw, artists, True   # scatter set_offsets + set_facecolors works with blit

        else:
            raise ValueError(f"Unknown render-data type: {kind!r}")
