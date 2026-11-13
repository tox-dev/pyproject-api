"""
Handles communication on the backend side between frontend and backend.

Please keep this file Python 2.7 compatible.
See https://tox.readthedocs.io/en/rewrite/development.html#code-style-guide
"""

import importlib
import json
import locale
import os
import sys
import traceback


class MissingCommand(TypeError):  # ruff:ignore[error-suffix-on-exception-name]  # the frontend reports it by this name  # simplint: ignore[missing-from-all]  # backend-only exception
    ...


class BackendProxy:  # simplint: ignore[missing-from-all]  # backend-only proxy
    def __init__(self, backend_module, backend_obj):
        self.backend_module = backend_module
        self.backend_object = backend_obj
        backend = importlib.import_module(self.backend_module)
        if self.backend_object:
            for name in self.backend_object.split("."):
                backend = getattr(backend, name)
        self.backend = backend

    def __call__(self, name, *args, **kwargs):
        on_object = self if name.startswith("_") else self.backend
        if not hasattr(on_object, name):
            msg = f"{on_object!r} has no attribute {name!r}"
            raise MissingCommand(msg)
        return getattr(on_object, name)(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(backend={self.backend})"

    def _exit(self):  # ruff:ignore[no-self-use]  # called through BackendProxy.__call__
        return 0

    def _optional_hooks(self):
        return {
            k: hasattr(self.backend, k)
            for k in (
                "get_requires_for_build_sdist",
                "prepare_metadata_for_build_wheel",
                "get_requires_for_build_wheel",
                "build_editable",
                "get_requires_for_build_editable",
                "prepare_metadata_for_build_editable",
            )
        }


def flush():  # simplint: ignore[missing-from-all]  # backend-only output helper
    sys.stderr.flush()
    sys.stdout.flush()


def run(argv):  # simplint: ignore[missing-from-all]  # backend script entry point
    reuse_process = argv[0].lower() == "true"
    try:
        backend_proxy = BackendProxy(argv[1], None if len(argv) == 2 else argv[2])  # ruff:ignore[magic-value-comparison]  # argv may omit the backend object
    except BaseException:
        print("failed to start backend", file=sys.stderr)
        raise
    else:
        print(f"started backend {backend_proxy}", file=sys.stdout)
    finally:
        flush()  # pragma: no branch # the finally runs on both paths
    while True:
        content = read_line()
        if not content:
            continue
        flush()  # flush any output generated before
        # ignore messages that are not valid JSON and contain a valid result path
        try:
            parsed_message, result_file = _parse_request(content)
        except Exception:  # ruff:ignore[blind-except]  # any malformed request is reported and skipped
            print(f"Backend: incorrect request to backend: {content}", file=sys.stderr)
            flush()
        else:
            result, response = _execute(backend_proxy, parsed_message)
            _write_response(result_file, result, response)
            if "return" in result and parsed_message.get("cmd") == "_exit":
                break
        if reuse_process is False:  # pragma: no branch # no test for reuse process in root test env
            break
    return 0


def _parse_request(content):
    # python 2 does not support loading from bytearray
    if sys.version_info[0] == 2:  # pragma: no branch # only python 2 takes this path
        content = content.decode()  # pragma: no cover # only python 2 takes this path
    parsed_message = json.loads(content)
    return parsed_message, parsed_message["result"]


def _execute(backend_proxy, parsed_message):
    result = {}
    try:
        cmd = parsed_message["cmd"]
        print("Backend: run command {} with args {}".format(cmd, parsed_message["kwargs"]))
        result["return"] = backend_proxy(cmd, **parsed_message["kwargs"])
        return result, json.dumps(result)
    except BaseException as exception:  # ruff:ignore[blind-except]  # every failure is sent back to the frontend
        try:
            result = {
                "code": exception.code if isinstance(exception, SystemExit) else 1,
                "exc_type": exception.__class__.__name__,
                "exc_msg": str(exception),
            }
            response = json.dumps(result)
        except BaseException:  # ruff:ignore[blind-except]  # the exception itself may not serialize
            result = {
                "code": 1,
                "exc_type": "RuntimeError",
                "exc_msg": "Failed to serialize backend exception",
            }
            response = json.dumps(result)
        if not isinstance(exception, MissingCommand):  # for missing command do not print stack
            traceback.print_exc()
        return result, response


def _write_response(result_file, result, response):
    try:
        encoding = locale.getpreferredencoding(do_setlocale=False)
        with open(  # ruff:ignore[builtin-open, write-whole-file]  # the module stays Python 2.7 compatible
            result_file, "w", encoding=encoding
        ) as file_handler:
            file_handler.write(response)
    except Exception:  # ruff:ignore[blind-except]  # the frontend learns of the failure from the missing response
        traceback.print_exc()
    finally:
        # used as done marker by frontend
        print(f"Backend: Wrote response {result} to {result_file}")
        flush()  # pragma: no branch # the finally runs on every path


def read_line(fd=0):  # simplint: ignore[missing-from-all]  # backend-only input helper
    # for some reason input() seems to break (hangs forever) so instead we read byte by byte the unbuffered stream
    content = bytearray()
    while True:
        char = os.read(fd, 1)
        if not char:
            if not content:
                msg = "EOF without reading anything"
                raise EOFError(msg)  # we didn't get a line at all, let the caller know
            break  # pragma: no cover # covered by test_read_line_eof_before_newline
        if char == b"\n":
            break
        if char != b"\r":
            content += char
    return content


if __name__ == "__main__":
    # printed paths may hold characters the stdout encoding cannot represent
    sys.stdout.reconfigure(errors="backslashreplace")  # type: ignore[unresolved-attribute]  # stub says TextIO
    sys.exit(run(sys.argv[1:]))
