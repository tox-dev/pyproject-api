``pyproject-api``
=================

``pyproject-api`` aims to abstract away interaction with ``pyproject.toml`` style projects in a flexible way.

API
+++

.. currentmodule:: pyproject_api

.. autodata:: __version__

Frontend
--------
.. autoclass:: Frontend

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

Wheel metadata
~~~~~~~~~~~~~~
.. autoclass:: MetadataForBuildWheelResult

Source distribution
~~~~~~~~~~~~~~~~~~~
.. autoclass:: SdistResult

Wheel
~~~~~
.. autoclass:: WheelResult

Fresh subprocess frontend
-------------------------
.. autoclass:: SubprocessFrontend

.. toctree::
   :hidden:

   self
   changelog
