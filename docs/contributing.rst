Contributing
============

Add a release note when a pull request changes the API, supported Python versions, package installation, or documented
behavior. Put each distinct change in its own ``docs/changelog.d/+short-name.<category>.rst`` file. The name need not
contain a pull request number; release preparation links it to the squash-merged pull request.

Use ``feature`` for new behavior and Python support changes, ``change`` for changes to existing behavior, ``bugfix``
for corrections, and ``doc`` for documentation changes users need to know about. Use ``security``, ``performance``,
``deprecation``, ``removal``, or ``packaging`` when those describe a user-facing change more precisely. The rendered
changelog calls the first four categories Added, Changes, Fixed, and Documentation. Empty categories are omitted.

For example, a change to backend path handling can use ``docs/changelog.d/+backend-paths.bugfix.rst``:

.. code-block:: rst

   Resolve in-tree backend paths relative to the project root.

Keep a fragment focused on its effect for users. The release process adds the pull request link and human author
credit, so the fragment should not contain either. A maintenance-only pull request can use the ``skip news`` label;
the label can be added after the pull request opens. Bot pull requests without a fragment get that label automatically.
If a bot pull request does include a fragment, it is published without crediting the bot as an author.

Run ``prek run --all-files`` before pushing. Release preparation runs the same hooks on the assembled changelog before
it creates a commit and tag.
