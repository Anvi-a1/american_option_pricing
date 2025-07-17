import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import necessary libraries

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from core.option import Option
from core.pricers.binomial import price_american_binomial
from core.pricers.fd_explicit import price_american_fd_explicit
from core.pricers.fd_implicit import price_american_fd_implicit
from core.pricers.fd_cn import price_american_fd_cn
from core.pricers.monte_carlo_lsm import price_american_mc_lsm
from core.greeks import compute_all_greeks

st.set_page_config(page_title="American Option Pricing", layout="wide")
st.title("📈 American Option Pricing & Greeks Explorer")

# Sidebar inputs
st.sidebar.header("Option Parameters")
S = st.sidebar.slider("Spot Price (S)", 50.0, 150.0, 100.0)
K = st.sidebar.slider("Strike Price (K)", 50.0, 150.0, 100.0)
T = st.sidebar.slider("Time to Maturity (T)", 0.01, 3.0, 1.0)
r = st.sidebar.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05)
sigma = st.sidebar.slider("Volatility (σ)", 0.05, 1.0, 0.2)
option_type = st.sidebar.selectbox("Option Type", ["put", "call"])
method = st.sidebar.selectbox("Pricing Method", ["Binomial", "FDM Explicit", "FDM Implicit", "FDM Crank-Nicolson", "Monte Carlo LSM"])
steps = st.sidebar.slider("Steps (Binomial or FDM)", 10, 500, 100)

# Monte Carlo parameters
if method == "Monte Carlo LSM":
    n_paths = st.sidebar.number_input("MC Paths", min_value=1000, max_value=100000, value=10000, step=1000)
    n_mc_steps = st.sidebar.slider("MC Steps", 10, 200, 50)
    poly_degree = st.sidebar.slider("MC Poly Degree", 1, 5, 2)
    mc_seed = st.sidebar.number_input("MC Seed", min_value=0, max_value=99999, value=42, step=1)

# Create option object
opt = Option(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type, style="american")

# Select pricer
if method == "Binomial":
    pricer = lambda o, s: price_american_binomial(o, s)
elif method == "FDM Explicit":
    pricer = lambda o, s: price_american_fd_explicit(o, M=s, N=s)
elif method == "FDM Implicit":
    pricer = lambda o, s: price_american_fd_implicit(o, M=s, N=s)
elif method == "FDM Crank-Nicolson":
    pricer = lambda o, s: price_american_fd_cn(o, M=s, N=s)
elif method == "Monte Carlo LSM":
    pricer = lambda o, s: price_american_mc_lsm(o, n_paths=n_paths, n_steps=n_mc_steps, poly_degree=poly_degree, seed=mc_seed)
else:
    pricer = None

# Compute price
if pricer is not None:
    price = pricer(opt, steps)
else:
    price = None

# Compute Greeks
if pricer is not None:
    delta, gamma, theta, vega, rho = compute_all_greeks(pricer, opt, steps)
else:
    delta = gamma = theta = vega = rho = None

# Display results
st.markdown("## 💰 Price")
if price is not None:
    st.write(f"**{method} American {option_type.capitalize()} Price:** ${price:.4f}")
else:
    st.warning("No pricer selected or price could not be computed.")

st.markdown("## ⚖️ Greeks")
if delta is not None:
    st.write(f"**Delta:** {delta:.4f}")
else:
    st.warning("No pricer selected or delta could not be computed.")
if gamma is not None:
    st.write(f"**Gamma:** {gamma:.4f}")
else:
    st.warning("No pricer selected or gamma could not be computed.")
if theta is not None:
    st.write(f"**Theta:** {theta:.4f}")
else:
    st.warning("No pricer selected or theta could not be computed.")
if vega is not None:
    st.write(f"**Vega:** {vega:.4f}")
else:
    st.warning("No pricer selected or vega could not be computed.")
if rho is not None:
    st.write(f"**Rho:** {rho:.4f}")
else:
    st.warning("No pricer selected or rho could not be computed.")

# --- Price vs Spot Plot ---
st.markdown("## 📊 Price vs Spot Plot")

if pricer is not None:
    S_vals = np.linspace(50, 150, 50)
    prices = [pricer(Option(S=s, K=K, T=T, r=r, sigma=sigma, option_type=option_type, style="american"), steps) for s in S_vals]
    # Ensure prices is a flat list of floats for plotting
    if isinstance(prices, np.ndarray):
        prices = prices.tolist()
    elif isinstance(prices, list):
        prices = [float(p) if not isinstance(p, float) else p for p in prices]
    fig1, ax1 = plt.subplots()
    ax1.plot(S_vals, prices, label=f"{method}")
    ax1.set_xlabel("Spot Price (S)")
    ax1.set_ylabel("Option Price")
    ax1.set_title("Price vs Spot")
    ax1.legend()
    st.pyplot(fig1)
else:
    st.warning("No pricer selected.")

# --- Payoff Plot ---
st.markdown("## 💵 Payoff Diagram at Expiry")

payoff = np.maximum(K - S_vals, 0) if option_type == "put" else np.maximum(S_vals - K, 0)

fig2, ax2 = plt.subplots()
ax2.plot(S_vals, payoff, color="purple", label="Payoff at Expiry")
ax2.set_xlabel("Spot Price (S)")
ax2.set_ylabel("Payoff")
ax2.set_title("Payoff Diagram")
ax2.legend()
st.pyplot(fig2)

# Footer
st.markdown("---")
st.write("✅ Adjust parameters from the sidebar to see how prices and Greeks change in real-time.")
st.markdown("💬 _Built with ❤️ using Python, Streamlit, and your custom numerical pricers._")

