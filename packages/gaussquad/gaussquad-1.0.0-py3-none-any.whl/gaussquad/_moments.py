import numpy as np

from ._validate_utils import _validate_interval, _validate_fn


def compute_moments(method, nr_moments, weight_fn, interval, **kwargs):
    """
    Compute moments using a specified method.

    Parameters
    ----------
    method : str
        'legendre' or 'exact'.
    nr_moments : int
        Number of moments to compute.
    weight_fn : Callable[[np.ndarray], np.ndarray]
        Weight function to integrate.
    interval : Tuple[float, float]
        Integration bounds (a, b).
    kwargs : dict
        Additional arguments for the method (e.g., degree for 'legendre').

    Returns
    -------
    moments : np.ndarray
        The computed moments.

    Raises
    -------
    ValueError
        If required arguments are missing or invalid.
    NotImplementedError
        If the specified method is not implemented.
    """
    if method == "exact":
        return _compute_exact_moments(nr_moments, weight_fn, interval)
    if method == "legendre":
        if "degree" not in kwargs:
            raise ValueError("The `degree` argument is required for 'legendre' method.")
        return _compute_legendre_moments(nr_moments, weight_fn, interval, kwargs["degree"])
    else:
        raise NotImplementedError(f"Unknown moment method '{method}'.")


def _compute_exact_moments(nr_moments, weight_fn, interval):
    """
    Compute exact moments for a constant weight function.

    Parameters
    ----------
    nr_moments : int
        Number of moments to compute.
    weight_fn : Callable[[np.ndarray], np.ndarray]
        Weight function to integrate.
    interval : Tuple[float, float]
        Integration bounds (a, b).

    Returns
    -------
    moments : np.ndarray
        The computed moments.

    Raises
    -------
    ValueError
        If the interval is not a tuple of two finite numbers (a, b) with a < b.
    ValueError
        If the weight function is not constant over the interval.
    TypeError
        If `weight_fn` is not callable.
    ValueError
        If `weight_fn` does not return a NumPy array when called with test input.
    """
    _validate_interval(interval)
    _validate_fn(weight_fn, interval)

    a, b = interval
    if not np.allclose(weight_fn(a), weight_fn(b)):
        raise ValueError("Weight function must be constant over interval for exact moments.")

    const = weight_fn(a)
    ks = np.arange(1, nr_moments + 1)
    return const * ((b**ks - a**ks) / ks)


def _compute_legendre_moments(nr_moments, weight_fn, interval, degree):
    """
    Compute moments using Legendre-Gauss quadrature.

    Parameters
    ----------
    nr_moments : int
        Number of moments to compute.
    weight_fn : Callable[[np.ndarray], np.ndarray]
        Weight function to integrate.
    interval : Tuple[float, float]
        Integration bounds (a, b).
    degree : int
        Degree of the quadrature rule.

    Returns
    -------
    moments : np.ndarray
        The computed moments.

    Raises
    -------
    ValueError
        If the interval is not a tuple of two finite numbers (a, b) with a < b.
    TypeError
        If `weight_fn` is not callable.
    ValueError
        If `weight_fn` does not return a NumPy array when called with test input.
    """
    _validate_interval(interval)
    _validate_fn(weight_fn, interval)

    a, b = interval
    x, w = np.polynomial.legendre.leggauss(degree)
    scale = 0.5 * (b - a)
    shift = 0.5 * (a + b)
    x_mapped = scale * x + shift

    moments = np.zeros(nr_moments)
    for k in range(nr_moments):
        integrand = (x_mapped**k) * weight_fn(x_mapped)
        moments[k] = scale * np.sum(w * integrand)

    return moments
