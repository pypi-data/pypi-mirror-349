import ase.build
from ase import units
from ase.calculators.emt import EMT
from ase.md import VelocityVerlet
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution

from ase_extension.constraints.fix import FixBondLengths


def test_shake():
    atoms = ase.build.molecule("H2")
    d_H2 = atoms.get_distance(0, 1)
    fix = FixBondLengths([(0, 1)], [d_H2], algorithm="SHAKE")
    atoms.calc = EMT()
    atoms.set_constraint(fix)
    # Run NVE MD
    MaxwellBoltzmannDistribution(atoms, temperature_K=300)
    dyn = VelocityVerlet(atoms, 1.0 * units.fs)
    for _ in range(10):
        dyn.run(1)
        # Check bond length
        d_H2_new = atoms.get_distance(0, 1)
        assert abs(d_H2_new - d_H2) < 1e-5, f"Bond length changed: {d_H2_new} vs {d_H2}"
