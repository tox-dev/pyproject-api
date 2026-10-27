from __future__ import annotations

import json
import os
import subprocess  # ruff:ignore[suspicious-subprocess-import]
import sys
from textwrap import dedent
from typing import TYPE_CHECKING, Any, assert_type

import pytest

from pyproject_api import _backend
from pyproject_api._backend import BackendProxy, read_line, run

if TYPE_CHECKING:
    from pathlib import Path

    import pytest_mock


def test_backend_proxy_private_command_types() -> None:
    class TypedBackendProxy(BackendProxy):
        def check(self) -> None:
            assert assert_type(self._optional_hooks(), dict[str, bool])["build_editable"] is False
            assert assert_type(self._exit(), int) == 0

    TypedBackendProxy("json", None).check()


def test_invalid_module(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ImportError):
        run([str(False), "an.invalid.module"])

    captured = capsys.readouterr()
    assert "failed to start backend" in captured.err


def test_invalid_request(mocker: pytest_mock.MockerFixture, capsys: pytest.CaptureFixture[str]) -> None:
    """Validate behavior when an invalid request is issued."""
    command = "invalid json"

    backend_proxy = mocker.MagicMock(spec=BackendProxy)
    backend_proxy.return_value = "dummy_result"
    backend_proxy.__str__.return_value = "FakeBackendProxy"
    mocker.patch("pyproject_api._backend.BackendProxy", return_value=backend_proxy)
    mocker.patch("pyproject_api._backend.read_line", return_value=bytearray(command, "utf-8"))

    ret = run([str(False), "a.dummy.module"])

    assert ret == 0
    captured = capsys.readouterr()
    assert "started backend " in captured.out
    assert "Backend: incorrect request to backend: " in captured.err


