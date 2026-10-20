Release History
===============

.. towncrier release notes start

.. _release-1-12-0:

v1.12.0 (2026-10-18)
--------------------

.. _release-1-12-0-fixed:

Fixed
^^^^^

- Validate in-tree backend paths and reject metadata directories that contain the project root.
- Contain response serialization failures.

.. _release-1-11-7:

v1.11.7 (2026-10-15)
--------------------

.. _release-1-11-7-fixed:

Fixed
^^^^^

- Resolve dotted backend object paths.

.. _release-1-11-6:

v1.11.6 (2026-10-14)
--------------------

.. _release-1-11-6-fixed:

Fixed
^^^^^

- Resolve output directories before invoking backends.

.. _release-1-11-5:

v1.11.5 (2026-10-10)
--------------------

.. _release-1-11-5-added:

Added
^^^^^

- Require Python 3.11 or newer and default to Python 3.15.

.. _release-1-11-5-fixed:

Fixed
^^^^^

- Import in-tree backends from relative roots.

.. _release-1-11-4:

v1.11.4 (2026-10-07)
--------------------

.. _release-1-11-4-fixed:

Fixed
^^^^^

- Stop hanging on undecodable backend output.

.. _release-1-11-3:

v1.11.3 (2026-10-03)
--------------------

.. _release-1-11-3-fixed:

Fixed
^^^^^

- Validate ``build-system`` value types when reading a project folder.

.. _release-1-11-2:

v1.11.2 (2026-09-18)
--------------------

.. _release-1-11-2-fixed:

Fixed
^^^^^

- Avoid pipe deadlocks when sending large backend requests.

.. _release-1-11-1:

v1.11.1 (2026-09-15)
--------------------

.. _release-1-11-1-fixed:

Fixed
^^^^^

- Remove directory symlinks in ``ensure_empty_dir``.

.. _release-1-11-0:

v1.11.0 (2026-07-21)
--------------------

.. _release-1-11-0-added:

Added
^^^^^

- Support Python 3.15.

.. _release-1-10-1:

v1.10.1 (2026-05-28)
--------------------

.. _release-1-10-0:

v1.10.0 (2025-10-09)
--------------------

.. _release-1-10-0-added:

Added
^^^^^

- Support Python 3.14.
- End support for Python 3.9.

.. _release-1-9-1:

v1.9.1 (2025-05-12)
-------------------

.. _release-1-9-1-changes:

Changes
^^^^^^^

- Remove ``wheel`` from the default requirements.

.. _release-1-9-0:

v1.9.0 (2025-01-21)
-------------------

.. _release-1-9-0-added:

Added
^^^^^

- End support for Python 3.8.

.. _release-1-8-0:

v1.8.0 (2024-09-18)
-------------------

.. _release-1-8-0-added:

Added
^^^^^

- Finish dropping Python 2 support.

.. _release-1-7-2:

v1.7.2 (2024-09-17)
-------------------

.. _release-1-7-1:

v1.7.1 (2024-06-22)
-------------------

.. _release-1-7-1-documentation:

Documentation
^^^^^^^^^^^^^

- Move release notes from the documentation site to GitHub Releases.

.. _release-1-7-0:

v1.7.0 (2024-06-22)
-------------------

.. _release-1-7-0-documentation:

Documentation
^^^^^^^^^^^^^

- Correct the documentation homepage URL.

.. _release-1-7-0-packaging:

Packaging
^^^^^^^^^

- Update build dependencies.

.. _release-1-6-1:

v1.6.1 (2023-08-29)
-------------------

.. _release-1-6-1-fixed:

Fixed
^^^^^

- Fix :meth:`pyproject_api.Frontend.metadata_from_built` only extracts one of the dist info files.

.. _release-1-6-0:

v1.6.0 (2023-08-29)
-------------------

.. _release-1-6-0-changes:

Changes
^^^^^^^

- Remove ``build_<wheel|editable>`` from ``prepare_metadata_for_build_<wheel|editable>`` to allow separate config
  parametrization and instead add :meth:`pyproject_api.Frontend.metadata_from_built` the user can call when the prepare
  fails. Pass ``None`` for ``metadata_directory`` for such temporary wheel builds.

.. _release-1-5-4:

v1.5.4 (2023-08-17)
-------------------

.. _release-1-5-4-fixed:

Fixed
^^^^^

- Make sure that the order of Requires-Dist does not matter

.. _release-1-5-3:

v1.5.3 (2023-07-06)
-------------------

.. _release-1-5-3-fixed:

Fixed
^^^^^

- Fix ``read_line`` to raise ``EOFError`` if nothing was read

.. _release-1-5-2:

v1.5.2 (2023-06-14)
-------------------

.. _release-1-5-1:

v1.5.1 (2023-03-12)
-------------------

.. _release-1-5-1-documentation:

Documentation
^^^^^^^^^^^^^

- docs: set html_last_updated_fmt to format string

.. _release-1-5-0:

v1.5.0 (2023-01-17)
-------------------

.. _release-1-5-0-fixed:

Fixed
^^^^^

- When getting metadata from a built wheel, do not pass ``metadata_directory`` to ``build_wheel``, which forces the
  backend to generate the metadata by :user:`masenf` (:issue:`47`).

.. _release-1-4-0:

v1.4.0 (2023-01-04)
-------------------

.. _release-1-4-0-added:

Added
^^^^^

- Add minimal CLI for debugging

.. _release-1-3-0:

v1.3.0 (2023-01-03)
-------------------

.. _release-1-3-0-fixed:

Fixed
^^^^^

- Do not allow exceptions to propagate in backend

.. _release-1-2-1:

v1.2.1 (2022-12-04)
-------------------

.. _release-1-2-1-added:

Added
^^^^^

- Allow skipping prepare metadata for the full build by returning None as basename

.. _release-1-2-1-fixed:

Fixed
^^^^^

- Fix Python 2 incompatibility on the backend

.. _release-1-2-0:

v1.2.0 (2022-12-04)
-------------------

.. _release-1-2-0-added:

Added
^^^^^

- Expose which optional hooks are present or missing via :meth:`pyproject_api.Frontend.optional_hooks`

.. _release-1-1-2:

v1.1.2 (2022-10-30)
-------------------

.. _release-1-1-2-fixed:

Fixed
^^^^^

- Fix editable classes not exported at root level

.. _release-1-1-1:

v1.1.1 (2022-09-10)
-------------------

.. _release-1-1-0:

v1.1.0 (2022-09-10)
-------------------

.. _release-1-1-0-added:

Added
^^^^^

- PEP-660 support

.. _release-1-0-0:

v1.0.0 (2022-09-10)
-------------------

.. _release-1-0-0-added:

Added
^^^^^

- Support Python 3.11.

.. _release-1-0-0-packaging:

Packaging
^^^^^^^^^

- Use Hatchling as the build backend.

.. _release-0-1-1:

v0.1.1 (2021-12-30)
-------------------

.. _release-0-1-1-added:

Added
^^^^^

- Drop Python 3.6 support

.. _release-0-1-0:

v0.1.0 (2021-10-21)
-------------------

.. _release-0-1-0-added:

Added
^^^^^

- first version
