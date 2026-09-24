# Sphinx configuration for the sciro API reference (the same toolchain as
# docs.pybricks.com: autodoc over the typed stubs).
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# The upstream pybricks stubs give their enums a metaclass __dir__ that raises
# ("'type' object is not iterable") when autodoc lists class members. Replace
# it with the plain type.__dir__ for the documentation build.
from pybricks import parameters as _pybricks_parameters  # noqa: E402

_pybricks_parameters._PybricksEnumMeta.__dir__ = lambda cls: list(type.__dir__(cls))

project = "sciro"
copyright = "2026 Sciurus Robotics"
author = "Sciurus Robotics"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autodoc_default_options = {"members": True, "undoc-members": False}
# The MaybeAwaitable* helpers are typing-only; show them by name.
autodoc_type_aliases = {}
napoleon_google_docstring = True

intersphinx_mapping = {
    "pybricks": ("https://docs.pybricks.com/en/stable/", None),
}

html_theme = "furo"
html_title = "sciro API reference"
html_static_path = []
