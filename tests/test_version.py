from __future__ import annotations


def test_version() -> None:
    from pyproject_api import __version__  # ruff:ignore[import-outside-top-level]  # checks the package exports its version

    assert __version__
