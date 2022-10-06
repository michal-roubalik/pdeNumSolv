from distutils.command.config import config
from typing import Any
from System import System
from Solution import Solution
from BoundaryCondition import BoundaryCondition
import numpy as np
import pandas as pd
from scipy.interpolate import interpn
import matplotlib.pyplot as plt

class Model:
    def __init__(self, config) -> None:
        self.config = config
        self.n_x = self.get_n_x()
        self.n_y = self.get_n_y()
        self.dx = self.get_dx()
        self.dy = self.get_dy()
        self.dt = self.get_dt()
        self.initial_condition = self.setup_initial_condition()
        self.boundary_conditions = self.setup_boundary_conditions()
        self.right_hand_side = self.setup_right_hand_side()
        self.solution = self.solve()

    def solve(self) -> Solution:
        if self.config.equation_type == "Parabolic":
            return self.solve_parabolic_equation()
        elif self.config.equation_type == "Elliptic":
            return self.build_elliptic_system()
        elif self.config.equation_type == "Hyperbolic":
            return self.build_hyperbolic_system()
        else:
            raise Exception("Unknown equation type.")


    def solve_parabolic_equation(self) -> Solution:
        if self.config.time_dependent:
            return self.solve_parabolic_equation_time_dependent()
        else:
            return self.solve_parabolic_equation_static()
    
    def solve_parabolic_equation_static(self) -> Solution:
        
        N = self.n_x * self.n_y
        A = np.zeros((N, N))
        b = np.zeros(N)
        
        for i in range(self.n_x):
            for j in range(self.n_y):
                n = (self.n_x * j)+i # row of A and b
                # South BC
                if j == 0:
                    if self.boundary_conditions["South"].type == "Dirichlet":
                        A[n,n] = 1
                        b[n] = self.boundary_conditions["South"].vector[i]
                    elif self.boundary_conditions["South"].type == "Neumann":
                        A[n,n] = 1
                        A[n,n+self.n_x] = -1
                        b[n] = -self.boundary_conditions["South"].vector[i] * self.dx
                    else:
                        raise Exception("Unknown Boundary Condition type.")
                # North BC
                elif j == self.n_y-1:
                    if self.boundary_conditions["North"].type == "Dirichlet":
                        A[n,n] = 1
                        b[n] = self.boundary_conditions["North"].vector[i]
                    elif self.boundary_conditions["North"].type == "Neumann":
                        A[n,n] = 1
                        A[n,n-self.n_x]  = -1
                        b[n] = self.boundary_conditions["North"].vector[i] * self.dx
                    else:
                        raise Exception("Unknown Boundary Condition type.")
                # West BC
                elif i == 0:    
                    if self.boundary_conditions["West"].type == "Dirichlet":
                        A[n,n] = 1
                        b[n] = self.boundary_conditions["West"].vector[j]
                    elif self.boundary_conditions["West"].type == "Neumann":
                        A[n,n] = 1
                        A[n,n+1] -1
                        b[n] = -self.boundary_conditions["West"].vector[j] * self.dy
                    else:
                        raise Exception("Unknown Boundary Condition type.")
                # East BC
                elif i == self.n_x-1:
                    if self.boundary_conditions["East"].type == "Dirichlet":
                        A[n,n] = 1
                        b[n] = self.boundary_conditions["East"].vector[j]
                    elif self.boundary_conditions["East"].type == "Neumann":
                        A[n,n] = 1
                        A[n,n-1] -1
                        b[n] = self.boundary_conditions["East"].vector[j] * self.dy
                    else:
                        raise Exception("Unknown Boundary Condition type.")
                # Inner space
                else:
                    # Center
                    A[n,n] = -((2/(self.dx)**2) + (2/(self.dy)**2))
                    # Southern neighbour
                    A[n,n - self.n_x] = 1/(self.dy)**2
                    # Northern neighbour
                    A[n,n + self.n_x] = 1/(self.dy)**2
                    # Western neighbour
                    A[n,n - 1] = 1/(self.dx)**2
                    # Eastern neighbour
                    A[n,n + 1] = 1/(self.dx)**2

                    b[n] = -self.right_hand_side[i,j]

        system = System(A, b, self.n_x, self.n_y)

        solution = system.solve()
        return solution

    def solve_parabolic_equation_time_dependent(self) -> Solution:
        pass

    def build_elliptic_system(self) -> System:
        pass

    def build_hyperbolic_system(self) -> System:
        pass

    def get_n_x(self) -> int:
        n_x = self.config.x_length / (self.get_dx()) + 1
        return np.int(n_x)

    def get_n_y(self) -> int:
        n_y = self.config.y_length / (self.get_dy()) + 1
        return np.int(n_y)

    def get_dx(self) -> float:
        dx = np.minimum(self.config.space_granularity, self.config.x_length / (self.config.N - 1))
        return dx

    def get_dy(self) -> float:
        dy = np.minimum(self.config.space_granularity, self.config.y_length / (self.config.N - 1))
        return dy

    def get_dt(self) -> float:
        default = 0.01
        return default

    def setup_initial_condition(self) -> Any:
        cfg_file_path = self.config.cfg_file_path
        initial_condition = pd.read_excel(
            cfg_file_path, usecols="D:N", skiprows=10, nrows=self.config.N
        ).values[0][0]
        return initial_condition

    def setup_boundary_conditions(self) -> Any:
        # North, South, East, West
        cfg_file_path = self.config.cfg_file_path

        boundary_condition_S_type = pd.read_excel(
            cfg_file_path, usecols="E", skiprows=10, nrows=1
        ).values[0][0]
        boundary_condition_S = pd.read_excel(
            cfg_file_path, usecols="E:O", skiprows=12, nrows=1
        ).values[0]

        boundary_condition_W_type = pd.read_excel(
            cfg_file_path, usecols="E", skiprows=13, nrows=1
        ).values[0][0]
        boundary_condition_W = pd.read_excel(
            cfg_file_path, usecols="E:O", skiprows=15, nrows=1
        ).values[0]

        boundary_condition_N_type = pd.read_excel(
            cfg_file_path, usecols="E", skiprows=16, nrows=1
        ).values[0][0]
        boundary_condition_N = pd.read_excel(
            cfg_file_path, usecols="E:O", skiprows=18, nrows=1
        ).values[0]

        boundary_condition_E_type = pd.read_excel(
            cfg_file_path, usecols="E", skiprows=19, nrows=1
        ).values[0][0]
        boundary_condition_E = pd.read_excel(
            cfg_file_path, usecols="E:O", skiprows=21, nrows=1
        ).values[0]

        boundary_conditions = {
            "South": BoundaryCondition(
                self.config,
                self.n_x,
                "South",
                boundary_condition_S_type,
                boundary_condition_S,
            ),
            "West": BoundaryCondition(
                self.config,
                self.n_y,
                "West",
                boundary_condition_W_type,
                boundary_condition_W,
            ),
            "North": BoundaryCondition(
                self.config,
                self.n_x,
                "North",
                boundary_condition_N_type,
                boundary_condition_N,
            ),
            "East": BoundaryCondition(
                self.config,
                self.n_y,
                "East",
                boundary_condition_E_type,
                boundary_condition_E,
            ),
        }
        return boundary_conditions

    def setup_right_hand_side(self) -> Any:
        cfg_file_path = self.config.cfg_file_path
        data = pd.read_excel(
            cfg_file_path, usecols="D:N", skiprows=39, nrows=self.config.N
        )
        x_p = np.linspace(start=0, stop=self.config.x_length, num=self.config.N)
        y_p = np.linspace(start=0, stop=self.config.y_length, num=self.config.N)
        
        x_grid = np.linspace(start=0, stop=self.config.x_length, num=self.n_x)
        y_grid = np.linspace(start=0, stop=self.config.y_length, num=self.n_y)

        x_grid_values = np.array([])
        y_grid_values = np.array([])

        for i in range(self.n_x):
            for j in range(self.n_y):
                x_grid_values = np.append(x_grid_values, x_grid[i])
                y_grid_values = np.append(y_grid_values, y_grid[j])

        rhs = interpn(points=(x_p, y_p), values = data.values, xi=(x_grid_values, y_grid_values))
        rhs = rhs.reshape(self.n_x, self.n_y)
        return rhs
