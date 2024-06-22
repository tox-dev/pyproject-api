from __future__ import annotations

import sys
from contextlib import contextmanager
from stat import S_IWGRP, S_IWOTH, S_IWUSR
from typing import TYPE_CHECKING, Iterator, NamedTuple

import pytest

from pyproject_api._frontend import BackendFailed
from pyproject_api._via_fresh_subprocess import SubprocessFrontend

if TYPE_CHECKING:
    from pathlib import Path

    from _pytest.tmpdir import TempPathFactory
    from pytest_mock import MockerFixture

from importlib.metadata import Distribution, EntryPoint


@pytest.fixture(scope="session")
def frontend_setuptools(tmp_path_factory: TempPathFactory) -> SubprocessFrontend:
    prj = tmp_path_factory.mktemp("proj")
    (prj / "pyproject.toml").write_text(
        '[build-system]\nrequires=["setuptools","wheel"]\nbuild-backend = "setuptools.build_meta"',
    )
    cfg = """
        [metadata]
        name = demo
        version = 1.0

        [options]
        packages = demo
        install_requires =
          requests>2
          magic>3

        [options.entry_points]
        console_scripts =
            demo_exe = demo:a
        """
    (prj / "setup.cfg").write_text(cfg)
    (prj / "setup.py").write_text("from setuptools import setup; setup()")
    demo = prj / "demo"
    demo.mkdir()
    (demo / "__init__.py").write_text("def a(): print('ok')")
    args = SubprocessFrontend.create_args_from_folder(prj)
    return SubprocessFrontend(*args[:-1])


def test_setuptools_get_requires_for_build_sdist(frontend_setuptools: SubprocessFrontend) -> None:
    result = frontend_setuptools.get_requires_for_build_sdist()
    assert result.requires == ()
    assert isinstance(result.out, str)
    assert isinstance(result.err, str)


def test_setuptools_get_requires_for_build_wheel(frontend_setuptools: SubprocessFrontend) -> None:
    result = frontend_setuptools.get_requires_for_build_wheel()
    assert not result.requires
    assert isinstance(result.out, str)
    assert isinstance(result.err, str)


def test_setuptools_prepare_metadata_for_build_wheel(frontend_setuptools: SubprocessFrontend, tmp_path: Path) -> None:
    meta = tmp_path / "meta"
    result = frontend_setuptools.prepare_metadata_for_build_wheel(metadata_directory=meta)
    assert result is not None
    dist = Distribution.at(str(result.metadata))
    assert list(dist.entry_points) == [EntryPoint(name="demo_exe", value="demo:a", group="console_scripts")]
    assert dist.version == "1.0"
    assert dist.metadata["Name"] == "demo"
    values = [v for k, v in dist.metadata.items() if k == "Requires-Dist"]  # type: ignore[attr-defined]
    # ignore because "PackageMetadata" has no attribute "items"
    assert sorted(values) == ["magic >3", "requests >2"]
    assert isinstance(result.out, str)
    assert isinstance(result.err, str)

    # call it again regenerates it because frontend always deletes earlier content
    before = result.metadata.stat().st_mtime
    result = frontend_setuptools.prepare_metadata_for_build_wheel(metadata_directory=meta)
    assert result is not None
    after = result.metadata.stat().st_mtime
    assert after > before


def test_setuptools_build_sdist(frontend_setuptools: SubprocessFrontend, tmp_path: Path) -> None:
    result = frontend_setuptools.build_sdist(tmp_path)
    sdist = result.sdist
    assert sdist.exists()
    assert sdist.is_file()
    assert sdist.name == "demo-1.0.tar.gz"
    assert isinstance(result.out, str)
    assert isinstance(result.err, str)


def test_setuptools_build_wheel(frontend_setuptools: SubprocessFrontend, tmp_path: Path) -> None:
    result = frontend_setuptools.build_wheel(tmp_path)
    wheel = result.wheel
    assert wheel.exists()
    assert wheel.is_file()
    assert wheel.name == "demo-1.0-py3-none-any.whl"
    assert isinstance(result.out, str)
    assert isinstance(result.err, str)


def test_setuptools_exit(frontend_setuptools: SubprocessFrontend) -> None:
    result, out, err = frontend_setuptools.send_cmd("_exit")
    assert isinstance(out, str)
    assert isinstance(err, str)
    assert result == 0


def test_setuptools_missing_command(frontend_setuptools: SubprocessFrontend) -> None:
    with pytest.raises(BackendFailed):
        frontend_setuptools.send_cmd("missing_command")


def test_setuptools_exception(frontend_setuptools: SubprocessFrontend) -> None:
    with pytest.raises(BackendFailed) as context:
        frontend_setuptools.send_cmd("build_wheel")
    assert isinstance(context.value.out, str)
    assert isinstance(context.value.err, str)
    assert context.value.exc_type == "TypeError"
    prefix = "_BuildMetaBackend." if sys.version_info >= (3, 10) else ""
    msg = f"{prefix}build_wheel() missing 1 required positional argument: 'wheel_directory'"
    assert context.value.exc_msg == msg
    assert context.value.code == 1
    assert context.value.args == ()
    assert repr(context.value)
    assert str(context.value)
    assert repr(context.value) != str(context.value)


def test_bad_message(frontend_setuptools: SubprocessFrontend, tmp_path: Path) -> None:
    with frontend_setuptools._send_msg("bad_cmd", tmp_path / "a", "{{") as status:  # noqa: SLF001
        while not status.done:  # pragma: no branch
            pass
    out, err = status.out_err()
    assert out
    assert "Backend: incorrect request to backend: bytearray(b'{{')" in err


class _Result(NamedTuple):
    name: str


def test_result_missing(frontend_setuptools: SubprocessFrontend, tmp_path: Path, mocker: MockerFixture) -> None:
    @contextmanager
    def named_temporary_file(prefix: str) -> Iterator[_Result]:
        write = S_IWUSR | S_IWGRP | S_IWOTH
        base = tmp_path / prefix
        result = base.with_suffix(".json")
        result.write_text("")
        result.chmod(result.stat().st_mode & ~write)  # force json write to fail due to R/O
        patch = mocker.patch("pyproject_api._frontend.Path.exists", return_value=False)  # make it missing
        try:
            yield _Result(str(base))
        finally:
            patch.stop()
            result.chmod(result.stat().st_mode | write)  # cleanup
            result.unlink()

    mocker.patch("pyproject_api._frontend.NamedTemporaryFile", named_temporary_file)
    with pytest.raises(BackendFailed) as context:
        frontend_setuptools.send_cmd("_exit")
    exc = context.value
    assert exc.exc_msg == f"Backend response file {tmp_path / 'pep517__exit-.json'} is missing"
    assert exc.exc_type == "RuntimeError"
    assert exc.code == 1
    assert "Traceback" in exc.err
    assert "PermissionError" in exc.err
