import numpy as np
from scipy.linalg import solve_banded
from core.option import Option

def price_american_fd_implicit(option: Option, M: int = 100, N: int = 100):
    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    is_call = option.option_type == 'call'

    S_max = 2 * S
    dS = S_max / M
    dt = T / N
    stock_prices = np.linspace(0, S_max, M + 1)
    grid = np.zeros((M + 1, N + 1))

    # Terminal payoff
    if is_call:
        grid[:, -1] = np.maximum(stock_prices - K, 0)
    else:
        grid[:, -1] = np.maximum(K - stock_prices, 0)

    # Boundary conditions
    if is_call:
        grid[-1, :] = S_max - K * np.exp(-r * dt * (N - np.arange(N + 1)))
        grid[0, :] = 0
    else:
        grid[0, :] = K * np.exp(-r * dt * (N - np.arange(N + 1)))
        grid[-1, :] = 0

    # Coefficients
    i_vals = np.arange(1, M)
    a = -0.5 * dt * (sigma**2 * i_vals**2 - r * i_vals)
    b = 1 + dt * (sigma**2 * i_vals**2 + r)
    c = -0.5 * dt * (sigma**2 * i_vals**2 + r * i_vals)

    ab = np.zeros((3, M - 1))

    for j in reversed(range(N)):
        rhs = grid[1:M, j + 1].copy()

        # Adjust for boundary conditions
        rhs[0] -= a[0] * grid[0, j]
        rhs[-1] -= c[-1] * grid[M, j]

        # Fill band matrix
        ab[0, 1:] = c[:-1]        # upper diagonal
        ab[1, :] = b              # main diagonal
        ab[2, :-1] = a[1:]        # lower diagonal

        # Solve
        x = solve_banded((1, 1), ab, rhs)

        # Early exercise
        S_vals = stock_prices[1:M]
        if is_call:
            exercise = np.maximum(S_vals - K, 0)
        else:
            exercise = np.maximum(K - S_vals, 0)
        grid[1:M, j] = np.maximum(x, exercise)

    return np.interp(S, stock_prices, grid[:, 0])
