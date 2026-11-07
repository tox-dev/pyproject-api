from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyproject_api._util import ensure_empty_dir

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


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


@pytest.mark.parametrize(
    ("target_name", "target_is_directory"),
    [
        pytest.param("missing", False, id="dangling-file"),
        pytest.param("missing", True, id="dangling-directory"),
        pytest.param("file", False, id="file"),
        pytest.param("folder", True, id="directory"),
    ],
)
def test_ensure_empty_dir_replaces_symlink(tmp_path: Path, target_name: str, target_is_directory: bool) -> None:
    (tmp_path / "file").write_text("keep file")
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "c").write_text("keep folder contents")
    path = tmp_path / "a"
    path.symlink_to(tmp_path / target_name, target_is_directory=target_is_directory)
    ensure_empty_dir(path)
    assert not path.is_symlink()
    assert list(path.iterdir()) == []
    assert (tmp_path / "file").read_text() == "keep file"
    assert (folder / "c").read_text() == "keep folder contents"


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


def test_nested_cleanup_error_propagates(tmp_path: Path, mocker: MockerFixture) -> None:
    blocked = tmp_path / "blocked"
    blocked.mkdir()
    stale = blocked / "stale.txt"
    stale.write_text("stale metadata")
    failure = PermissionError("file removal refused")
    mocker.patch("os.unlink", autospec=True, side_effect=failure)
    with pytest.raises(PermissionError) as captured:
        ensure_empty_dir(tmp_path)

    assert captured.value is failure
    assert stale.read_text() == "stale metadata"
