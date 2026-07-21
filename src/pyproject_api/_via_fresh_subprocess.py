from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from subprocess import PIPE, Popen  # ruff:ignore[suspicious-subprocess-import]
from threading import Thread
from typing import IO, TYPE_CHECKING, Any, cast

from ._frontend import CmdStatus, Frontend

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from packaging.requirements import Requirement


class SubprocessCmdStatus(CmdStatus, Thread):
    def __init__(self, process: Popen[str]) -> None:
        super().__init__()
        self.process = process
        self._out_err: tuple[str, str] | None = None
        self.start()

    def run(self) -> None:
        self._out_err = self.process.communicate()

    @property
    def done(self) -> bool:
        # communicate() sets returncode before run() stores what it returned, so a caller polling the process can
        # reach out_err() while it still holds None. Free-threaded builds land in that window; report the command
        # finished only once its output is actually there.
        return self._out_err is not None

    def out_err(self) -> tuple[str, str]:
        return cast("tuple[str, str]", self._out_err)


class SubprocessFrontend(Frontend):
    """A frontend that creates fresh subprocess at every call to communicate with the backend."""

    def __init__(
        self,
        root: Path,
        backend_paths: tuple[Path, ...],
        backend_module: str,
        backend_obj: str | None,
        requires: tuple[Requirement, ...],
    ) -> None:
        """
        Create a subprocess frontend.

        :param root: the root path to the built project
        :param backend_paths: paths that are available on the python path for the backend
        :param backend_module: module where the backend is located
        :param backend_obj: object within the backend module identifying the backend
        :param requires: seed requirements for the backend
        """
        super().__init__(root, backend_paths, backend_module, backend_obj, requires, reuse_backend=False)
        self.executable = sys.executable

    @contextmanager
    def _send_msg(self, cmd: str, result_file: Path, msg: str) -> Iterator[SubprocessCmdStatus]:  # ruff:ignore[unused-method-argument]
        env = os.environ.copy()
        backend = os.pathsep.join(str(i) for i in self._backend_paths).strip()
        if backend:
            env["PYTHONPATH"] = backend
        process = Popen(
            args=[self.executable, *self.backend_args],
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            universal_newlines=True,
            cwd=self._root,
            env=env,
        )
        cast("IO[str]", process.stdin).write(f"{os.linesep}{msg}{os.linesep}")
        yield SubprocessCmdStatus(process)

    def send_cmd(self, cmd: str, **kwargs: Any) -> tuple[Any, str, str]:
        """
        Send a command to the backend.

        :param cmd: the command to send
        :param kwargs: keyword arguments to the backend
        :return: a tuple of: backend response, standard output text, standard error text
        """
        return self._send(cmd, **kwargs)


__all__ = ("SubprocessFrontend",)
