import matplotlib.pyplot as plt
import numpy as np

def plot_price_vs_spot(pricer, base_option, S_range=(50, 150), steps=100, title="Price vs Spot", label=None):
    spot_prices = np.linspace(*S_range, 100)
    prices = []

    for S in spot_prices:
        opt = base_option.__class__(S=S, K=base_option.K, T=base_option.T, r=base_option.r,
                                    sigma=base_option.sigma, option_type=base_option.option_type, style=base_option.style)
        prices.append(pricer(opt, steps))

    plt.figure(figsize=(8, 5))
    plt.plot(spot_prices, prices, label=label or pricer.__name__)
    plt.xlabel("Spot Price (S)")
    plt.ylabel("Option Price")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_greek_vs_spot(greek_func, pricer, base_option, S_range=(50, 150), steps=100, greek_name="Delta"):
    spot_prices = np.linspace(*S_range, 100)
    greek_vals = []

    for S in spot_prices:
        opt = base_option.__class__(S=S, K=base_option.K, T=base_option.T, r=base_option.r,
                                    sigma=base_option.sigma, option_type=base_option.option_type, style=base_option.style)
        greek_vals.append(greek_func(pricer, opt, steps))

    plt.figure(figsize=(8, 5))
    plt.plot(spot_prices, greek_vals, label=greek_name, color='darkgreen')
    plt.xlabel("Spot Price (S)")
    plt.ylabel(greek_name)
    plt.title(f"{greek_name} vs Spot Price")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()