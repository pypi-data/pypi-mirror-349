import numpy as np
import pytest
from gaussquad._moments import compute_moments


def test_compute_exact_moments_constant_weight():
    weight_fn = lambda x: np.ones_like(x)
    interval = (0, 1)
    nr_moments = 4
    moments = compute_moments(
        method="exact",
        nr_moments=nr_moments,
        weight_fn=weight_fn,
        interval=interval,
    )
    expected = [1 / (k + 1) for k in range(nr_moments)]
    np.testing.assert_allclose(moments, expected, atol=1e-10)


def test_invalid_interval_not_tuple():
    with pytest.raises(ValueError, match="tuple"):
        compute_moments("exact", 3, lambda x: x, interval=[-1])


def test_invalid_interval_nonfinite():
    with pytest.raises(ValueError, match="finite"):
        compute_moments("exact", 3, lambda x: x, interval=(-np.inf, 1))


def test_invalid_interval_order():
    with pytest.raises(ValueError, match="a < b"):
        compute_moments("exact", 3, lambda x: x, interval=(1, 0))


def test_invalid_weight_fn_type():
    with pytest.raises(TypeError, match="callable"):
        compute_moments("exact", 3, weight_fn="not_callable", interval=(0, 1))


def test_invalid_weight_fn_output_type():
    def bad_fn(x):
        return 42  # not a NumPy array

    with pytest.raises(ValueError, match="return a NumPy array"):
        compute_moments("exact", 3, weight_fn=bad_fn, interval=(0, 1))


def test_exact_requires_constant_weight_fn():
    def not_constant(x):
        return x

    with pytest.raises(ValueError, match="constant"):
        compute_moments("exact", 3, weight_fn=not_constant, interval=(0, 1))


def test_moments_output_type_and_shape():
    weight_fn = lambda x: np.ones_like(x)
    result = compute_moments("exact", 5, weight_fn, (-1, 1))
    assert isinstance(result, np.ndarray)
    assert result.shape == (5,)