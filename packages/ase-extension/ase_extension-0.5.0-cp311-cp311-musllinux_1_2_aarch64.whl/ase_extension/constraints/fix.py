from collections.abc import Sequence
from typing import Literal

import numpy as np
from ase import Atoms
from ase.constraints import FixConstraint

from ase_extension import _ext


class FixBondLengths(FixConstraint):
    """Fix the bond lengths of a set of atom pairs.

    Args:
        atoms (Atoms): The Atoms object to which the constraint is applied.
        bond_indices (Sequence[tuple[int, int]] | np.ndarray): Pairs of atom indices to fix the bond lengths for.
        bond_lengths (Sequence[float] | np.ndarray | None): Initial bond lengths. If None, will be initialized from
            the current positions.
        algorithm (Literal["SHAKE", "LINCS"]): Algorithm to use for fixing the bond lengths.
            Currently only "SHAKE" is supported.
        maxiter (int): Maximum number of iterations for convergence of SHAKE.
        rtol (float): Relative tolerance for convergence.
    """

    def __init__(
        self,
        bond_indices: Sequence[tuple[int, int]] | np.ndarray,
        bond_lengths: Sequence[float] | np.ndarray | None = None,
        algorithm: Literal["SHAKE", "LINCS"] = "SHAKE",
        maxiter: int = 500,
        rtol: float = 1e-13,
    ):
        self.bond_indices = [(int(i), int(j)) for i, j in bond_indices]
        self.bond_lengths = bond_lengths
        self.algorithm = algorithm
        self.maxiter = maxiter
        self.rtol = rtol

        match self.algorithm:
            case "SHAKE":
                pass
            case "LINCS":
                raise NotImplementedError("LINCS algorithm is not implemented yet.")
            case _:
                raise ValueError(f"Unknown algorithm: {algorithm}. Available: ['SHAKE', 'LINCS']")
        self.shake = _ext.SHAKE(self.bond_indices, self.bond_lengths, maxiter, rtol)

    def get_removed_dof(self, atoms: Atoms):
        return len(self.bond_indices)

    def adjust_positions(self, atoms: Atoms, new: np.ndarray):
        if self.bond_lengths is None:
            self.bond_lengths = self.initialize_bond_lengths(atoms)
            self.shake.bond_lengths = self.bond_lengths

        old = atoms.positions
        cell = atoms.cell.array
        pbc = atoms.pbc.tolist()
        masses = atoms.get_masses()

        new_pos = self.shake.adjust_positions(old, new, masses, cell, pbc)
        new[:] = new_pos

    def adjust_momenta(self, atoms: Atoms, p: np.ndarray):
        if self.bond_lengths is None:
            self.bond_lengths = self.initialize_bond_lengths(atoms)
            self.shake.bond_lengths = self.bond_lengths

        old = atoms.positions
        masses = atoms.get_masses()
        cell = atoms.cell.array
        pbc = atoms.pbc.tolist()

        new_momenta = self.shake.adjust_momenta(old, p, masses, cell, pbc)
        p[:] = new_momenta

    def adjust_forces(self, atoms: Atoms, forces: np.ndarray):
        self.constraint_forces = -forces
        self.adjust_momenta(atoms, forces)
        self.constraint_forces += forces

    def get_indices(self):
        return np.unique(self.bond_indices.ravel())

    def todict(self):
        return {
            "name": "FixBondLengths",
            "kwargs": {
                "bond_indices": self.bond_indices,
                "bond_lengths": self.bond_lengths,
                "algorithm": self.algorithm,
                "maxiter": self.maxiter,
                "rtol": self.rtol,
            },
        }

    def index_shuffle(self, atoms, ind):
        """Shuffle the indices of the two atoms in this constraint"""
        map_ = np.zeros(len(atoms), int)
        map_[ind] = 1
        n = map_.sum()
        map_[:] = -1
        map_[ind] = range(n)
        pairs = map_[self.bond_indices]
        self.bond_indices = pairs[(pairs != -1).all(1)]
        if len(self.bond_indices) == 0:
            raise IndexError("Constraint not part of slice")

    def initialize_bond_lengths(self, atoms: Atoms) -> list[float]:
        """Initialize bond lengths from current atomic positions if not provided.

        Args:
            atoms: ASE Atoms object

        Returns:
            Array of bond lengths
        """
        bondlengths = np.zeros(len(self.bond_indices))

        for i, (a, b) in enumerate(self.bond_indices):
            bondlengths[i] = atoms.get_distance(a, b, mic=True)

        return bondlengths.tolist()
