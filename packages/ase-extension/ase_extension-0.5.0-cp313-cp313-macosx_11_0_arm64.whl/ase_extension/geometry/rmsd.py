from ase import Atoms

from ase_extension import _ext


def compute_rmsd(atoms: Atoms, atoms_ref: Atoms) -> _ext.RMSDResult:
    if atoms.pbc.any() or atoms_ref.pbc.any():
        raise ValueError("PBC is not supported in computing RMSD.")
    pos = atoms.get_positions()
    pos_ref = atoms_ref.get_positions()
    if pos.shape != pos_ref.shape:
        raise ValueError("Atoms objects must have the same number of atoms.")
    if atoms.get_chemical_symbols() != atoms_ref.get_chemical_symbols():
        raise ValueError("Atoms objects must have the same chemical symbols.")

    return _ext.compute_rmsd(pos, pos_ref)
