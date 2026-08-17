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
# Fully Synchronized Control Component (With Individual & Master Lock)
# ---------------------------------------------------------------------
def create_synced_control(label_prefix, var_name, master_locked=False):
    state_key = f"val_{var_name}"
    slider_key = f"slider_{var_name}"
    num_key = f"num_{var_name}"
    lock_key = f"lock_{var_name}"

    # Initialize master value state
    if state_key not in st.session_state:
        st.session_state[state_key] = 0.0000

    # Initialize individual lock state (unlocked by default)
    if lock_key not in st.session_state:
        st.session_state[lock_key] = False

    # A control is disabled if either the Master Lock or its Individual Lock is active
    is_disabled = master_locked or st.session_state[lock_key]

    # Sync Master State -> Widget Keys
    st.session_state[slider_key] = round(float(st.session_state[state_key]), 4)
    st.session_state[num_key] = round(float(st.session_state[state_key]), 4)

    def sync_from_slider():
        st.session_state[state_key] = round(st.session_state[slider_key], 4)

    def sync_from_num():
        st.session_state[state_key] = round(st.session_state[num_key], 4)

    def set_to_zero():
        st.session_state[state_key] = 0.0000

    def toggle_individual_lock():
        st.session_state[lock_key] = not st.session_state[lock_key]

    # Row Layout: Slider (2.8), Number Box (1.2), Lock Toggle (0.6), Zero Button (0.6)
    c_s, c_n, c_l, c_z = st.sidebar.columns([2.8, 1.2, 0.6, 0.6])
    
    with c_s:
        st.slider(
            label_prefix,
            min_value=-5.0,
            max_value=5.0,
            step=0.0001,
            format="%.4f",
            key=slider_key,
            on_change=sync_from_slider,
            disabled=is_disabled
        )
    with c_n:
        st.number_input(
            f"{label_prefix} val",
            min_value=-5.0,
            max_value=5.0,
            step=0.0001,
            format="%.4f",
            key=num_key,
            on_change=sync_from_num,
            label_visibility="collapsed",
            disabled=is_disabled
        )
    with c_l:
        lock_icon = "🔒" if st.session_state[lock_key] else "🔓"
        st.button(
            lock_icon,
            key=f"btn_lock_{var_name}",
            on_click=toggle_individual_lock,
            help=f"Toggle lock for {label_prefix}",
            disabled=master_locked
        )
    with c_z:
        st.button(
            "0",
            key=f"zero_{var_name}",
            on_click=set_to_zero,
            help=f"Set {label_prefix} to 0.0000",
            disabled=is_disabled
        )

    return round(float(st.session_state[state_key]), 4)

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

# Checkbox to hide/show interval background shade
show_interval_shade = st.sidebar.checkbox("Highlight Active Interval Zone", value=False)

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

# Master Lock toggle
master_lock = st.sidebar.checkbox("🔒 Lock ALL Coefficients (Master Lock)", value=False)

# Global Reset Button
def reset_all_coefficients():
    for key in list(st.session_state.keys()):
        if key.startswith("val_"):
            st.session_state[key] = 0.0000

st.sidebar.button("🧹 Set ALL Coefficients to 0.0000", on_click=reset_all_coefficients, disabled=master_lock)

st.sidebar.markdown("---")

# DC Component (a0)
a0 = create_synced_control("a₀", "a0", master_locked=master_lock)

# Cosine Coefficients
a_vals = []
st.sidebar.markdown("**Cosine Coefficients ($a_n$)**")
for i in range(1, n_cos + 1):
    val = create_synced_control(f"a_{i}", f"a_{i}", master_locked=master_lock)
    a_vals.append(val)

# Sine Coefficients
b_vals = []
st.sidebar.markdown("**Sine Coefficients ($b_n$)**")
for i in range(1, n_sin + 1):
    val = create_synced_control(f"b_{i}", f"b_{i}", master_locked=master_lock)
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

def style_axis_interval(ax, title):
    ax.set_title(title, fontsize=10, fontweight='bold')
    
    if show_interval_shade:
        ax.axvspan(a_bound, b_bound, color='yellow', alpha=0.15, zorder=0, label="Active Interval")
    
    ax.axvline(a_bound, color='gray', linestyle='--', linewidth=1)
    ax.axvline(b_bound, color='gray', linestyle='--', linewidth=1)
    ax.axvline(0, color='black', linestyle='-', linewidth=1.2, alpha=0.75, zorder=2)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_ylabel("Amp", fontsize=8)

# 1. Total Combined Signal Grid
fig_total, ax_total = plt.subplots(figsize=(9, 2.8))
style_axis_interval(ax_total, "1. Total Combined Signal Approximation vs Target")
if y_target is not None and not np.iscomplexobj(y_target):
    ax_total.plot(x_plot, y_target, color='black', linestyle='--', linewidth=1.6, label="Target f(x)")
    ax_total.set_ylim(y_min, y_max)
ax_total.plot(x_plot, total_fourier, color='crimson', linewidth=2.0, label="Constructed S(x)")
ax_total.legend(loc="upper right", fontsize=8)
plt.tight_layout()
st.pyplot(fig_total)

# 2 & 3. Cosine and Sine Harmonics Grids Side-by-Side
col_cos_plot, col_sin_plot = st.columns(2)

with col_cos_plot:
    fig_cos, ax_cos = plt.subplots(figsize=(4.5, 3.2))
    style_axis_interval(ax_cos, f"2. Cosine Harmonics ({n_cos} Terms)")
    for i in range(n_cos):
        ax_cos.plot(x_plot, cos_terms[i], linestyle=':', color=colors[i], alpha=0.85, label=f"a_{i+1}")
    ax_cos.plot(x_plot, cos_sum, color='royalblue', linewidth=1.8, label="a₀/2 + Cos Sum")
    ax_cos.set_xlabel("x", fontsize=8)
    ax_cos.legend(loc="upper right", fontsize=7, ncol=2)
    plt.tight_layout()
    st.pyplot(fig_cos)

with col_sin_plot:
    fig_sin, ax_sin = plt.subplots(figsize=(4.5, 3.2))
    style_axis_interval(ax_sin, f"3. Sine Harmonics ({n_sin} Terms)")
    for i in range(n_sin):
        ax_sin.plot(x_plot, sin_terms[i], linestyle=':', color=colors[i], alpha=0.85, label=f"b_{i+1}")
    ax_sin.plot(x_plot, sin_sum, color='darkorange', linewidth=1.8, label="Sine Sum")
    ax_sin.set_xlabel("x", fontsize=8)
    ax_sin.legend(loc="upper right", fontsize=7, ncol=2)
    plt.tight_layout()
    st.pyplot(fig_sin)
