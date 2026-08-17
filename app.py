import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Page configuration
st.set_page_config(
    page_title="Fourier Series Coefficient Explorer",
    layout="wide"
)

st.title("Fourier Series Coefficient Explorer")
st.markdown("""
Adjust the Fourier coefficients ($a_0$, $a_n$, $b_n$) and domain settings in the sidebar to see how individual harmonics sum up to approximate the target signal $f(x)$.
""")

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------
def parse_interval(interval_str):
    try:
        s = interval_str.replace(" ", "").replace("\\pi", "pi").replace("π", "pi")
        s = s.strip("()[]")
        parts = s.split(",")
        a_val = float(sp.sympify(parts[0]))
        b_val = float(sp.sympify(parts[1]))
        if a_val < b_val:
            return a_val, b_val
    except Exception:
        pass
    return -np.pi, np.pi

def get_multipliers(mode, count):
    if mode == "odd":
        return [2 * i - 1 for i in range(1, count + 1)]
    if mode == "even":
        return [2 * i for i in range(1, count + 1)]
    return [i for i in range(1, count + 1)]

# ---------------------------------------------------------------------
# Fully Synchronized Control Component
# ---------------------------------------------------------------------
def create_synced_control(label_prefix, var_name):
    """
    Creates a slider and number input linked to a single unified Session State variable.
    """
    state_key = f"val_{var_name}"
    slider_key = f"slider_{var_name}"
    num_key = f"num_{var_name}"

    # Initialize master state value if missing
    if state_key not in st.session_state:
        st.session_state[state_key] = 0.0

    # Sync Master State -> Widget Keys before rendering
    st.session_state[slider_key] = float(st.session_state[state_key])
    st.session_state[num_key] = float(st.session_state[state_key])

    # Callbacks to keep master state updated
    def sync_from_slider():
        st.session_state[state_key] = st.session_state[slider_key]

    def sync_from_num():
        st.session_state[state_key] = st.session_state[num_key]

    c_s, c_n = st.sidebar.columns([3, 1])
    with c_s:
        st.slider(
            label_prefix,
            min_value=-5.0,
            max_value=5.0,
            step=0.0001,
            key=slider_key,
            on_change=sync_from_slider
        )
    with c_n:
        st.number_input(
            f"{label_prefix} val",
            min_value=-5.0,
            max_value=5.0,
            step=0.0001,
            key=num_key,
            on_change=sync_from_num,
            label_visibility="collapsed"
        )

    return float(st.session_state[state_key])

# ---------------------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------------------
st.sidebar.header("1. Target Signal & Interval")

func_str = st.sidebar.text_input(
    "Target f(x):", 
    value="x", 
    help="e.g. x, x**2, sin(x), abs(x)"
)

interval_choice = st.sidebar.selectbox(
    "Interval:",
    options=["(-π, π)", "(0, 2π)", "(-1, 1)", "(0, 1)", "(0, 2)", "Custom..."],
    index=0
)

if interval_choice == "Custom...":
    custom_int_str = st.sidebar.text_input("Custom [a, b]:", value="-pi, pi")
elif interval_choice == "(-π, π)":
    custom_int_str = "-pi, pi"
elif interval_choice == "(0, 2π)":
    custom_int_str = "0, 2*pi"
else:
    custom_int_str = interval_choice.replace("(", "").replace(")", "")

a_bound, b_bound = parse_interval(custom_int_str)

st.sidebar.markdown("---")
st.sidebar.header("2. Number of Terms & Modes")

col_terms1, col_terms2 = st.sidebar.columns(2)
with col_terms1:
    n_cos = st.number_input("Cos Terms:", min_value=1, max_value=10, value=5, step=1)
    c_mode = st.selectbox("Cos Mode:", options=["all", "odd", "even"], format_func=lambda x: f"{x.capitalize()} (1,2,3...)" if x=="all" else (f"{x.capitalize()} (1,3,5...)" if x=="odd" else f"{x.capitalize()} (2,4,6...)"))

with col_terms2:
    n_sin = st.number_input("Sin Terms:", min_value=1, max_value=10, value=5, step=1)
    s_mode = st.selectbox("Sin Mode:", options=["all", "odd", "even"], format_func=lambda x: f"{x.capitalize()} (1,2,3...)" if x=="all" else (f"{x.capitalize()} (1,3,5...)" if x=="odd" else f"{x.capitalize()} (2,4,6...)"))

st.sidebar.markdown("---")
st.sidebar.header("3. Coefficient Controls")

# DC Component (a0)
a0 = create_synced_control("a₀", "a0")

# Cosine Coefficients
a_vals = []
st.sidebar.markdown("**Cosine Coefficients ($a_n$)**")
for i in range(1, n_cos + 1):
    val = create_synced_control(f"a_{i}", f"a_{i}")
    a_vals.append(val)

