import numpy as np
from Solution import Solution


class System:
    def __init__(self, A, b, n_x, n_y) -> None:
        self.A = A
        self.b = b
        self.n_x = n_x
        self.n_y = n_y

    def get_A(self) -> np.ndarray:
        return self.A

    def get_b(self) -> np.ndarray:
        return self.b

    def solve(self) -> Solution:
        """Solution of Ax=b system. TODO: Implement own numeric solver."""
        x = np.linalg.solve(self.A, self.b)
        solution = np.reshape(x, (self.n_y, self.n_x))
        return Solution(solution)
