"""
Please keep this file Python 2.7 compatible.
See https://tox.readthedocs.io/en/rewrite/development.html#code-style-guide
"""

from __future__ import annotations

import os
import sys
import tarfile
from pathlib import Path
from textwrap import dedent
from zipfile import ZipFile

name = "demo_pkg_inline"
pkg_name = name.replace("_", "-")

version = "1.0.0"
dist_info = f"{name}-{version}.dist-info"
logic = f"{name}/__init__.py"
metadata_file = f"{dist_info}/METADATA"
wheel = f"{dist_info}/WHEEL"
record = f"{dist_info}/RECORD"
content = {
    logic: f"def do():\n    print('greetings from {name}')",
}
metadata = {
    metadata_file: f"""
        Metadata-Version: 2.1
        Name: {pkg_name}
        Version: {version}
        Summary: UNKNOWN
        Home-page: UNKNOWN
        Author: UNKNOWN
        Author-email: UNKNOWN
        License: UNKNOWN
        Platform: UNKNOWN

        UNKNOWN
       """,
    wheel: f"""
        Wheel-Version: 1.0
        Generator: {name}-{version}
        Root-Is-Purelib: true
        Tag: py{sys.version_info[0]}-none-any
       """,
    f"{dist_info}/top_level.txt": name,
    record: f"""
        {name}/__init__.py,,
        {dist_info}/METADATA,,
        {dist_info}/WHEEL,,
        {dist_info}/top_level.txt,,
        {dist_info}/RECORD,,
       """,
}


def build_wheel(
    wheel_directory: str,
    metadata_directory: str | None = None,
    config_settings: dict[str, str] | None = None,  # noqa: ARG001
) -> str:
    base_name = f"{name}-{version}-py{sys.version_info[0]}-none-any.whl"
    path = Path(wheel_directory) / base_name
    with ZipFile(str(path), "w") as zip_file_handler:
        for arc_name, data in content.items():
            zip_file_handler.writestr(arc_name, dedent(data).strip())
        if metadata_directory is not None:
            for sub_directory, _, filenames in os.walk(metadata_directory):
                for filename in filenames:
                    zip_file_handler.write(
                        str(Path(metadata_directory) / sub_directory / filename),
                        str(Path(sub_directory) / filename),
                    )
        else:
            for arc_name, data in metadata.items():
                zip_file_handler.writestr(arc_name, dedent(data).strip())
    print(f"created wheel {path}")  # noqa: T201
    return base_name


def get_requires_for_build_wheel(config_settings: dict[str, str] | None = None) -> list[str]:  # noqa: ARG001
    return []  # pragma: no cover # only executed in non-host pythons


def build_sdist(sdist_directory: str, config_settings: dict[str, str] | None = None) -> str:  # noqa: ARG001
    result = f"{name}-{version}.tar.gz"
    with tarfile.open(str(Path(sdist_directory) / result), "w:gz") as tar:
        root = Path(__file__).parent
        tar.add(str(root / "build.py"), "build.py")
        tar.add(str(root / "pyproject.toml"), "pyproject.toml")
    return result


def get_requires_for_build_sdist(config_settings: dict[str, str] | None = None) -> list[str]:  # noqa: ARG001
    return []  # pragma: no cover # only executed in non-host pythons


if "HAS_REQUIRES_EDITABLE" in os.environ:

    def get_requires_for_build_editable(config_settings: dict[str, str] | None = None) -> list[str]:  # noqa: ARG001
        return [1] if "REQUIRES_EDITABLE_BAD_RETURN" in os.environ else ["editables"]  # type: ignore[list-item]


if "HAS_PREPARE_EDITABLE" in os.environ:

    def prepare_metadata_for_build_editable(
        metadata_directory: str,
        config_settings: dict[str, str] | None = None,  # noqa: ARG001
    ) -> str:
        dest = Path(metadata_directory) / dist_info
        dest.mkdir(parents=True)
        for arc_name, data in metadata.items():
            (dest.parent / arc_name).write_text(dedent(data).strip())
        print(f"created metadata {dest}")  # noqa: T201
        if "PREPARE_EDITABLE_BAD" in os.environ:
            return 1  # type: ignore[return-value] # checking bad type on purpose
        return dist_info


def build_editable(
    wheel_directory: str,
    metadata_directory: str | None = None,
    config_settings: dict[str, str] | None = None,
) -> str:
    if "BUILD_EDITABLE_BAD" in os.environ:
        return 1  # type: ignore[return-value] # checking bad type on purpose
    return build_wheel(wheel_directory, metadata_directory, config_settings)
