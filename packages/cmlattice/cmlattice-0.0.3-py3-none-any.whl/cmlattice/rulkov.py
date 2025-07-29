from __future__ import annotations

import numpy as np

from .cmlattice import CoupledMapLattice


class RulkovLattice(CoupledMapLattice):
    """An implementation of the Rulkov map.

    The Rulkov map is a coupled map lattice model that exhibits
    complex behavior, including chaos and synchronization.

    Attributes:
        n (int): The size of the lattice.
        r (float): The parameter for the map function.
        mu (float): The parameter for the map function.
        sigma (float): The parameter for the map function.
        epsilion (float): The coupling strength.
        state (np.ndarray): The current state of the lattice.
        history (list[np.ndarray]): The history of the lattice states.
        time (int): The current time step.
    """

    def __init__(
        self,
        n: int,
        r: float,
        mu: float,
        sigma: float,
        epsilon: float = 1,
    ) -> None:
        super().__init__(n, r, epsilon)
        self.mu = mu
        self.sigma = sigma
        self.history = [self.state[0]]

    def __repr__(self):
        return f"RulkovLattice(n={self.n}, r={self.r}, epsilion={self.epsilon}, mu={self.mu}, sigma={self.sigma})"

    def init_state(self) -> np.ndarray:
        """Initializes the state of the lattice."""
        return np.random.uniform(0, 1, (2, self.n, self.n))

    @CoupledMapLattice.state.setter
    def state(self, value: np.ndarray) -> None:
        """Sets the state of the lattice.
        Args:
            value (np.ndarray): The new state of the lattice.
        """
        if not isinstance(value, np.ndarray):
            raise ValueError('State must be a numpy array.')
        if value.ndim != 3:
            raise ValueError('State must be a 3D array.')
        if value.dtype != np.float64:
            raise ValueError('State must be a float64 array.')

        if value.shape != (2, self.n, self.n):
            raise ValueError(
                f"State must be of shape (2, {self.n}, {self.n}).",
            )
        self._state = value

    def state_function(self, x: np.ndarray, y: np.ndarray = None) -> np.ndarray:
        """Applies the Rulkov map update function to the state of the lattice.

        Args:
            x (np.ndarray): The input array representing the first state.
            y (np.ndarray): The input array representing the second state.

        Returns:
            np.ndarray: The updated state.
        """
        x_next = (self.r / (1 + x**2)) + y
        y_next = y - self.mu * (x_next - self.sigma)
        return np.array([x_next, y_next])

    def _update_coupled(self) -> None:
        """Updates the state of the lattice using the Rulkov map."""
        state = self.state.copy()
        for i in range(self.n):
            left_neighbor = state[:, (i - 1) % self.n]
            right_neighbor = state[:, (i + 1) % self.n]
            for j in range(self.n):
                # Apply the Rulkov map update
                state[:, i, j] = self.epsilon * self.state_function(
                    state[0, i, j],
                    state[1, i, j],
                ) + (self.epsilon / 2) * (
                    self.state_function(left_neighbor[0, j], left_neighbor[1, j]) +
                    self.state_function(
                        right_neighbor[0, j], right_neighbor[1, j],
                    )
                )
        self.state = state

    def _update_independent(self) -> None:
        """Updates the state of the lattice using an independent map."""
        self.state = self.state_function(self.state[0], self.state[1])

    def update(self):
        if self.epsilon < 1:
            self._update_coupled()
        else:
            self._update_independent()

        assert self.state[0].shape == (
            self.n, self.n,
        ), 'The shape is not correct'
        self.append_history(self.state[0])
        self.time += 1
