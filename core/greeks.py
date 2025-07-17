import copy

def perturb_option(option, attr, epsilon):
    """
    Return two copies of the option object with the specified attribute
    perturbed up and down by epsilon.
    """
    opt_up = copy.deepcopy(option)
    opt_down = copy.deepcopy(option)
    setattr(opt_up, attr, getattr(opt_up, attr) + epsilon)
    setattr(opt_down, attr, getattr(opt_down, attr) - epsilon)
    return opt_up, opt_down

def compute_delta(pricer, option, steps=100, epsilon=1e-2):
    """
    Compute Delta: ∂V/∂S using central difference.
    """
    opt_up, opt_down = perturb_option(option, 'S', epsilon)
    price_up = pricer(opt_up, steps)
    price_down = pricer(opt_down, steps)
    return (price_up - price_down) / (2 * epsilon)

def compute_gamma(pricer, option, steps=100, epsilon=1e-2):
    """
    Compute Gamma: ∂²V/∂S² using central difference.
    """
    opt_up, opt_down = perturb_option(option, 'S', epsilon)
    price_up = pricer(opt_up, steps)
    price_down = pricer(opt_down, steps)
    price_mid = pricer(option, steps)
    return (price_up - 2 * price_mid + price_down) / (epsilon ** 2)

def compute_theta(pricer, option, steps=100, epsilon=1e-4):
    """
    Compute Theta: ∂V/∂T using forward difference.
    Returns negative value as per standard convention.
    """
    if option.T <= epsilon:
        return float('nan')  # Avoid zero or negative maturity
    opt_t = copy.deepcopy(option)
    opt_t.T -= epsilon
    price_now = pricer(option, steps)
    price_later = pricer(opt_t, steps)
    return -(price_later - price_now) / epsilon

def compute_vega(pricer, option, steps=100, epsilon=1e-3):
    """
    Compute Vega: ∂V/∂σ using central difference.
    """
    opt_up, opt_down = perturb_option(option, 'sigma', epsilon)
    price_up = pricer(opt_up, steps)
    price_down = pricer(opt_down, steps)
    return (price_up - price_down) / (2 * epsilon)

def compute_rho(pricer, option, steps=100, epsilon=1e-4):
    """
    Compute Rho: ∂V/∂r using central difference.
    """
    opt_up, opt_down = perturb_option(option, 'r', epsilon)
    price_up = pricer(opt_up, steps)
    price_down = pricer(opt_down, steps)
    return (price_up - price_down) / (2 * epsilon)

def compute_all_greeks(pricer, option, steps=100):
    """
    Convenience function to compute all Greeks at once.
    """
    delta = compute_delta(pricer, option, steps)
    gamma = compute_gamma(pricer, option, steps)
    theta = compute_theta(pricer, option, steps)
    vega  = compute_vega(pricer, option, steps)
    rho   = compute_rho(pricer, option, steps)
    return delta, gamma, theta, vega, rho