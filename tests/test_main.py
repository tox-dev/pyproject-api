from __future__ import annotations

from pathlib import Path
from shutil import copytree
from typing import TYPE_CHECKING

import pytest

import pyproject_api.__main__
from pyproject_api._frontend import EditableResult, SdistResult, WheelResult

if TYPE_CHECKING:
    import pytest_mock


@pytest.mark.parametrize(
    ("distribution", "filename"),
    [
        pytest.param("--sdist", "demo_pkg_inline-1.0.0.tar.gz", id="sdist"),
        pytest.param("--wheel", "demo_pkg_inline-1.0.0-py3-none-any.whl", id="wheel"),
        pytest.param("--editable", "demo_pkg_inline-1.0.0-py3-none-any.whl", id="editable"),
    ],
)
@pytest.mark.parametrize(
    ("outdir_args", "outdir"),
    [
        pytest.param([], "project/dist", id="default-outdir"),
        pytest.param(["--outdir", "artifacts"], "artifacts", id="relative-outdir"),
    ],
)
def test_cli_build_relative_to_caller(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    distribution: str,
    filename: str,
    outdir_args: list[str],
    outdir: str,
) -> None:
    copytree(Path(__file__).parent / "demo_pkg_inline", tmp_path / "project")
    monkeypatch.chdir(tmp_path)

    pyproject_api.__main__.main(["project", distribution, *outdir_args])

    assert (tmp_path / outdir / filename).is_file()


@pytest.mark.parametrize(
    ("cli_args", "srcdir", "outdir", "hooks"),
    [
        (
            [],
            Path.cwd(),
            Path.cwd() / "dist",
            ["build_sdist", "build_wheel"],
        ),
        (
            ["src"],
            Path("src"),
            Path("src").absolute() / "dist",
            ["build_sdist", "build_wheel"],
        ),
        (
            ["-o", "out"],
            Path.cwd(),
            Path("out").absolute(),
            ["build_sdist", "build_wheel"],
        ),
        (
            ["-s"],
            Path.cwd(),
            Path.cwd() / "dist",
            ["build_sdist"],
        ),
        (
            ["-w"],
            Path.cwd(),
            Path.cwd() / "dist",
            ["build_wheel"],
        ),
        (
            ["-e"],
            Path.cwd(),
            Path.cwd() / "dist",
            ["build_editable"],
        ),
        (
            ["-s", "-w"],
            Path.cwd(),
            Path.cwd() / "dist",
            ["build_sdist", "build_wheel"],
        ),
    ],
)
def test_parse_args(
    mocker: pytest_mock.MockerFixture,
    capsys: pytest.CaptureFixture[str],
    cli_args: list[str],
    srcdir: Path,
    outdir: Path,
    hooks: list[str],
) -> None:
    subprocess_frontend = mocker.patch("pyproject_api.__main__.SubprocessFrontend", autospec=True)
    subprocess_frontend.create_args_from_folder.return_value = (srcdir, (), "foo.bar", "baz", (), True)
    subprocess_frontend.return_value.build_sdist.return_value = SdistResult(
        sdist=outdir / "foo.whl",
        out="sdist out",
        err="sdist err",
    )
    subprocess_frontend.return_value.build_wheel.return_value = WheelResult(
        wheel=outdir / "foo.whl",
        out="wheel out",
        err="wheel err",
    )
    subprocess_frontend.return_value.build_editable.return_value = EditableResult(
        wheel=outdir / "foo.whl",
        out="editable wheel out",
        err="editable wheel err",
    )

    pyproject_api.__main__.main(cli_args)

    subprocess_frontend.create_args_from_folder.assert_called_once_with(srcdir)
    captured = capsys.readouterr()

    if "build_sdist" in hooks:
        assert "Building sdist..." in captured.out
        subprocess_frontend.return_value.build_sdist.assert_called_once_with(outdir)
        assert "sdist out" in captured.out
        assert "sdist err" in captured.err

    if "build_wheel" in hooks:
        assert "Building wheel..." in captured.out
        subprocess_frontend.return_value.build_wheel.assert_called_once_with(outdir)
        assert "wheel out" in captured.out
        assert "wheel err" in captured.err

    if "build_editable" in hooks:
        assert "Building editable wheel..." in captured.out
        subprocess_frontend.return_value.build_editable.assert_called_once_with(outdir)
        assert "editable wheel out" in captured.out
        assert "editable wheel err" in captured.err
