import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.set_page_config(page_title="Fourier Series Explorer", layout="wide")

st.title("Fourier Series Explorer")

# Sidebar inputs
st.sidebar.header("Configuration")
func_str = st.sidebar.text_input("Target Function f(x)", value="x")
num_terms = st.sidebar.slider("Number of Terms (N)", min_value=1, max_value=30, value=5)

# Use caching so heavy symbolic math does not freeze Streamlit Cloud on startup
@st.cache_data
def calculate_fourier(f_expr_str, N_terms):
    try:
        x = sp.Symbol('x')
        f_expr = sp.sympify(f_expr_str)
        
        # Compute a0, an, bn over [-pi, pi]
        a0 = (1 / sp.pi) * sp.integrate(f_expr, (x, -sp.pi, sp.pi))
        
        terms = []
        for n in range(1, N_terms + 1):
            an = (1 / sp.pi) * sp.integrate(f_expr * sp.cos(n * x), (x, -sp.pi, sp.pi))
            bn = (1 / sp.pi) * sp.integrate(f_expr * sp.sin(n * x), (x, -sp.pi, sp.pi))
            terms.append((an, bn))
            
        return float(a0), terms, None
    except Exception as e:
        return 0, [], str(e)

# Run calculation
a0, terms, error = calculate_fourier(func_str, num_terms)

if error:
    st.error(f"Error parsing or integrating function: {error}")
else:
    # Evaluate numerical values for plot
    x_vals = np.linspace(-np.pi, np.pi, 1000)
    
    # Base DC component
    y_vals = np.full_like(x_vals, a0 / 2.0)
    
    for n, (an, bn) in enumerate(terms, start=1):
        y_vals += float(an) * np.cos(n * x_vals) + float(bn) * np.sin(n * x_vals)
    
    # Plot results
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label=f"Fourier Approximation (N={num_terms})", color="crimson")
    ax.grid(True)
    ax.legend()
    
    st.pyplot(fig)
