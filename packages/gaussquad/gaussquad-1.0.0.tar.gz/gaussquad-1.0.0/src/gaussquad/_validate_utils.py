import numpy as np


def _validate_degree(degree: int) -> None:
    """
    Validate the degree of the polynomial.

    Parameters
    ----------
    degree : int
        The degree of the polynomial.

    Raises
    ------
    ValueError
        If the degree is not a positive integer.
    """
    if not isinstance(degree, int) or degree <= 0:
        raise ValueError("Degree must be a positive integer.")


def _validate_interval(interval: tuple) -> None:
    """
    Validate the interval.

    Parameters
    ----------
    interval : Tuple[float, float]
        The interval to validate.

    Raises
    ------
    ValueError
        If the interval is not a tuple of two finite numbers (a, b) with a < b.
    """
    if not isinstance(interval, (tuple, list)) or len(interval) != 2:
        raise ValueError(f"`interval` must be a tuple of (a, b), got {interval}.")
    a, b = interval
    if not (np.isfinite(a) and np.isfinite(b)):
        raise ValueError(f"Interval bounds must be finite, got {interval}.")
    if a >= b:
        raise ValueError(f"Interval must satisfy a < b, got a = {a}, b = {b}.")


def _validate_fn(fn: callable, interval: tuple) -> None:
    """
    Validate the weight function.

    Parameters
    ----------
    fn : Callable[[np.ndarray], np.ndarray]
        The function to validate.

    Raises
    ------
    TypeError
        If `fn` is not callable.
    ValueError
        If `fn` does not return a NumPy array when called with test input.
    """
    if not callable(fn):
        raise TypeError("`fn` must be callable.")
    try:
        a, b = interval
        test_input = np.linspace(a, b, 5)
        test_output = fn(test_input)
        if not isinstance(test_output, np.ndarray):
            raise TypeError("`fn` must return a NumPy array.")
    except Exception as e:
        raise ValueError(f"`fn` failed when called on test input: {e}")


def _validate_moment_method(moment_method: str) -> None:
    """
    Validate the moment method.

    Parameters
    ----------
    moment_method : Optional[Union[str, Callable]]
        The moment method to validate.

    Raises
    ------
    TypeError
        If `moment_method` is not a string or callable.
    """
    if not isinstance(moment_method, str) and not callable(moment_method):
        raise TypeError(f"`moment_method` must be a string or callable, got {type(moment_method)}.")


def _validate_moment_degree(moment_degree: int, degree: int) -> None:
    """
    Validate the moment degree.

    Parameters
    ----------
    moment_degree : int
         The degree of the quadrature rule used to compute the moments.
    degree : int
         The degree of the quadrature.

    Raises
    ------
    ValueError
        If `moment_degree` is not an integer or is less than `degree`.
    """
    if moment_degree is None:
        return
    if not isinstance(moment_degree, int) or moment_degree < degree:
        raise ValueError(
            f"`moment_degree` must be an integer ≥ degree ({degree}), got {moment_degree}."
        )
