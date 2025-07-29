# File: src/gaussquad/gauss_quadrature.py

import numpy as np
from scipy.linalg import eigh_tridiagonal
from ._moments import compute_moments
from ._validate_utils import (
    _validate_fn,
    _validate_degree,
    _validate_moment_method,
    _validate_moment_degree,
)
from ._logging_utils import logger, logging_context

__all__ = ["wquad", "wquad_nodes_weights"]


def wquad(
    fn, weight_fn, interval, degree, moment_method="legendre", moment_degree=None, verbose=False
) -> float:
    """
    Approximate the integral of a weighted function
    defined on a finite interval
    by computing the quadrature nodes and weights
    using the Golub–Welsch algorithm
    (see `Golub & Welsch, 1967
    <http://i.stanford.edu/pub/cstr/reports/cs/tr/67/81/CS-TR-67-81.pdf>`_).

    Parameters
    ----------
    fn: Callable[[np.ndarray], np.ndarray]
        The function to integrate f(x), must be vectorized.
    weight_fn: Callable[[np.ndarray], np.ndarray]
        The weight function w(x), must be vectorized.
    interval: Tuple[float, float]
        The finite integration bounds (a, b).
    degree: int
        The number of nodes and weights for the quadrature.
    moment_method: Optional[Union[str, Callable]]
        Optional custom method to compute the k-th moment.
        If None, defaults to "legendre" for Gauss-Legendre.
    moment_degree: Optional[int]
        The degree of the quadrature rule used to compute the moments.
        If None, defaults to 2 * degree.
    verbose: Optional[bool]
        If True, enables verbose logging.
        If None, defaults to False.

    Returns
    -------
    result: float
        The computed integral of the weighted function.

    Raises
    -------
    ValueError
        If the moment Hankel matrix is not positive-definite.
    ValueError
        If any of the input parameters are invalid.
    TypeError
        If any of the input parameters are of the wrong type.

    Examples
    --------
    >>> import numpy as np
    >>> from gaussquad import wquad
    >>> result = wquad(
    ...     fn=lambda x: x**2,
    ...     weight_fn=lambda x: np.ones_like(x),
    ...     interval=(0, 1),
    ...     degree=3,
    ...     moment_method="exact"
    ... )  # --> 0.3333333333333335
    """
    _validate_fn(fn, interval)

    nodes, weights = wquad_nodes_weights(
        weight_fn,
        interval,
        degree,
        moment_method=moment_method,
        moment_degree=moment_degree,
        verbose=verbose,
    )
    result = np.sum(weights * fn(nodes))
    logger.debug("Computed integral:\n%s", result)
    return result


