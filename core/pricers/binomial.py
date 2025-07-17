import numpy as np
from core.option import Option

def price_american_binomial(option: Option, steps: int = 100) -> float:
    # Extracting parameters from the option
    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    is_call = option.option_type == 'call'

    # Time step and binomial tree parameters
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability

    # Initialize asset price tree and option value tree
    asset_prices = np.zeros((steps + 1, steps + 1))  # Asset prices at each node
    option_values = np.zeros((steps + 1, steps + 1))  # Option values at each node

    # Calculate asset prices at maturity (leaf nodes)
    for j in range(steps + 1):
        asset_prices[j, steps] = S * (u ** j) * (d ** (steps - j))
        option_values[j, steps] = max(asset_prices[j, steps] - K, 0) if is_call else max(K - asset_prices[j, steps], 0)

    # Backward induction: Calculate option values at each node
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            # Calculate the asset price at each node
            asset_prices[j, i] = S * (u ** j) * (d ** (i - j))
            
            # Option value is the maximum of holding or exercising early
            holding_value = np.exp(-r * dt) * (p * option_values[j + 1, i + 1] + (1 - p) * option_values[j, i + 1])
            early_exercise_value = max(asset_prices[j, i] - K, 0) if is_call else max(K - asset_prices[j, i], 0)
            option_values[j, i] = max(holding_value, early_exercise_value)

    return option_values[0, 0]
