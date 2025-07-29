from ase_extension import _ext

from .bias import BiasPotential


class ConfineSphere(BiasPotential):
    """Apply logfermi potential for confined molecular dynamics in a sphere.
    Method referenced from https://xtb-docs.readthedocs.io/en/latest/xcontrol.html#confining-in-a-cavity

    Args:
        radius (float): Radius of the confining sphere.
        temperature (float): Temperature in Kelvin.
        beta (float): Beta parameter for the potential.
    """

    def __init__(self, radius: float = 5.0, temperature: float = 300, beta: float = 6):
        self.radius = radius
        self.temperature = temperature
        self.beta = beta

    def _get_bias_energy_and_force(self, atoms):
        E, E_grad = _ext.log_fermi_spherical_potential(atoms.positions, self.radius, self.temperature, self.beta)
        return E, -E_grad
