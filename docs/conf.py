# noqa: D100
from __future__ import annotations

from pyproject_api import __version__

project = name = "pyproject_api"
company = "tox-dev"
copyright = f"{company}"  # noqa: A001
version, release = __version__, __version__.split("+")[0]

extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]
master_doc, source_suffix = "index", ".rst"

html_theme = "furo"
html_title, html_last_updated_fmt = "pyproject-api docs", "%Y-%m-%dT%H:%M:%S"
pygments_style, pygments_dark_style = "sphinx", "monokai"

autoclass_content, autodoc_typehints = "both", "none"
autodoc_default_options = {"members": True, "member-order": "bysource", "undoc-members": True, "show-inheritance": True}
inheritance_alias = {}

extlinks = {
    "issue": ("https://github.com/tox-dev/pyproject-api/issues/%s", "#%s"),
    "pull": ("https://github.com/tox-dev/pyproject-api/pull/%s", "PR #%s"),
    "user": ("https://github.com/%s", "@%s"),
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "packaging": ("https://packaging.pypa.io/en/latest", None),
}

nitpicky = True
nitpick_ignore = []
