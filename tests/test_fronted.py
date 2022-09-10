from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Callable

import pytest
from packaging.requirements import Requirement

from pyproject_api._frontend import BackendFailed
from pyproject_api._via_fresh_subprocess import SubprocessFrontend


@pytest.fixture()
def local_builder(tmp_path: Path) -> Callable[[str], Path]:
    def _f(content: str) -> Path:
        toml = '[build-system]\nrequires=[]\nbuild-backend = "build_tester"\nbackend-path=["."]'
        (tmp_path / "pyproject.toml").write_text(toml)
        (tmp_path / "build_tester.py").write_text(dedent(content))
        return tmp_path

    return _f


def test_missing_backend(local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("")
    toml = tmp_path / "pyproject.toml"
    toml.write_text('[build-system]\nrequires=[]\nbuild-backend = "build_tester"')
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])
    with pytest.raises(BackendFailed) as context:
        fronted.build_wheel(tmp_path / "wheel")
    exc = context.value
    assert exc.exc_type == "RuntimeError"
    assert exc.code == 1
    assert "failed to start backend" in exc.err
    assert "ModuleNotFoundError: No module named " in exc.err


@pytest.mark.parametrize("cmd", ["build_wheel", "build_sdist"])
def test_missing_required_cmd(cmd: str, local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(BackendFailed) as context:
        getattr(fronted, cmd)(tmp_path)
    exc = context.value
    assert f"has no attribute '{cmd}'" in exc.exc_msg
    assert exc.exc_type == "MissingCommand"


def test_empty_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[build-system]")
    root, backend_paths, backend_module, backend_obj, requires, _ = SubprocessFrontend.create_args_from_folder(tmp_path)
    assert root == tmp_path
    assert backend_paths == ()
    assert backend_module == "setuptools.build_meta"
    assert backend_obj == "__legacy__"
    for left, right in zip(requires, (Requirement("setuptools>=40.8.0"), Requirement("wheel"))):
        assert isinstance(left, Requirement)
        assert str(left) == str(right)


@pytest.fixture(scope="session")
def demo_pkg_inline() -> Path:
    return Path(__file__).absolute().parent / "demo_pkg_inline"


def test_backend_no_prepare_wheel(tmp_path: Path, demo_pkg_inline: Path) -> None:
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.prepare_metadata_for_build_wheel(tmp_path)
    assert result.metadata.name == "demo_pkg_inline-1.0.0.dist-info"


def test_backend_build_sdist_demo_pkg_inline(tmp_path: Path, demo_pkg_inline: Path) -> None:
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.build_sdist(sdist_directory=tmp_path)
    assert result.sdist == tmp_path / "demo_pkg_inline-1.0.0.tar.gz"


def test_backend_obj(tmp_path: Path) -> None:
    toml = """
        [build-system]
        requires=[]
        build-backend = "build.api:backend:"
        backend-path=["."]
        """
    api = """
        class A:
            def get_requires_for_build_sdist(self, config_settings=None):
                return ["a"]

        backend = A()
        """
    (tmp_path / "pyproject.toml").write_text(dedent(toml))
    build = tmp_path / "build"
    build.mkdir()
    (build / "__init__.py").write_text("")
    (build / "api.py").write_text(dedent(api))
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])
    result = fronted.get_requires_for_build_sdist()
    for left, right in zip(result.requires, (Requirement("a"),)):
        assert isinstance(left, Requirement)
        assert str(left) == str(right)


@pytest.mark.parametrize("of_type", ["wheel", "sdist"])
def test_get_requires_for_build_missing(of_type: str, local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])
    result = getattr(fronted, f"get_requires_for_build_{of_type}")()
    assert result.requires == ()


