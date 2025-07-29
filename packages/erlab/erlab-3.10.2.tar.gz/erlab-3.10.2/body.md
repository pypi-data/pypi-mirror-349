## v3.10.2 (2025-05-20)

### 🐞 Bug Fixes

- **io.dataloader:** fix concatenation of multiple files (#139) ([0f16d96](https://github.com/kmnhan/erlabpy/commit/0f16d9667b5b9b82b1f394cfe0e5abd67b942cc6))

  Reverts the behavior of the concatenation of multiple files, fixing failures while loading multidimensional motor scans.

  Also adds support for data across multiple files with some data missing non-dimensional coordinates.

- **imagetool.manager:** set xarray option `keep_attrs` to `True` by default in console ([330aca9](https://github.com/kmnhan/erlabpy/commit/330aca9d2adc405e9a769f40a66e7550a791caaf))

### ♻️ Code Refactor

- **io.plugins.erpes:** add 'laser_power' to coordinate attributes (#140) ([0b86283](https://github.com/kmnhan/erlabpy/commit/0b862834e4ac2d895e88ed1b2fd3b515c1eb647a))

- remove deprecated direct comparison of uncertainties ([c237a4d](https://github.com/kmnhan/erlabpy/commit/c237a4d30432c638529d1a2c7183651b58db53ba))

[main c0d69a1] bump: version 3.10.1 → 3.10.2
 3 files changed, 5 insertions(+), 3 deletions(-)