# Sine Coefficients
b_vals = []
st.sidebar.markdown("**Sine Coefficients ($b_n$)**")
for i in range(1, n_sin + 1):
    val = create_synced_control(f"b_{i}", f"b_{i}")
    b_vals.append(val)

# ---------------------------------------------------------------------
# Math Computation & Signal Generation
# ---------------------------------------------------------------------
margin = (b_bound - a_bound) * 0.15
x_plot = np.linspace(a_bound - margin, b_bound + margin, 1000)
x_in_interval = np.linspace(a_bound, b_bound, 500)

T = b_bound - a_bound
w0 = 2 * np.pi / T

a_mults = get_multipliers(c_mode, n_cos)
b_mults = get_multipliers(s_mode, n_sin)

cos_terms = [a_vals[i] * np.cos(a_mults[i] * w0 * x_plot) for i in range(n_cos)]
sin_terms = [b_vals[i] * np.sin(b_mults[i] * w0 * x_plot) for i in range(n_sin)]

cos_sum = np.full_like(x_plot, a0 / 2.0) + (np.sum(cos_terms, axis=0) if n_cos > 0 else 0)
sin_sum = np.sum(sin_terms, axis=0) if n_sin > 0 else np.zeros_like(x_plot)
total_fourier = cos_sum + sin_sum

# Target Function Parser
y_target = None
y_min, y_max = -2.0, 2.0
try:
    expr_clean = func_str.strip().replace("\\left", "").replace("\\right", "").replace("\\sin", "sin").replace("\\cos", "cos")
    x_sym = sp.Symbol('x')
    sym_expr = sp.sympify(expr_clean)
    func = sp.lambdify(x_sym, sym_expr, modules=["numpy", "sympy"])

    y_target = func(x_plot)
    y_target_in = func(x_in_interval)

    if np.isscalar(y_target):
        y_target = np.full_like(x_plot, y_target)
        y_target_in = np.full_like(x_in_interval, y_target_in)

    target_min, target_max = np.nanmin(y_target_in), np.nanmax(y_target_in)
    y_range = max(target_max - target_min, 1.0)
    y_min = target_min - 0.45 * y_range
    y_max = target_max + 0.45 * y_range
except Exception:
    y_target = None

# ---------------------------------------------------------------------
# Rendering Plots
# ---------------------------------------------------------------------
colors = plt.cm.tab10(np.linspace(0, 1, 10))
fig, (ax_total, ax_cos, ax_sin) = plt.subplots(3, 1, figsize=(10, 11))

def style_axis_interval(ax, title):
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.axvspan(a_bound, b_bound, color='lightyellow', alpha=0.5, zorder=0, label="Active Interval")
    ax.axvline(a_bound, color='gray', linestyle='--', linewidth=1)
    ax.axvline(b_bound, color='gray', linestyle='--', linewidth=1)
    ax.axvline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.75, zorder=2)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_ylabel("Amp", fontsize=9)

# Plot 1: Combined Approximation
style_axis_interval(ax_total, "1. Total Combined Signal Approximation vs Target")
if y_target is not None and not np.iscomplexobj(y_target):
    ax_total.plot(x_plot, y_target, color='black', linestyle='--', linewidth=1.8, label="Target f(x)")
    ax_total.set_ylim(y_min, y_max)
ax_total.plot(x_plot, total_fourier, color='crimson', linewidth=2.2, label="Constructed S(x)")
ax_total.legend(loc="upper right", fontsize=8)

# Plot 2: Cosine Terms
style_axis_interval(ax_cos, f"2. Cosine Harmonics ({n_cos} Terms) over [{a_bound:.2f}, {b_bound:.2f}]")
for i in range(n_cos):
    ax_cos.plot(x_plot, cos_terms[i], linestyle=':', color=colors[i], alpha=0.85, label=f"a_{i+1} term")
ax_cos.plot(x_plot, cos_sum, color='royalblue', linewidth=2, label="a₀/2 + Cos Sum")
ax_cos.legend(loc="upper right", fontsize=8, ncol=2)

# Plot 3: Sine Terms
style_axis_interval(ax_sin, f"3. Sine Harmonics ({n_sin} Terms) over [{a_bound:.2f}, {b_bound:.2f}]")
for i in range(n_sin):
    ax_sin.plot(x_plot, sin_terms[i], linestyle=':', color=colors[i], alpha=0.85, label=f"b_{i+1} term")
ax_sin.plot(x_plot, sin_sum, color='darkorange', linewidth=2, label="Sine Sum")
ax_sin.set_xlabel("x", fontsize=9)
ax_sin.legend(loc="upper right", fontsize=8, ncol=2)

plt.tight_layout()
st.pyplot(fig)
