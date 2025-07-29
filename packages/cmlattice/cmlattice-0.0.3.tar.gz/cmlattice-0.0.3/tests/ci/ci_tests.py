from __future__ import annotations

import numpy as np
from cmlattice import CoupledMapLattice
from cmlattice import KanekoLattice
from cmlattice import RulkovLattice


def test_kaneko():
    """Test the kaneko latttice."""
    kaneko_coupled = KanekoLattice(10, r=0.5, epsilon=0.5)
    initial_state = kaneko_coupled.state.copy()
    kaneko_coupled.update()
    assert not np.array_equal(initial_state, kaneko_coupled.state), (
        'State should change after update.'
    )
    assert len(kaneko_coupled.history) == 2, (
        'History should contain one element after first update.'
    )
    assert np.array_equal(kaneko_coupled.history[0], initial_state), (
        'History should contain the initial state.'
    )
    assert kaneko_coupled.time == 1, 'Time should increment after update.'
    assert kaneko_coupled.state.shape == (10, 10), (
        'State should have the same shape as the lattice.'
    )
    assert kaneko_coupled.state.dtype == np.float64, 'State should be of type float64.'
    assert kaneko_coupled.state.ndim == 2, 'State should be a 2D array.'


def test_rulkov():
    """Test the rulkov latttice."""
    rulkov_decoupled = RulkovLattice(10, 0.5, 1, 1)
    initial_state = rulkov_decoupled.state.copy()
    rulkov_decoupled.update()
    assert not np.array_equal(initial_state, rulkov_decoupled.state), (
        'State should change after update.'
    )
    assert len(rulkov_decoupled.history) == 2, (
        'History should contain one element after first update.'
    )
    assert np.array_equal(rulkov_decoupled.history[0], initial_state[0]), (
        'History should contain the initial state.'
    )
    assert rulkov_decoupled.time == 1, 'Time should increment after update.'
    assert rulkov_decoupled.state.shape == (2, 10, 10), (
        'State should have the same shape as the lattice.'
    )
    assert rulkov_decoupled.state.dtype == np.float64, (
        'State should be of type float64.'
    )
    assert rulkov_decoupled.state.ndim == 3, 'State should be a 3D array.'
    assert np.array_equal(
        rulkov_decoupled.state[0],
        ((
            rulkov_decoupled.r /
            (1 + initial_state[0] ** 2)
        ) + initial_state[1]),
    ), 'State update formula is incorrect.'

    rulkov_coupled = RulkovLattice(10, 0.5, 1, 0.5)
    initial_state = rulkov_coupled.state.copy()
    rulkov_coupled.update()
    assert not np.array_equal(initial_state, rulkov_coupled.state), (
        'State should change after update.'
    )
    assert len(rulkov_coupled.history) == 2, (
        'History should contain one element after first update.'
    )
    assert np.array_equal(rulkov_coupled.history[0], initial_state[0]), (
        'History should contain the initial state.'
    )
    assert rulkov_coupled.time == 1, 'Time should increment after update.'
    assert rulkov_coupled.state.shape == (2, 10, 10), (
        'State should have the same shape as the lattice.'
    )
    assert rulkov_coupled.state.dtype == np.float64, 'State should be of type float64.'
    assert rulkov_coupled.state.ndim == 3, 'State should be a 3D array.'


def test_update():
    """Test the update method of the CoupledMapLattice class."""
    # Create a CoupledMapLattice instance
    lattice = CoupledMapLattice(10, r=1)

    initial_state = lattice.state.copy()
    lattice.update()
    assert not np.array_equal(initial_state, lattice.state), (
        'State should change after update.'
    )
    assert len(lattice.history) == 2, (
        'History should contain one element after first update.'
    )
    assert np.array_equal(lattice.history[0], initial_state), (
        'History should contain the initial state.'
    )
    assert lattice.time == 1, 'Time should increment after update.'
    assert lattice.state.shape == (10, 10), (
        'State should have the same shape as the lattice.'
    )
    assert lattice.state.dtype == np.float64, 'State should be of type float64.'
    assert lattice.state.ndim == 2, 'State should be a 2D array.'
    assert (
        lattice.state.flatten().tolist()
        == (lattice.r * initial_state * (1 - initial_state)).flatten().tolist()
    ), 'State update formula is incorrect.'

    coupled_lattice = CoupledMapLattice(10, r=0.5, epsilon=0.5)
    coupled_lattice.update()
    assert lattice.state.shape == (10, 10), (
        'State should have the same shape as the lattice.'
    )
    assert lattice.state.dtype == np.float64, 'State should be of type float64.'
    assert lattice.state.ndim == 2, 'State should be a 2D array.'


def test_simulate():
    """Test the simulate method of the CoupledMapLattice class."""
    # Create a CoupledMapLattice instance
    lattice = CoupledMapLattice(10, r=0.5)
    initial_state = lattice.state.copy()

    # Simulate for 5 time steps
    simulator = lattice.simulate(5)

    assert simulator is not None, 'Simulator should not be None.'
    assert sum(1 for _ in simulator) == 5, 'Simulator should yield 5 time steps.'

    assert len(lattice.history) == 6, (
        'History should contain 6 elements after simulating 5 steps.'
    )

    assert np.array_equal(lattice.history[0], initial_state), (
        'First element in history should be the initial state.'
    )