def test_exception(mocker: pytest_mock.MockerFixture, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """Ensure an exception in the backend is not bubbled up."""
    result = str(tmp_path / "result")
    command = json.dumps({"cmd": "dummy_command", "kwargs": {"foo": "bar"}, "result": result})

    backend_proxy = mocker.MagicMock(spec=BackendProxy)
    backend_proxy.side_effect = SystemExit(1)
    backend_proxy.__str__.return_value = "FakeBackendProxy"
    mocker.patch("pyproject_api._backend.BackendProxy", return_value=backend_proxy)
    mocker.patch("pyproject_api._backend.read_line", return_value=bytearray(command, "utf-8"))

    ret = run([str(False), "a.dummy.module"])

    # We still return 0 and write a result file. The exception should *not* bubble up
    assert ret == 0
    captured = capsys.readouterr()
    assert "started backend FakeBackendProxy" in captured.out
    assert "Backend: run command dummy_command with args {'foo': 'bar'}" in captured.out
    assert "Backend: Wrote response " in captured.out
    assert "SystemExit: 1" in captured.err


def test_valid_request(mocker: pytest_mock.MockerFixture, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """Validate the "success" path."""
    result = str(tmp_path / "result")
    command = json.dumps({"cmd": "dummy_command", "kwargs": {"foo": "bar"}, "result": result})

    backend_proxy = mocker.MagicMock(spec=BackendProxy)
    backend_proxy.return_value = "dummy-result"
    backend_proxy.__str__.return_value = "FakeBackendProxy"
    mocker.patch("pyproject_api._backend.BackendProxy", return_value=backend_proxy)
    mocker.patch("pyproject_api._backend.read_line", return_value=bytearray(command, "utf-8"))

    ret = run([str(False), "a.dummy.module"])

    assert ret == 0
    captured = capsys.readouterr()
    assert "started backend FakeBackendProxy" in captured.out
    assert "Backend: run command dummy_command with args {'foo': 'bar'}" in captured.out
    assert "Backend: Wrote response " in captured.out
    assert not captured.err


def test_reuse_process(mocker: pytest_mock.MockerFixture, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """Validate behavior when reusing the backend proxy process.

    There are a couple of things we'd like to check here:

    - Ensure we can actually reuse the process.
    - Ensure an exception in a call to the backend does not affect subsequent calls.
    - Ensure we can exit safely by calling the '_exit' command.
    """
    results = [
        str(tmp_path / "result_a"),
        str(tmp_path / "result_b"),
        str(tmp_path / "result_c"),
        str(tmp_path / "result_d"),
    ]
    commands = [
        json.dumps({"cmd": "dummy_command_a", "kwargs": {"foo": "bar"}, "result": results[0]}),
        json.dumps({"cmd": "dummy_command_b", "kwargs": {"baz": "qux"}, "result": results[1]}),
        json.dumps({"cmd": "dummy_command_c", "kwargs": {"win": "wow"}, "result": results[2]}),
        json.dumps({"cmd": "_exit", "kwargs": {}, "result": results[3]}),
    ]

    def fake_backend(name: str, *args: Any, **kwargs: Any) -> Any:  # ruff:ignore[unused-function-argument]
        if name == "dummy_command_b":
            raise SystemExit(2)

        return "dummy-result"

    backend_proxy = mocker.MagicMock(spec=BackendProxy)
    backend_proxy.side_effect = fake_backend
    backend_proxy.__str__.return_value = "FakeBackendProxy"
    mocker.patch("pyproject_api._backend.BackendProxy", return_value=backend_proxy)
    mocker.patch("pyproject_api._backend.read_line", side_effect=[bytearray(x, "utf-8") for x in commands])

    ret = run([str(True), "a.dummy.module"])

    # We still return 0 and write a result file. The exception should *not* bubble up and all commands should execute.
    # It is the responsibility of the caller to handle errors.
    assert ret == 0
    captured = capsys.readouterr()
    assert "started backend FakeBackendProxy" in captured.out
    assert "Backend: run command dummy_command_a with args {'foo': 'bar'}" in captured.out
    assert "Backend: run command dummy_command_b with args {'baz': 'qux'}" in captured.out
    assert "Backend: run command dummy_command_c with args {'win': 'wow'}" in captured.out
    assert "SystemExit: 2" in captured.err


@pytest.mark.parametrize("code", ["Path('failure.txt')", "b'failure'"])
@pytest.mark.parametrize("previous_success", [False, True])
def test_reused_process_non_serializable_exit(tmp_path: Path, code: str, previous_success: bool) -> None:
    (tmp_path / "exit_backend.py").write_text(
        dedent(f"""
        import os
        from pathlib import Path

        calls = 0

        def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
            global calls
            calls += 1
            print("hook pid={{}} calls={{}}".format(os.getpid(), calls))
            if config_settings["fail"]:
                raise SystemExit({code})
            return "demo-{{}}.whl".format(calls)
        """)
    )
    failures = [False, True, False] if previous_success else [True, False]
    requests = [
        {"cmd": "build_wheel", "kwargs": {"wheel_directory": str(tmp_path), "config_settings": {"fail": fail}}}
        for fail in failures
    ]
    requests.append({"cmd": "_exit", "kwargs": {}})
    result_files = [tmp_path / f"response-{index}.json" for index in range(len(requests))]
    messages = [
        json.dumps({**request, "result": str(path)}) for request, path in zip(requests, result_files, strict=True)
    ]
    completed = subprocess.run(
        [sys.executable, _backend.__file__, "True", "exit_backend"],
        input="\n".join(messages) + "\n",
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(tmp_path)},
        timeout=30,
        check=False,
    )

    # Inspect the failed request first: the previous candidate returns the earlier wheel here.
    failed = json.loads(result_files[failures.index(True)].read_text())
    assert "return" not in failed
    assert failed == {"code": 1, "exc_type": "RuntimeError", "exc_msg": "Failed to serialize backend exception"}
    assert completed.returncode == 0, completed.stderr
    for index, fail in enumerate(failures):
        if not fail:
            assert json.loads(result_files[index].read_text()) == {"return": f"demo-{index + 1}.whl"}
    assert json.loads(result_files[-1].read_text()) == {"return": 0}
    hook_lines = [line for line in completed.stdout.splitlines() if line.startswith("hook pid=")]
    assert len(hook_lines) == len(failures)
    assert len({line.split()[1] for line in hook_lines}) == 1
    assert [line.split()[2] for line in hook_lines] == [f"calls={index + 1}" for index in range(len(failures))]
    assert "SystemExit" in completed.stderr


def test_read_line_success() -> None:
    r, w = os.pipe()
    try:
        line_in = b"this is a line\r\n"
        os.write(w, line_in)
        line_out = read_line(fd=r)
        assert line_out == bytearray(b"this is a line")
    finally:
        os.close(r)
        os.close(w)


def test_read_line_eof_before_newline() -> None:
    r, w = os.pipe()
    try:
        line_in = b"this is a line"
        os.write(w, line_in)
        os.close(w)
        line_out = read_line(fd=r)
        assert line_out == bytearray(b"this is a line")
    finally:
        os.close(r)


def test_read_line_eof_at_the_beginning() -> None:
    r, w = os.pipe()
    try:
        os.close(w)
        with pytest.raises(EOFError):
            read_line(fd=r)
    finally:
        os.close(r)
