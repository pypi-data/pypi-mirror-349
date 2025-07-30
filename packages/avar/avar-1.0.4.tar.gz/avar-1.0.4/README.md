[![PyPI Downloads](https://img.shields.io/pypi/dm/avar.svg?label=PyPI%20downloads)](https://pypi.org/project/avar/)

# Allan Variance Tools

The `avar` library provides tools for Allan variance analysis, a statistical
method used to quantify the stability of time series data, particularly in the
context of noise characterization for signals. The library includes functions to
compute Allan variances, generate various types of noise, and interactively fit
Allan variance curves. It is built using Python with dependencies on NumPy,
Matplotlib, and SciPy.

## Window Generation

```python
M = avar.windows(K, min_size=1, density=64)
```

Generates an array of integer averaging window sizes for Allan variance
analysis. It creates logarithmically spaced window sizes between `min_size` and
`K/2`, with approximately `density` sizes per decade. It ensures unique integer
values.

## Allan Variance Calculation

```python
va = avar.variance(y, M)
```

Computes Allan variance for a time series `y` over specified window sizes `M`.
Supports both 1D arrays (single time series) and 2D arrays (multiple time
series). Uses cumulative sums to calculate variance efficiently, handling
overlapping windows.

## Ideal Allan Variance

```python
va = avar.ideal_variance(tau, ks, T=None)
```

Calculates theoretical Allan variance curves for various noise types. Supports
quantization, white, first-order Gauss-Markov (FOGM), Brownian, and ramp noises.
Parameter `ks` defines noise slopes and variances, and `T` specifies the
sampling period (required for FOGM).

## Noise Generation

The library provides functions to generate different types of noise, each with
specific statistical properties:

```python
y = avar.noise_quantization(var, T, K)
y = avar.noise_white(var, T, K)
y = avar.noise_fogm(var, tau, T, K, y0=None)
y = avar.noise_brownian(var, T, K)
y = avar.noise_ramp(var, T, K)
```

## Interactive Allan Variance Fitting

```python
avar.fit(
    tau: np.ndarray,
    va: np.ndarray,
    T: float = 1.0,
    ks: tuple | list | None = None,
    ax: axes = None,
    truecolor: str = "tab:blue",
    fitcolor: str = "tab:orange")
```

Provides an interactive Matplotlib-based interface for fitting Allan variance
curves. Displays true Allan variance (`va`) and fitted curves based on noise
components (`ks`).

Supports interactive manipulation via mouse and keyboard:

-   Left-click and drag: Move noise components.
-   Shift and left-click or middle-click: Pan the view.
-   Scroll: Zoom (faster with shift).
-   Keys 'q', 'w', 'f', 'b', 'r': Add quantization, white, FOGM, Brownian, or
    ramp noise components.
-   'Delete', 'backspace', or key 'x': Remove components.
-   Key 'o': Optimize component variances using least-squares fitting.
-   Key 'h': Reset view to the data limits.
-   Key '?': toggle the help menu.

Features log-log scaling, customizable colors, and optimization bounds for
fitting. Handles multiple noise types with specific slopes (-2 to +2) and
parameters (e.g., time constant for FOGM).
