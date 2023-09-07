# Configuration file for the Sphinx documentation builder.

from datetime import date
import sphinx_rtd_theme

# -- Project information

project = "PyGraft"
copyright = f"2023-{date.today().year}, Nicolas Hubert"
author = "Nicolas Hubert"

release = "0.1.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    'sphinxcontrib.bibtex',
    "sphinxemoji.sphinxemoji",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

bibtex_bibfiles = ['bibliography.bib']
sphinxemoji_style = "twemoji"

# -- Extension configuration

# -- Options for intersphinx extension

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None)
}

# generate autosummary pages
autosummary_generate = True

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']
# The master toctree document.
master_doc = "index"
language = "en"
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# General information about the project.
project = 'PyGraft'
copyright = 'PyGraft is licensed under the MIT License'
author = 'Nicolas Hubert'

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'style_nav_header_background': '#FFFFFF',
}

# html_static_path = ["_static"]
html_css_files = [
    'style.css'
]
html_logo = "logo.svg"

# -- Options for HTMLHelp output

# Output file base name for HTML help builder.
htmlhelp_basename = "PyGraftdoc"

# -- Options for EPUB output
epub_show_urls = "footnote"
