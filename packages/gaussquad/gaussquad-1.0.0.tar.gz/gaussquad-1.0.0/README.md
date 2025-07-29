# gaussquad

A mini-package to compute Gauss quadrature nodes and weights for arbitrary weight functions on finite intervals using the
Golub–Welsch algorithm.

> Based on:  
> - [Golub & Welsch (1969)](https://doi.org/10.1090/S0025-5718-69-99647-1)  
> - [Technical report (1967)](http://i.stanford.edu/pub/cstr/reports/cs/tr/67/81/CS-TR-67-81.pdf)

Documentation is available at [thatmariia.github.io/gaussquad](https://thatmariia.github.io/gaussquad)

[![GitHub Pages](https://img.shields.io/badge/view-docs-blue?logo=github)](https://thatmariia.github.io/gaussquad)

---

## Features

- Compute **quadrature nodes and weights** for custom weight functions
- Use them directly to **approximate integrals**

## Installation

From PyPI (when released):

```bash
pip install gaussquad
```

From GitHub:

```bash
pip install git+https://github.com/thatmariia/gaussquad.git
```
> **Requirements:** Python 3.13 or newer, numpy, scipy

## Usage

You can integrate *x^2 * w(x)* from 0 to 5 with a weight function *w(x)=exp(-x)*:

```python
import numpy as np
from gaussquad import wquad

result = wquad(
    fn=lambda x: x**2,
    weight_fn=lambda x: np.exp(-x),
    interval=(0, 5),
    degree=5,
    moment_method="legendre"  # approximation for moments
)

print(f"Integral of x^2 from 0 to 5 with weight function exp(-x): {result}")  # ≈ 1.7507
```

More examples: [docs » usage.md](https://thatmariia.github.io/gaussquad/usage.html).

## Development & docs

```bash
git clone https://github.com/thatmariia/gaussquad.git
cd gaussquad
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -e ".[dev,docs]"
```

| Command | Description |
| ------- | ----------- |
| `pytest` | Run tests |
| `flake8 src/` | Check code style |
| `black --check src/` | Check code style |
| `cd docs && make html` | Build docs |
| `open docs/build/html/index.html` | View docs (macOS) |
| `python -m http.server --directory docs/build/html` | View docs (all OS) |

---

## Citation

If you use this package in your research, please cite it 
using the information under "Cite this repository" on the right side of the GitHub page.

If you need a version-specific citation, you can find it on [Zenodo](https://doi.org/10.5281/zenodo.15468025).

---

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.
