import numpy as np
import pytest
from gaussquad._moments import compute_moments

from scipy.integrate import quad


def test_legendre_moments_exp_weight():
    weight_fn = lambda x: x**2 + 1
    interval = (-3, 5)
    degree = 6
    nr_moments = 5

    computed = compute_moments(
        method="legendre",
        nr_moments=nr_moments,
        weight_fn=weight_fn,
        interval=interval,
        degree=degree
    )

    expected = []
    for k in range(nr_moments):
        integrand = lambda x: (x ** k) * weight_fn(x)
        moment, _ = quad(integrand, *interval)
        expected.append(moment)

    np.testing.assert_allclose(computed, expected, rtol=1e-6, atol=1e-8)


def test_invalid_interval_not_tuple():
    with pytest.raises(ValueError, match="tuple"):
        compute_moments("legendre", 3, lambda x: x, interval=[-1], degree=3)


def test_invalid_interval_nonfinite():
    with pytest.raises(ValueError, match="finite"):
        compute_moments("legendre", 3, lambda x: x, interval=(-np.inf, 1), degree=3)


def test_invalid_interval_order():
    with pytest.raises(ValueError, match="a < b"):
        compute_moments("legendre", 3, lambda x: x, interval=(1, 0), degree=3)


def test_invalid_weight_fn_type():
    with pytest.raises(TypeError, match="callable"):
        compute_moments("legendre", 3, weight_fn="not_callable", interval=(0, 1), degree=3)


def test_invalid_weight_fn_output_type():
    def bad_fn(x):
        return 42  # not a NumPy array

    with pytest.raises(ValueError, match="return a NumPy array"):
        compute_moments("legendre", 3, weight_fn=bad_fn, interval=(0, 1), degree=3)


def test_moments_output_type_and_shape():
    weight_fn = lambda x: np.ones_like(x)
    result = compute_moments("legendre", 5, weight_fn, (-1, 1), degree=6)
    assert isinstance(result, np.ndarray)
    assert result.shape == (5,)