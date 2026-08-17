# Fourier Series Coefficient Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://<your-app-name>.streamlit.app)

Click the badge above or visit [our live demo](https://<your-app-name>.streamlit.app) to interact with the Fourier Series Explorer online!
# fourier-series-explorer
To learn how Fourier Series Coefficients works to build a function

Here is a complete, publication-ready `README.md` template tailored specifically for your Streamlit app. You can copy and paste this directly into your GitHub repository.

---

# 🌊 Fourier Series Coefficient Explorer

An interactive, educational web application built with **Streamlit**, **Matplotlib**, and **SymPy** to help students and instructors visualize real-time Fourier series synthesis. Manipulate individual harmonic coefficients ($a_0, a_n, b_n$) and observe how trigonometric polynomial sums converge to approximate arbitrary target functions $f(x)$.

---

## 📌 Features

* **Bi-Directional Synchronized Controls:** Adjust harmonic amplitudes seamlessly via dual-linked sliders and 4-decimal-precision numeric input boxes.
* **Flexible Domain Intervals:** Explore standard intervals ($[-\pi, \pi]$, $[0, 2\pi]$) or define arbitrary custom boundaries $[a, b]$.
* **Harmonic Selection Modes:** Toggle between **All** ($1, 2, 3\dots$), **Odd** ($1, 3, 5\dots$), or **Even** ($2, 4, 6\dots$) harmonic modes to observe symmetry behavior (e.g., square or sawtooth wave constructions).
* **Multi-Panel Grid Layout:**
* **Top Panel:** Main comparison grid plotting the constructed Fourier sum $S(x)$ against the target signal $f(x)$.
* **Bottom Panels:** Side-by-side grids detailing the isolated Cosine and Sine constituent harmonic components.



---

## 🧮 Mathematical Background

A real-valued function $f(x)$ integrable on an interval $[a, b]$ with fundamental period $T = b - a$ and fundamental frequency $\omega_0 = \frac{2\pi}{T}$ can be represented by its Fourier series expansion:

$$S(x) = \frac{a_0}{2} + \sum_{n=1}^{N_{cos}} a_n \cos(n \omega_0 x) + \sum_{n=1}^{N_{sin}} b_n \sin(n \omega_0 x)$$

### Coefficient Definitions

* **DC Component ($a_0$):** Twice the mean value of the signal over one period:
$$a_0 = \frac{2}{T} \int_{a}^{b} f(x) \, dx$$


* **Cosine Amplitudes ($a_n$):** Even symmetry harmonic weights:
$$a_n = \frac{2}{T} \int_{a}^{b} f(x) \cos(n \omega_0 x) \, dx$$


* **Sine Amplitudes ($b_n$):** Odd symmetry harmonic weights:
$$b_n = \frac{2}{T} \int_{a}^{b} f(x) \sin(n \omega_0 x) \, dx$$



---

## 🚀 Quickstart & Local Installation

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fourier-series-explorer.git
cd fourier-series-explorer

```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

Create a `requirements.txt` file (or use the one in the repository) with the following dependencies:

```text
streamlit
numpy
matplotlib
sympy

```

Then install them using `pip`:

```bash
pip install -r requirements.txt

```

### 4. Run the Streamlit App Locally

```bash
streamlit run app.py

```

The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📖 User Guidelines & Instructions

1. **Define the Target Signal:**
* Enter a valid mathematical expression for $f(x)$ in the sidebar (e.g., `x`, `x**2`, `sin(x)`, `abs(x)`).
* Select a predefined interval or select **Custom...** to enter your own $[a, b]$ domain.


2. **Configure Harmonic Terms:**
* Set the maximum number of cosine ($N_{cos}$) and sine ($N_{sin}$) terms (up to 10 each).
* Choose harmonic modes (**All**, **Odd**, or **Even**) to restrict non-zero indices.


3. **Adjust Amplitudes:**
* Use the **Sliders** or type precise values up to **4 decimal places** in the adjacent text boxes.
* Observe how setting specific coefficients to zero illustrates wave symmetry:
* **Odd functions** $f(-x) = -f(x)$ require only Sine terms ($b_n$).
* **Even functions** $f(-x) = f(x)$ require only Cosine terms ($a_n$ and $a_0$).





---

## 🛠️ Project Structure

```text
fourier-series-explorer/
│
├── app.py              # Main Streamlit application logic & Matplotlib rendering
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation and guidelines
└── LICENSE             # MIT License

```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/your-username/fourier-series-explorer/issues).

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
