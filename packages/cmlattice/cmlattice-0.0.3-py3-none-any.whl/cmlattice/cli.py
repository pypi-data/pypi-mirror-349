from __future__ import annotations

from argparse import ArgumentParser

from .cmlattice import CoupledMapLattice
from .kaneko import KanekoLattice
from .rulkov import RulkovLattice
from .viz import Visualization


def main():
    parser = ArgumentParser(
        description='Run Coupled Map Lattice simulations.',
        prog='cml',
    )
    subparsers = parser.add_subparsers(dest='command', prog='cml')
    sim_parser = subparsers.add_parser(
        'simulate',
        help='Runs a cml simualation.',
    )

    sim_parser.add_argument(
        '-n',
        '--nuerons',
        type=int,
        required=True,
        help='Number of neurons in the lattice.',
    )

    sim_parser.add_argument(
        '-r',
        '--r',
        type=float,
        required=True,
        help='Parameter r for the lattice.',
    )

    sim_parser.add_argument(
        '-e',
        '--epsilon',
        type=float,
        default=0.5,
        help='Parameter epsilon for the lattice.',
    )

    sim_parser.add_argument(
        '-t',
        '--time',
        type=int,
        default=100,
        help='Number of time steps to simulate.',
    )

    sim_parser.add_argument(
        '-k',
        '--key',
        help='Type of simulation to run.',
        default='cml',
        choices=['cml', 'kaneko', 'rulkov'],
    )

    sim_parser.add_argument(
        '-m',
        '--mu',
        type=float,
        default=None,
        help='Parameter mu for the Rulkov lattice.',
    )

    sim_parser.add_argument(
        '-s',
        '--sigma',
        type=float,
        default=None,
        help='Parameter sigma for the Rulkov lattice.',
    )

    args = parser.parse_args()
    if args.command == 'simulate':
        if args.key == 'kaneko':
            lattice = KanekoLattice(args.nuerons, args.r, args.epsilon)
        elif args.key == 'rulkov':
            assert args.mu is not None, 'Mu parameter is required for Rulkov lattice.'
            assert args.sigma is not None, (
                'Sigma parameter is required for Rulkov lattice.'
            )
            lattice = RulkovLattice(
                args.nuerons,
                args.r,
                args.mu,
                args.sigma,
                args.epsilon,
            )
        else:
            lattice = CoupledMapLattice(args.nuerons, args.r, args.epsilon)

        for _ in range(args.time):
            lattice.update()

        viz = Visualization(lattice)
        viz.animate(show=False)


if __name__ == '__main__':
    main()
