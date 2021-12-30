from __future__ import annotations


def test_version() -> None:
    from pyproject_api import __version__

    assert __version__
