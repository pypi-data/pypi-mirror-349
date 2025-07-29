from __future__ import annotations

import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import PillowWriter
from matplotlib.image import AxesImage

from .cmlattice import CoupledMapLattice


class Visualization:
    """A class for visualizing the state of a Coupled Map Lattice (CML)."""

    def __init__(self, lattice: CoupledMapLattice) -> None:
        self.lattice = lattice

    @property
    def lattice(self) -> CoupledMapLattice:
        """Returns the current lattice."""
        return self._lattice

    @lattice.setter
    def lattice(self, value: CoupledMapLattice) -> None:
        """Sets the lattice to the given value.
        Args:
            value (CoupledMapLattice): The new lattice.
        """
        if not isinstance(value, CoupledMapLattice):
            raise ValueError(
                'lattice must be an instance of CoupledMapLattice.',
            )

        assert (
            len(
                value.history,
            )
            > 1
        ), 'History must contain at least two elements.'
        assert len(np.array(value.history).shape) <= 3, ('Histroy must be 2D.')

        self._lattice = value

    def animate(self, show: bool = False, save: bool = True) -> animation.FuncAnimation:
        """Vizulizes the simulation of the lattice over time.
        This method creates an animation of the lattice's state over time
        and saves it as a GIF file. The animation shows the activation
        of the lattice's neurons at each time step.

        Args:
            show (bool): Whether to show the plot immediately.
                Defaults to False.

        Returns:
            animation.FuncAnimation: The animation object.

        Raises:
            AssertionError: If the lattice is not a CoupledMapLattice
                or if the history does not contain at least two elements.
        """
        self.lattice = self.lattice
        self.fig, self.ax = plt.subplots()
        return self._animate(frames=len(self.lattice.history), show=show, save=save)

    def show_nueron(self, nueron: tuple[int]) -> None:
        """Shows the activation over time of a single neuron.
        Args:
            nueron (int): The index of the neuron to visualize.

        Raises:
            AssertionError: If the lattice is not a CoupledMapLattice
                or if the history does not contain at least two elements.
        """
        self.fig, self.ax = plt.subplots()
        hist = np.array(self.lattice.history)
        self.ax.plot(hist[:, nueron[0], nueron[1]])
        self.ax.set_title(f"Neuron {nueron} Activation Over Time")
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Activation')
        plt.show()

    def generate_filename(self) -> str:
        """Generate a filename for the animation based on the current date and time.

        Returns:
            str: The generated filename.
        """
        now = datetime.now()
        return now.strftime('lattice_animation_%Y%m%d_%H%M%S.gif')

    def init_animation(self) -> AxesImage:
        """Initialize the animation."""
        self.ax.clear()
        self.im = self.ax.imshow(
            self.lattice.history[0],
            cmap='plasma',
            interpolation='nearest',
            animated=True,
        )
        return (self.im,)

    def update(self, i: int) -> AxesImage:
        """Update the visualization for the given frame.

        Args:
            i (int): The current frame number.
        """
        self.im.set_array(np.nan_to_num(self.lattice.history[i]))

        self.ax.set_title(f"Time: {i}")
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_xticks([])
        return (self.im,)

    def _animate(self, show: bool, frames: int | None = None, save: bool = True) -> animation.FuncAnimation:
        """Animate the visualization.

        Args:
            show (bool): Whether to show the plot immediately.
            frames (Optional[int]): The number of frames to animate. If None, use the length of the history.
                    Defaults to None.

        Returns:
            animation.FuncAnimation: The animation object.
        """
        self.ax.clear()
        if frames is None:
            frames = len(self.lattice.history)

        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            init_func=self.init_animation,
            interval=50,
            blit=True,
            repeat_delay=1000,
        )

        if save:
            os.makedirs('map_animations', exist_ok=True)
            filename = self.generate_filename()
            ani.save(
                os.path.join('map_animations', filename),
                writer=PillowWriter(fps=5),
            )

        if show:
            plt.show()
        return ani
