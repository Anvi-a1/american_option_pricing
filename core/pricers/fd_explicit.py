import numpy as np
from core.option import Option

def price_american_fd_explicit(option: Option, M: int = 50, N: int = 50):
    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    is_call = option.option_type == 'call'

    S_max = 2 * S
    dS = S_max / M
    dt = T / N

    # Check explicit FDM stability
    dt_stable = 1 / (sigma**2 * M**2)
    if dt > dt_stable:
        print(f"[Warning] dt = {dt:.5f} is too large for stability. Reducing to dt_stable = {dt_stable:.5f}.")
        N = int(T / dt_stable) + 1
        dt = T / N

    grid = np.zeros((M + 1, N + 1))
    stock_prices = np.linspace(0, S_max, M + 1)

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

    # Explicit finite difference loop
    for j in reversed(range(N)):
        for i in range(1, M):
            Si = i * dS
            a = 0.5 * dt * (sigma**2 * i**2 - r * i)
            b = 1 - dt * (sigma**2 * i**2 + r)
            c = 0.5 * dt * (sigma**2 * i**2 + r * i)

            grid[i, j] = a * grid[i - 1, j + 1] + b * grid[i, j + 1] + c * grid[i + 1, j + 1]

            # Early exercise condition
            exercise = max(Si - K, 0) if is_call else max(K - Si, 0)
            grid[i, j] = max(grid[i, j], exercise)

    # Interpolate to get value at S
    return np.interp(S, stock_prices, grid[:, 0])
