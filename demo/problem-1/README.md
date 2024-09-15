# Solve 1D Heat equation using numerical method

Solve for $u(x,t)$

$$
\begin{cases}
\partial_t u=\alpha\partial_{xx}u\\
u(0,t)=T_1\\
u(1,t)=T_2\\
u(x,0)=0\\
\end{cases}
$$

Using limit definition

$$
\partial_t u=\lim_{\Delta t\to 0}\frac{u(x,t+\Delta t)-u(x,t)}{\Delta t}=\lim_{\Delta t\to 0}\frac{u(x,t)-u(x,t-\Delta t)}{\Delta t}
$$

we can get a good approximation by choosing a small $\Delta t$.

$$
\Delta_t u=\frac{\Delta u}{\Delta t}\approx\frac{u(x,t+\Delta t)-u(x,t)}{\Delta t}
$$

The same principle applies for the second derivative $\partial_{xx}u$. We will use the second derivative formula to expand the $\Delta_x u(x,t)$ to get a more "symmetric" result 

$$
\begin{align}
\Delta_{xx}u\\
\frac{\Delta_x u(x+\Delta x,t)-\Delta_x u(x,t)}{\Delta x}\\
\frac{u(x+\Delta x, t)-u(x,t)}{\Delta x^2}-\frac{u(x,t)-u(x-\Delta x, t)}{\Delta x^2}\\
\frac{u(x+\Delta x, t)-u(x,t)-u(x,t)+u(x-\Delta x, t)}{\Delta x^2}\\
\frac{u(x+\Delta x, t)-2u(x,t)+u(x-\Delta x, t)}{\Delta x^2}\\
\end{align}
$$

Now approximated equation becomes

$$
\begin{align}
\frac{u(x,t+\Delta t)-u(x,t)}{\Delta t}&\approx\alpha\frac{u(x+\Delta x, t)-2u(x,t)+u(x-\Delta x, t)}{\Delta x^2}\\

u(x,t+\Delta t)&\approx u(x,t)+\alpha\frac{\Delta t}{\Delta x^2}(u(x+\Delta x, t)-2u(x,t)+u(x-\Delta x, t)) \\


u(x,t+\Delta t)&\approx u(x,t)\left(1-2\alpha\frac{\Delta t}{\Delta x^2}\right)+\alpha\frac{\Delta t}{\Delta x^2}(u(x+\Delta x, t)+u(x-\Delta x, t))

\end{align}
$$

The last transformation was performed to highlight the constant next to $u(x,t)$ term. If it ever becomes negative, the simulation can go haywire so it is important to ensure that

$$
\begin{align}
1-2\alpha\frac{\Delta t}{\Delta x^2}&\geqslant 0\\
1&\geqslant 2\alpha\frac{\Delta t}{\Delta x^2}\\
\frac{\Delta x^2}{2\alpha}&\geqslant\Delta t\\
\Delta t&\leqslant\frac{\Delta x^2}{2\alpha}\\
\end{align}
$$
