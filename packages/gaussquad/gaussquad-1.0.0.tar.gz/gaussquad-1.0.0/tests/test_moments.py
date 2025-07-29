import numpy as np
import pytest
from gaussquad._moments import compute_moments


def test_compute_moments_invalid_method():
    with pytest.raises(NotImplementedError):
        compute_moments(
            method="unknown",
            nr_moments=3,
            weight_fn=lambda x: x,
            interval=(-1, 1),
        )


def test_compute_legendre_missing_degree():
    with pytest.raises(ValueError, match="degree"):
        compute_moments(
            method="legendre",
            nr_moments=3,
            weight_fn=lambda x: x,
            interval=(-1, 1),
        )