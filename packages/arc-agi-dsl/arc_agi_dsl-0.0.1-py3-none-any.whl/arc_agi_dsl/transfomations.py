from .utils import transformation
import numpy as np
from numpy.typing import NDArray


@transformation
def rotate(x: NDArray) -> NDArray:
    return np.rot90(x)


@transformation
def h_flip(x: np.ndarray) -> np.ndarray:
    return np.fliplr(x)
