import numpy as np

class BoundaryCondition():
    def __init__(self, config, n, side, type, vector) -> None:
        self.config = config
        self.n = n
        self.side = side
        self.type = type
        self.vector = self.get_vector(vector)
        
    def get_vector(self, vector) -> np.ndarray:
        if self.type in ["South", "North"]:
            n = self.n
            L = self.config.x_length
        else:
            n = self.n
            L = self.config.y_length

        x_p = np.linspace(start=0, stop=L, num=len(vector))
        y_p = vector

        x_interp = np.linspace(start=0, stop=L, num=n)
        y_interp = np.interp(x_interp, xp=x_p, fp=y_p)

        return y_interp