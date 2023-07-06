from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

import pytest

from pyproject_api._backend import BackendProxy, read_line, run

if TYPE_CHECKING:
    from pathlib import Path

    import pytest_mock


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

    def fake_backend(name: str, *args: Any, **kwargs: Any) -> Any:  # noqa: ARG001
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
