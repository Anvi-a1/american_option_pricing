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
method = st.sidebar.selectbox("Pricing Method", ["Binomial", "FDM Explicit", "FDM Implicit", "FDM Crank-Nicolson"])
steps = st.sidebar.slider("Steps (Binomial or FDM)", 10, 500, 100)

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
else:
    pricer = None

# Compute price
price = pricer(opt, steps)

# Compute Greeks
delta, gamma, theta, vega, rho = compute_all_greeks(pricer, opt, steps)

# Display results
st.markdown("## 💰 Price")
st.write(f"**{method} American {option_type.capitalize()} Price:** ${price:.4f}")

st.markdown("## ⚖️ Greeks")
st.write(f"**Delta:** {delta:.4f}")
st.write(f"**Gamma:** {gamma:.4f}")
st.write(f"**Theta:** {theta:.4f}")
st.write(f"**Vega:** {vega:.4f}")
st.write(f"**Rho:** {rho:.4f}")

# --- Price vs Spot Plot ---
st.markdown("## 📊 Price vs Spot Plot")

S_vals = np.linspace(50, 150, 50)
prices = [pricer(Option(S=s, K=K, T=T, r=r, sigma=sigma, option_type=option_type, style="american"), steps) for s in S_vals]

fig1, ax1 = plt.subplots()
ax1.plot(S_vals, prices, label=f"{method}")
ax1.set_xlabel("Spot Price (S)")
ax1.set_ylabel("Option Price")
ax1.set_title("Price vs Spot")
ax1.legend()
st.pyplot(fig1)

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

