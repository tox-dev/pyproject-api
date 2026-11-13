from __future__ import annotations

import sys
import threading
from subprocess import Popen  # ruff:ignore[suspicious-subprocess-import]  # inspect the spawned backend
from textwrap import dedent
from typing import TYPE_CHECKING, Final

import pytest

from pyproject_api import SubprocessFrontend

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
    process_constructor: Final = mocker.spy(sys.modules[SubprocessFrontend.__module__], "Popen")
    mocker.patch("pyproject_api._frontend.sleep", autospec=True, side_effect=error_type("build interrupted"))
    threads_before: Final = set(threading.enumerate())

    with pytest.raises(error_type):
        SubprocessFrontend(*SubprocessFrontend.create_args_from_folder(tmp_path)[:-1]).build_wheel(tmp_path / "dist")

    process: Final = process_constructor.spy_return
    assert isinstance(process, Popen)
    try:
        assert process.poll() is not None
        assert all(thread.daemon for thread in set(threading.enumerate()) - threads_before)
    finally:
        # A failed cleanup test must not leave a live child process.
        process.kill()
        process.wait(timeout=10)
