Release History
===============

.. towncrier-draft-entries:: Draft

.. towncrier release notes start

.. _release-1-12-2:

v1.12.2 (2026-10-28)
--------------------

.. _release-1-12-2-fixed:

Fixed
^^^^^

- Drop the backend proxy stub declarations for its private commands; one named a method the proxy does not have
  (:pr:`331`) by :user:`tridev-tej` and :user:`gaborbernat`.
- Keep a trailing space in the last backend path when putting it on ``PYTHONPATH`` (:pr:`329`) by :user:`jdotc1` and
  :user:`gaborbernat`.
- Preserve ``BackendFailed`` details when copying or pickling an exception, including when a build runs in a process
  pool (:pr:`337`) by :user:`jdotc1`.
- Stop the backend from crashing when it prints a path its standard output encoding cannot represent (:pr:`330`) by
  :user:`nk-batman21` and :user:`gaborbernat`.
- Stop the backend process and join its output collection thread when a frontend call is interrupted (:pr:`332`) by
  :user:`zfz2005` and :user:`gaborbernat`.

.. _release-1-12-1:

v1.12.1 (2026-10-27)
--------------------

.. _release-1-12-1-packaging:

Packaging
^^^^^^^^^

- Releases now run on the shared tox-dev/github-workflows pipeline, with a locked release toolchain and generated GitHub
  Release notes (:pr:`338`) by :user:`gaborbernat`.

.. _release-1-12-0:

v1.12.0 (2026-10-18)
--------------------

.. _release-1-12-0-fixed:

Fixed
^^^^^

- Validate in-tree backend paths (:pull:`320`) by :user:`blouirts123`.
- Reject metadata directories that contain the project root (:pull:`323`) by :user:`edsonsims`.
- Contain response serialization failures (:pull:`322`) by :user:`AryanRG`.

.. _release-1-12-0-documentation:

Documentation
^^^^^^^^^^^^^

- Correct the frontend construction example (:pull:`321`) by :user:`travisfortney`.

.. _release-1-11-7:

v1.11.7 (2026-10-15)
--------------------

.. _release-1-11-7-fixed:

Fixed
^^^^^

- Resolve dotted backend object paths (:pull:`319`) by :user:`gaborbernat`.

.. _release-1-11-6:

v1.11.6 (2026-10-14)
--------------------

.. _release-1-11-6-fixed:

Fixed
^^^^^

- Resolve output directories before invoking backends (:pull:`316`) by :user:`harbinresearcher`.

.. _release-1-11-5:

v1.11.5 (2026-10-10)
--------------------

.. _release-1-11-5-added:

Added
^^^^^

- Require Python 3.11 or newer (:pull:`312`) by :user:`gaborbernat`.

.. _release-1-11-5-changes:

Changes
^^^^^^^

- Use Python 3.15 by default (:pull:`312`) by :user:`gaborbernat`.

.. _release-1-11-5-fixed:

Fixed
^^^^^

- Import in-tree backends from relative roots (:pull:`313`) by :user:`ac1982`.

.. _release-1-11-4:

v1.11.4 (2026-10-07)
--------------------

.. _release-1-11-4-fixed:

Fixed
^^^^^

- Stop hanging on undecodable backend output (:pull:`311`) by :user:`xiehuanyi`.

.. _release-1-11-3:

v1.11.3 (2026-10-03)
--------------------

.. _release-1-11-3-fixed:

Fixed
^^^^^

- Validate ``build-system`` value types when reading a project folder (:pull:`309`) by :user:`pasmud`.

.. _release-1-11-3-documentation:

Documentation
^^^^^^^^^^^^^

- Correct build result streams and dependency descriptions (:pull:`303`) by :user:`agammann`.

.. _release-1-11-2:

v1.11.2 (2026-09-18)
--------------------

.. _release-1-11-2-fixed:

Fixed
^^^^^

- Avoid pipe deadlocks when sending large backend requests (:pull:`302`) by :user:`caamer20`.

.. _release-1-11-1:

v1.11.1 (2026-09-15)
--------------------

.. _release-1-11-1-fixed:

Fixed
^^^^^

- Remove directory symlinks in ``ensure_empty_dir`` (:pull:`300`) by :user:`Str0k`.

.. _release-1-11-1-documentation:

Documentation
^^^^^^^^^^^^^

- Fix the documentation links in the PyPI project description (:pull:`291`) by :user:`webknjaz`.
- Publish ``llms.txt`` from the documentation build (:pull:`292`) by :user:`gaborbernat`.

.. _release-1-11-0:

v1.11.0 (2026-07-21)
--------------------

.. _release-1-11-0-added:

Added
^^^^^

- Support Python 3.15 (:pull:`282`) by :user:`gaborbernat`.

.. _release-1-10-1:

v1.10.1 (2026-05-28)
--------------------

.. _release-1-10-0:

v1.10.0 (2025-10-09)
--------------------

.. _release-1-10-0-added:

Added
^^^^^

- Support Python 3.14 (:pull:`216`) by :user:`gaborbernat`.
- End support for Python 3.9 (:pull:`216`) by :user:`gaborbernat`.

.. _release-1-9-1:

v1.9.1 (2025-05-12)
-------------------

.. _release-1-9-1-changes:

Changes
^^^^^^^

- Remove ``wheel`` from the default requirements (:pull:`192`) by :user:`gaborbernat`.

.. _release-1-9-0:

v1.9.0 (2025-01-21)
-------------------

.. _release-1-9-0-added:

Added
^^^^^

- End declared support for Python 3.8.

.. _release-1-8-0:

