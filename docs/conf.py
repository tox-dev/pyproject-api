# ruff:ignore[undocumented-public-module]  # Sphinx executes this file as configuration, nothing imports it
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Final

from sphinx.domains.python import PythonDomain

from pyproject_api import __version__

if TYPE_CHECKING:
    from docutils.nodes import Element, reference
    from sphinx.addnodes import pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
project = name = "pyproject_api"
company: Final[str] = "tox-dev"
project_copyright: Final[str] = f"{company}"
version, release = __version__, __version__.split("+")[0]

extensions = [
    "sphinx_llm.txt",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.towncrier.ext",
]
master_doc, source_suffix = "index", ".rst"
exclude_patterns = ["changelog.d/*"]
autosectionlabel_maxdepth: Final[int] = 2
towncrier_draft_autoversion_mode: Final[str] = "draft"
towncrier_draft_include_empty: Final[bool] = True
towncrier_draft_working_directory = Path(__file__).parent.parent

html_theme: Final[str] = "furo"
html_title, html_last_updated_fmt = "pyproject-api docs", "%Y-%m-%dT%H:%M:%S"
pygments_style, pygments_dark_style = "sphinx", "monokai"

autoclass_content, autodoc_typehints = "both", "none"
autodoc_default_options = {"members": True, "member-order": "bysource", "undoc-members": True, "show-inheritance": True}
inheritance_alias = {}

extlinks = {
    "issue": ("https://github.com/tox-dev/pyproject-api/issues/%s", "#%s"),
    "pull": ("https://github.com/tox-dev/pyproject-api/pull/%s", "PR #%s"),
    "pr": ("https://github.com/tox-dev/pyproject-api/pull/%s", "PR #%s"),
    "user": ("https://github.com/%s", "@%s"),
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "packaging": ("https://packaging.pypa.io/en/latest", None),
}

nitpicky: Final[bool] = True
nitpick_ignore = []


def setup(app: Sphinx) -> None:
    class PatchedPythonDomain(PythonDomain):
        def resolve_xref(  # ruff:ignore[too-many-arguments, too-many-positional-arguments]  # the signature is Sphinx's resolve_xref override
            self,
            env: BuildEnvironment,
            fromdocname: str,
            builder: Builder,
            type: str,  # ruff:ignore[builtin-argument-shadowing]  # the name is fixed by Sphinx's resolve_xref signature
            target: str,
            node: pending_xref,
            contnode: Element,
        ) -> reference | None:
            # fixup some wrongly resolved mappings
            mapping = {
                "pathlib._local.Path": "pathlib.Path",
            }
            if target in mapping:
                target = node["reftarget"] = mapping[target]
            return super().resolve_xref(env, fromdocname, builder, type, target, node, contnode)

    app.add_domain(PatchedPythonDomain, override=True)


markdown_http_base = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
