from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from pyproject_api._util import ensure_empty_dir

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


def test_ensure_empty_dir_on_empty(tmp_path: Path) -> None:
    ensure_empty_dir(tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_ensure_empty_dir_on_path_missing(tmp_path: Path) -> None:
    path = tmp_path / "a"
    ensure_empty_dir(path)
    assert list(path.iterdir()) == []


def test_ensure_empty_dir_on_path_file(tmp_path: Path) -> None:
    path = tmp_path / "a"
    path.write_text("")
    ensure_empty_dir(path)
    assert list(path.iterdir()) == []


def test_ensure_empty_dir_on_path_folder(tmp_path: Path) -> None:
    """
    ├──  a
    │  ├──  a
    │  └──  b
    │     └──  c
    └──  d
    """
    path = tmp_path / "a"
    path.mkdir()
    (path / "a").write_text("")
    sub_dir = path / "b"
    sub_dir.mkdir()
    (sub_dir / "c").write_text("")
    (tmp_path / "d").write_text("")
    ensure_empty_dir(tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_ensure_empty_dir_on_path_symlink_to_folder(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / "c").write_text("")
    path = tmp_path / "a"
    path.mkdir()
    (path / "b").symlink_to(target, target_is_directory=True)
    ensure_empty_dir(path)
    assert list(path.iterdir()) == []
    assert list(target.iterdir()) == [target / "c"]


def test_nested_cleanup_error_propagates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    blocked = tmp_path / "blocked"
    blocked.mkdir()
    stale = blocked / "stale.txt"
    stale.write_text("owned stale metadata")
    blocked_stat = blocked.stat()
    real_scandir = os.scandir
    failure = PermissionError("owned directory scan refused")

    def fail_blocked_scandir(path: Any) -> Any:
        # rmtree uses a directory descriptor on some platforms and a path on others.
        if os.path.samestat(os.stat(path), blocked_stat):  # ruff:ignore[os-stat]
            raise failure
        return real_scandir(path)

    monkeypatch.setattr(os, "scandir", fail_blocked_scandir)
    with pytest.raises(PermissionError) as captured:
        ensure_empty_dir(tmp_path)

    assert captured.value is failure
    assert stale.read_text() == "owned stale metadata"
