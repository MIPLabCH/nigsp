# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import nigsp  # noqa

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "nigsp"
copyright = "2022, Stefano Moia, EPFL"
author = "Stefano Moia"

# Import project to get version info
sys.path.insert(0, os.path.abspath(os.path.pardir))

# The short X.Y version
version = nigsp.__version__
# The full version, including alpha/beta/rc tags
release = nigsp.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.import sphinx_rtd_theme  # noqa

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxarg.ext",
    "myst_parser",
]

# Generate the API documentation when building
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": False,
    "exclude-members": "LGR",
}

numpydoc_show_class_members = False
autoclass_content = "class"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Integrate GitHub
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "MIPLabCH",  # Username
    "github_repo": "nigsp",  # Repo name
    "github_version": "master",  # Version
    "conf_py_path": "/docs/",  # Path in the checkout to the docs root
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
html_show_sourcelink = False

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ["_static"]


# html_favicon = '_static/logo.png'
# html_logo = '_static/logo.png'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "nigsp"


# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.6", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
}


# -- Generate API automagically -----------------------------------------------
def run_apidoc(_):
    from sphinx.ext.apidoc import main

    cur_dir = os.path.normpath(os.path.dirname(__file__))
    output_path = os.path.join(cur_dir, "api")
    modules = os.path.normpath(os.path.join(cur_dir, "../nigsp"))
    exclusions = [
        "../nigsp/tests/*",
        "../nigsp/cli/*",
    ]
    main(["-e", "-f", "-T", "-o", output_path, modules] + exclusions)


# -- Final Setup -------------------------------------------------------------


# https://github.com/rtfd/sphinx_rtd_theme/issues/117
# launch setup
def setup(app):  # noqa
    app.connect("builder-inited", run_apidoc)
    app.add_css_file("theme_overrides.css")
    app.add_js_file("https://cdn.rawgit.com/chrisfilo/zenodo.js/v0.1/zenodo.js")
