Release History
===============

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

v1.4.0 - (2022-01-04)
---------------------
- Add minimal CLI for debugging

v1.3.0 - (2022-01-03)
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

v0.0.1 - (2021-12-30)
---------------------
- Drop Python 3.6 support

v0.1.0 - (2021-10-21)
---------------------
- first version
