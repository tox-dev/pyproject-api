from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING, Final

import pytest

from pyproject_api import SubprocessFrontend
from pyproject_api._via_fresh_subprocess import SubprocessCmdStatus

if TYPE_CHECKING:
    from pathlib import Path

    import pytest_mock


@pytest.mark.parametrize(
    "error_type",
    [
        pytest.param(KeyboardInterrupt, id="keyboard-interrupt"),
        pytest.param(SystemExit, id="system-exit"),
        pytest.param(RuntimeError, id="runtime-error"),
    ],
)
def test_interrupted_frontend_cleans_up_backend(
    error_type: type[BaseException], tmp_path: Path, mocker: pytest_mock.MockerFixture
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[build-system]\nrequires=[]\nbuild-backend = "build_tester"\nbackend-path=["."]', encoding="utf-8"
    )
    (tmp_path / "build_tester.py").write_text(
        dedent("""\
            import time

            def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
                time.sleep(60)
                return "demo-1.0-py3-none-any.whl"
        """),
        encoding="utf-8",
    )
    status_constructor: Final = mocker.spy(SubprocessCmdStatus, "__init__")
    mocker.patch("pyproject_api._frontend.sleep", autospec=True, side_effect=error_type("build interrupted"))

    try:
        with pytest.raises(error_type):
            SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1]).build_wheel(
                tmp_path / "dist"
            )

        assert not status_constructor.call_args.args[0].is_alive()
    finally:
        # A failed cleanup test must not leave a live child process.
        status: Final = status_constructor.call_args.args[0]
        status.process.kill()
        status.join(timeout=10)
