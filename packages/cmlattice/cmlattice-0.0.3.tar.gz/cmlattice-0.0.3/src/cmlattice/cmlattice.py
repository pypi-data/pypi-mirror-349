from __future__ import annotations

from collections.abc import Generator

import numpy as np


class CoupledMapLattice:
    """An implementation of a coupled map lattice (CML) model.
    Used as a base class for other CML models.

    Attributes:
        n (int): The size of the lattice.
        r (float): The parameter for the map function.
        epsilion (float): The coupling strength.
        state (np.ndarray): The current state of the lattice.
        history (list[np.ndarray]): The history of the lattice states.
        time (int): The current time step.
    """

    def __init__(self, n: int, r: float, epsilon: float = 1) -> None:
        self.n = n
        self.r = r
        self.epsilon = epsilon
        self.state = self.init_state()
        self.history = [self.state]
        self.time = 0

    def __repr__(self) -> str:
        return f"CoupledMapLattice(n={self.n}, r={self.r}, epsilion={self.epsilon})"

    def init_state(self) -> np.ndarray:
        """Initializes the state of the lattice."""
        return np.random.uniform(0, 1, (self.n, self.n))

    @property
    def state(self) -> np.ndarray:
        """Returns the current state of the lattice."""
        return self._state.copy()

    @state.setter
    def state(self, value: np.ndarray) -> None:
        """Sets the state of the lattice.
        Args:
            value (np.ndarray): The new state of the lattice.
        """
        if not isinstance(value, np.ndarray):
            raise ValueError('State must be a numpy array.')
        if value.ndim != 2:
            raise ValueError('State must be a 2D array.')
        if value.dtype != np.float64:
            raise ValueError('State must be a float64 array.')

        if value.shape != (self.n, self.n):
            raise ValueError(f"State must be of shape ({self.n}, {self.n}).")
        self._state = value

    @property
    def history(self) -> list[np.ndarray]:
        """Returns the history of the lattice."""
        return self._history.copy()

    @history.setter
    def history(self, value: list[np.ndarray]) -> None:
        """Sets the history of the lattice.
        Args:
            value (List[np.ndarray]): The new history of the lattice.
        """
        if not isinstance(value, list):
            raise ValueError('History must be a list.')
        if not all(isinstance(x, np.ndarray) for x in value):
            raise ValueError('All elements in history must be numpy arrays.')

        self._history = value

    def append_history(self, value: np.ndarray) -> None:
        """Appends a new state to the history of the lattice.
        Args:
            value (np.ndarray): The new state to append.
        """
        if not isinstance(value, np.ndarray):
            raise ValueError('Value must be a numpy array.')
        self._history.append(value)

    def state_function(self, x: np.ndarray) -> np.ndarray:
        """Applies a function to the state of the lattice.
        Args:
            x (np.ndarray): The input array.

        Returns:
            np.ndarray: The output array after applying the function.
        """
        return self.r * x * (1 - x)

    def update(self) -> None:
        """Updates the state of the lattice.
        If `coupled` is True, the update is coupled.
        """
        if self.epsilon < 1:
            self._update_coupled()
        else:
            self._update_independent()
        self.append_history(self.state)
        self.time += 1

    def _update_coupled(self) -> None:
        """Updates the state of the lattice using a coupled map."""
        new_lattice = self.state.copy()
        for i in range(self.n):
            left_neighbor = self.state[(i - 1) % self.n]
            for j in range(self.n):
                # Apply the coupled map update
                new_lattice[i, j] = self.epsilon * self.state_function(
                    self.state[i, j],
                ) + (1 - self.epsilon) * self.state_function(left_neighbor[j])
        self.state = new_lattice

    def _update_independent(self) -> None:
        """Updates the state of the lattice using an independent map."""
        self.state = self.state_function(self.state)

    def reset(self) -> None:
        """Resets the lattice to its initial state."""
        self.state = self.init_state()
        self.history = []
        self.time = 0

    def simulate(self, steps: int) -> Generator[np.ndarray]:
        """Simulates the lattice for a given number of steps.

        Args:
            steps (int): The number of steps to simulate.

        Yields:
            np.ndarray: The state of the lattice at each step.
        """
        for _ in range(steps):
            self.update()
            yield self.state
