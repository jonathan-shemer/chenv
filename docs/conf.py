"""Sphinx configuration."""
from datetime import datetime


project = "chenv"
author = "Jonathan Shemer"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
html_static_path = []
