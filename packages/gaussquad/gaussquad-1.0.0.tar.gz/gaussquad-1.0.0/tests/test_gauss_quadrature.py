import numpy as np
import pytest
from scipy.integrate import quad

from gaussquad.gauss_quadrature import wquad_nodes_weights


def test_gauss_quadrature_exact_constant_weight_x_squared():
    weight_fn = lambda x: np.ones_like(x)
    interval = (-1, 1)
    degree = 2

    nodes, weights = wquad_nodes_weights(
        weight_fn=weight_fn,
        interval=interval,
        degree=degree,
        moment_method="exact",
        verbose=True
    )
    result = np.sum(weights * nodes**2)
    expected, _ = quad(lambda x: x**2 * weight_fn(x), *interval)
    assert np.isclose(result, expected, atol=1e-8)


def test_gauss_quadrature_legendre_constant_weight_x_cubed():
    weight_fn = lambda x: np.ones_like(x)
    interval = (-2, 5)
    degree = 3

    nodes, weights = wquad_nodes_weights(
        weight_fn=weight_fn,
        interval=interval,
        degree=degree,
        moment_method="legendre",
        moment_degree=6,
        verbose=True
    )
    result = np.sum(weights * nodes**3)
    expected, _ = quad(lambda x: x**3 * weight_fn(x), *interval)
    assert np.isclose(result, expected, atol=1e-8)


def test_gauss_quadrature_exponential_weight():
    weight_fn = lambda x: np.exp(-x)
    interval = (-4, 0)
    degree = 3

    nodes, weights = wquad_nodes_weights(
        weight_fn=weight_fn,
        interval=interval,
        degree=degree,
        moment_method="legendre",
        moment_degree=6,
        verbose=True
    )
    result = np.sum(weights * nodes**2)
    expected, _ = quad(lambda x: x**2 * weight_fn(x), *interval)
    assert np.isclose(result, expected, atol=1e-5)


def test_invalid_hankel_due_to_nan_weights():
    bad_weight_fn = lambda x: np.full_like(x, np.nan)
    with pytest.raises(ValueError, match="(positive-definite|infs or NaNs)"):
        wquad_nodes_weights(bad_weight_fn, (-1, 1), degree=3, moment_method="legendre", moment_degree=6)


def test_invalid_moment_method_type():
    with pytest.raises(TypeError, match="string or callable"):
        wquad_nodes_weights(lambda x: x, (-1, 1), 3, moment_method=123)


def test_invalid_moment_degree_too_low():
    with pytest.raises(ValueError, match="must be an integer ≥ degree"):
        wquad_nodes_weights(lambda x: x, (-1, 1), 4, moment_method="legendre", moment_degree=3)