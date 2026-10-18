Release History
===============

.. towncrier release notes start

v1.12.0 (2026-10-18)
--------------------
- Validate in-tree backend paths and reject metadata directories that contain the project root.
- Contain response serialization failures.

v1.11.7 (2026-10-15)
--------------------
- Resolve dotted backend object paths.

v1.11.6 (2026-10-14)
--------------------
- Resolve output directories before invoking backends.

v1.11.5 (2026-10-10)
--------------------
- Require Python 3.11, default to Python 3.15, and import in-tree backends from relative roots.

v1.11.4 (2026-10-07)
--------------------
- Stop hanging on undecodable backend output.

v1.11.3 (2026-10-03)
--------------------
- Validate ``build-system`` value types when reading a project folder.

v1.11.2 (2026-09-18)
--------------------
- Avoid pipe deadlocks when sending large backend requests.

v1.11.1 (2026-09-15)
--------------------
- Remove directory symlinks in ``ensure_empty_dir``.

v1.11.0 (2026-07-21)
--------------------
- Add Python 3.15 to the test matrix.

v1.10.1 (2026-05-28)
--------------------
- Move development tooling to ``tox.toml``, dependency groups, and ty.

v1.10.0 (2025-10-09)
--------------------
- Add Python 3.14 support and end support for Python 3.9.

v1.9.1 (2025-05-12)
-------------------
- Remove ``wheel`` from the default requirements.

v1.9.0 (2025-01-21)
-------------------
- Update project maintenance metadata.

v1.8.0 (2024-09-18)
-------------------
- Finish dropping Python 2 support.

v1.7.2 (2024-09-17)
-------------------
- Improve CI.

v1.7.1 (2024-06-22)
-------------------
- Move release notes from the documentation site to GitHub Releases.

v1.7.0 (2024-06-22)
-------------------
- Correct the documentation homepage URL and update build dependencies.

v1.6.1 - (2023-08-29)
---------------------
- Fix :meth:`pyproject_api.Frontend.metadata_from_built` only extracts one of the dist info files.

v1.6.0 - (2023-08-29)
---------------------
- Remove ``build_<wheel|editable>`` from ``prepare_metadata_for_build_<wheel|editable>`` to allow separate config
  parametrization and instead add :meth:`pyproject_api.Frontend.metadata_from_built` the user can call when the prepare
  fails. Pass ``None`` for ``metadata_directory`` for such temporary wheel builds.

v1.5.4 - (2023-08-17)
---------------------
- Make sure that the order of Requires-Dist does not matter

v1.5.3 - (2023-07-06)
---------------------
- Fix ``read_line`` to raise ``EOFError`` if nothing was read

v1.5.2 - (2023-06-14)
---------------------
- Use ruff for linting.
- Drop 2.7 test run.

v1.5.1 - (2023-03-12)
---------------------
- docs: set html_last_updated_fmt to format string

v1.5.0 - (2023-01-17)
---------------------
- When getting metadata from a built wheel, do not pass ``metadata_directory``
  to ``build_wheel``, which forces the backend to generate the metadata - by :user:`masenf`.
  (`#47 <https://github.com/tox-dev/pyproject-api/issues/47>`_)

v1.4.0 - (2023-01-04)
---------------------
- Add minimal CLI for debugging

v1.3.0 - (2023-01-03)
---------------------
- Do not allow exceptions to propagate in backend

v1.2.1 - (2022-12-04)
---------------------
- Fix Python 2 incompatibility on the backend
- Allow skipping prepare metadata for the full build by returning None as basename

v1.2.0 - (2022-12-04)
---------------------
- Expose which optional hooks are present or missing via :meth:`pyproject_api.Frontend.optional_hooks`

v1.1.2 - (2022-10-30)
---------------------
- Fix editable classes not exported at root level

v1.1.1 - (2022-09-10)
---------------------
- Add missed ``wheel`` as test dependency

v1.1.0 - (2022-09-10)
---------------------
- PEP-660 support

v1.0.0 - (2022-09-10)
---------------------
- Use hatchling as build backend
- 3.11 support

v0.1.1 - (2021-12-30)
---------------------
- Drop Python 3.6 support

v0.1.0 - (2021-10-21)
---------------------
- first version
