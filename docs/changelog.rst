Release History
===============

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
