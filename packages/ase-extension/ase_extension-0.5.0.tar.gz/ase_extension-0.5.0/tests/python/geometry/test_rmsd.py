import ase.build
import numpy as np
from ase.build import minimize_rotation_and_translation

from ase_extension.geometry import compute_rmsd


def test_rmsd_with_ase():
    def rmsd(X, Y):
        return np.sqrt(((X - Y) ** 2).sum(axis=1).mean())

    rng = np.random.default_rng(42)
    atoms_ref = ase.build.molecule("CH3CH2OH")
    atoms_1 = atoms_ref.copy()
    atoms_1.rattle(0.2)
    atoms_1.positions += rng.random(3)
    atoms_2 = atoms_1.copy()

    minimize_rotation_and_translation(atoms_1, atoms_ref)
    rmsd_ase = rmsd(atoms_1.positions, atoms_ref.positions)
    rmsd_this = compute_rmsd(atoms_2, atoms_ref).val
    assert abs(rmsd_ase - rmsd_this) < 1e-5, f"RMSD mismatch: {rmsd_ase} vs {rmsd_this}"
