import matplotlib.pyplot as plt
import numpy as np

class OutputGenerator:
    def __init__(self, model, config) -> None:
        self.model = model
        self.config = config
    
    def generate_outputs(self) -> None:
        x_grid = np.linspace(start=0, stop=self.config.x_length, num=self.model.n_x)
        y_grid = np.linspace(start=0, stop=self.config.y_length, num=self.model.n_y)
        X, Y = np.meshgrid(x_grid, y_grid)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, self.model.solution.solution, 50)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.savefig('solution.png')
