# Problem 5

## Problem formulation

$$
\frac{\partial u}{\partial t}=\alpha\Delta u
$$

With initial conditions

$$
A = [0,0.5L]\times[0,0.5L]\cup[0.5L,L]\times[0.5L,L]\\
u(x, y, 0) = 100,\quad (x, y)\in A\\
u(x, y, 0) = 0,\quad (x, y)\notin A
$$

and boundary conditions

$$

\frac{\partial u}{\partial x}\Big|_{x=0}=\frac{\partial u}{\partial x}\Big|_{x=L}=0,\quad y\in[0,L],\quad t\in[0,T]\\

\frac{\partial u}{\partial y}\Big|_{y=0}=\frac{\partial u}{\partial y}\Big|_{y=L}=0,\quad x\in[0,L],\quad t\in[0,T]\\
$$

where $L$ is the side length of the plate and $T$ is the duration of the simulation.

## Numerical models

We will use explicit finite difference method to get a solution for the heat function

$$
\frac{u^{n+1}_{i,j}-u^{n}_{i,j}}{\Delta t}=\alpha\left(\frac{u^n_{i+1,j}-2u^n_{i,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}-2u^n_{i,j}+u^n_{i,j-1}}{\Delta y^2}\right)\\

u^{n+1}_{i,j}=u^{n}_{i,j}-\alpha\Delta t\left(\frac{2u^n_{i,j}}{\Delta x^2}+\frac{2u^n_{i,j}}{\Delta y^2}\right)+\alpha\Delta t\left(\frac{u^n_{i+1,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}+u^n_{i,j-1}}{\Delta y^2}\right)\\

u^{n+1}_{i,j}=\left(1-2\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\right)u^{n}_{i,j}+\alpha\Delta t\left(\frac{u^n_{i+1,j}+u^n_{i-1,j}}{\Delta x^2}+\frac{u^n_{i,j+1}+u^n_{i,j-1}}{\Delta y^2}\right)
$$

To ensure numerical stability we need to make sure the coefficient in front of $u_{i,j}^n$ is always positive so

$$
1-2\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\geqslant 0\\

\frac{1}{2}\geqslant\alpha\Delta t\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)\\

\Delta t\leqslant\frac{1}{2\alpha}\left(\frac{\Delta x^2\Delta y^2}{\Delta x^2+\Delta y^2}\right)
$$
