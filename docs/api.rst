
API
+++

.. currentmodule:: pyproject_api

.. autodata:: __version__

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

Fresh subprocess frontend
-------------------------
.. autoclass:: SubprocessFrontend
