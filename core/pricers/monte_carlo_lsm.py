import numpy as np
from numpy.polynomial.polynomial import Polynomial
from core.option import Option

def price_american_mc_lsm(option: Option, n_paths=10000, n_steps=50, poly_degree=2, seed=42):
    """
    Price American option using Monte Carlo + Longstaff-Schwartz Method.

    Parameters:
        option (Option): Option instance.
        n_paths (int): Number of simulated price paths.
        n_steps (int): Time discretization steps.
        poly_degree (int): Degree of polynomial for regression.
        seed (int): RNG seed for reproducibility.

    Returns:
        float: American option price.
    """
    np.random.seed(seed)

    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    is_call = option.option_type == 'call'
    dt = T / n_steps
    discount = np.exp(-r * dt)

    # 1. Simulate asset paths
    Z = np.random.normal(size=(n_paths, n_steps))
    S_paths = np.zeros_like(Z)
    S_paths[:, 0] = S

    for t in range(1, n_steps):
        S_paths[:, t] = S_paths[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z[:, t])

    # 2. Compute payoff matrix
    if is_call:
        payoff = np.maximum(S_paths - K, 0)
    else:
        payoff = np.maximum(K - S_paths, 0)

    # 3. Initialize cashflows: last time step payoff
    cashflow = payoff[:, -1]

    # 4. Backward induction
    for t in range(n_steps - 2, 0, -1):
        in_the_money = payoff[:, t] > 0
        X = S_paths[in_the_money, t]
        Y = cashflow[in_the_money] * discount

        if len(X) < poly_degree + 1:
            # Not enough points to fit the polynomial, skip regression
            continue

        # Regression: estimate continuation value
        coeffs = Polynomial.fit(X, Y, poly_degree).convert().coef
        continuation = np.polyval(coeffs[::-1], X)

        # Exercise decision
        exercise = payoff[in_the_money, t] > continuation
        cashflow[in_the_money] = np.where(exercise, payoff[in_the_money, t], cashflow[in_the_money] * discount)

    # 5. Discount to time 0
    price = np.mean(cashflow) * discount
    return price
