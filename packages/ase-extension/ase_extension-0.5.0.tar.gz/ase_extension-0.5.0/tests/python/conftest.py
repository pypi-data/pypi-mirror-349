import ase.build
import pytest


@pytest.fixture
def water_molecule():
    return ase.build.molecule("H2O")
