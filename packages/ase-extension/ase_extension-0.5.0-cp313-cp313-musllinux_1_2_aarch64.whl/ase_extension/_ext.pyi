from typing import Protocol

import numpy as np

class RMSDResult(Protocol):
    val: float
    grad: np.ndarray
    rotation: np.ndarray
    translation: np.ndarray
