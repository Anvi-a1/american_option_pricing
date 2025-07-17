class Option:
    """
    A class representing a financial option contract.

    Attributes:
        S (float): Spot price of the underlying asset
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free interest rate (annualized)
        sigma (float): Volatility of the underlying asset (annualized)
        option_type (str): 'call' or 'put'
        style (str): 'american' or 'european'
    """

    def __init__(self, S, K, T, r, sigma, option_type='put', style='american'):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
        self.style = style.lower()
        
        self._validate()

    def _validate(self):
        if self.option_type not in ['call', 'put']:
            raise ValueError("option_type must be either 'call' or 'put'")
        if self.style not in ['american', 'european']:
            raise ValueError("style must be either 'american' or 'european'")
        if any(x < 0 for x in [self.S, self.K, self.T, self.sigma]):
            raise ValueError("S, K, T, and sigma must be non-negative")
        if self.T == 0:
            raise ValueError("Time to maturity must be greater than 0")

    def describe(self):
        """Return a dictionary summary of the option."""
        return {
            "Spot Price (S)": self.S,
            "Strike Price (K)": self.K,
            "Time to Maturity (T)": self.T,
            "Risk-Free Rate (r)": self.r,
            "Volatility (σ)": self.sigma,
            "Option Type": self.option_type,
            "Option Style": self.style
        }

    def __repr__(self):
        return (f"Option({self.option_type.capitalize()} {self.style.capitalize()} | "
                f"S={self.S}, K={self.K}, T={self.T}, r={self.r}, sigma={self.sigma})")
