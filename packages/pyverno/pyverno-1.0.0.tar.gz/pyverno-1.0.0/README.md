# Python package version checker/updater

Check or update the version number defined in a Python source file such as
`__init__.py`

## Sub-commands

- `check` - Verify that the `__version__` in `PY_FILE` matches the one embedded
  in `GIT_TAG_REF`.
- `update` - Append a timestamped dev version component formatted as
  `.devYYYYmmddHHMMSS` to the `__version__` string in `PY_FILE`.

Usage:
```sh
pyverno check PY_FILE GIT_TAG_REF

pyverno update PY_FILE
```

## Conventions

- The version must be assigned to a variable named `__version__` in the
  provided `PY_FILE`. The assignment must be at the beginning of the line and
  have single-character string delimiters, e.g. `__version__ = "X.Y.Z"`.
- `GIT_TAG_REF` is formatted as `refs/tags/vX.Y.Z`. This implies that git
  version tags should have the format `vX.Y.Z`, where the `X.Y.Z` portion uses
  whatever version number format makes sense for the project.

`pyverno` is not opinionated about version number formats. The only restriction
is that a version number may not contain quote characters of the same style used
to delimit the version string. Exmaples of valid version numbers: `1.0.0`,
`2025-05-22`, `20250522`

## Purpose

`pyverno` was developed to automate a version check or update during
[trusted publishing to PyPI](https://docs.pypi.org/trusted-publishers/using-a-publisher/).
The `check` command is useful when publishing a new final release, and the
`update` command is useful to create a reasonably unique version number when
publishing to https://test.pypi.org.

## Publishing new versions to PyPI

Push a new tag to Github using the format `vX.Y.Z` where `X.Y.Z` matches the
version in [`pyverno.py`](pyverno.py).

A new version is published to https://test.pypi.org/p/pyverno on every
push to the *main* branch.

Publishing is automated with [Github Actions](.github/workflows/pypi.yml).