@pytest.mark.parametrize("of_type", ["sdist", "wheel"])
def test_bad_return_type_get_requires_for_build(of_type: str, local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder(f"def get_requires_for_build_{of_type}(config_settings=None): return 1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(BackendFailed) as context:
        getattr(fronted, f"get_requires_for_build_{of_type}")()

    exc = context.value
    msg = f"'get_requires_for_build_{of_type}' on 'build_tester' returned 1 but expected type 'list of string'"
    assert exc.exc_msg == msg
    assert exc.exc_type == "TypeError"


def test_bad_return_type_build_sdist(local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("def build_sdist(sdist_directory, config_settings=None): return 1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(BackendFailed) as context:
        fronted.build_sdist(tmp_path)

    exc = context.value
    assert exc.exc_msg == f"'build_sdist' on 'build_tester' returned 1 but expected type {str!r}"
    assert exc.exc_type == "TypeError"


def test_bad_return_type_build_wheel(local_builder: Callable[[str], Path]) -> None:
    txt = "def build_wheel(wheel_directory, config_settings=None, metadata_directory=None): return 1"
    tmp_path = local_builder(txt)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(BackendFailed) as context:
        fronted.build_wheel(tmp_path)

    exc = context.value
    assert exc.exc_msg == f"'build_wheel' on 'build_tester' returned 1 but expected type {str!r}"
    assert exc.exc_type == "TypeError"


def test_bad_return_type_prepare_metadata_for_build_wheel(local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None): return 1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(BackendFailed) as context:
        fronted.prepare_metadata_for_build_wheel(tmp_path / "meta")

    exc = context.value
    assert exc.exc_type == "TypeError"
    assert exc.exc_msg == f"'prepare_metadata_for_build_wheel' on 'build_tester' returned 1 but expected type {str!r}"


def test_prepare_metadata_for_build_wheel_meta_is_root(local_builder: Callable[[str], Path]) -> None:
    tmp_path = local_builder("def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None): return 1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(RuntimeError) as context:
        fronted.prepare_metadata_for_build_wheel(tmp_path)

    assert str(context.value) == f"the project root and the metadata directory can't be the same {tmp_path}"


def test_no_wheel_prepare_metadata_for_build_wheel(local_builder: Callable[[str], Path]) -> None:
    txt = "def build_wheel(wheel_directory, config_settings=None, metadata_directory=None): return 'out'"
    tmp_path = local_builder(txt)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(RuntimeError, match="missing wheel file return by backed *"):
        fronted.prepare_metadata_for_build_wheel(tmp_path / "meta")


def test_bad_wheel_prepare_metadata_for_build_wheel(local_builder: Callable[[str], Path]) -> None:
    txt = """
    import sys
    from pathlib import Path
    from zipfile import ZipFile

    def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
        path = Path(wheel_directory) / "out"
        with ZipFile(str(path), "w") as zip_file_handler:
            pass
        print(f"created wheel {path}")
        return path.name
    """
    tmp_path = local_builder(txt)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1])

    with pytest.raises(RuntimeError, match="no .dist-info found inside generated wheel*"):
        fronted.prepare_metadata_for_build_wheel(tmp_path / "meta")


def test_create_no_pyproject(tmp_path: Path) -> None:
    result = SubprocessFrontend.create_args_from_folder(tmp_path)
    assert len(result) == 6
    assert result[0] == tmp_path
    assert result[1] == ()
    assert result[2] == "setuptools.build_meta"
    assert result[3] == "__legacy__"
    assert all(isinstance(i, Requirement) for i in result[4])
    assert [str(i) for i in result[4]] == ["setuptools>=40.8.0", "wheel"]
    assert result[5] is True


def test_backend_get_requires_for_build_editable(demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HAS_REQUIRES_EDITABLE", "1")
    monkeypatch.delenv("REQUIRES_EDITABLE_BAD_RETURN", raising=False)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.get_requires_for_build_editable()
    assert [str(i) for i in result.requires] == ["editables"]
    assert isinstance(result.requires[0], Requirement)
    assert " get_requires_for_build_editable " in result.out
    assert not result.err


def test_backend_get_requires_for_build_editable_miss(demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HAS_REQUIRES_EDITABLE", raising=False)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.get_requires_for_build_editable()
    assert not result.requires
    assert " get_requires_for_build_editable " in result.out
    assert not result.err


def test_backend_get_requires_for_build_editable_bad(demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HAS_REQUIRES_EDITABLE", "1")
    monkeypatch.setenv("REQUIRES_EDITABLE_BAD_RETURN", "1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    with pytest.raises(BackendFailed) as context:
        fronted.get_requires_for_build_editable()
    exc = context.value
    assert exc.code is None
    assert not exc.err
    assert " get_requires_for_build_editable " in exc.out
    assert not exc.args
    assert exc.exc_type == "TypeError"
    assert exc.exc_msg == "'get_requires_for_build_editable' on 'build' returned [1] but expected type 'list of string'"


def test_backend_prepare_editable(tmp_path: Path, demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HAS_PREPARE_EDITABLE", "1")
    monkeypatch.delenv("PREPARE_EDITABLE_BAD", raising=False)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.prepare_metadata_for_build_editable(tmp_path)
    assert result.metadata.name == "demo_pkg_inline-1.0.0.dist-info"
    assert " prepare_metadata_for_build_editable " in result.out
    assert " build_editable " not in result.out
    assert not result.err


def test_backend_prepare_editable_miss(tmp_path: Path, demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HAS_PREPARE_EDITABLE", raising=False)
    monkeypatch.delenv("BUILD_EDITABLE_BAD", raising=False)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.prepare_metadata_for_build_editable(tmp_path)
    assert result.metadata.name == "demo_pkg_inline-1.0.0.dist-info"
    assert " prepare_metadata_for_build_editable " not in result.out
    assert " build_editable " in result.out
    assert not result.err


def test_backend_prepare_editable_bad(tmp_path: Path, demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HAS_PREPARE_EDITABLE", "1")
    monkeypatch.setenv("PREPARE_EDITABLE_BAD", "1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    with pytest.raises(BackendFailed) as context:
        fronted.prepare_metadata_for_build_editable(tmp_path)
    exc = context.value
    assert exc.code is None
    assert not exc.err
    assert " prepare_metadata_for_build_editable " in exc.out
    assert not exc.args
    assert exc.exc_type == "TypeError"
    assert exc.exc_msg == "'prepare_metadata_for_build_wheel' on 'build' returned 1 but expected type <class 'str'>"


def test_backend_build_editable(tmp_path: Path, demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BUILD_EDITABLE_BAD", raising=False)
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    result = fronted.build_editable(tmp_path)
    assert result.wheel.name == "demo_pkg_inline-1.0.0-py3-none-any.whl"
    assert " build_editable " in result.out
    assert not result.err


def test_backend_build_editable_bad(tmp_path: Path, demo_pkg_inline: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BUILD_EDITABLE_BAD", "1")
    fronted = SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(demo_pkg_inline)[:-1])
    with pytest.raises(BackendFailed) as context:
        fronted.build_editable(tmp_path)
    exc = context.value
    assert exc.code is None
    assert not exc.err
    assert " build_editable " in exc.out
    assert not exc.args
    assert exc.exc_type == "TypeError"
    assert exc.exc_msg == "'build_editable' on 'build' returned 1 but expected type <class 'str'>"
