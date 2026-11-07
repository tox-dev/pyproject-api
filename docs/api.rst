
API
+++

.. currentmodule:: pyproject_api

.. data:: __version__

   The semantic version of the project.

Frontend
--------
.. autoclass:: Frontend

Build and metadata directory arguments may be relative to the caller's current
working directory. They are passed to the backend as absolute paths, since the
backend runs from the project directory. Result paths retain the spelling of the
directory argument. Configuration settings and generic command arguments are
passed through unchanged.

Metadata preparation replaces a symlink used as the output directory with a real directory, leaving the link target
untouched. Dangling links are replaced too. Paths resolving to the project root or one of its ancestors are still
rejected before cleanup.

Metadata preparation clears the output directory before calling the metadata hook. If cleanup fails, the filesystem
error propagates and the hook is not called. When extracting metadata from a built wheel, cleanup errors stop extraction
after the wheel has been built.

.. autoclass:: OptionalHooks

Exceptions
----------

Backend failed
~~~~~~~~~~~~~~
.. autoclass:: BackendFailed

Results
-------

Build source distribution requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: RequiresBuildSdistResult

Build wheel requires
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: RequiresBuildWheelResult

Editable requires
~~~~~~~~~~~~~~~~~
.. autoclass:: RequiresBuildEditableResult

Wheel metadata
~~~~~~~~~~~~~~
.. autoclass:: MetadataForBuildWheelResult

Editable metadata
~~~~~~~~~~~~~~~~~
.. autoclass:: MetadataForBuildEditableResult

Source distribution
~~~~~~~~~~~~~~~~~~~
.. autoclass:: SdistResult

Editable
~~~~~~~~
.. autoclass:: EditableResult

Wheel
~~~~~
.. autoclass:: WheelResult

Frontend arguments
~~~~~~~~~~~~~~~~~~
.. autoclass:: FrontendArgs

Built metadata
~~~~~~~~~~~~~~
.. autoclass:: BuiltMetadata

Fresh subprocess frontend
-------------------------
.. autoclass:: SubprocessFrontend
