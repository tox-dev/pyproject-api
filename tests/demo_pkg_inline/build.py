from __future__ import annotations

import os
import sys
import tarfile
from pathlib import Path
from textwrap import dedent
from typing import Final
from zipfile import ZipFile

_NAME: Final[str] = "demo_pkg_inline"
_PKG_NAME: Final[str] = _NAME.replace("_", "-")

_VERSION: Final[str] = "1.0.0"
_DIST_INFO: Final[str] = f"{_NAME}-{_VERSION}.dist-info"
_LOGIC: Final[str] = f"{_NAME}/__init__.py"
_METADATA_FILE: Final[str] = f"{_DIST_INFO}/METADATA"
_WHEEL: Final[str] = f"{_DIST_INFO}/WHEEL"
_RECORD: Final[str] = f"{_DIST_INFO}/RECORD"
_CONTENT: Final[dict[str, str]] = {
    _LOGIC: f"def do():\n    print('greetings from {_NAME}')",
}
_METADATA: Final[dict[str, str]] = {
    _METADATA_FILE: f"""
        Metadata-Version: 2.1
        Name: {_PKG_NAME}
        Version: {_VERSION}
        Summary: UNKNOWN
        Home-page: UNKNOWN
        Author: UNKNOWN
        Author-email: UNKNOWN
        License: UNKNOWN
        Platform: UNKNOWN

        UNKNOWN
       """,
    _WHEEL: f"""
        Wheel-Version: 1.0
        Generator: {_NAME}-{_VERSION}
        Root-Is-Purelib: true
        Tag: py{sys.version_info[0]}-none-any
       """,
    f"{_DIST_INFO}/top_level.txt": _NAME,
    _RECORD: f"""
        {_NAME}/__init__.py,,
        {_DIST_INFO}/METADATA,,
        {_DIST_INFO}/WHEEL,,
        {_DIST_INFO}/top_level.txt,,
        {_DIST_INFO}/RECORD,,
       """,
}


def get_requires_for_build_wheel(config_settings: dict[str, str] | None = None) -> list[str]:  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
    return []  # pragma: no cover # only executed in non-host pythons


def build_sdist(sdist_directory: str, config_settings: dict[str, str] | None = None) -> str:  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
    result = f"{_NAME}-{_VERSION}.tar.gz"
    with tarfile.open(str(Path(sdist_directory) / result), "w:gz") as tar:
        root = Path(__file__).parent
        tar.add(str(root / "build.py"), "build.py")
        tar.add(str(root / "pyproject.toml"), "pyproject.toml")
    return result


def get_requires_for_build_sdist(config_settings: dict[str, str] | None = None) -> list[str]:  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
    return []  # pragma: no cover # only executed in non-host pythons


if "HAS_REQUIRES_EDITABLE" in os.environ:

    def get_requires_for_build_editable(config_settings: dict[str, str] | None = None) -> list[str]:  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
        return [1] if "REQUIRES_EDITABLE_BAD_RETURN" in os.environ else ["editables"]  # type: ignore[invalid-return-type]  # returns a bad type on purpose for the test


if "HAS_PREPARE_EDITABLE" in os.environ:

    def prepare_metadata_for_build_editable(
        metadata_directory: str,
        config_settings: dict[str, str] | None = None,  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
    ) -> str:
        dest = Path(metadata_directory) / _DIST_INFO
        dest.mkdir(parents=True)
        for arc_name, data in _METADATA.items():
            (dest.parent / arc_name).write_text(dedent(data).strip())
        print(f"created metadata {dest}")  # ruff:ignore[print]  # the test backend reports its progress on stdout
        if "PREPARE_EDITABLE_BAD" in os.environ:
            return 1  # type: ignore[invalid-return-type] # checking bad type on purpose
        return _DIST_INFO


def build_editable(
    wheel_directory: str,
    metadata_directory: str | None = None,
    config_settings: dict[str, str] | None = None,
) -> str:
    if "BUILD_EDITABLE_BAD" in os.environ:
        return 1  # type: ignore[invalid-return-type] # checking bad type on purpose
    return build_wheel(wheel_directory, metadata_directory, config_settings)


def build_wheel(
    wheel_directory: str,
    metadata_directory: str | None,
    config_settings: dict[str, str] | None,  # ruff:ignore[unused-function-argument]  # the hook signature is fixed by PEP 517
) -> str:
    base_name = f"{_NAME}-{_VERSION}-py{sys.version_info[0]}-none-any.whl"
    path = Path(wheel_directory) / base_name
    with ZipFile(str(path), "w") as zip_file_handler:
        for arc_name, data in _CONTENT.items():
            zip_file_handler.writestr(arc_name, dedent(data).strip())
        if metadata_directory is not None:
            for sub_directory, _, filenames in os.walk(metadata_directory):
                for filename in filenames:
                    zip_file_handler.write(
                        str(Path(metadata_directory) / sub_directory / filename),
                        str(Path(sub_directory) / filename),
                    )
        else:
            for arc_name, data in _METADATA.items():
                zip_file_handler.writestr(arc_name, dedent(data).strip())
    print(f"created wheel {path}")  # ruff:ignore[print]  # the test backend reports its progress on stdout
    return base_name
