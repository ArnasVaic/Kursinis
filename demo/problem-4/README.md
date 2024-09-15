# Problem 4

## Problem formulation

$$
\frac{\partial u}{\partial t}=\alpha\Delta u
$$

With initial conditions

$$
u(x, y, 0) = 0,\quad x\in[0,L],\quad y\in[0,L]\\
$$

and boundary conditions

$$
u(0, y, t) = 100,\quad y\in[0,L],\quad t\in[0,T]\\
\phantom{.}\\
u(x, L, t) = 0,\quad x\in[0,L],\quad t\in[0,T]\\
\phantom{.}\\
\frac{\partial u}{\partial x}=0\Big|_{x=L},\quad y\in[0,L],\quad t\in[0,T]\\
\phantom{.}\\
\frac{\partial u}{\partial y}=0\Big|_{y=0},\quad x\in[0,L],\quad t\in[0,T]\\
$$

where $L$ is the side length of the plate and $T$ is the duration of the simulation.

## Numerical models

We will use explicit finite difference method to get a solution for the heat function

$$
\frac{u^{n+1}_{i,j}-u^{n}_{i,j}}{\Delta t}=\alpha\left(\frac{u^n_{i+1,j}-2u^n_{i,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}-2u^n_{i,j}+u^n_{i,j-1}}{\Delta y^2}\right)\\
\phantom{.}\\
u^{n+1}_{i,j}=u^{n}_{i,j}-\alpha\Delta t\left(\frac{2u^n_{i,j}}{\Delta x^2}+\frac{2u^n_{i,j}}{\Delta y^2}\right)+\alpha\Delta t\left(\frac{u^n_{i+1,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}+u^n_{i,j-1}}{\Delta y^2}\right)\\
\phantom{.}\\
u^{n+1}_{i,j}=\left(1-2\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\right)u^{n}_{i,j}+\alpha\Delta t\left(\frac{u^n_{i+1,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}+u^n_{i,j-1}}{\Delta y^2}\right)
$$

To ensure numerical stability we need to make sure the coefficient in front of $u_{i,j}^n$ is always positive so

$$
1-2\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\geqslant 0\\
\phantom{.}\\
\frac{1}{2}\geqslant\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\\
\phantom{.}\\
\Delta t\leqslant\frac{1}{2\alpha}\left(\frac{\Delta x^2\Delta y^2}{\Delta x^2+\Delta y^2}\right)
$$