def wquad_nodes_weights(
    weight_fn, interval, degree, moment_method="legendre", moment_degree=None, verbose=False
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute general-purpose Gauss quadrature nodes and weights
    defined on a finite interval using the Golub–Welsch algorithm
    (see `Golub & Welsch, 1967
    <http://i.stanford.edu/pub/cstr/reports/cs/tr/67/81/CS-TR-67-81.pdf>`_).

    Parameters
    ----------
    weight_fn: Callable[[np.ndarray], np.ndarray]
        The weight function w(x), must be vectorized.
    interval: Tuple[float, float]
        The finite integration bounds (a, b).
    degree: int
        The number of nodes and weights for the quadrature.
    moment_method: Optional[Union[str, Callable]]
        Optional custom method to compute the k-th moment.
        If None, defaults to "legendre" for Gauss-Legendre.
    moment_degree: Optional[int]
        The degree of the quadrature rule used to compute the moments.
        If None, defaults to 2 * degree.
    verbose: Optional[bool]
        If True, enables verbose logging.
        If None, defaults to False.

    Returns
    -------
    nodes: np.ndarray
        The quadrature nodes.
    weights: np.ndarray
        The quadrature weights.

    Raises
    -------
    ValueError
        If the moment Hankel matrix is not positive-definite.
    ValueError
        If any of the input parameters are invalid.
    TypeError
        If any of the input parameters are of the wrong type.

    Examples
    --------
    >>> import numpy as np
    >>> from gaussquad import wquad_nodes_weights
    >>> nodes, weights = wquad_nodes_weights(
    ...     weight_fn=lambda x: np.ones_like(x),
    ...     interval=(0, 1),
    ...     degree=3,
    ...     moment_method="exact",
    ... )  # --> [-1.04471955,  0.23701648,  0.80770307], [0.00101608, 0.53588233, 0.46310159]
    """
    _validate_degree(degree)
    _validate_moment_method(moment_method)

    with logging_context(verbose):

        moment_degree = 2 * degree if moment_degree is None else moment_degree

        moments = _compute_moments(weight_fn, interval, degree, moment_method, moment_degree)
        logger.debug("Computed moments:\n%s", moments)
        hankel = _compute_hankel(moments, degree)
        logger.debug("Hankel matrix:\n%s", hankel)

        try:
            lower_cholesky = np.linalg.cholesky(hankel)
        except np.linalg.LinAlgError:
            raise ValueError(
                "Moment Hankel matrix is not positive-definite. "
                "Check the weight function, interval, or degree (it may be too high)."
            )

        upper_cholesky = lower_cholesky.T
        logger.debug("Upper Cholesky factor:\n%s", upper_cholesky)

        alpha, beta = _compute_coefficients(upper_cholesky, degree)
        logger.debug("Alpha coefficients:\n%s", alpha)
        logger.debug("Beta coefficients:\n%s", beta)

        nodes, vecs = eigh_tridiagonal(alpha, beta)
        logger.debug("Eigenvalues (nodes):\n%s", nodes)
        logger.debug("Eigenvectors:\n%s", vecs)

        weights = moments[0] * vecs[0] ** 2
        logger.debug("Weights:\n%s", weights)

        return nodes, weights


def _compute_moments(weight_fn, interval, degree, moment_method, moment_degree) -> np.ndarray:
    """
    Compute the moments of the weight function using the specified method.

    Parameters
    ----------
    weight_fn: Callable[[np.ndarray], np.ndarray]
        The weight function w(x), must be vectorized.
    interval: Tuple[float, float]
        The finite integration bounds (a, b).
    degree: int
        The number of nodes and weights for the quadrature.
    moment_method: Union[str, Callable]
        The method to compute the moments.
        If a string, it must be one of the predefined methods.
    moment_degree: int
        The degree of the quadrature rule used to compute the moments.

    Returns
    -------
    moments: np.ndarray
        The computed moments.

    Raises
    -------
    TypeError
        If the moment method is not a string or callable.
    ValueError
        If `moment_degree` is not an integer or is less than `degree`.
    """
    nr_moments = 2 * degree + 1
    if isinstance(moment_method, str):
        _validate_moment_degree(moment_degree, degree)
        return compute_moments(moment_method, nr_moments, weight_fn, interval, degree=moment_degree)
    elif callable(moment_method):
        return moment_method(nr_moments, weight_fn, interval, moment_degree)
    else:
        raise TypeError("`moment_method` must be a string or callable")


def _compute_hankel(moments, degree) -> np.ndarray:
    """
    Compute the Hankel matrix from the moments.

    Parameters
    ----------
    moments: np.ndarray
        The computed moments.
    degree: int
        The degree of the quadrature.

    Returns
    -------
    hankel: np.ndarray
        The Hankel matrix.

    Raises
    -------
    ValueError
        If the number of moments is less than `2 * degree + 1`.
    """
    if len(moments) < 2 * degree + 1:
        raise ValueError(f"Expected at least {2 * degree + 1} moments, got {len(moments)}.")

    hankel = np.empty((degree + 1, degree + 1))
    for i in range(degree + 1):
        for j in range(degree + 1):
            hankel[i, j] = moments[i + j]
    return hankel


def _compute_coefficients(coefs, degree) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the coefficients for the tridiagonal matrix from the Cholesky factorization.

    Parameters
    ----------
    coefs: np.ndarray
        The Cholesky factorization of the Hankel matrix (coefficients for the polynomials).
    degree: int
        The degree of the quadrature.

    Returns
    -------
    alpha: np.ndarray
        The alpha coefficients for the tridiagonal matrix (diagonal elements).
    beta: np.ndarray
        The beta coefficients for the tridiagonal matrix (off-diagonal elements).
    """
    alpha = np.zeros(degree)
    beta = np.zeros(degree - 1)

    for i in range(degree):
        prev_prev = coefs[i - 1, i - 1] if i > 0 else 1
        prev_i = coefs[i - 1, i] if i > 0 else 0
        i_next = coefs[i, i + 1] if i + 1 < degree else 0
        alpha[i] = i_next / coefs[i, i] - prev_i / prev_prev

        if i < degree - 1:
            beta[i] = coefs[i + 1, i + 1] / coefs[i, i]

    return alpha, beta