v1.8.0 (2024-09-18)
-------------------

.. _release-1-8-0-added:

Added
^^^^^

- Remove backend compatibility with Python 3.8 and older (:pull:`154`) by :user:`kloczek`.

.. _release-1-7-2:

v1.7.2 (2024-09-17)
-------------------

.. _release-1-7-1:

v1.7.1 (2024-06-22)
-------------------

.. _release-1-7-1-documentation:

Documentation
^^^^^^^^^^^^^

- Move release notes from the documentation site to GitHub Releases (:pull:`141`) by :user:`gaborbernat`.

.. _release-1-7-0:

v1.7.0 (2024-06-22)
-------------------

.. _release-1-7-0-documentation:

Documentation
^^^^^^^^^^^^^

- Correct the documentation homepage URL (:pull:`116`) by :user:`bernardcooke53`.

.. _release-1-6-1:

v1.6.1 (2023-08-29)
-------------------

.. _release-1-6-1-fixed:

Fixed
^^^^^

- Extract every dist-info file in :meth:`pyproject_api.Frontend.metadata_from_built` (:pull:`100`) by
  :user:`gaborbernat`.

.. _release-1-6-0:

v1.6.0 (2023-08-29)
-------------------

.. _release-1-6-0-changes:

Changes
^^^^^^^

- Separate the build and metadata preparation configuration for wheels and editable installs (:pull:`99`) by
  :user:`gaborbernat`.
- Add :meth:`pyproject_api.Frontend.metadata_from_built` for metadata preparation failures (:pull:`99`) by
  :user:`gaborbernat`.
- Pass ``None`` for ``metadata_directory`` when building a temporary wheel (:pull:`99`) by :user:`gaborbernat`.

.. _release-1-5-4:

v1.5.4 (2023-08-17)
-------------------

.. _release-1-5-4-fixed:

Fixed
^^^^^

- Ignore the order of ``Requires-Dist`` metadata entries (:pull:`95`) by :user:`frenzymadness`.

.. _release-1-5-3:

v1.5.3 (2023-07-06)
-------------------

.. _release-1-5-3-fixed:

Fixed
^^^^^

- Raise ``EOFError`` when ``read_line`` cannot read anything (:pull:`86`) by :user:`sk1p`.

.. _release-1-5-2:

v1.5.2 (2023-06-14)
-------------------

.. _release-1-5-2-added:

Added
^^^^^

- Support Python 3.12 (:pull:`74`) by :user:`gaborbernat`.

.. _release-1-5-1:

v1.5.1 (2023-03-12)
-------------------

.. _release-1-5-1-documentation:

Documentation
^^^^^^^^^^^^^

- Show the last updated date in the documentation (:pull:`54`) by :user:`paravoid`.

.. _release-1-5-0:

v1.5.0 (2023-01-17)
-------------------

.. _release-1-5-0-fixed:

Fixed
^^^^^

- Omit ``metadata_directory`` when building a wheel to get metadata, so the backend generates it (:pull:`48`,
  :issue:`47`) by :user:`masenf`.

.. _release-1-4-0:

v1.4.0 (2023-01-04)
-------------------

.. _release-1-4-0-added:

Added
^^^^^

- Add a minimal CLI for debugging (:pull:`42`) by :user:`stephenfin`.

.. _release-1-3-0:

v1.3.0 (2023-01-03)
-------------------

.. _release-1-3-0-fixed:

Fixed
^^^^^

- Contain exceptions from backend hooks (:pull:`40`) by :user:`stephenfin`.

.. _release-1-2-1:

v1.2.1 (2022-12-04)
-------------------

.. _release-1-2-1-added:

Added
^^^^^

- Allow skipping metadata preparation for a full build by returning ``None`` as the basename by :user:`gaborbernat`.

.. _release-1-2-1-fixed:

Fixed
^^^^^

- Fix Python 2 compatibility in the backend by :user:`gaborbernat`.

.. _release-1-2-0:

v1.2.0 (2022-12-04)
-------------------

.. _release-1-2-0-added:

Added
^^^^^

- Expose which optional hooks are present or missing via :meth:`pyproject_api.Frontend.optional_hooks` by
  :user:`gaborbernat`.

.. _release-1-1-2:

v1.1.2 (2022-10-30)
-------------------

.. _release-1-1-2-documentation:

Documentation
^^^^^^^^^^^^^

- Restore the project documentation and API index by :user:`gaborbernat`.

.. _release-1-1-2-fixed:

Fixed
^^^^^

- Export editable classes from the package root by :user:`gaborbernat`.

.. _release-1-1-1:

v1.1.1 (2022-09-10)
-------------------

.. _release-1-1-0:

v1.1.0 (2022-09-10)
-------------------

.. _release-1-1-0-added:

Added
^^^^^

- Support editable installs under PEP 660 (:pull:`21`) by :user:`gaborbernat`.

.. _release-1-0-0:

v1.0.0 (2022-09-10)
-------------------

.. _release-1-0-0-added:

Added
^^^^^

- Support Python 3.11 by :user:`gaborbernat`.

.. _release-1-0-0-packaging:

Packaging
^^^^^^^^^

- Use Hatchling as the build backend by :user:`gaborbernat`.

.. _release-0-1-1:

v0.1.1 (2021-12-30)
-------------------

.. _release-0-1-1-added:

Added
^^^^^

- End support for Python 3.6 by :user:`gaborbernat`.

.. _release-0-1-0:

v0.1.0 (2021-10-21)
-------------------

.. _release-0-1-0-added:

Added
^^^^^

- Publish the initial pyproject-api release by :user:`gaborbernat`.
