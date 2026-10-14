``pyproject-api``
=================

``pyproject-api`` aims to abstract away interaction with ``pyproject.toml`` style projects in a flexible way.

The CLI accepts a relative project directory and resolves a relative ``--outdir`` from the caller's working directory.
Without ``--outdir``, distributions are written to ``dist`` inside the project directory.

.. toctree::
   :hidden:

   self
   api
