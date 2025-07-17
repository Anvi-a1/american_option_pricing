import numpy as np
from scipy.linalg import solve_banded
from core.option import Option

def price_american_fd_cn(option: Option, M: int = 100, N: int = 100):
    """
    Price an American option using the Crank-Nicolson finite difference method.

    Parameters:
        option (Option): Option instance.
        M (int): Number of asset price steps.
        N (int): Number of time steps.

    Returns:
        float: American option price
    """
    # Unpack parameters
    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    is_call = option.option_type == 'call'

    # Grid setup
    S_max = 2 * S
    dS = S_max / M
    dt = T / N
    grid = np.zeros((M + 1, N + 1))
    stock_prices = np.linspace(0, S_max, M + 1)

    # Payoff at maturity
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

    # Coefficients for interior points
    i_vals = np.arange(1, M)
    a = 0.25 * dt * (sigma**2 * i_vals**2 - r * i_vals)
    b = -0.5 * dt * (sigma**2 * i_vals**2 + r)
    c = 0.25 * dt * (sigma**2 * i_vals**2 + r * i_vals)

    main_diag = 1 - b
    lower_diag = -a[1:]
    upper_diag = -c[:-1]

    ab = np.zeros((3, M - 1))

    for j in reversed(range(N)):
        rhs = a * grid[i_vals - 1, j + 1] + (1 + b) * grid[i_vals, j + 1] + c * grid[i_vals + 1, j + 1]

        ab[0, 1:] = upper_diag
        ab[1, :] = main_diag
        ab[2, :-1] = lower_diag

        x = solve_banded((1, 1), ab, rhs)

        # Early exercise
        S_vals = stock_prices[1:M]
        if is_call:
            exercise = np.maximum(S_vals - K, 0)
        else:
            exercise = np.maximum(K - S_vals, 0)
        grid[1:M, j] = np.maximum(x, exercise)

    return np.interp(S, stock_prices, grid[:, 0])
