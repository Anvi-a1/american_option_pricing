import numpy as np
from scipy.stats import norm
from core.option import Option

def black_scholes_price(option: Option) -> float:
    """
    Computes the European Black-Scholes price for a Call/Put option.
    """
    S, K, T, r, sigma = option.S, option.K, option.T, option.r, option.sigma
    if T <= 0 or sigma <= 0:
        return max(0, S - K) if option.option_type == 'call' else max(0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option.option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
