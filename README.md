# American Option Pricing

A Python project for pricing American options using multiple numerical methods, with visualization and interactive exploration via Jupyter Notebook and Streamlit web app.

## Overview
This project provides tools to price American (and European) options using:
- Binomial Tree
- Finite Difference Methods (Explicit, Implicit, Crank-Nicolson)
- Monte Carlo Longstaff-Schwartz (LSM)

It also computes option Greeks and provides visualizations for option prices and sensitivities.

## Features
- Price American and European call/put options
- Multiple numerical pricers (Binomial, FDM, Monte Carlo LSM)
- Compute Greeks: Delta, Gamma, Theta, Vega, Rho
- Interactive Streamlit web app
- Jupyter notebook for demonstrations
- Visualization of price and Greeks vs. spot price

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd american_option_pricing
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install numpy scipy matplotlib streamlit
   ```

## Usage

### 1. Jupyter Notebook
- Open `main.ipynb` in Jupyter Lab/Notebook.
- Run the cells to see pricing, Greeks, and plots for various methods.

### 2. Streamlit Web App
- Run the app from the project root:
  ```bash
  streamlit run webapp/streamlit_app.py
  ```
- Open the provided local URL (usually http://localhost:8501) in your browser.
- Use the sidebar to adjust option parameters, method, and see real-time results and plots.

## Project Structure
```
american_option_pricing/
  core/
    option.py           # Option class and validation
    greeks.py           # Greeks calculation
    pricers/
      binomial.py       # Binomial tree pricer
      fd_explicit.py    # Explicit FDM pricer
      fd_implicit.py    # Implicit FDM pricer
      fd_cn.py          # Crank-Nicolson FDM pricer
      monte_carlo_lsm.py# Monte Carlo LSM pricer
  utils/
    plotter.py          # Plotting utilities
    validators.py       # Black-Scholes and input validation
  webapp/
    streamlit_app.py    # Streamlit UI
  main.ipynb            # Jupyter notebook demo
  requirements.txt      # Python dependencies
  README.md             # Project documentation
```

## Credits
- Developed by Anvi Dubey
- License: MIT

## Acknowledgments
- Numerical methods based on standard option pricing literature
- Streamlit for interactive UI
- Matplotlib for plotting

---
Feel free to contribute or raise issues for improvements!