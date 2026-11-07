Replace a symlink passed to ``ensure_empty_dir`` instead of following it, so a dangling link no longer raises
``FileExistsError`` and a link to a directory no longer has its target emptied.
