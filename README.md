# Lambda-Nabla PDE Num Solver

This is first draft of implementation of numerical solver of Partial Differential Equations:
- Parabolic (e.g. Diffusion)
- Hyperbolic (e.g. Transport)
- Elliptic (e.g. Waves)

`main` function is in file `nabla_lambda.py`.

Input dada are taken from .xlsx file, these inclue:
- Equation type
- Solution scheme
- Time dependency, horizon and granularity
- Space Granularity

## Currently implemented
- Static Parabolic Equation with Dirichlet and Neumann Boundary Conditions
![alt text](https://github.com/michal-roubalik/pdeNumSolv/blob/master/solution.png?raw=true)

## ToBeDone
- other Equation type solutions
- time dependency
- solution schemes: Crank-Nicholson, Upwind, Lax-Wendroff,...
- improving code quality
- tests, asserts
- better output handling
- more complex geometries
