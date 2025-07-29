from __future__ import annotations

from .cmlattice import CoupledMapLattice


class KanekoLattice(CoupledMapLattice):
    """An implementation of the Kaneko map."""

    def __init__(self, n: int, r: float, epsilon: float = 1) -> None:
        super().__init__(n, r, epsilon)

    def __repr__(self):
        return f"KenekoLattice(n={self.n}, r={self.r}, epsilion={self.epsilon})"

    def update(self):
        """Updates the state of the lattice using the Kaneko map."""
        state = self.state.copy()
        for i in range(self.n):
            left_neighbor = state[(i - 1) % self.n]
            right_neighbor = state[(i + 1) % self.n]
            for j in range(self.n):
                # Apply the Kaneko map update
                state[i, j] = self.epsilon * self.state_function(state[i, j]) + (
                    self.epsilon / 2
                ) * (
                    self.state_function(
                        left_neighbor[j] +
                        self.state_function(right_neighbor[j]),
                    )
                )
        self.state = state
        self.append_history(self.state)
        self.time += 1
